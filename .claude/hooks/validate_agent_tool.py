#!/usr/bin/env python3
"""Fail-closed tool policy and instruction receipts for unattended routines."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import sys
import tempfile
import time
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd())).resolve()
SYMBOL = re.compile(r"^[A-Z][A-Z0-9.-]{0,9}$")
READ_ONLY = {"account", "positions", "position", "history", "orders", "clock", "calendar", "snapshot", "quote", "bars", "help"}
BULL_CROSS_READ = {
    "memory/aggressive/portfolio.md",
    "memory/aggressive/trade-log.md",
    "memory/aggressive/closed-trades.md",
    "memory/aggressive/weekly-review.md",
    "memory/aggressive/performance.csv",
    "memory/aggressive/trades.jsonl",
}
COMMON_READ = {
    "CLAUDE.md",
    "memory/_lock",
    "memory/control.md",
    "memory/knowledge-base.md",
    "memory/quant-research-playbook.md",
    "memory/upstream-methodology-index.md",
    "third_party/README.md",
    "third_party/snapshots.json",
}
SHARED_IMMUTABLE = {
    "memory/control.md",
    "memory/knowledge-base.md",
    "memory/quant-research-playbook.md",
    "memory/upstream-methodology-index.md",
}
UPSTREAM_REFERENCE_READ = {
    "third_party/quant-mind/LICENSE",
    "third_party/quant-mind/docs/library.md",
    "third_party/quant-mind/docs/design/en/news.md",
    "third_party/quant-mind/quantmind/knowledge/_base.py",
    "third_party/quant-mind/quantmind/knowledge/_tree.py",
    "third_party/quant-mind/quantmind/knowledge/paper.py",
    "third_party/quant-mind/quantmind/preprocess/_news_types.py",
    "third_party/quant-mind/quantmind/preprocess/news.py",
    "third_party/quant-mind/quantmind/flows/batch.py",
    "third_party/quant-mind/quantmind/library/_types.py",
    "third_party/quant-mind/quantmind/library/local.py",
    "third_party/quant-mind/quantmind/library/_internal/retrieval_targets.py",
    "third_party/quant-mind/quantmind/library/_internal/exact_cosine.py",
    "third_party/quant-mind/quantmind/library/_internal/sqlite_store.py",
    "third_party/atlas-gic/LICENSE",
    "third_party/atlas-gic/architecture/overview.md",
    "third_party/atlas-gic/architecture/layers.md",
    "third_party/atlas-gic/architecture/autoresearch.md",
}
RESEARCH_LEDGER = {
    "bull": "memory/research-evidence.jsonl",
    "aggro": "memory/aggressive/research-evidence.jsonl",
}
RESEARCH_PENDING = {
    "bull": "memory/research-packet.pending.json",
    "aggro": "memory/aggressive/research-packet.pending.json",
}
MEMORY_ROOT = (ROOT / "memory").resolve()
UPSTREAM_REMOTE_TOKENS = (
    "llmquant/quant-mind",
    "chrisworsey55/atlas-gic",
)
SHARED_IMMUTABLE_PATHS = {
    (ROOT / relative).resolve() for relative in SHARED_IMMUTABLE
}
METHODOLOGY_INDEX = (ROOT / "memory/upstream-methodology-index.md").resolve()
RECEIPT_TTL_SECONDS = 8 * 60 * 60


class Denied(ValueError):
    pass


class QuietParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise Denied(message)


def _require_canonical_path_case(relative: Path) -> None:
    if ".." in relative.parts:
        raise Denied("path traversal components are not allowed")
    current = ROOT
    for component in relative.parts:
        if current.is_dir():
            try:
                names = {entry.name for entry in current.iterdir()}
            except OSError as exc:
                raise Denied(f"cannot verify canonical path components: {exc}") from exc
            if component not in names and any(
                name.casefold() == component.casefold() for name in names
            ):
                raise Denied(
                    "path component casing must match the repository entry exactly"
                )
        current /= component


def _resolve_repo_path(raw: object) -> Path:
    if not isinstance(raw, str) or not raw:
        raise Denied("missing repository path")
    supplied = Path(raw)
    candidate = supplied if supplied.is_absolute() else ROOT / supplied
    try:
        lexical_relative = candidate.relative_to(ROOT)
    except ValueError as exc:
        raise Denied("path is outside the repository") from exc
    _require_canonical_path_case(lexical_relative)
    resolved = candidate.resolve(strict=False)
    if not resolved.is_relative_to(ROOT):
        raise Denied("path escapes the repository")
    return resolved


def _same_existing_file(left: Path, right: Path) -> bool:
    try:
        return left.exists() and right.exists() and left.samefile(right)
    except OSError:
        return False


def _matches_path(candidate: Path, canonical: Path) -> bool:
    return candidate == canonical or _same_existing_file(candidate, canonical)


def _decision(
    allow: bool,
    reason: str,
    *,
    updated_input: dict[str, object] | None = None,
) -> None:
    output: dict[str, object] = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow" if allow else "deny",
            "permissionDecisionReason": reason,
        }
    }
    if updated_input is not None:
        output["hookSpecificOutput"]["updatedInput"] = updated_input
    print(json.dumps(output))


def _post_context(message: str | None = None) -> None:
    output: dict[str, object] = {
        "hookSpecificOutput": {"hookEventName": "PostToolUse"}
    }
    if message:
        output["hookSpecificOutput"]["additionalContext"] = message
    print(json.dumps(output))


def _session_receipt_path(payload: dict[str, object]) -> Path:
    session_id = payload.get("session_id")
    if not isinstance(session_id, str) or not session_id or len(session_id) > 500:
        raise Denied("a valid Claude session_id is required for instruction receipts")
    root_key = hashlib.sha256(str(ROOT).encode("utf-8")).hexdigest()[:20]
    session_key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    directory = Path(tempfile.gettempdir()) / "claude-trading-instruction-receipts"
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    return directory / f"{root_key}-{session_key}.json"


def _index_sha256() -> str:
    try:
        return hashlib.sha256(METHODOLOGY_INDEX.read_bytes()).hexdigest()
    except OSError as exc:
        raise Denied("mandatory methodology index is unavailable") from exc


def _record_methodology_receipt(payload: dict[str, object]) -> bool:
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return False
    try:
        resolved = _resolve_repo_path(tool_input.get("file_path"))
    except Denied:
        return False
    if not _matches_path(resolved, METHODOLOGY_INDEX):
        return False
    if tool_input.get("offset") is not None or tool_input.get("limit") is not None:
        return False
    receipt = {
        "schema_version": 1,
        "index_sha256": _index_sha256(),
        "recorded_at": time.time(),
    }
    path = _session_receipt_path(payload)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}")
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            os.chmod(temporary, 0o600)
            json.dump(receipt, handle, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    return True


def _methodology_receipt(payload: dict[str, object]) -> str | None:
    try:
        path = _session_receipt_path(payload)
        receipt = json.loads(path.read_text(encoding="utf-8"))
        recorded_at = float(receipt["recorded_at"])
        digest = receipt["index_sha256"]
        current_digest = _index_sha256()
    except (
        Denied,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ):
        return None
    age = time.time() - recorded_at
    if (
        age < -60
        or age > RECEIPT_TTL_SECONDS
        or not isinstance(digest, str)
        or digest != current_digest
    ):
        return None
    return digest


def _is_notify_command(command: str) -> bool:
    tokens = shlex.split(command, posix=True)
    offset = 1 if tokens and tokens[0] == "bash" else 0
    return (
        len(tokens) > offset
        and tokens[offset] in {"./scripts/notify.sh", "scripts/notify.sh"}
    )


def _inject_proof_receipt(command: str, digest: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise Denied("invalid QuantMind/ATLAS instruction receipt")
    return shlex.join([*shlex.split(command, posix=True), "--proof-receipt", digest])


def _agent() -> str:
    value = os.environ.get("TRADING_AGENT", "").strip().lower()
    if value not in {"bull", "aggro"}:
        raise Denied("TRADING_AGENT must be exactly bull or aggro")
    return value


def _safe_decimal(value: str) -> None:
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise Denied("quantity must be numeric") from exc
    if not parsed.is_finite() or parsed <= 0 or parsed != parsed.to_integral_value():
        raise Denied("quantity must be positive whole shares")


def _trade(args: list[str], agent: str) -> None:
    parser = QuietParser(add_help=False, allow_abbrev=False)
    sub = parser.add_subparsers(dest="command", required=True)
    buy = sub.add_parser("buy", add_help=False, allow_abbrev=False)
    buy.add_argument("--agent", required=True)
    buy.add_argument("--symbol", required=True)
    buy.add_argument("--dry-run", action="store_true")
    sell = sub.add_parser("sell", add_help=False, allow_abbrev=False)
    sell.add_argument("--agent", required=True)
    sell.add_argument("--symbol", required=True)
    sell.add_argument("--qty", required=True)
    sell.add_argument("--trigger", required=True)
    sell.add_argument("--reason", required=True)
    audit = sub.add_parser("reconcile", add_help=False, allow_abbrev=False)
    audit.add_argument("--agent", required=True)
    audit.add_argument("--repair", action="store_true")
    parsed = parser.parse_args(args)
    if parsed.agent != agent:
        raise Denied(f"routine is bound to {agent}, not {parsed.agent}")
    if hasattr(parsed, "symbol") and not SYMBOL.fullmatch(parsed.symbol.upper()):
        raise Denied("invalid symbol")
    if parsed.command == "sell":
        _safe_decimal(parsed.qty)
        if parsed.trigger not in {"planned", "midday_loss"}:
            raise Denied("invalid sell trigger")
        if len(parsed.reason.strip()) < 15 or len(parsed.reason) > 1000:
            raise Denied("sell reason length is invalid")


def _alpaca(args: list[str]) -> None:
    if not args or args[0] not in READ_ONLY:
        raise Denied("alpaca.sh is read-only")
    cmd, values = args[0], args[1:]
    if cmd in {"account", "positions", "clock", "help"} and values:
        raise Denied(f"unexpected {cmd} arguments")
    if cmd in {"position", "snapshot", "quote"}:
        if len(values) != 1 or not SYMBOL.fullmatch(values[0].upper()):
            raise Denied(f"{cmd} requires one valid symbol")
    if cmd == "history" and (len(values) > 2 or any(not re.fullmatch(r"[0-9]+[A-Za-z]+", item) for item in values)):
        raise Denied("invalid history arguments")
    if cmd == "orders":
        if len(values) > 2 or (values and values[0] not in {"open", "closed", "all"}):
            raise Denied("invalid orders arguments")
        if len(values) == 2 and (not values[1].isdigit() or not 1 <= int(values[1]) <= 500):
            raise Denied("invalid orders limit")
    if cmd == "bars":
        if not 1 <= len(values) <= 3 or not SYMBOL.fullmatch(values[0].upper()):
            raise Denied("invalid bars arguments")
        if len(values) >= 2 and not re.fullmatch(r"[0-9]+[A-Za-z]+", values[1]):
            raise Denied("invalid bars timeframe")
        if len(values) == 3 and (not values[2].isdigit() or not 1 <= int(values[2]) <= 10_000):
            raise Denied("invalid bars limit")
    if cmd == "calendar":
        if len(values) != 2 or any(not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) for value in values):
            raise Denied("calendar requires start and end dates")


def _bash(command: object, agent: str) -> str:
    if not isinstance(command, str) or not command.strip() or len(command) > 8_000:
        raise Denied("invalid Bash command")
    if any(item in command for item in ("\x00", "\n", "\r", "`", "$")):
        raise Denied("shell expansion and multiline commands are forbidden")
    lexer = shlex.shlex(command, posix=True, punctuation_chars="();<>|&")
    lexer.whitespace_split = True
    if any(token and set(token) <= set("();<>|&") for token in lexer):
        raise Denied("shell operators are forbidden")
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError as exc:
        raise Denied(f"invalid command quoting: {exc}") from exc
    if not tokens:
        raise Denied("empty command")

    if tokens[:2] == ["python3", "scripts/persist_memory.py"]:
        if len(tokens) != 2:
            raise Denied("persist_memory.py takes no arguments")
        return shlex.join(tokens)
    if tokens[:2] == ["python3", "scripts/trade.py"]:
        _trade(tokens[2:], agent)
        return shlex.join(tokens)
    if tokens[:2] == ["python3", "scripts/research.py"]:
        if tuple(tokens[2:]) not in {
            ("validate", "--agent", agent),
            ("append", "--agent", agent),
        }:
            raise Denied(
                "research.py accepts exactly validate|append --agent for the bound profile"
            )
        return shlex.join(tokens)

    offset = 0
    if tokens[0] == "bash":
        offset = 1
    if len(tokens) > offset and tokens[offset] in {"./scripts/alpaca.sh", "scripts/alpaca.sh"}:
        _alpaca(tokens[offset + 1:])
        return shlex.join(tokens)
    if len(tokens) > offset and tokens[offset] in {"./scripts/notify.sh", "scripts/notify.sh"}:
        message = tokens[offset + 1:]
        if len(message) != 1 or not message[0].strip() or len(message[0]) > 4000:
            raise Denied("notify.sh requires exactly one message up to 4000 characters")
        return shlex.join(tokens)
    raise Denied("command is outside the unattended trading allowlist")


def _write_path(raw: object, agent: str) -> None:
    resolved = _resolve_repo_path(raw)
    if not resolved.is_relative_to(MEMORY_ROOT):
        raise Denied("writes are confined to memory")
    relative = resolved.relative_to(ROOT).as_posix()
    if relative == "memory/_lock":
        return
    if any(_matches_path(resolved, item) for item in SHARED_IMMUTABLE_PATHS):
        raise Denied("shared control and research references are human-owned")
    ledger = (ROOT / RESEARCH_LEDGER[agent]).resolve()
    if _matches_path(resolved, ledger):
        raise Denied(
            "research evidence is append-only through scripts/research.py; "
            "write the profile pending packet instead"
        )
    if agent == "bull":
        if relative.startswith("memory/aggressive/") or relative in {"memory/control.md", "memory/strategy.md"}:
            raise Denied("Bull cannot write shared control, active strategy, or AGGRO memory")
        if not relative.startswith("memory/"):
            raise Denied("Bull write is outside its memory")
    else:
        if not relative.startswith("memory/aggressive/") or relative in {
            "memory/aggressive/strategy.md", "memory/aggressive/profile.md"
        }:
            raise Denied("AGGRO cannot write outside mutable AGGRO memory")
    if resolved.suffix.lower() not in {".md", ".csv", ".jsonl"}:
        pending = (ROOT / RESEARCH_PENDING[agent]).resolve()
        if resolved.suffix.lower() != ".json" or not _matches_path(resolved, pending):
            raise Denied(
                "unsupported journal file type; only the bound "
                "research-packet.pending.json may use .json"
            )


def _read_path(raw: object, agent: str) -> None:
    resolved = _resolve_repo_path(raw)
    if not resolved.is_relative_to(ROOT) or not resolved.is_file():
        raise Denied("read path must be an existing repository file")
    relative = resolved.relative_to(ROOT).as_posix()
    if relative in COMMON_READ or relative in UPSTREAM_REFERENCE_READ:
        return
    if relative.startswith(("config/", "schemas/")):
        return
    if relative.startswith(".claude/commands/"):
        command = Path(relative).name
        if (agent == "bull" and not command.startswith("aggro-")) or (
            agent == "aggro" and command.startswith("aggro-")
        ):
            return
        raise Denied(f"{agent} cannot read the other profile's command playbook")
    if agent == "bull":
        if relative in BULL_CROSS_READ:
            return
        if relative.startswith("memory/") and not relative.startswith("memory/aggressive/"):
            return
    elif relative.startswith("memory/aggressive/"):
        return
    raise Denied(f"{agent} read is outside its profile allowlist")


def _webfetch(raw: object) -> None:
    if not isinstance(raw, str) or not raw.strip() or "\x00" in raw:
        raise Denied("WebFetch requires a URL")
    parsed = urlsplit(raw)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise Denied("WebFetch is limited to HTTP(S) sources")
    decoded = raw
    for _ in range(3):
        expanded = unquote(decoded)
        if expanded == decoded:
            break
        decoded = expanded
    normalized = decoded.casefold().replace("\\", "/")
    if any(token in normalized for token in UPSTREAM_REMOTE_TOKENS):
        raise Denied(
            "remote QuantMind/ATLAS fetches are blocked; use only the pinned "
            "local reference paths in memory/upstream-methodology-index.md"
        )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        event = payload.get("hook_event_name", "PreToolUse")
        tool = payload.get("tool_name")
        tool_input = payload.get("tool_input") or {}
        agent = _agent()
        if event == "PostToolUse":
            if tool != "Read":
                _post_context()
                return 0
            if _record_methodology_receipt(payload):
                _post_context(
                    "QuantMind/ATLAS methodology index read receipt recorded for "
                    "this session. Telegram proof is now eligible after the playbook finishes."
                )
            else:
                _post_context()
            return 0
        if event != "PreToolUse":
            raise Denied(f"unexpected hook event: {event}")
        updated_input = None
        if tool == "Bash":
            canonical = _bash(tool_input.get("command"), agent)
            if _is_notify_command(canonical):
                receipt = _methodology_receipt(payload)
                if receipt is not None:
                    canonical = _inject_proof_receipt(canonical, receipt)
            updated_input = {"command": canonical}
        elif tool in {"Edit", "Write"}:
            _write_path(tool_input.get("file_path"), agent)
        elif tool == "Read":
            _read_path(tool_input.get("file_path"), agent)
        elif tool == "WebFetch":
            _webfetch(tool_input.get("url"))
        elif tool in {"Glob", "Grep"}:
            raise Denied(f"{tool} is disabled; read only explicit profile-scoped files")
        else:
            raise Denied(f"unexpected tool for trading policy hook: {tool}")
    except BaseException as exc:
        # Claude treats hook process failures as non-blocking in some cases. Always
        # emit an explicit deny decision, including for malformed/unexpected input.
        _decision(False, f"validator rejected request: {type(exc).__name__}: {exc}")
        return 0
    _decision(
        True,
        "validated unattended trading operation",
        updated_input=updated_input,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
