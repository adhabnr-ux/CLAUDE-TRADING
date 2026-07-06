Run the Bull **pre-market** routine.

## 0. Live-switch guard, lock, control switch, memory
- **Live-switch guard:** if `ALPACA_BASE_URL` does not contain `paper`, send
  🚨 "live endpoint detected, halting", place no orders, stop.
- **Lock:** read `memory/_lock`. If present and not expired, abort and notify
  "skipped, another routine active". Otherwise write `_lock` with
  `{routine: premarket, started, expires: +8min}` and continue.
- **Control switch:** read `memory/control.md`. If `STATUS: PAUSED`, write
  "paused by human" to the research log, notify, release the lock, commit,
  and stop. If `STATUS: RISK_OFF`, plan no new buys today. Acknowledge any
  `NOTE:` line in the journal. If a `QUERY:` line is present, draft a
  paragraph answer for inclusion in the notify (step 9) and clear the line by
  rewriting the file.
- **Memory:** read every file in `memory/` (`strategy.md`, `portfolio.md`,
  `trade-log.md`, `research-log.md`, `lessons.md`, `weekly-review.md`,
  `knowledge-base.md`, `closed-trades.md`, last ~50 lines of `trades.jsonl`).
  Also read `CLAUDE.md` for the guardrails.

## 1. First-run check
If `memory/strategy.md` still has `STATUS: NOT_INITIALIZED`:
- Do the one-time strategy design described in that file: research current
  macro conditions, indices, rates, and sector trends with `WebSearch`.
- Rewrite `memory/strategy.md` with a full strategy (thesis, universe, entry
  signals, sizing, exit signals, cash policy, watchlist) and set
  `STATUS: ACTIVE`.
- Record the inception baseline in `memory/portfolio.md`: today's date and the
  account's current equity (from `./scripts/alpaca.sh account`). Every future
  "vs SPY since inception" comparison anchors to this baseline.
- Then continue with the steps below.

## 2. Sync portfolio state
- `./scripts/alpaca.sh account` and `./scripts/alpaca.sh positions`.
- Update `memory/portfolio.md` with current equity, cash, buying power, and
  every open position (qty, avg entry, current price, market value,
  unrealized P/L, % of portfolio, **sector**). Keep a one-line sector-exposure
  summary under the positions table (e.g. `Tech 38% | Healthcare 8% | Cash 54%`).

## 3. Risk posture check
Before planning any buys:
- **Drawdown note:** `./scripts/alpaca.sh history 1A 1D` — find the equity
  high-water mark and journal current equity vs. it as one line. This is
  informational only — it does not block new buys (removed as a hard
  guardrail 2026-06-30; use judgment on genuinely bad macro days instead).
- **Sector cap:** note current sector exposure. No planned buy may push one
  sector above **60%** of portfolio value.

## 3b. Thesis contract review
Every position carries an `invalidation` and a `review_by` date (from its
entry plan and trade-log; if a legacy position has none, write one now). For
each held position, check both against the current price and this morning's
news. If the invalidation has triggered or the review date has passed: decide
hold / trim / exit explicitly today and journal the decision — renew the
contract with a new `review_by` if holding.

## 3c. Conviction-weighted holding review (Monday only)
On Mondays, re-rank every held position **A / B / C**:
- **A** — original thesis intact, working, conviction still high.
- **B** — working but flat, or thesis intact but the catalyst slipped.
- **C** — thesis is wobbling, position is dragging, or it's been quiet too long.

Track each position's rating in `memory/portfolio.md`. **If a name has been
rated C for 3 consecutive Monday reviews and has not been promoted to B+,
plan to trim it by half today.** Forces decisions on quiet underperformers
instead of letting them rot toward the −7% rule.

## 4. Research (WebSearch)
- **Market posture:** search `"S&P 500 futures pre-market <today's date>"` —
  overnight direction, macro news (Fed, CPI, jobs, geopolitical), and the
  broad risk-on/off mood.
- **Each held position:** search `"<SYMBOL> stock news <today's date>"` —
  earnings, analyst changes, guidance, thesis-breaking events.
