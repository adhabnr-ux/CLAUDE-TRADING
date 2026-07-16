#!/usr/bin/env python3
"""Publish only the active paper agent's journal files to origin/main.

This fixed, no-argument helper is the only Git capability exposed to scheduled
Claude Code routines. It rejects stale bases, staged changes, foreign-profile
writes, control-plane changes, and unexpected remotes before committing.
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
    "memory/strategy-proposals.md",
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
    "memory/aggressive/strategy-proposals.md",
}


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


def main() -> int:
    if len(sys.argv) != 1:
        raise PersistenceError("persist_memory.py takes no arguments")
    agent = os.environ.get("TRADING_AGENT", "").strip().lower()
    if agent not in {"bull", "aggro"}:
        raise PersistenceError("TRADING_AGENT must be exactly bull or aggro")

    lock_path = ROOT / "memory" / "_lock"
    if lock_path.exists() and lock_path.read_text(encoding="utf-8").strip() not in {"", "{}"}:
        raise PersistenceError("memory/_lock must be released before persistence")

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

    _run("git", "add", "--", *sorted(changed))
    staged = _lines("git", "diff", "--cached", "--name-only", "--")
    if staged != changed or any(not _allowed(path, agent) for path in staged):
        raise PersistenceError("staged change set differs from verified journal change set")

    _run("git", "config", "user.email", f"{agent}-bull-bot@users.noreply.github.com")
    _run("git", "config", "user.name", "Aggro Bull Bot" if agent == "aggro" else "Bull Bot")
    _run("git", "commit", "-m", f"{agent}: verified scheduled memory update")
    _run("git", "push", "origin", "HEAD:main")
    print(f"persisted {len(staged)} authorized {agent} memory file(s) to main")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.SubprocessError, PersistenceError) as exc:
        print(f"PERSISTENCE BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(2)
