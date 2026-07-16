# Quant research knowledge integration

## Scope and safety boundary

This integration reviewed two public repositories as untrusted source material
and translated selected concepts into Bull's own research-governance system. No
third-party runtime, prompt, model weight, dataset, signal, threshold, trade,
or performance claim was imported. No upstream code was executed.

The result is intentionally asymmetric: research may become stricter and may
veto a candidate, but it cannot authorize an order, loosen a limit, change
`config/`, edit active strategy, or bypass `scripts/trade.py`. Both accounts
remain paper-only and `memory/control.md` remains the human switch.

## Reviewed snapshots and licenses

| Repository | Snapshot | License | Used for |
|---|---|---|---|
| [LLMQuant/quant-mind](https://github.com/LLMQuant/quant-mind) | `168720dc5f4eed3d8b2e55f23026fe77ecb95b67` | MIT, Copyright 2025 LLMQuant | Evidence/provenance schemas, explicit as-of time, completeness/failures, strict validation |
| [chrisworsey55/atlas-gic](https://github.com/chrisworsey55/atlas-gic) | `fcfc40dcf628f6af091c28cb2c33827f42cef8fd` | MIT for framework architecture, documentation, and example prompts; production prompts absent | Layered specialist review, adversarial CRO lens, reversible single-change experiments |

This repository uses an original synthesis and original implementation. The
upstream license notices and disclaimers remain in their repositories. If
future work copies a substantial portion of upstream software or documentation,
the applicable MIT notice must travel with that material.

## What was adopted from QuantMind

The useful implemented ideas came primarily from
`quantmind/knowledge/_base.py`, `quantmind/knowledge/paper.py`,
`quantmind/preprocess/_news_types.py`, `quantmind/preprocess/news.py`,
`quantmind/flows/batch.py`, and `docs/design/en/news.md`:

- Source observations and agent interpretations are different records.
- Every financial claim needs a time of validity and typed provenance fields.
- Collection defines a replayable window, reports completeness, and preserves
  partial failures instead of silently dropping them.
- Stable identities and canonical URLs identify exact or replayed URL
  duplicates. Distinct syndicated URLs still require origin and content-hash
  checks before they can count as independent confirmation.
- Strict, no-extra-field schemas reduce quiet contract drift.
- Deterministic offline validation is separate from optional live source-health
  checks.

Bull implements those ideas through:

- `schemas/research-packet.schema.json`;
- `bulltrader/research.py` semantic and referential validation;
- profile-isolated `research-evidence.jsonl` ledgers;
- atomically claimed fixed pending packets, retained failure artifacts, plus
  `scripts/research.py append --agent ...` and `validate --agent ...`;
- the mandatory compact playbook in `memory/quant-research-playbook.md`.

The packet contains sources, claims, inferences, and non-executable decision
support as separate layers. Candidate assessments require self-declared complete
coverage, symbol-scoped supporting evidence, distinct declared publishers and
exact hosts, tier-1 evidence, a current unqualified exchange-market observation,
an opposing claim, and no unresolved critical unknown. Source `as_of` cannot be
later than fetch time; fetches must be inside the half-open declared window.
URLs are stored canonically, and duplicate canonical URLs or captured-content
hashes are rejected. These are structural checks, not source attestation.
New appends apply the current human-owned market-source freshness policy.
Historical schema-v1 rows are revalidated against an immutable 24-hour
protocol ceiling, so later policy tightening cannot rewrite or brick the
append-only record. The execution gate separately applies the current, tighter
policy again at order time.

### QuantMind concepts deliberately not imported

QuantMind is a document-acquisition and extraction project in active migration,
not a complete trading research platform. At the reviewed snapshot:

- storage/retrieval and `mind/` memory described in some docs were absent;
- graph, factor, and thesis models were placeholders;
- citations were requested from an LLM but not source-span verified;
- some memory, budget, and archive hooks were no-ops;
- no replication, temporal-leakage, investability, or cost filter was evident
  in the reviewed paper-catalog path or its metadata.

Therefore Bull did not vendor its package, dump its paper list into context,
add embeddings, or treat extracted text as validated investment knowledge.

## What was adopted from ATLAS

The useful conceptual material came from `architecture/overview.md`,
`architecture/layers.md`, and `architecture/autoresearch.md`:

- move from evidence collection through domain analysis to synthesis;
- force a distinct adversarial risk review before a favorable assessment;
- preserve disagreement rather than manufacturing consensus;
- isolate one research change at a time and keep a reversible audit trail;
- evaluate across regimes and horizons instead of assuming one environment.

Bull translates those ideas into sequential review lenses, not a claim of 25
independent minds. `schemas/strategy-experiment.schema.json` is only a draft
field checklist for controls the ATLAS description lacks: immutable
artifact/data hashes, point-in-time and survivorship requirements,
train/validation/untouched-test separation, purge/embargo, costs, uncertainty,
multiple-testing families, sensitivity, shadow criteria, rollback, and human
review. It permits only `DRAFT` and `REJECTED`; it does not register, run,
validate, or promote an experiment.

### ATLAS mechanisms deliberately not imported

The public repository is illustrative rather than a deployable trading system.
Core orchestration, data clients, risk logic, trained prompts, scorecards, and
deployment configuration are absent. More importantly, reviewed code and
artifacts contain research defects:

- five-day before/after Sharpe selection has tiny samples, repeated testing,
  overlapping outcomes, and no untouched holdout or cost model;
- agent convictions and synthetic outcomes are uncalibrated;
- `src/mirofish/mirofish_trainer.py` exposes synthetic forward-path returns to
  the model before scoring, creating look-ahead leakage;
- the lightweight swarm is one model role-playing many participants, so its
  agreement is not independent evidence;
- scenario drifts, correlations, event probabilities, and price anchors are
  largely hand-set, stale, or not causally connected to generated outcomes;
- shared JSON state is not transactional, and some data/parse failures continue
  with empty or default values without a propagated validity flag;
- `results/summary.json` reports -5.91% total return, while the README foregrounds
  a +22% deployment phase without a reproducible split, benchmark, or cost model;
  checked artifacts also disagree on dates, starting values, and experiment
  counts.

Bull therefore did not import Darwinian weights, JANUS blending, MiroFish
probabilities, autorewrites, automatic agent spawning, or any advertised trade
result. Scenario generation remains a source of stress-test ideas only.

## Operating workflow

```text
untrusted sources
  -> timestamped source records + visible collection failures
  -> cited claims
  -> falsifiable inferences
  -> data/macro/sector/company/implementation review
  -> adversarial risk review with opposing evidence
  -> non-executable candidate/hold/avoid/watch assessment
  -> locked validate-before-append ledger
  -> separate typed trade plan
  -> fresh-buy packet ID/hash + thesis/invalidation/review-date verification
  -> deterministic policy and execution gateway
```

An invalid, stale, semantically mismatched, or materially incomplete research
packet blocks a genuinely new buy in the deterministic gateway even if a plan
was written. The gate checks the latest same-session premarket packet, exact
symbol, candidate assessment, packet ID, canonical content hash, thesis,
invalidation, and review date. Candidate-packet and current-market-source ages
come from human-owned `config/risk-policy.json`. It does not re-gate protection
or completion of an already-filled/partially-filled entry. A zero-fill attempt
found after restart cannot submit a later buy attempt. Passing validation proves
only that the declared record satisfies this structural contract; it does not
prove source authenticity, correctness, or expected profit. Sell-side risk
controls and reconciliation remain available when research validation fails.

The optional GitHub/Groq runner is discovery-only: it can return search URLs
but cannot retrieve and inspect source content. Its append subprocess therefore
sets a non-agent-controlled restriction that rejects every `candidate` packet.
Groq may record `hold`, `watch`, or `avoid`, but it cannot create fresh-buy
research. Full Claude Code runs still require both search and source fetch.

### Current trust limitation

Publisher, host, source type/tier, timestamps, completeness, claim text, and the
prompt-injection flag are still agent-declared. The validator does not fetch a
URL, attest returned bytes, resolve common ownership/registrable domains, or
require a captured hash. Search and fetch tool output is discovery input, not a
trusted acquisition receipt. A malicious or mistaken agent can therefore create
a structurally valid false record; the surrounding deterministic policy limits
the consequence but does not make the research true. The system remains paused
and paper-only. Trusted acquisition receipts, a human source registry, and
deterministic source classification remain roadmap work.

## What this changes—and what it does not

This raises the minimum standard for traceability, declared source diversity,
disconfirming evidence, experiment design, and honest uncertainty. It makes
missing lineage, exact duplicates, stale timestamps, look-ahead-prone designs,
and unreviewed strategy drift easier to detect; it cannot eliminate model error
or prompt injection.

It does not establish alpha. A top-tier quant process still needs licensed
point-in-time data, reproducible backtesting, corporate-action and delisting
history, realistic transaction costs, calibrated forecasts, portfolio risk
models, independent replication, a long shadow period, and operational controls
listed in `ROADMAP.md`.
