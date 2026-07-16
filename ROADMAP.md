# Bull - evidence-based roadmap

This roadmap separates controls that exist in code from research or operations
that still need evidence. A checked box means implemented and tested in this
repository; it does not mean error-free, profitable, or ready for live capital.

## Implemented safety foundation

- [x] Human `ACTIVE` / `RISK_OFF` / `PAUSED` control state.
- [x] Exact canonical Alpaca paper endpoint; direct shell mutations disabled.
- [x] Strict, same-day, schema-versioned `buy` / `trim` / `exit` plans.
- [x] Human-owned risk policy and instrument/sector master.
- [x] Human-owned earnings calendar with exact-match and freshness enforcement;
  an empty calendar blocks all buys.
- [x] Environment-bound account fingerprint and `TRADING_AGENT` profile binding.
- [x] Broker-side deterministic client IDs and lookup-before-submit.
- [x] Bounded limit entries and cumulative-remainder exits; cancellation
  confirmation and immutable recovery identities.
- [x] Position, order, modeled stop-risk, cash, sector, daily-deployment,
  weekly-new-position, spread, earnings, shock, and drawdown gates.
- [x] Exact aggregate trailing-stop coverage with PATCH-in-place repair and
  failed-replacement protection preservation.
- [x] Restart recovery: a completed entry cannot be bought again that day, even
  if narrative changes; an existing broker attempt also makes its quantity
  immutable.
- [x] Full-position midday loss exit as the sole same-day risk exception.
- [x] Per-agent execution-event and fill journals with broker identifiers.
- [x] Scheduled-runner command/path confinement and visible sync/push failures.
- [x] Same-host per-account, per-command operating-system lock and shared GitHub workflow
  concurrency group.
- [x] Automated tests and CI for policy, parsing, risk, idempotency, recovery,
  stop handling, runner boundaries, shell syntax, and schemas.

## Implemented research-governance foundation

- [x] Shared immutable quant-research playbook with evidence/inference
  separation, source tiers, explicit as-of time, visible collection failures,
  adversarial review, abstention, and prompt-injection boundaries.
- [x] Complete pinned QuantMind and ATLAS tracked-source snapshots with
  preserved MIT licenses, reconstructed-Git-tree integrity checks, quarantined
  instruction surfaces, exact unattended-agent read allowlists, and a mandatory
  human-owned methodology index. Vendoring supplies provenance, not alpha.
- [x] Strict profile-isolated research packets with canonical-URL duplicate
  and captured-content duplicate checks, referential integrity, symbol-scoped
  support, candidate source diversity, tier-1 primary evidence, opposing
  evidence, and critical-unknown gates.
- [x] Locked validate-before-append ledgers plus a deterministic fresh-buy gate.
  A new buy requires the latest same-session premarket packet to contain an
  exact-symbol candidate within human-owned age limits; packet ID/hash, thesis,
  invalidation, and review date must match the buy plan, and the evidence
  identity is written to execution audit records. Filled/partial recovery,
  protective actions, sells, and
  reconciliation remain available independently of research state.
- [x] Inactive strategy-experiment draft checklist with source lineage,
  one-change fields, immutable hashes, point-in-time/holdout controls, costs,
  uncertainty, multiple-testing, sensitivity, shadow, rollback, and human
  review. It permits only `DRAFT` and `REJECTED` and does not register, run,
  validate, or promote an experiment.

These controls improve research hygiene; they do not supply a dataset,
backtester, portfolio model, proven signal, or evidence of alpha.

## P0 - production-grade paper operations

These are prerequisites for calling the paper system operationally mature.

1. **Independent account registry.** Move profile-to-account identity outside
   the routine environment so a coordinated credential/expected-ID swap cannot
   pass.
2. **Cross-host serialization.** Add a durable account-scoped lease or a single
   execution service. Same-host file locking, workflow concurrency, and client
   IDs do not serialize independently scheduled cloud hosts.
