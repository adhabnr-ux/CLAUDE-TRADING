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
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    import google.generativeai as genai
    from google.generativeai import protos
except ImportError:
    sys.exit("Missing dependency — run: pip install google-generativeai")

# ── Constants ────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.resolve()
# If GEMINI_MODEL is set, it wins. Otherwise resolve_model() asks the API
# which models this key can actually use and picks the best free one.
MODEL_OVERRIDE = os.environ.get("GEMINI_MODEL", "").strip()
MAX_TURNS = 50

# Preference order — first match (by substring) among the key's available
# models wins. "flash" tiers are cheapest and have the most generous free
# quota; "lite" highest of all. Listed newest-stable first.
MODEL_PREFERENCE = [
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-latest",
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash",
]


def resolve_model() -> str:
    """Ask the API which models this key supports, then pick the best free one.

    This is the key robustness fix: Google retires model names for new keys
    and varies them by region, so we never hardcode. We list what's actually
    available and choose, preferring cheap high-quota 'flash' tiers.
    """
    if MODEL_OVERRIDE:
        print(f"[runner] GEMINI_MODEL override = {MODEL_OVERRIDE}")
        return MODEL_OVERRIDE

    available = []
    for m in genai.list_models():
        if "generateContent" in getattr(m, "supported_generation_methods", []):
            # names come back like "models/gemini-2.0-flash" — strip prefix
            available.append(m.name.split("/", 1)[-1])

    if not available:
        sys.exit("No models support generateContent for this API key. "
                 "Check the key at https://aistudio.google.com/apikey")

    # Avoid preview/experimental/vision/thinking variants when a stable one exists
    def is_stable(name: str) -> bool:
        return not any(tag in name for tag in ("exp", "preview", "thinking", "vision"))

    stable = [n for n in available if is_stable(n)]
    pool = stable or available

    for pref in MODEL_PREFERENCE:
        for name in pool:
            if name == pref:
                print(f"[runner] resolved model = {name}")
                return name
    # Loose substring match next (e.g. dated variant 'gemini-2.0-flash-001')
    for pref in MODEL_PREFERENCE:
        for name in pool:
            if pref in name:
                print(f"[runner] resolved model = {name} (matched '{pref}')")
                return name

    # Last resort: anything that works
    print(f"[runner] no preferred match; using {pool[0]}")
    print(f"[runner] available models were: {', '.join(available)}")
    return pool[0]

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


def _read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        return f"(file not found: {path})"
    try:
        return p.read_text(encoding="utf-8")
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
    """Search the web via DuckDuckGo (no API key needed)."""
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        results = []
        if data.get("Abstract"):
            results.append(f"Summary: {data['Abstract']} (Source: {data.get('AbstractSource', '')})")
        for topic in data.get("RelatedTopics", [])[:6]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(f"- {topic['Text']}")

        # Also try news via RSS for financial queries
        if not results or any(w in query.lower() for w in ["stock", "market", "price", "earnings", "sp500", "spy"]):
            rss_results = _fetch_finance_rss(query)
            if rss_results:
                results.append("\nRecent news:")
                results.extend(rss_results)

        return "\n".join(results) if results else f"No results for: {query}"
    except Exception as e:
        return f"Search error: {e}"


def _fetch_finance_rss(query: str) -> list:
    """Fetch recent headlines from Yahoo Finance RSS."""
    try:
        # Extract ticker if present (uppercase word 2-5 chars)
        tickers = re.findall(r'\b([A-Z]{2,5})\b', query)
        symbol = tickers[0] if tickers else "SPY"
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            xml = resp.read().decode("utf-8")
        titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", xml)
        dates = re.findall(r"<pubDate>(.*?)</pubDate>", xml)
        items = []
        for title, date in zip(titles[1:6], dates[:5]):  # skip feed title
            items.append(f"  [{date[:16]}] {title}")
        return items
    except Exception:
        return []


TOOL_FNS = {
    "bash_execute":   _bash,
    "read_file":      _read,
    "write_file":     _write,
    "list_directory": _ls,
    "web_search":     _web_search,
}

# ── Gemini tool declarations (google-generativeai format) ────────────────────

TOOL_DECLARATIONS = protos.Tool(
    function_declarations=[
        protos.FunctionDeclaration(
            name="bash_execute",
            description=(
                "Run any shell command in the repo root. Use for: "
                "./scripts/alpaca.sh (trading), ./scripts/notify.sh (Telegram), "
                "git commands (commit, push, pull), and any other CLI operation."
            ),
            parameters=protos.Schema(
                type=protos.Type.OBJECT,
                properties={"command": protos.Schema(type=protos.Type.STRING, description="Shell command to run")},
                required=["command"],
            ),
        ),
        protos.FunctionDeclaration(
            name="read_file",
            description="Read a file from the repository (relative path from repo root).",
            parameters=protos.Schema(
                type=protos.Type.OBJECT,
                properties={"path": protos.Schema(type=protos.Type.STRING, description="Relative file path")},
                required=["path"],
            ),
        ),
        protos.FunctionDeclaration(
            name="write_file",
            description="Write content to a file in the repository. Creates parent directories automatically.",
            parameters=protos.Schema(
                type=protos.Type.OBJECT,
                properties={
                    "path":    protos.Schema(type=protos.Type.STRING, description="Relative file path"),
                    "content": protos.Schema(type=protos.Type.STRING, description="Full file content to write"),
                },
                required=["path", "content"],
            ),
        ),
        protos.FunctionDeclaration(
            name="list_directory",
            description="List files in a directory (relative path, defaults to repo root).",
            parameters=protos.Schema(
                type=protos.Type.OBJECT,
                properties={"path": protos.Schema(type=protos.Type.STRING, description="Relative directory path")},
                required=[],
            ),
        ),
        protos.FunctionDeclaration(
            name="web_search",
            description=(
                "Search the web for current information. Use this whenever the playbook says WebSearch. "
                "Good for: stock news, earnings, analyst ratings, macro events, market conditions."
            ),
            parameters=protos.Schema(
                type=protos.Type.OBJECT,
                properties={"query": protos.Schema(type=protos.Type.STRING, description="Search query")},
                required=["query"],
            ),
        ),
    ]
)

