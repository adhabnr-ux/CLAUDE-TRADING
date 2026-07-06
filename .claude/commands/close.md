Run the Bull **end-of-day close** routine.

## 0. Live-switch guard, lock, control switch, memory
- **Live-switch guard:** assert `ALPACA_BASE_URL` contains `paper`. If not,
  🚨 notify and stop.
- **Lock:** read `memory/_lock`. If present and not expired, abort and notify.
  Otherwise write `_lock` with `{routine: close, started, expires: +8min}`.
- **Control switch:** read `memory/control.md` and note its STATUS in the
  journal (close places no orders, so PAUSED/RISK_OFF only changes what you
  report).
- **Memory:** read every file in `memory/` and `CLAUDE.md`.

## 0b. Half-day / dedup guard
- Check the Alpaca clock's `next_close` field. If today is a **half-day**
  (next_close was at 13:00 ET, not 16:00 ET), still run — but mark it in the
  journal so the dashboard knows.
- **Dedup:** if `memory/performance.csv` already has a row for today's date
  + `bull`, do NOT append another. Update the existing row instead. The
  routine sometimes fires late on a half-day after the market is already
  closed and would otherwise double-write.

## 1. Pull final numbers
- `./scripts/alpaca.sh account` — equity, cash.
- `./scripts/alpaca.sh positions` — final positions.
- `./scripts/alpaca.sh history 1A 1D` — portfolio equity history (also gives
  the high-water mark for the circuit breaker).
- `./scripts/alpaca.sh bars SPY 1Day 30` — SPY bars to compute the benchmark.

## 2. Compute performance
- Today's portfolio P/L (dollar and %).
- SPY's return today and since inception.
- Bull vs SPY: since-inception difference (the number that actually matters).
- Equity vs. its high-water mark — if within 2% of the −10% circuit-breaker
  level, flag it in the journal and the notify message.

## 3. Reconcile exits
Compare today's positions against `memory/trade-log.md` and
`memory/closed-trades.md`. If any position exited today (stop fill, midday
cut, manual close) and has **no entry in `memory/closed-trades.md`**, add it
now using the template — and for a loss, append the required dated lesson to
`memory/lessons.md`. The ledger must never lag reality by more than one day.

## 4. Market close context (WebSearch)
Search `"stock market summary today <today's date>"`. Write one sentence of
context in the journal: what drove the market today, and whether it supports
or threatens Bull's current position theses.

## 5. Journal
- Update `memory/portfolio.md` (account, positions with sector, the vs-SPY
  table, sector-exposure line).
- If anything notable happened today, append a dated lesson to
  `memory/lessons.md`.
- On a day with zero trades and no exits, keep the `portfolio.md` narrative
  section to a short paragraph rather than a full multi-bullet writeup.

## 5b. Race scoreboard
Read `memory/aggressive/portfolio.md` (read-only) and compute the race:
Bull % vs AGGRO % vs SPY % since inception. Include one scoreboard line in
the notify, e.g. `Race: Bull +1.2 | AGGRO -4.2 | SPY +2.3 (pct since start)`.

## 5c. Performance history
Append one row to `memory/performance.csv` — create it with the header
`date,agent,equity,cash,spy_close` if missing: today's date, `bull`, final
equity, final cash, SPY's closing price. This feeds the dashboard in `docs/`
and the weekly cash-drag audit.

## 5d. Friday watchdog
If today is Friday and the newest entry in `memory/weekly-review.md` is more
than 7 days old, last week's review never ran — flag it with 🚨 in the notify
so the human can check the routine schedule.

## 5e. Monthly housekeeping
- On the first trading day of each month: move `research-log.md` and
  `trade-log.md` entries older than 30 days into
  `memory/archive/<YYYY-MM>.md` (create the folder if needed), leaving a
  one-line pointer at the top of each log.
- Quarterly (Mar/Jun/Sep/Dec, mid-month): WebSearch the latest SPY
  ex-dividend amount and add it to a cumulative-dividends note in
  `portfolio.md`, so the vs-SPY comparison reflects total return, not just
  price.

## 6. Notify (every weekday)
Send a Telegram end-of-day summary via `./scripts/notify.sh`, starting with
`Bull EOD <date>:` — equity in USD, today's %, vs SPY since inception, the
race scoreboard line, number of trades today, and a one-line note. Start with
🚨 if a position exited at a loss today, the circuit breaker is near/active,
or the Friday watchdog fired. Never put a literal `$` in the message; use
`USD`/plain numbers and single-quote the argument.

## 7. Commit
`git add -A && git commit -m "close: <summary>" && git push origin HEAD:main`.
If the push is rejected because `main` moved, run
`git fetch origin main && git rebase origin/main`, then push again.