3. **Out-of-process kill switch.** Put a broker/account-level halt outside the
   agent checkout; a Markdown control file is not an independent safety system.
4. **Durable transactional ledger.** Store orders, fills, positions, decisions,
   reconciliations, and state transitions in a database with uniqueness and
   referential constraints. JSONL/Markdown remain reports only.
5. **Broker activity ingestion.** Consume order/fill events continuously and
   reconcile them against the ledger, rather than waiting for scheduled agents.
6. **Observability and paging.** Metrics and alerts for stale data, missed runs,
   unknown order outcomes, unprotected shares, rejected stops, account drift,
   drawdown, notification failure, and repository persistence failure.
7. **Calendar-aware scheduling.** Exchange calendar, holidays, early closes,
   daylight saving, lateness budgets, and a watchdog for missed routines.
8. **Incident and chaos testing.** Exercise response loss after order acceptance,
   partial fills, delayed cancellation, broker/API outage, stale quotes, corrupt
   plans, failed pushes, and simultaneous routines.
9. **Independent security review.** Secret isolation, branch protection,
   CODEOWNERS/review requirements for the control plane, dependency pinning,
   provenance, and prompt-injection testing.

## P1 - research process that can earn the word quant

1. Define every signal mathematically; narrative news may annotate a signal but
   cannot create an untestable exception.
2. Build point-in-time, survivorship-bias-free datasets with splits, dividends,
   delistings, symbol changes, earnings timestamps, and corporate actions.
3. Run walk-forward and regime-stratified tests with untouched holdouts. Report
   confidence intervals, multiple-testing corrections, turnover, capacity, and
   parameter sensitivity - not one headline return.
4. Model commissions, spread, impact, open-auction behavior, borrow constraints,
   latency, failed fills, and taxes where applicable.
5. Add portfolio construction based on volatility, covariance, factor exposure,
   liquidity, risk contribution, and drawdown budgets. Compare it with simple
   equal-weight and SPY baselines.
6. Create a canonical performance service: time-weighted return, cash flows,
   dividends, daily benchmark snapshots from one feed, attribution, exposure,
   turnover, hit rate, payoff ratio, and maximum drawdown.
7. Register strategy versions. Agents may propose a change, but promotion needs
   reproducible evidence, review, a shadow period, rollback criteria, and a
   human-approved policy diff.
8. Add trusted acquisition receipts, a human-owned source registry, and a
   content-origin resolver. Agent-declared publisher, domain, source tier,
   timestamps, hashes, completeness, and prompt-injection status are not proof;
   fetched bytes, syndicated ownership, and privileged primary classifications
   need deterministic verification.
9. Build a real experiment registry and semantic validator for ordered,
   non-overlapping windows, immutable evaluator/environment hashes, effective
   independent sample size, power/precision targets, trial-family size,
   multiplicity correction, typed base/stress costs, and forecast calibration.

## P2 - execution and portfolio sophistication

1. Add minimum ADV/dollar-volume, quote-size, spread persistence, volatility-halt,
   and corporate-action gates.
2. Measure implementation shortfall and fill quality. Use those results to test
   time-sliced or passive execution away from unstable opening minutes.
3. Research volatility- and structure-aware exits against the fixed trailing
   stops. Do not activate dynamic stops until simulations and shadow runs show
   robust improvement across regimes.
4. Add portfolio-level stress tests for correlated gaps, sector shocks, rate
   shocks, earnings clusters, and data-center/AI factor concentration.
5. Add a deterministic end-of-day position/account snapshot and automated
   broker-to-ledger break report.

## Promotion gates

No duration or return threshold alone makes a strategy safe. Advancement beyond
paper requires independently reviewed code and data, zero unresolved broker
breaks, tested recovery objectives, statistically credible out-of-sample
evidence after realistic costs, stable shadow execution, legal/compliance review,
and an explicit human decision. Live-capital enablement is outside this repo's
current scope.
