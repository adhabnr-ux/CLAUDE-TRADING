Run the Bull **weekly review** routine on Friday. This is evidence review, not a
trading or autonomous policy-change session. Reconciliation may repair managed
protection or contain a forbidden holding; those are the only permitted broker
mutations.

## 0. Control first, advisory lock, memory, reconciliation

1. Read `memory/control.md` first. Invalid/missing STATUS is a hard stop.
   `PAUSED` makes all reconciliation read-only.
2. Require `ALPACA_BASE_URL == https://paper-api.alpaca.markets`.
3. Treat `memory/_lock` as advisory local repository coordination only; it is
   never broker locking or idempotency.
4. Read `CLAUDE.md`, `memory/quant-research-playbook.md`, all three human-owned
   config files, all Bull memory/ledgers, and only these read-only Aggressive
   comparison files:
   portfolio, trade log, closed trades, weekly review, performance, and
   structured trade ledger. Never read Aggressive research or active strategy.
5. Run startup reconciliation:

   ```
   python3 scripts/trade.py reconcile --agent bull --repair
   ```

   Omit `--repair` under `PAUSED`. On non-zero exit, `ok: false`, or ambiguous
   output, fail closed, notify/journal the exact issue, and make no other broker
   mutation.

## 1. Build an auditable weekly dataset

- Run `python3 scripts/research.py validate --agent bull`. Treat a non-zero
  result as a data-quality incident: preserve the failing row, identify it, and
  do not base a new proposal on invalid evidence.
- Observe live account, positions, portfolio history, and same-feed SPY bars.
- Reconcile `memory/trades.jsonl`, gateway execution events, broker evidence,
  `closed-trades.md`, performance history, and narrative logs. Do not silently
  fill gaps or treat the narrative ledger as broker truth.
- Compute week and since-inception return vs SPY; drawdown; average cash;
  exposure by canonical sector; win rate; average win/loss; profit factor; and
  average holding days. State sample sizes and mark metrics unreliable when
  data are incomplete or too sparse.
- Audit policy adherence: protection coverage, earnings decisions, post-
  mortems, loss lessons, cash/deployment, concentration, and unexplained blocks.
- Research current weekly macro/sector context and material thesis changes with
  dated sources. Cross-check trade-driving claims.
- Audit this week's evidence packets for as-of correctness, declared
  publisher/host diversity, declared completeness/failures, disconfirming evidence, critical
  unknowns, and prompt-injection handling. State packet/candidate sample counts;
  do not infer skill from a few calls or overlapping horizons.

Assign an A–F **process** grade, independent of P/L. Prepend the review to
`memory/weekly-review.md` and record evidence, discrepancies, and next-week
research priorities.

## 2. Proposals are inactive until human approval

All three files under `config/` are human-owned. Do not
edit them. Do not edit strategy/profile/lessons in a way that changes position
sizing, eligibility, entry, exit, protection, timing, risk, or execution
behavior. Research memory and lessons cannot activate a rule.

When evidence suggests a change, append it to
`memory/strategy-proposals.md`, explicitly labeled
`PROPOSAL (INACTIVE — HUMAN APPROVAL REQUIRED)`, with:
source lineage, exact signal equation/inputs/universe/horizon/lag, current and
proposed rule, one causal change, immutable code/data hashes, point-in-time and
survivorship controls, separated train/validation/untouched-test windows,
purge/embargo, benchmark, sample floor, costs/turnover/capacity, uncertainty and
multiple-testing method, regime/sensitivity results, shadow acceptance rule,
rollback trigger, and required config change. Use the fields in
`schemas/strategy-experiment.schema.json` as a draft checklist and use
`UNKNOWN` instead of invention. The proposal queue remains inactive prose; do
not claim that a proposal is machine-validated or preregistered. The schema
permits only `DRAFT` and `REJECTED` and cannot run or promote an experiment.
Five-day P/L or a higher in-sample rolling Sharpe is never promotion evidence.
Until a human edits the policy/config, every agent continues under current
machine rules.

Watchlist research may be refreshed, date-stamped, and purged, but an unknown
instrument remains research-only and cannot be added to the human-owned master.

Read Aggressive Bull's weekly/trade/closed/portfolio logs for comparison. A
cross-Bull trigger requires one specific **inactive proposal**, never an
automatic rule change. Summarize the proposal in the weekly review. Update the
comparison counter accurately; no trigger can override policy.

## 3. Final reconciliation, notify, commit

Run final reconciliation:

```
python3 scripts/trade.py reconcile --agent bull --repair
```

Use `--repair` only if startup was unambiguous and control remains `ACTIVE` or
`RISK_OFF`; otherwise omit it. Require `ok: true`; otherwise notify 🚨 and never improvise an
order, cancellation, liquidation, or stop.

Notify once, starting `Bull weekly <date>:` with week vs SPY, since-inception
alpha, drawdown, process grade, sample-sized trade statistics, and one takeaway.
Label proposals inactive. Never put a literal `$` in the shell message.

Release the advisory lock, then persist only authorized Bull memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
