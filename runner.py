#!/usr/bin/env python3
"""
Bull Trading Agent — Groq runner.

Usage:
    python runner.py <routine>

Routines:
    premarket, market-open, midday, close, weekly-review, monthly-review
    aggro-premarket, aggro-market-open, aggro-midday, aggro-close, aggro-weekly-review

Required env vars:
    GROQ_API_KEY
    ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY, ALPACA_BASE_URL
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
"""

import os
import sys
import subprocess
import textwrap
import urllib.request
import urllib.parse
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from groq import Groq
except ImportError:
    sys.exit("Missing dependency — run: pip install groq")

# ── Constants ────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.resolve()
MODEL_OVERRIDE = os.environ.get("GROQ_MODEL", "").strip()
MAX_TURNS = 50

# Preference order — best free-tier Groq models for agentic tool use
MODEL_PREFERENCE = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama3-70b-8192",
    "llama-3.1-8b-instant",
    "llama3-8b-8192",
]


def resolve_model(client: Groq) -> str:
    if MODEL_OVERRIDE:
        print(f"[runner] GROQ_MODEL override = {MODEL_OVERRIDE}")
        return MODEL_OVERRIDE
    try:
        available = [m.id for m in client.models.list().data]
    except Exception as e:
        print(f"[runner] could not list models ({e}), defaulting to llama-3.3-70b-versatile")
        return "llama-3.3-70b-versatile"

    for pref in MODEL_PREFERENCE:
        if pref in available:
            print(f"[runner] resolved model = {pref}")
            return pref
    for pref in MODEL_PREFERENCE:
        for name in available:
            if pref in name:
                print(f"[runner] resolved model = {name} (matched '{pref}')")
                return name

    print(f"[runner] no preferred match; using {available[0]}")
    print(f"[runner] available models: {', '.join(available)}")
    return available[0]


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
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True,
        cwd=str(ROOT), timeout=120, env={**os.environ},
    )
    out = result.stdout.strip()
    if result.stderr.strip():
        out += f"\n[stderr] {result.stderr.strip()}"
    if result.returncode != 0:
        out += f"\n[exit {result.returncode}]"
    return out or "(no output)"


MAX_READ_CHARS = 60_000


def _read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        return f"(file not found: {path})"
    try:
        text = p.read_text(encoding="utf-8")
        if len(text) > MAX_READ_CHARS:
            half = MAX_READ_CHARS // 2 - 200
            text = (text[:half]
                    + f"\n\n… [truncated {len(text) - MAX_READ_CHARS} chars from middle] …\n\n"
                    + text[-half:])
        return text
    except Exception as e:
        return f"(read error: {e})"


def _write(path: str, content: str) -> str:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"wrote {len(content)} chars → {path}"


def _ls(path: str = ".") -> str:
    p = ROOT / path
    if not p.exists():
        return f"(directory not found: {path})"
    return "\n".join(str(f.relative_to(ROOT)) for f in sorted(p.iterdir()))


def _web_search(query: str) -> str:
    try:
        url = (f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}"
               "&format=json&no_html=1&skip_disambig=1")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        results = []
        if data.get("Abstract"):
            results.append(f"Summary: {data['Abstract']} (Source: {data.get('AbstractSource', '')})")
        for topic in data.get("RelatedTopics", [])[:6]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(f"- {topic['Text']}")

        if not results or any(w in query.lower() for w in ["stock", "market", "price", "earnings", "sp500", "spy"]):
            rss = _fetch_finance_rss(query)
            if rss:
                results.append("\nRecent news:")
                results.extend(rss)

        return "\n".join(results) if results else f"No results for: {query}"
    except Exception as e:
        return f"Search error: {e}"


def _fetch_finance_rss(query: str) -> list:
    try:
        tickers = re.findall(r'\b([A-Z]{2,5})\b', query)
        symbol = tickers[0] if tickers else "SPY"
        url = (f"https://feeds.finance.yahoo.com/rss/2.0/headline"
               f"?s={symbol}&region=US&lang=en-US")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            xml = resp.read().decode("utf-8")
        titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", xml)
        dates = re.findall(r"<pubDate>(.*?)</pubDate>", xml)
        return [f"  [{d[:16]}] {t}" for t, d in zip(titles[1:6], dates[:5])]
    except Exception:
        return []


