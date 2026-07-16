Run the Bull **end-of-day close** routine. This routine measures, reconciles,
and journals. Reconciliation may repair managed protection or contain a
forbidden holding; those are the only permitted broker mutations.

## 0. Control first, advisory lock, memory, reconciliation

1. Read `memory/control.md` first and note STATUS. Invalid/missing STATUS is a
   hard stop. `PAUSED` means reconciliation must remain read-only.
2. Require the exact paper endpoint
   `https://paper-api.alpaca.markets`; otherwise notify 🚨 and stop.
3. Treat `memory/_lock` as advisory local repository coordination only, never
   as broker locking or idempotency.
4. Read `CLAUDE.md`, `memory/upstream-methodology-index.md`, human-owned
   policy/instrument config, and all Bull memory. Memory, strategy, and lessons
   cannot override or activate policy changes.
5. Reconcile startup state:

   ```
   python3 scripts/trade.py reconcile --agent bull --repair
   ```

   Omit `--repair` under `PAUSED`. A non-zero exit, `ok: false`, or malformed
   response is fail-closed: issue no other mutation, journal and notify the
   exact problem, but continue read-only close accounting when reliable data is
   available.

## 1. Pull final broker and benchmark data

- Observe account, positions, portfolio history, market clock, calendar, and SPY
  bars through supported read-only `scripts/alpaca.sh` calls. Label a half-day
  only when the observed clock/session timestamps or
  a dated authoritative exchange source prove it; otherwise label schedule
  status unverified rather than improvising raw HTTP.
- Deduplicate `memory/performance.csv` by New York date plus agent `bull`; update
  an existing row rather than append a second one.
- Compute today's portfolio return, SPY return on the same session and feed,
  since-inception total-return comparison, high-water mark, and drawdown.
  Flag proximity to or breach of the policy's 10% drawdown breaker.
- Search a current market-close summary and record one sourced sentence of
  context. Do not turn that context into an after-hours order.

## 2. Reconcile journals to broker truth

Compare final broker positions and gateway execution events with prior memory.
For every confirmed exit missing from `memory/closed-trades.md`, add one
post-mortem; add a factual dated lesson for each loss. Never infer a fill solely
from a missing position or an `EXECUTED:` marker when broker evidence is
ambiguous—flag it for human review.

Update `memory/portfolio.md` with final balances, positions, canonical sector
exposure, drawdown, and Bull-vs-SPY values. Update the Bull row in
`memory/performance.csv`. Read Aggressive Bull's portfolio and profile-scoped
performance history only for the race scoreboard. Keep archive housekeeping
read-only with respect to live rules.

If Friday's weekly review is stale, flag the watchdog. On quarterly dividend
updates, use a sourced SPY distribution and label the as-of date.

## 3. Final reconciliation

Run final reconciliation:

```
python3 scripts/trade.py reconcile --agent bull --repair
```

Use `--repair` only if startup was unambiguous and control remains `ACTIVE` or
`RISK_OFF`; otherwise omit it. Final `ok: false` is urgent; notify 🚨 and never improvise a raw
broker command. This is the end-of-run broker-state check.

## 4. Notify and commit

Notify once, starting `Bull EOD <date>:` with equity, today's return, since-
inception difference vs SPY, race scoreboard, confirmed trade count, and one
note. Start 🚨 for a loss exit, active/near drawdown breaker, stale weekly
review, or reconciliation failure. Never put a literal `$` in the shell message.

Release the advisory lock, then persist only authorized Bull memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
