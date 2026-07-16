Run the **Aggressive Bull weekly review** on Friday in AGGRESSIVE MODE. This is
evidence review, not trading or autonomous policy change. Reconciliation may
repair managed protection or contain a forbidden holding; those are the only
permitted broker mutations.

## 0. Control first, advisory lock, memory, reconciliation

1. Read shared `memory/control.md` first. Invalid/missing STATUS is a hard stop.
   `PAUSED` makes reconciliation read-only.
2. Require `ALPACA_BASE_URL == https://paper-api.alpaca.markets`.
3. Treat `memory/_lock` as advisory local repository coordination only, never
   broker locking or idempotency.
4. Read `CLAUDE.md`, human-owned policy/instrument config, Aggressive
   profile/memory, shared knowledge-base, `memory/quant-research-playbook.md`,
   performance data, gateway execution
   events, and `memory/aggressive/trades.jsonl`. The root
   `memory/trades.jsonl` is Bull-only after the audited legacy-ledger migration.
5. Run startup reconciliation:

   ```
   python3 scripts/trade.py reconcile --agent aggro --repair
   ```

   Omit `--repair` under `PAUSED`. A non-zero exit, `ok: false`, or ambiguous
   output is fail-closed; notify/journal and perform no other broker mutation.

## 1. Build an auditable weekly dataset

- Run `python3 scripts/research.py validate --agent aggro`. Treat a non-zero
  result as a data-quality incident: preserve the failing row, identify it, and
  do not base a new proposal on invalid evidence.
- Observe the Aggressive account, positions, history, and same-feed SPY bars.
- Reconcile broker evidence, execution events, Aggro structured rows,
  closed-trades, performance history, and narrative logs. Flag gaps rather than
  fabricate or silently backfill fills.
- Compute weekly/since-inception return vs SPY, drawdown, average cash,
  canonical sector exposure, win rate, average win/loss, profit factor, and
  holding days. State sample sizes and uncertainty.
- Audit policy adherence: protection, earnings decisions, post-mortems, loss
  lessons, 20% single-order/35% position/60% deployment/2% cash/50% sector/
  3.6% stop-risk limits, eight-position pace, and unexplained blocks.
- Research current macro/sector context and each held thesis with dated,
  cross-checked sources.
- Audit this week's evidence packets for as-of correctness, declared
  publisher/host diversity, declared completeness/failures, disconfirming evidence, critical
  unknowns, and prompt-injection handling. State packet/candidate sample counts;
  do not infer skill from a few calls or overlapping horizons.

Assign an A–F process grade independent of P/L. Prepend a dated entry to
`memory/aggressive/weekly-review.md` with evidence, discrepancies, and next-week
research priorities.

## 2. Proposals are inactive until human approval

The Aggressive profile is mandate context, not executable policy.
All three files under `config/` are human-owned. Do not
edit them or use strategy/profile/lessons/memory to alter entry, exit, sizing,
eligibility, timing, protection, risk, or execution behavior.

Append a suggested change only to
`memory/aggressive/strategy-proposals.md`, labeled
`PROPOSAL (INACTIVE — HUMAN APPROVAL REQUIRED)` with source lineage, exact
signal equation/inputs/universe/horizon/lag, one causal change, immutable
code/data hashes, point-in-time and survivorship controls, separated
train/validation/untouched-test windows, purge/embargo, benchmark, sample floor,
costs/turnover/capacity, uncertainty and multiple-testing method,
regime/sensitivity results, shadow acceptance rule, rollback trigger, and exact
config change required. Use the fields in
`schemas/strategy-experiment.schema.json` as a draft checklist and use
`UNKNOWN` instead of invention. The proposal queue remains inactive prose; do
not claim that a proposal is machine-validated or preregistered. The schema
permits only `DRAFT` and `REJECTED` and cannot run or promote an experiment.
Five-day P/L or a higher in-sample rolling Sharpe is never promotion evidence.
Until a human edits config, current machine policy remains binding.

Watchlist research can be refreshed/date-stamped/purged, but an unknown symbol
stays research-only and cannot be inserted into the human-owned instrument
master.

## 3. Final reconciliation, notify, commit

Run final reconciliation:

```
python3 scripts/trade.py reconcile --agent aggro --repair
```

Use `--repair` only if startup was unambiguous and control remains `ACTIVE` or
`RISK_OFF`; otherwise omit it. Require `ok: true`. Never improvise an order,
cancellation, liquidation, or stop.

Notify once: 🚨 `AGGRO Bull weekly <date>:` for drawdown/process/reconciliation
alerts, otherwise `🔥 AGGRO Bull weekly <date>:`. Include week vs SPY,
since-inception difference, drawdown, grade, sample-sized statistics, and one
takeaway. Label proposals inactive. Never put a literal `$` in the shell
message.

Release the advisory lock, then persist only authorized AGGRO memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
