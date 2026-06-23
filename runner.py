#!/usr/bin/env python3
"""
Bull Trading Agent — free Gemini runner.

Usage:
    python runner.py <routine>

Routines:
    premarket, market-open, midday, close, weekly-review, monthly-review
    aggro-premarket, aggro-market-open, aggro-midday, aggro-close, aggro-weekly-review

Required env vars:
    GEMINI_API_KEY
    ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY, ALPACA_BASE_URL
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
"""

import os
import sys
import subprocess
import textwrap
from datetime import datetime, timezone
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    sys.exit("Missing dependency — run: pip install google-genai")

# ── Constants ────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.resolve()
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-lite")
MAX_TURNS = 50  # hard safety limit per run

ROUTINES = {
    "premarket":           ".claude/commands/premarket.md",
    "market-open":         ".claude/commands/market-open.md",
    "midday":              ".claude/commands/midday.md",
    "close":               ".claude/commands/close.md",
    "weekly-review":       ".claude/commands/weekly-review.md",
    "monthly-review":      ".claude/commands/monthly-review.md",
    "aggro-premarket":     ".claude/commands/aggro-premarket.md",
    "aggro-market-open":   ".claude/commands/aggro-market-open.md",
    "aggro-midday":        ".claude/commands/aggro-midday.md",
    "aggro-close":         ".claude/commands/aggro-close.md",
    "aggro-weekly-review": ".claude/commands/aggro-weekly-review.md",
}

# Files always loaded into context upfront
BASE_MEMORY = [
    "CLAUDE.md",
    "memory/control.md",
    "memory/strategy.md",
    "memory/portfolio.md",
    "memory/trade-log.md",
    "memory/research-log.md",
    "memory/lessons.md",
    "memory/weekly-review.md",
    "memory/knowledge-base.md",
    "memory/closed-trades.md",
]

AGGRO_MEMORY = [
    "memory/aggressive/profile.md",
    "memory/aggressive/portfolio.md",
    "memory/aggressive/trade-log.md",
    "memory/aggressive/research-log.md",
    "memory/aggressive/lessons.md",
    "memory/aggressive/weekly-review.md",
    "memory/aggressive/closed-trades.md",
    "memory/aggressive/strategy.md",
]

# ── Tool implementations ─────────────────────────────────────────────────────

def _bash(command: str) -> str:
    """Run a shell command in the repo root."""
    env = {**os.environ}
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True,
        cwd=str(ROOT), timeout=120, env=env,
    )
    out = result.stdout.strip()
    if result.stderr.strip():
        out += f"\n[stderr] {result.stderr.strip()}"
    if result.returncode != 0:
        out += f"\n[exit {result.returncode}]"
    return out or "(no output)"


def _read(path: str) -> str:
    """Read a file relative to the repo root."""
    p = ROOT / path
    if not p.exists():
        return f"(file not found: {path})"
    try:
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"(read error: {e})"


def _write(path: str, content: str) -> str:
    """Write a file relative to the repo root, creating dirs as needed."""
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"wrote {len(content)} chars → {path}"


def _ls(path: str = ".") -> str:
    """List files in a directory relative to the repo root."""
    p = ROOT / path
    if not p.exists():
        return f"(directory not found: {path})"
    items = sorted(p.iterdir())
    return "\n".join(str(i.relative_to(ROOT)) for i in items)


TOOL_FNS = {
    "bash_execute":   _bash,
    "read_file":      _read,
    "write_file":     _write,
    "list_directory": _ls,
}

# ── Gemini tool declarations ─────────────────────────────────────────────────

TOOL_DECLS = [
    types.FunctionDeclaration(
        name="bash_execute",
        description=(
            "Run any shell command in the repo root. Use this for: "
            "./scripts/alpaca.sh (trading), ./scripts/notify.sh (Telegram), "
            "git commands (commit, push, pull), and any other CLI operation."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={"command": types.Schema(type=types.Type.STRING, description="Shell command to run")},
            required=["command"],
        ),
    ),
    types.FunctionDeclaration(
        name="read_file",
        description="Read a file from the repository (relative path from repo root).",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={"path": types.Schema(type=types.Type.STRING, description="Relative file path")},
            required=["path"],
        ),
    ),
    types.FunctionDeclaration(
        name="write_file",
        description="Write content to a file in the repository. Creates parent directories automatically.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "path":    types.Schema(type=types.Type.STRING, description="Relative file path"),
                "content": types.Schema(type=types.Type.STRING, description="Full file content to write"),
            },
            required=["path", "content"],
        ),
    ),
    types.FunctionDeclaration(
        name="list_directory",
        description="List files in a directory (relative path, defaults to repo root).",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={"path": types.Schema(type=types.Type.STRING, description="Relative directory path")},
            required=[],
        ),
    ),
]

