#!/usr/bin/env python3
"""Send one Telegram message and acknowledge a pending profile proof marker.

The scheduled agent may invoke only ``scripts/notify.sh``.  That wrapper calls
this trusted helper so Telegram success is parsed before a proof marker is
deleted. A marker is consumed only in a Claude Code remote environment and only
after Telegram returns a positive message id. Base safety notifications remain
deliverable when proof is pending or invalid.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable, Mapping


ROOT = Path(__file__).resolve().parents[1]
PROOF_TEXT = "New instructions recieve from QuantMind and ATLAS"
PROOF_BYTES = f"{PROOF_TEXT}\n".encode("utf-8")
MAX_INPUT_CHARS = 4_000
MAX_TELEGRAM_CHARS = 4_096
MAX_RESPONSE_BYTES = 65_536
PROOF_MARKERS = {
    "bull": "memory/telegram-quantmind-atlas.pending",
    "aggro": "memory/aggressive/telegram-quantmind-atlas.pending",
}
EXPECTED_SNAPSHOTS = {
    "quant-mind": {
        "commit": "2c1f2cb9ae278cbee7c69a982a9151230be596f1",
        "tree": "ff65a0977856b46a226db6363112cb53debf9aa3",
    },
    "atlas-gic": {
        "commit": "fcfc40dcf628f6af091c28cb2c33827f42cef8fd",
        "tree": "e526c1e212a15839121a3671787a601818b04d13",
    },
}


class NotifyError(RuntimeError):
    """Fail-visible notification or proof validation error."""


def _required_env(env: Mapping[str, str], name: str) -> str:
    value = env.get(name, "").strip()
    if not value:
        raise NotifyError(f"required environment variable is missing: {name}")
    return value


def _agent(env: Mapping[str, str]) -> str:
    agent = _required_env(env, "TRADING_AGENT").lower()
    if agent not in PROOF_MARKERS:
        raise NotifyError("TRADING_AGENT must be exactly bull or aggro")
    return agent


def _marker_path(agent: str) -> Path:
    return ROOT / PROOF_MARKERS[agent]


def _proof_lock(agent: str):
    root_key = hashlib.sha256(str(ROOT).encode("utf-8")).hexdigest()[:20]
    path = Path(tempfile.gettempdir()) / f"claude-trading-notify-{root_key}-{agent}.lock"
    handle = path.open("a+", encoding="utf-8")
    os.chmod(path, 0o600)
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    return handle


def _marker_is_armed(path: Path) -> bool:
    if not path.exists() and not path.is_symlink():
        return False
    if path.is_symlink() or not path.is_file():
        raise NotifyError(f"proof marker must be a regular file: {path.relative_to(ROOT)}")
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise NotifyError("could not read the Telegram proof marker") from exc
    if payload != PROOF_BYTES:
        raise NotifyError("Telegram proof marker content is invalid")
    return True


def _methodology_digest() -> str:
    try:
        return hashlib.sha256(
            (ROOT / "memory" / "upstream-methodology-index.md").read_bytes()
        ).hexdigest()
    except OSError as exc:
        raise NotifyError("mandatory methodology index is unavailable") from exc


def _verify_integration() -> None:
    """Verify the reviewed snapshots and mandatory agent context before proof."""
    manifest_path = ROOT / "third_party" / "snapshots.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise NotifyError("could not validate the upstream snapshot manifest") from exc
    if not isinstance(manifest, dict):
        raise NotifyError("upstream snapshot manifest is malformed")
    snapshots = manifest.get("snapshots")
    if not isinstance(snapshots, list):
        raise NotifyError("upstream snapshot manifest is malformed")
    observed = {}
    for item in snapshots:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise NotifyError("upstream snapshot manifest is malformed")
        observed[item["name"]] = {
            "commit": item.get("commit"),
            "tree": item.get("tree"),
        }
    if observed != EXPECTED_SNAPSHOTS:
        raise NotifyError("upstream snapshot pins do not match the reviewed integration")

    required_reference = "memory/upstream-methodology-index.md"
    try:
        claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        index = (ROOT / required_reference).read_text(encoding="utf-8")
        commands = sorted((ROOT / ".claude" / "commands").glob("*.md"))
    except (OSError, UnicodeError) as exc:
        raise NotifyError("could not validate mandatory agent instructions") from exc
    if required_reference not in claude or not index.strip():
        raise NotifyError("mandatory QuantMind/ATLAS context is unavailable")
    try:
        commands_are_bound = len(commands) == 11 and all(
            required_reference in path.read_text(encoding="utf-8")
            for path in commands
        )
    except (OSError, UnicodeError) as exc:
        raise NotifyError("could not validate scheduled command instructions") from exc
    if not commands_are_bound:
        raise NotifyError("not every scheduled command requires the methodology index")

    try:
        result = subprocess.run(
            [sys.executable, "scripts/verify_upstream_snapshots.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            shell=False,
            timeout=45,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise NotifyError("upstream snapshot verification could not run") from exc
    if result.returncode != 0:
        raise NotifyError("upstream snapshot verification failed")


def _append_proof(message: str) -> str:
    if message.rstrip().endswith(PROOF_TEXT):
        rendered = message.rstrip()
    else:
        rendered = f"{message.rstrip()}\n{PROOF_TEXT}"
    if len(rendered) > MAX_TELEGRAM_CHARS:
        raise NotifyError("Telegram message exceeds 4096 characters after proof suffix")
    return rendered


def _send_telegram(
    token: str,
    chat_id: str,
    message: str,
    *,
    opener: Callable[..., object] = urllib.request.urlopen,
) -> int:
    body = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with opener(request, timeout=30) as response:
            payload = response.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        code = exc.code
        exc.close()
        raise NotifyError(f"Telegram send failed with HTTP {code}") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise NotifyError("Telegram send failed with a network error") from None
    if len(payload) > MAX_RESPONSE_BYTES:
        raise NotifyError("Telegram response exceeded the safety limit")
    try:
        decoded = json.loads(payload.decode("utf-8"))
        message_id = decoded["result"]["message_id"]
    except (UnicodeError, json.JSONDecodeError, KeyError, TypeError):
        raise NotifyError("Telegram returned an invalid response") from None
    if decoded.get("ok") is not True or type(message_id) is not int or message_id <= 0:
        raise NotifyError("Telegram did not confirm message delivery")
    return message_id


def _consume_marker(path: Path) -> None:
    if not _marker_is_armed(path):
        raise NotifyError("Telegram proof marker disappeared before acknowledgement")
    try:
        path.unlink()
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError as exc:
        raise NotifyError("Telegram delivered but proof acknowledgement could not be recorded") from exc


def deliver(
    message: str,
    *,
    env: Mapping[str, str] | None = None,
    sender: Callable[[str, str, str], int] | None = None,
    proof_receipt: str | None = None,
) -> dict[str, object]:
    env = os.environ if env is None else env
    if not isinstance(message, str) or not message.strip():
        raise NotifyError("notification message must be non-empty")
    if len(message) > MAX_INPUT_CHARS:
        raise NotifyError("notification message exceeds 4000 characters")
    token = _required_env(env, "TELEGRAM_BOT_TOKEN")
    chat_id = _required_env(env, "TELEGRAM_CHAT_ID")
    agent = _agent(env)
    marker = _marker_path(agent)
    remote = env.get("CLAUDE_CODE_REMOTE", "").strip().lower() == "true"
    sender = _send_telegram if sender is None else sender

    with _proof_lock(agent):
        armed = False
        proof_error: NotifyError | None = None
        if remote and (marker.exists() or marker.is_symlink()):
            try:
                armed = _marker_is_armed(marker)
            except Exception as exc:
                proof_error = (
                    exc
                    if isinstance(exc, NotifyError)
                    else NotifyError(
                        "unexpected proof validation failure: "
                        f"{type(exc).__name__}"
                    )
                )
        outgoing = message
        proof_appended = False
        if armed and proof_receipt is not None:
            try:
                if proof_receipt != _methodology_digest():
                    raise NotifyError("QuantMind/ATLAS instruction receipt is invalid")
                _verify_integration()
                outgoing = _append_proof(message)
                proof_appended = True
            except Exception as exc:
                proof_error = (
                    exc
                    if isinstance(exc, NotifyError)
                    else NotifyError(
                        "unexpected proof validation failure: "
                        f"{type(exc).__name__}"
                    )
                )
        message_id = sender(token, chat_id, outgoing)
        if type(message_id) is not int or message_id <= 0:
            raise NotifyError("Telegram sender did not return a positive message id")
        if proof_appended:
            _consume_marker(marker)
        if proof_error is not None:
            raise NotifyError(
                f"Telegram delivered without proof suffix: {proof_error}"
            ) from None
    return {
        "ok": True,
        "message_id": message_id,
        "proof_appended": proof_appended,
        "proof_pending": armed and not proof_appended,
        "delivery_semantics": "at_least_once_until_persisted",
    }


def main() -> int:
    proof_receipt = None
    if len(sys.argv) == 4 and sys.argv[2] == "--proof-receipt":
        proof_receipt = sys.argv[3]
    elif len(sys.argv) != 2:
        raise NotifyError('usage: ./scripts/notify.sh "message"')
    result = deliver(sys.argv[1], proof_receipt=proof_receipt)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except NotifyError as exc:
        print(f"NOTIFICATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(2)
