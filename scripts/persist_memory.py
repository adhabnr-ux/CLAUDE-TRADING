#!/usr/bin/env python3
"""Publish only the active paper agent's journal files to origin/main.

This fixed, no-argument helper is the only Git capability exposed to scheduled
Claude Code routines. It rejects stale bases, staged changes, foreign-profile
writes, control-plane changes, pending research packets, rewritten research
history, and unexpected remotes before committing.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REPOSITORY = "adhabnr-ux/CLAUDE-TRADING"

BULL_FILES = {
    "memory/_lock",
    "memory/portfolio.md",
    "memory/trade-log.md",
    "memory/research-log.md",
    "memory/lessons.md",
    "memory/weekly-review.md",
    "memory/closed-trades.md",
    "memory/performance.csv",
    "memory/trades.jsonl",
    "memory/execution-events.jsonl",
    "memory/research-evidence.jsonl",
    "memory/strategy-proposals.md",
    "memory/telegram-quantmind-atlas.pending",
}

AGGRO_FILES = {
    "memory/_lock",
    "memory/aggressive/portfolio.md",
    "memory/aggressive/trade-log.md",
    "memory/aggressive/research-log.md",
    "memory/aggressive/lessons.md",
    "memory/aggressive/weekly-review.md",
    "memory/aggressive/closed-trades.md",
    "memory/aggressive/performance.csv",
    "memory/aggressive/trades.jsonl",
    "memory/aggressive/execution-events.jsonl",
    "memory/aggressive/research-evidence.jsonl",
    "memory/aggressive/strategy-proposals.md",
    "memory/aggressive/telegram-quantmind-atlas.pending",
}
RESEARCH_LEDGER = {
    "bull": "memory/research-evidence.jsonl",
    "aggro": "memory/aggressive/research-evidence.jsonl",
}
PENDING_PACKETS = {
    "memory/research-packet.pending.json",
    "memory/aggressive/research-packet.pending.json",
}
PROOF_MARKERS = {
    "bull": "memory/telegram-quantmind-atlas.pending",
    "aggro": "memory/aggressive/telegram-quantmind-atlas.pending",
}
PROOF_MARKER_TEXT = "New instructions recieve from QuantMind and ATLAS\n"


class PersistenceError(RuntimeError):
    pass


def _run(*argv: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        list(argv),
        cwd=ROOT,
        text=True,
        capture_output=True,
        shell=False,
        timeout=60,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise PersistenceError(f"{' '.join(argv)} failed: {detail[:800]}")
    return result


def _lines(*argv: str) -> set[str]:
    return {line.strip() for line in _run(*argv).stdout.splitlines() if line.strip()}


def _allowed(path: str, agent: str) -> bool:
    normalized = PurePosixPath(path).as_posix()
    if normalized.startswith("/") or ".." in PurePosixPath(normalized).parts:
        return False
    if agent == "bull" and normalized.startswith("memory/archive/"):
        return normalized.endswith(".md")
    return normalized in (BULL_FILES if agent == "bull" else AGGRO_FILES)


def _verify_remote() -> None:
    url = _run("git", "remote", "get-url", "origin").stdout.strip()
    match = re.search(r"github\.com(?::|/)([^/]+/[^/]+?)(?:\.git)?$", url)
    if not match or match.group(1).lower() != EXPECTED_REPOSITORY.lower():
        raise PersistenceError(f"unexpected origin remote: {url!r}")


def _changed_paths() -> set[str]:
    changed = _lines("git", "diff", "--name-only", "--")
    changed |= _lines("git", "ls-files", "--others", "--exclude-standard")
    return changed


def _reject_pending_packets() -> None:
    present = {
        path
        for path in PENDING_PACKETS
        if (ROOT / path).exists() or (ROOT / path).is_symlink()
    }
    for directory in (ROOT / "memory", ROOT / "memory" / "aggressive"):
        if directory.is_dir():
            present.update(
                path.relative_to(ROOT).as_posix()
                for path in directory.glob(".research-packet.claimed-*.json")
            )
    if present:
        raise PersistenceError(
            "unconsumed research pending packet(s): " + ", ".join(sorted(present))
        )


def _tracked_blob(path: str) -> str:
    for reference in ("HEAD", "refs/remotes/origin/main"):
        result = _run("git", "show", f"{reference}:{path}", check=False)
        if result.returncode == 0:
            return result.stdout
    raise PersistenceError(
        f"research ledger {path} is not tracked in HEAD or origin/main"
    )


def _verify_research_append(path: str) -> None:
    local_path = ROOT / path
    if local_path.is_symlink() or not local_path.is_file():
        raise PersistenceError(f"research ledger {path} must be a regular file")
    try:
        current = local_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PersistenceError(f"could not read research ledger {path}: {exc}") from exc
    baseline = _tracked_blob(path)
    if not current.startswith(baseline):
        raise PersistenceError(
            f"research ledger {path} rewrote or deleted tracked history; only exact append is allowed"
        )
    if current == baseline:
        raise PersistenceError(
            f"research ledger {path} changed without appending a packet"
        )


def _validate_changed_research(changed: set[str], agent: str) -> None:
    ledger = RESEARCH_LEDGER[agent]
    if ledger not in changed:
        return
    _verify_research_append(ledger)
    _run(
        sys.executable,
        "scripts/research.py",
        "validate",
        "--agent",
        agent,
    )


def _validate_proof_marker_deletion(changed: set[str], agent: str) -> None:
    marker = PROOF_MARKERS[agent]
    if marker not in changed:
        return
    if _tracked_blob(marker) != PROOF_MARKER_TEXT:
        raise PersistenceError("tracked Telegram proof marker content is invalid")
    local = ROOT / marker
    if local.exists() or local.is_symlink():
        raise PersistenceError(
            "Telegram proof marker may only be deleted by a confirmed notification"
        )


def main() -> int:
    if len(sys.argv) != 1:
        raise PersistenceError("persist_memory.py takes no arguments")
    agent = os.environ.get("TRADING_AGENT", "").strip().lower()
    if agent not in {"bull", "aggro"}:
        raise PersistenceError("TRADING_AGENT must be exactly bull or aggro")

    lock_path = ROOT / "memory" / "_lock"
    if lock_path.exists() and lock_path.read_text(encoding="utf-8").strip() not in {"", "{}"}:
        raise PersistenceError("memory/_lock must be released before persistence")
    _reject_pending_packets()

    _verify_remote()
    if _lines("git", "diff", "--cached", "--name-only", "--"):
        raise PersistenceError("refusing pre-staged changes")

    _run("git", "fetch", "--no-tags", "origin", "main")
    head = _run("git", "rev-parse", "HEAD").stdout.strip()
    remote = _run("git", "rev-parse", "refs/remotes/origin/main").stdout.strip()
    if head != remote:
        raise PersistenceError(
            "checkout is not based exactly on current origin/main; discard/restart this routine"
        )

    changed = _changed_paths()
    rejected = sorted(path for path in changed if not _allowed(path, agent))
    if rejected:
        raise PersistenceError(
            f"{agent} routine changed unauthorized paths: {', '.join(rejected)}"
        )
    if not changed:
        print("no authorized memory changes to persist")
        return 0
    _validate_changed_research(changed, agent)
    _validate_proof_marker_deletion(changed, agent)

    _run("git", "add", "--", *sorted(changed))
    staged = _lines("git", "diff", "--cached", "--name-only", "--")
    if staged != changed or any(not _allowed(path, agent) for path in staged):
        raise PersistenceError("staged change set differs from verified journal change set")
    _reject_pending_packets()

    _run("git", "config", "user.email", f"{agent}-bull-bot@users.noreply.github.com")
    _run("git", "config", "user.name", "Aggro Bull Bot" if agent == "aggro" else "Bull Bot")
    _run("git", "commit", "-m", f"{agent}: verified scheduled memory update")
    _reject_pending_packets()
    _run("git", "push", "origin", "HEAD:main")
    print(f"persisted {len(staged)} authorized {agent} memory file(s) to main")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.SubprocessError, PersistenceError) as exc:
        print(f"PERSISTENCE BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(2)
