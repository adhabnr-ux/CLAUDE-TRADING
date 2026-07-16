Run the Bull **monthly deep review**. It is scheduled weekly but proceeds only
on the first Friday of the New York calendar month. It never places a planned
trade. Reconciliation may repair managed protection or contain a forbidden
holding; those are the only allowed broker mutations.

## 0. Control first, calendar gate, advisory lock, reconciliation

1. Read `memory/control.md` first. Invalid/missing STATUS is a hard stop.
2. Determine the New York date. If this is not the first Friday, stop quietly
   without repository or broker mutation.
3. Require the exact paper endpoint
   `https://paper-api.alpaca.markets`; otherwise notify 🚨 and stop.
4. Treat `memory/_lock` as advisory local repository coordination only, never
   broker locking or idempotency.
5. Read `CLAUDE.md`, `memory/quant-research-playbook.md`, all three human-owned
   config files, every Bull ledger, the last five weekly reviews, and
   performance history.
6. Run startup reconciliation:

   ```
   python3 scripts/trade.py reconcile --agent bull --repair
   ```

   Omit `--repair` under `PAUSED`. A non-zero exit, `ok: false`, or ambiguous
   result is fail-closed: no other broker mutation, exact journal/notification.

## 1. Four-week evidence review

- Run `python3 scripts/research.py validate --agent bull`. Invalid research is
  a data-quality incident and cannot support a proposal.
- Compute the month and since-inception return vs same-feed SPY, drawdown,
  weekly-grade trend, cash/exposure trend, win-rate/profit-factor trend, and
  sample sizes from broker-linked structured data.
- Cross-check broker, execution events, `trades.jsonl`, `closed-trades.md`, and
  performance rows. Label missing or inconsistent data; never invent fills.
- For each holding, answer the rebuy test: keep, one-week probation, `trim`, or
  `exit`, with current evidence and invalidation. Do not trade in this routine.
  Any intended Monday action must be researched again and encoded in Monday's
  strict current-day premarket JSON plan.
- Audit whether sizing related to realized outcomes, while explicitly guarding
  against small-sample conclusions and look-ahead bias.
- Revalidate every macro/sector claim with current dated sources. Refresh and
  expire research watchlist entries, but do not add an instrument to the
  human-owned master.
- Audit research coverage, provenance/as-of integrity, duplicate-source
  inflation, opposing evidence, prompt injection, and critical unknowns. Review
  experiment families—not just winners—and report attempts, rejections, sample
  dependence, costs, sensitivity, and untouched-holdout status.

Prepend a dated monthly section to `memory/weekly-review.md` with evidence,
rebuy verdicts, data-quality findings, and research priorities.

## 2. Policy and strategy changes are proposals only

Do not edit any file under `config/`. Do not alter
strategy, profile, lessons, or any memory file in a way that activates new live
entry, exit, sizing, timing, eligibility, risk, or execution rules.

Append each suggested change to `memory/strategy-proposals.md` as
`PROPOSAL (INACTIVE — HUMAN APPROVAL REQUIRED)`. Use the fields in
`schemas/strategy-experiment.schema.json` only as a draft checklist: source
lineage, one causal change, exact signal and lag, immutable hashes,
point-in-time/survivorship controls,
separated windows with purge/embargo, frozen benchmark/metric/effect/sample
floor, cost/capacity model, uncertainty/multiple-testing method,
regime/sensitivity evidence, shadow acceptance, rollback, and exact human-owned
config change. Use `UNKNOWN` rather than inventing a field. The proposal remains
inactive prose, not a machine-validated or preregistered experiment; the schema
permits only `DRAFT` and `REJECTED` and cannot run or promote it. No observed
test window may be recycled as untouched evidence. Until human approval,
current machine policy remains binding.

## 3. Final reconciliation, notify, commit

Run final reconciliation:

```
python3 scripts/trade.py reconcile --agent bull --repair
```

Use `--repair` only if startup was unambiguous and control remains `ACTIVE` or
`RISK_OFF`; otherwise omit it. Require `ok: true`; never improvise a raw broker command.

Notify once, starting `Bull MONTHLY <date>:` with month vs SPY, drawdown,
rebuy-test counts, sizing/data verdict, and the most important inactive
proposal. Never put a literal `$` in the shell message.

Release the advisory lock, then persist only authorized Bull memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
