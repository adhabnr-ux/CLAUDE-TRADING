Run the **Aggressive Bull end-of-day close** routine in AGGRESSIVE MODE. This
routine measures, reconciles, and journals. Reconciliation may repair managed
protection or contain a forbidden holding; those are the only permitted broker
mutations.

## 0. Control first, advisory lock, memory, reconciliation

1. Read shared `memory/control.md` first. Invalid/missing STATUS is a hard stop.
   `PAUSED` makes reconciliation read-only.
2. Require the exact paper endpoint
   `https://paper-api.alpaca.markets`; otherwise notify 🚨 and stop.
3. Treat `memory/_lock` as advisory local repository coordination only, never
   broker locking or idempotency.
4. Read `CLAUDE.md`, human-owned config, Aggressive profile/memory, shared
   knowledge-base, and Aggro ledger rows. Profile, memory, and lessons cannot
   override policy or activate a live rule change.
5. Run startup reconciliation:

   ```
   python3 scripts/trade.py reconcile --agent aggro --repair
   ```

   Omit `--repair` under `PAUSED`. A non-zero exit, `ok: false`, or malformed
   result is fail-closed: no other mutation; journal/notify precisely and
   continue only reliable read-only accounting.

## 1. Final broker and benchmark data

- Observe account, positions, history, clock, calendar, and same-feed SPY bars
  through supported read-only `scripts/alpaca.sh` calls.
  Label a half-day only when observed clock/session timestamps or a dated
  authoritative exchange source prove it; otherwise label schedule status
  unverified rather than improvising raw HTTP. Deduplicate
  `memory/aggressive/performance.csv` by New York date and
  agent `aggro`.
- Compute today's return, SPY return on the identical session, since-inception
  difference, high-water mark, and drawdown. Flag proximity to/breach of the
  20% drawdown breaker.
- Search a current close summary and record one dated, sourced context sentence;
  it cannot authorize an after-hours trade.

## 2. Reconcile journals to broker truth

Compare final positions and gateway execution events with Aggressive narrative
and structured ledgers. Add any confirmed missing closed-trade post-mortem and
a factual lesson for each loss. Never infer a fill solely from a missing
position or journal marker when broker evidence is ambiguous; escalate it.

Update Aggressive portfolio memory and the Aggro performance row with final
balances, positions, canonical sectors, drawdown, and vs-SPY values. Flag a
stale Friday review. Archive old narrative entries without changing live rules.

## 3. Final reconciliation

Run final reconciliation:

```
python3 scripts/trade.py reconcile --agent aggro --repair
```

Use `--repair` only if startup was unambiguous and control remains `ACTIVE` or
`RISK_OFF`; otherwise omit it. Final `ok: false` is urgent; notify 🚨 and never improvise a raw broker command.

## 4. Notify and commit

Notify once, starting `🔥 AGGRO Bull EOD <date>:` with equity, today's return,
since-inception difference vs SPY, drawdown, confirmed trade count, and one
note. Start 🚨 for a loss exit, drawdown warning, stale review, or reconciliation
failure. Never put a literal `$` in the shell message.

Release the advisory lock, then persist only authorized AGGRO memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