TOOL_FNS = {
    "bash_execute":   lambda command: _bash(command),
    "read_file":      lambda path: _read(path),
    "write_file":     lambda path, content: _write(path, content),
    "list_directory": lambda path=".": _ls(path),
    "web_search":     lambda query: _web_search(query),
}

# ── Tool declarations (OpenAI-compatible format for Groq) ────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash_execute",
            "description": (
                "Run any shell command in the repo root. Use for: "
                "./scripts/alpaca.sh (trading), ./scripts/notify.sh (Telegram), "
                "git commands (commit, push, pull), and any other CLI operation."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to run"},
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from the repository (relative path from repo root).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative file path"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file in the repository. Creates parent directories automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path":    {"type": "string", "description": "Relative file path"},
                    "content": {"type": "string", "description": "Full file content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files in a directory (relative path, defaults to repo root).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative directory path"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for current information. Use this whenever the playbook says WebSearch. "
                "Good for: stock news, earnings, analyst ratings, macro events, market conditions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                },
                "required": ["query"],
            },
        },
    },
]

# ── Context builder ──────────────────────────────────────────────────────────

def build_prompt(routine: str) -> str:
    playbook = _read(ROUTINES[routine])
    files = list(BASE_MEMORY)
    if routine.startswith("aggro"):
        files += AGGRO_MEMORY

    index_lines = []
    for f in files:
        p = ROOT / f
        if p.exists():
            kb = p.stat().st_size / 1024
            index_lines.append(f"  - {f} ({kb:.1f} KB)")
        else:
            index_lines.append(f"  - {f} (missing)")
    index = "\n".join(index_lines)

    inline = []
    for small in ("memory/control.md", "memory/strategy.md"):
        if small in files:
            inline.append(f"### {small}\n{_read(small)}")
    inline_block = "\n\n".join(inline)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return textwrap.dedent(f"""
        Current UTC time: {now_utc}

        ## YOUR PLAYBOOK — follow every step in order:

        {playbook}

        ---

        ## MEMORY FILES — read what each step needs via the read_file tool:

        {index}

        ---

        ## ALWAYS-LOADED CONTEXT (control switch + strategy):

        {inline_block}
    """).strip()


# ── Send wrapper: normalizes output, retries rate limits, recovers bad calls ──

def _recover_calls_from_failed_generation(emsg: str) -> list:
    """Groq's Llama models sometimes emit tool calls as raw text like
    `<function=read_file({"path": "x"})>` instead of structured JSON, and the
    server rejects the turn with a 400 `tool_use_failed`. The intended call is
    handed back in `failed_generation`, so we parse it and recover.

    Returns a list of normalized calls: {"id", "name", "arguments"} (args = JSON str).
    """
    calls = []
    # <function=NAME(  {json}  )>  — parens optional, tolerant of whitespace
    for i, m in enumerate(re.finditer(
            r'<function=([a-zA-Z_]\w*)[^{]*?(\{.*?\})\s*\)?\s*>', emsg, re.DOTALL)):
        name, raw = m.group(1), m.group(2)
        try:
            json.loads(raw)  # validate
        except json.JSONDecodeError:
            continue
        calls.append({"id": f"recovered_{i}", "name": name, "arguments": raw})
    return calls


def _complete(client: Groq, model: str, messages: list, *, attempt: int = 0):
    """Call Groq and return normalized (content, tool_calls).

    tool_calls is a list of {"id", "name", "arguments"(JSON str)}.
    Handles rate limits (sleep+retry) and malformed tool calls (recover from
    failed_generation) so the agentic loop only ever sees clean structured data.
    """
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,        # near-deterministic → far better tool-format compliance
            max_tokens=4096,
        )
        msg = resp.choices[0].message
        tool_calls = [
            {"id": tc.id, "name": tc.function.name, "arguments": tc.function.arguments}
            for tc in (msg.tool_calls or [])
        ]
        return (msg.content or ""), tool_calls
    except Exception as exc:
        emsg = str(exc)

        # 1) Malformed tool call — recover the intended call(s) and proceed.
        if "tool_use_failed" in emsg or "failed_generation" in emsg:
            recovered = _recover_calls_from_failed_generation(emsg)
            if recovered:
                names = ", ".join(c["name"] for c in recovered)
                print(f"[runner] recovered malformed tool call(s): {names}")
                return "", recovered
            # Couldn't parse it — nudge the model to retry in valid format.
            if attempt < 2:
                print("[runner] tool_use_failed and unparseable — nudging model to retry")
                messages.append({
                    "role": "user",
                    "content": ("Your last tool call was malformed. Reissue it as a proper "
                                "structured tool call (valid JSON arguments), not as text."),
                })
                return _complete(client, model, messages, attempt=attempt + 1)

        # 2) Rate limit — sleep the suggested delay and retry.
        is_rate = ("429" in emsg) or ("rate_limit" in emsg.lower()) or ("rate limit" in emsg.lower())
        delay_match = re.search(r"Please try again in ([\d.]+)s", emsg)
        delay = float(delay_match.group(1)) if delay_match else 60
        if is_rate and attempt < 3:
            print(f"[runner] rate limit — sleeping {delay:.0f}s then retrying (attempt {attempt + 1}/3)")
            time.sleep(delay + 1)
            return _complete(client, model, messages, attempt=attempt + 1)

        raise


