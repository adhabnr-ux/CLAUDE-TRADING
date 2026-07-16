# Cautious Bull strategy proposals

This is a proposal queue, not active policy. Research agents may append entries.
They must not edit or override `config/risk-policy.json`,
`config/instruments.json`, `bulltrader/`, or execution playbooks to activate a
proposal. Activation requires human review, tests, and a reviewed code change.

## Proposal template

### YYYY-MM-DD — concise title

- Status: PROPOSED
- Owner: Cautious Bull
- Source concept, repository/path, pinned commit, and license:
- One causal hypothesis and expected failure mode:
- Exact single change (no bundled edits):
- Signal equation, inputs, universe, exclusions, horizon, rebalance, and execution lag:
- Baseline commit/artifact hash and immutable data-snapshot hash:
- Point-in-time cutoff and release-lag policy:
- Survivorship, delisting, symbol-change, split, dividend, and membership controls:
- Train window / validation window / untouched test window / purge / embargo:
- Benchmark, primary metric, minimum useful effect, and sample floor:
- Expected benefit:
- Failure modes and conflicts:
- Commission, spread, impact, failed-fill, turnover, liquidity, and capacity model:
- Dependence-aware uncertainty method and multiple-testing family:
- Parameter-sensitivity grid and predeclared regime slices:
- Shadow sessions/decisions and frozen acceptance threshold:
- Rollback, drawdown, and data-quality triggers:
- Negative/rejected trials retained at:
- Proposed files and exact parameter changes:
- Human decision: PENDING

Use `UNKNOWN` for missing fields. Do not invent precision or reuse an observed
test window as untouched evidence. `schemas/strategy-experiment.schema.json`
is a draft field checklist only. This prose queue is not machine-validated or
preregistered, and the schema does not run or promote experiments. Five-day P/L
or a higher in-sample rolling Sharpe is not sufficient evidence.

Do not mark a proposal `APPROVED` or `ACTIVE`; only the human operator may do
that through a reviewed change.