# ── Context builder ──────────────────────────────────────────────────────────

def build_prompt(routine: str) -> str:
    playbook = _read(ROUTINES[routine])
    files = list(BASE_MEMORY)
    if routine.startswith("aggro"):
        files += AGGRO_MEMORY

    mem_sections = [f"### {f}\n{_read(f)}" for f in files]
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return textwrap.dedent(f"""
        Current UTC time: {now_utc}

        ## YOUR PLAYBOOK — follow every step in order:

        {playbook}

        ---

        ## MEMORY FILES (your current state — update via write_file):

        {chr(10).join(mem_sections)}
    """).strip()

# ── Error handling ────────────────────────────────────────────────────────────

def _handle_api_error(exc: Exception) -> None:
    """Turn cryptic Gemini API errors into one clear, actionable line."""
    msg = str(exc)
    if "429" in msg or "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower():
        print("\n[runner] ⚠️  Gemini free-tier quota hit (429). This is NOT a code "
              "bug — the key ran out of free requests for the day, or the chosen "
              "model has a 0 free quota in your region.\n"
              "        Fix options:\n"
              "        • Wait ~24h for the daily free quota to reset, or\n"
              "        • Set a GitHub secret GEMINI_MODEL to a lighter model "
              "(e.g. gemini-2.0-flash-lite), or\n"
              "        • Enable billing at https://aistudio.google.com/apikey "
              "(pay-as-you-go has far higher limits and is near-free at this volume).")
    elif "404" in msg or "not found" in msg.lower():
        print("\n[runner] ⚠️  Model not found (404). The runner auto-resolves models, "
              "so this usually means the key has access to no chat models at all.\n"
              "        Check the key at https://aistudio.google.com/apikey")
    elif "API_KEY_INVALID" in msg or "API key not valid" in msg:
        print("\n[runner] ⚠️  Invalid GEMINI_API_KEY. Re-copy it from "
              "https://aistudio.google.com/apikey into the GitHub secret.")
    else:
        print(f"\n[runner] ⚠️  Gemini API error: {msg}")


# ── Agentic loop ─────────────────────────────────────────────────────────────

def run(routine: str) -> None:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        sys.exit("GEMINI_API_KEY environment variable not set")
    if routine not in ROUTINES:
        sys.exit(f"Unknown routine: {routine}\nValid: {', '.join(ROUTINES)}")

    print(f"[runner] syncing with main …")
    _bash("git pull origin main --rebase --autostash 2>&1 || true")

    genai.configure(api_key=api_key)

    chosen_model = resolve_model()

    model = genai.GenerativeModel(
        model_name=chosen_model,
        tools=[TOOL_DECLARATIONS],
        system_instruction=(
            "You are Bull, an autonomous AI trading agent. "
            "Follow every step in the playbook exactly. "
            "Use bash_execute to run shell scripts (alpaca.sh, notify.sh) and git commands. "
            "Use write_file to update memory files. "
            "Use web_search whenever the playbook says to use WebSearch — treat them identically. "
            "At the END of every run, after all other steps, commit and push: "
            "bash_execute('git add -A && git commit -m \"<routine>: <summary>\" "
            "&& git push origin HEAD:main'). "
            "If push is rejected, run 'git fetch origin main && git rebase origin/main' then push again."
        ),
    )

    print(f"[runner] starting {routine} with {chosen_model}")
    chat = model.start_chat()
    try:
        response = chat.send_message(build_prompt(routine))
    except Exception as exc:
        _handle_api_error(exc)
        raise

    turns = 0
    while turns < MAX_TURNS:
        # Print any text
        for part in response.parts:
            if hasattr(part, "text") and part.text:
                print(f"[model] {part.text[:200].replace(chr(10), ' ')}")

        # Collect function calls
        fn_calls = []
        for part in response.parts:
            try:
                if part.function_call and part.function_call.name:
                    fn_calls.append(part.function_call)
            except Exception:
                pass

        if not fn_calls:
            print(f"[runner] routine complete ({turns + 1} turns)")
            break

        # Execute tools and collect responses
        fn_responses = []
        for fc in fn_calls:
            args = dict(fc.args)
            print(f"[tool]  {fc.name}({list(args.keys())})")
            fn = TOOL_FNS.get(fc.name)
            try:
                result = fn(**args) if fn else f"(unknown tool: {fc.name})"
            except Exception as exc:
                result = f"ERROR: {exc}"

            fn_responses.append(
                protos.Part(
                    function_response=protos.FunctionResponse(
                        name=fc.name,
                        response={"result": result},
                    )
                )
            )

        try:
            response = chat.send_message(fn_responses)
        except Exception as exc:
            _handle_api_error(exc)
            raise
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