def _handle_api_error(exc: Exception) -> None:
    msg = str(exc)
    if "429" in msg or "rate_limit" in msg.lower():
        print("\n[runner] ⚠️  Groq rate limit hit (429). Free tier allows 30 req/min.\n"
              "        The runner will retry automatically. If it keeps failing:\n"
              "        • Set GROQ_MODEL=llama-3.1-8b-instant (higher rate limits), or\n"
              "        • Wait a minute and re-run.")
    elif "401" in msg or "invalid_api_key" in msg.lower() or "authentication" in msg.lower():
        print("\n[runner] ⚠️  Invalid GROQ_API_KEY. Re-copy it from "
              "https://console.groq.com/keys into the GitHub secret.")
    elif "404" in msg or "not found" in msg.lower():
        print("\n[runner] ⚠️  Model not found (404). The runner auto-selects models, "
              "so this usually means the key has no access.\n"
              "        Check your key at https://console.groq.com/keys")
    else:
        print(f"\n[runner] ⚠️  Groq API error: {msg}")


# ── Agentic loop ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are Bull, an autonomous AI trading agent. "
    "Follow every step in the playbook exactly. "
    "Memory files are listed by index — call read_file(path) to load only "
    "the ones a step actually needs. Do not try to read every file upfront. "
    "Use bash_execute to run shell scripts (alpaca.sh, notify.sh) and git commands. "
    "Use write_file to update memory files. "
    "Use web_search whenever the playbook says to use WebSearch — treat them identically. "
    "At the END of every run, after all other steps, commit and push: "
    "bash_execute('git add -A && git commit -m \"<routine>: <summary>\" "
    "&& git push origin HEAD:main'). "
    "If push is rejected, run 'git fetch origin main && git rebase origin/main' then push again."
)


def run(routine: str) -> None:
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        sys.exit("GROQ_API_KEY environment variable not set")
    if routine not in ROUTINES:
        sys.exit(f"Unknown routine: {routine}\nValid: {', '.join(ROUTINES)}")

    print("[runner] syncing with main …")
    _bash("git pull origin main --rebase --autostash 2>&1 || true")

    client = Groq(api_key=api_key)
    chosen_model = resolve_model(client)
    print(f"[runner] starting {routine} with {chosen_model}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": build_prompt(routine)},
    ]

    turns = 0
    while turns < MAX_TURNS:
        try:
            content, tool_calls = _complete(client, chosen_model, messages)
        except Exception as exc:
            _handle_api_error(exc)
            raise

        # Print any text response
        if content:
            print(f"[model] {content[:200].replace(chr(10), ' ')}")

        # Add assistant message to history
        messages.append({
            "role": "assistant",
            "content": content,
            "tool_calls": [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {"name": tc["name"], "arguments": tc["arguments"]},
                }
                for tc in tool_calls
            ] or None,
        })

        if not tool_calls:
            print(f"[runner] routine complete ({turns + 1} turns)")
            break

        # Execute each tool call and collect results
        for tc in tool_calls:
            fn_name = tc["name"]
            try:
                args = json.loads(tc["arguments"])
            except json.JSONDecodeError:
                args = {}

            print(f"[tool]  {fn_name}({list(args.keys())})")
            fn = TOOL_FNS.get(fn_name)
            try:
                result = fn(**args) if fn else f"(unknown tool: {fn_name})"
            except Exception as exc:
                result = f"ERROR: {exc}"

            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": str(result),
            })

        turns += 1
        # Small pause to stay comfortably under the 30 req/min free-tier limit
        time.sleep(2)

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
