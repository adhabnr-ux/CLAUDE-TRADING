Run the Bull **market-open** routine.

## 0. Live-switch guard, lock, control switch, memory
- **Live-switch guard:** if `ALPACA_BASE_URL` does not contain `paper`, send
  🚨 "live endpoint detected, halting", stop.
- **Lock:** read `memory/_lock`. If present and not expired, abort and notify
  "skipped, another routine active". Otherwise write `_lock` with
  `{routine: market-open, started, expires: +8min}`.
- **Control switch:** read `memory/control.md`. If `STATUS: PAUSED`, journal,
  notify, release the lock, commit, stop. If `STATUS: RISK_OFF`, skip all
  buys but still run the stop audit (step 5).
- **Memory:** read every file in `memory/` and `CLAUDE.md`. Find the most
  recent **"Planned trades for today"** fenced JSON block in
  `memory/research-log.md` and confirm its `plan_date` is **today**. If the
  latest plan is from an earlier day, pre-market did not run today — treat
  the plan as stale, place no trades, journal that, and skip to step 6. (If
  the latest entry is older freeform prose without a JSON block, parse it
  carefully and note the format gap.)
- **Idempotency:** if today's plan block is already followed by an
  `EXECUTED:` line, this routine already ran today — place no trades and
  skip to step 5.

## 1. Confirm the market is open
`./scripts/alpaca.sh clock`. If `is_open` is false, place no trades — journal
"market closed, no action" and skip to step 6.

## 2. Breaking-news gate (WebSearch)
For each symbol in today's planned trades, search
`"<SYMBOL> stock news this morning <today's date>"`. If anything reveals an
earnings miss, major downgrade, trading halt, SEC action, or other
thesis-breaking event that was NOT in the pre-market plan — skip that trade
and note why in the journal. This is a fast go/no-go gate, not a full
re-research.

## 3. Re-check before executing
- `./scripts/alpaca.sh account` and `./scripts/alpaca.sh positions` for live state.
- **Shock check:** if equity is more than 4% below the account's
  `last_equity`, send a 🚨 notify, place no buys today, and journal the event.
- For each planned trade, `./scripts/alpaca.sh snapshot <SYM>` to confirm the
  price has not moved against the thesis. Skip any trade that no longer makes
  sense and note why.

## 4. Execute planned trades
For each approved trade, re-verify the guardrails in `CLAUDE.md` — write the
math in the journal: 20% max position, 25% max daily deployment, 5% min cash,
60% sector cap, earnings window. Then:
- Get the current ask: `./scripts/alpaca.sh quote <SYM>`. Compute a
  **marketable limit** = ask × 1.003 (rounded to cents) — pays at most 0.3%
  over the ask instead of whatever the opening auction does.
- Place the buy: `./scripts/alpaca.sh buy-limit <SYM> <qty> <limit>`.
- Verify the fill: `./scripts/alpaca.sh orders open` /
  `./scripts/alpaca.sh position <SYM>`. If still unfilled after a couple of
  minutes: cancel it, re-quote, and re-place at the new ask × 1.003 **once**.
  If the second attempt also doesn't fill, cancel, skip the trade, and
  journal "missed fill — price ran away" (chasing is how slippage wins).
- Immediately place a 10% trailing stop on the **filled** quantity:
  `./scripts/alpaca.sh trailing-stop <SYM> sell <qty> 10`.
- Verify the trailing-stop order exists.
- After **each** verified fill, append one JSON line to
  `memory/trades.jsonl` with the schema documented in
  `memory/trades.jsonl.md` (`agent: "bull"`, ts, action, symbol, qty,
  fill_price, thesis, invalidation, review_by). This is the structured
  feed for the weekly review's stats.
- After all trades are done, append a line `EXECUTED: <timestamp>` directly
  under today's plan block in `memory/research-log.md` so a re-run cannot
  double-buy.

## 5. Stop audit & exit reconciliation
- Compare `./scripts/alpaca.sh positions` against `./scripts/alpaca.sh orders open`:
  **every position must have a live trailing-stop order.** If one is missing,
  place it now (`trailing-stop <SYM> sell <qty> 10`) and journal that the
  audit recreated it.
- If a trailing stop **filled** since the last run (a position is gone or
  shrunk), record the exit in `memory/closed-trades.md` using its template —
  and for a loss, append the required dated lesson to `memory/lessons.md`.

## 6. Journal
- Append each trade to `memory/trade-log.md` (action, fill, why, stop order id,
  verified).
- Update `memory/portfolio.md` with the new positions, balances, and sector
  exposure.

## 7. Notify
Send one Telegram summary via `./scripts/notify.sh` on every run, starting
with `Bull market-open <date>:` — if trades were placed, list what was
bought/sold, fill price, and the stop set; if not, "no trades, <one-line
reason>". Start with 🚨 if a stop filled, a trade was blocked, or the audit
found an unprotected position. On a plain no-trade day, keep it to one
sentence. Never put a literal `$` in the message; use `USD`/plain numbers and
single-quote the argument.

**Journal length on no-trade days:** if the plan was empty and the stop audit
passed clean, write a short paragraph in `trade-log.md`/`portfolio.md`
(account snapshot, stop-audit result, one line why no trades) instead of a
long writeup.

## 8. Commit
`git add -A && git commit -m "market-open: <summary>" && git push origin HEAD:main`.
If the push is rejected because `main` moved, run
`git fetch origin main && git rebase origin/main`, then push again.