- **Earnings calendar:** for every held name and every buy candidate, confirm
  the next earnings date (search `"<SYMBOL> next earnings date"`).
- **Watchlist:** check catalysts and valuation for the highest-conviction
  names in `memory/strategy.md`.

Record findings as dated bullets in `memory/research-log.md` (source,
headline, relevance, date of the fact).

For **every held position**, the research-log entry MUST contain a one-line
"what changed since yesterday" — even if it is "nothing material, thesis
unchanged". Forces engagement with overnight news instead of stale theses.

## 5. Earnings-window rule
- **No new buy** in any name reporting earnings within the next 2 trading days.
- For every **held** name reporting within 2 trading days: make an explicit
  hold / trim decision and journal one sentence of reasoning. Gap risk blows
  through trailing stops — deciding by default is not allowed.

## 6. Cash-drag check
Compare cash % to the target band in `memory/strategy.md`. If cash has been
above the band for more than a week and the tape is constructive — either
plan at least one qualifying entry today or write one explicit sentence in
the research log explaining why staying heavy in cash is right. Idle cash
must be a decision, not a default.

## 6b. Daily candidate diligence (breaks the "sourced but never vetted" stall)
If any watchlist entry is marked research-only / undiligenced, run a full
pre-trade diligence pass (recent 10-Q/10-K highlights, valuation vs. peers,
balance sheet sanity check, one-paragraph thesis, ATR check) on **at least
one** such name every pre-market run — do not wait for the weekly review.
Pick the most-ready candidate first. Promote it to a real buy candidate today
if it clears the Entry Signals and ATR gate; otherwise journal specifically
what's still missing so tomorrow's run knows where to pick up. A candidate
sitting in "research-only" for more than a week without a diligence attempt
is a process failure, not a market condition.

## 7. Draft today's plan
Decide which trades (if any) to make at the open, strictly within the
guardrails in `CLAUDE.md`: 20% max per position, 25% max daily new-buy
deployment, 5% min cash, the 60% sector cap, and the earnings window. Prefer
whole-share quantities so trailing stops are possible.

**Volatility check:** for each planned buy, pull
`./scripts/alpaca.sh bars <SYM> 1Day 21` and estimate the 20-day average
daily range as a % of price (mean of `(high − low) / close`). If it exceeds
**3%**, halve the planned position size and journal the ATR figure — a 10%
trailing stop on a 4%-a-day name is only ~2.5 quiet days of room, so size
must carry the extra risk, not hope.

Append a new dated entry to `memory/research-log.md` ending with a
**"Planned trades for today"** section that contains a fenced JSON block in
exactly this shape (market-open parses it):

```json
{
  "plan_date": "YYYY-MM-DD",
  "trades": [
    {"action": "buy", "symbol": "XYZ", "qty": 10, "thesis": "one sentence",
     "invalidation": "price or event that kills the thesis",
     "review_by": "YYYY-MM-DD"}
  ]
}
```

If no trades are warranted, use `"trades": []` and write "No trades planned."
above the block.

## 8. Notify
Do NOT trade now (market is closed). Send a Telegram summary via
`./scripts/notify.sh` on every run, starting with `Bull pre-market <date>:` —
market posture in a phrase plus the planned trades (or "no trades planned").
Put anything urgent first (thesis-contract deadline, unprotected stop, shock
day). On a routine no-trade day with nothing urgent, keep the whole message
to 1-2 sentences — do not pad it out. Never put a literal `$` in the message;
use `USD`/plain numbers and single-quote the argument.

**Journal length on no-trade days:** if there are no trades, no thesis-contract
triggers, no stop-audit failures, and no shock event, write the
`research-log.md` entry as a short paragraph (account snapshot line, one line
per held position, one line on the diligence pass from step 6b, cash-drag
line) instead of the full multi-section report. Save the long-form writeup
for days something actually happened.

## 9. Commit
`git add -A && git commit -m "premarket: <summary>" && git push origin HEAD:main`.
If the push is rejected because `main` moved, run
`git fetch origin main && git rebase origin/main`, then push again.