# ── Context builder ──────────────────────────────────────────────────────────

def build_prompt(routine: str) -> str:
    playbook = _read(ROUTINES[routine])

    files = list(BASE_MEMORY)
    if routine.startswith("aggro"):
        files += AGGRO_MEMORY

    mem_sections = []
    for f in files:
        content = _read(f)
        mem_sections.append(f"### {f}\n{content}")
    memory_block = "\n\n---\n\n".join(mem_sections)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return textwrap.dedent(f"""
        Current UTC time: {now_utc}

        ## YOUR PLAYBOOK — follow every step in order:

        {playbook}

        ---

        ## MEMORY FILES (your current state — update via write_file):

        {memory_block}
    """).strip()


# ── Agentic loop ─────────────────────────────────────────────────────────────

def run(routine: str) -> None:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        sys.exit("GEMINI_API_KEY environment variable not set")
    if routine not in ROUTINES:
        sys.exit(f"Unknown routine: {routine}\nValid: {', '.join(ROUTINES)}")

    # Pull latest memory before starting
    print(f"[runner] syncing with main …")
    _bash("git pull origin main --rebase --autostash 2>&1 || true")

    client = genai.Client(api_key=api_key)

    tools = [
        types.Tool(function_declarations=TOOL_DECLS),
        types.Tool(google_search=types.GoogleSearch()),
    ]

    config = types.GenerateContentConfig(
        system_instruction=(
            "You are Bull, an autonomous AI trading agent. "
            "Your job is to run the routine described in the playbook below, step by step. "
            "Use bash_execute to run shell scripts (alpaca.sh, notify.sh) and git commands. "
            "Use write_file to update memory files. "
            "Use read_file or list_directory if you need to check something not already in context. "
            "Use google_search (built-in) whenever the playbook says WebSearch — treat it identically. "
            "At the END of every run, after all other steps are done: "
            "run 'git add -A && git commit -m \"<routine>: <one-line summary>\" "
            "&& git push origin HEAD:main' via bash_execute. "
            "If the push is rejected, run 'git fetch origin main && git rebase origin/main' then push again."
        ),
        tools=tools,
        temperature=0.1,
        max_output_tokens=8192,
    )

    print(f"[runner] starting {routine} with {MODEL}")
    prompt = build_prompt(routine)
    contents: list = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    turns = 0
    while turns < MAX_TURNS:
        response = client.models.generate_content(
            model=MODEL, contents=contents, config=config
        )

        if not response.candidates:
            print("[runner] empty response — stopping")
            break

        candidate = response.candidates[0]
        model_parts = candidate.content.parts if candidate.content else []
        contents.append(types.Content(role="model", parts=model_parts))

        # Print any text the model produced
        for part in model_parts:
            if hasattr(part, "text") and part.text:
                preview = part.text[:300].replace("\n", " ")
                print(f"[model] {preview}")

        # Collect function calls
        fn_calls = [p for p in model_parts if getattr(p, "function_call", None)]
        if not fn_calls:
            print(f"[runner] routine complete ({turns + 1} turns)")
            break

        # Execute each tool call
        fn_responses = []
        for part in fn_calls:
            fc = part.function_call
            fn = TOOL_FNS.get(fc.name)
            args = dict(fc.args) if fc.args else {}
            arg_keys = list(args.keys())
            print(f"[tool]  {fc.name}({arg_keys})")

            if fn is None:
                result = f"(unknown tool: {fc.name})"
            else:
                try:
                    result = fn(**args)
                except Exception as exc:
                    result = f"ERROR: {exc}"

            fn_responses.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name,
                        response={"result": result},
                    )
                )
            )

        contents.append(types.Content(role="user", parts=fn_responses))
        turns += 1

    if turns >= MAX_TURNS:
        print(f"[runner] hit {MAX_TURNS}-turn safety limit — forcing commit")
        _bash(
            f'git add -A && git commit -m "{routine}: safety-limit exit" '
            "&& git push origin HEAD:main 2>&1 || true"
        )


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python runner.py <routine>\n\nRoutines: {', '.join(ROUTINES)}")
        sys.exit(1)
    run(sys.argv[1])
