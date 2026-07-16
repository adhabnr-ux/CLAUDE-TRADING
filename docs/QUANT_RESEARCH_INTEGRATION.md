# Quant research knowledge integration

## Scope and safety boundary

This integration reviewed two public repositories as untrusted source material,
vendored their complete tracked trees for reproducible provenance, and
translated selected concepts into Bull's own research-governance system. The
snapshots are source evidence, not active dependencies: no third-party package
is installed or imported at runtime, and no upstream code, prompt, workflow,
model weight, dataset, result, signal, threshold, trade, or performance claim is
executed or accepted as authority.

The result is intentionally asymmetric: research may become stricter and may
veto a candidate, but it cannot authorize an order, loosen a limit, change
`config/`, edit active strategy, or bypass `scripts/trade.py`. Both accounts
remain paper-only and `memory/control.md` remains the human switch.

## Reviewed snapshots and licenses

| Repository | Snapshot | License | Used for |
|---|---|---|---|
| [LLMQuant/quant-mind](https://github.com/LLMQuant/quant-mind) | `2c1f2cb9ae278cbee7c69a982a9151230be596f1` | MIT, Copyright 2025 LLMQuant | Evidence/provenance schemas, dual financial time, canonical/derived separation, completeness/failures, strict validation |
| [chrisworsey55/atlas-gic](https://github.com/chrisworsey55/atlas-gic) | `fcfc40dcf628f6af091c28cb2c33827f42cef8fd` | MIT for framework architecture, documentation, and example prompts; production prompts absent | Layered specialist review, adversarial CRO lens, reversible single-change experiments |

The exact source trees live in `third_party/quant-mind/` and
`third_party/atlas-gic/`; their MIT license files are preserved. QuantMind's
`CLAUDE.md`, `AGENTS.md`, `.claude/`, and `.agents/` paths were renamed without
changing their bytes so they cannot become active project instructions or
skills. `third_party/snapshots.json` records commits, Git tree IDs, archive
hashes, sizes, counts, and path rewrites. Offline CI verifies local bytes,
paths, modes, counts, sizes, and each recorded Git tree; commit IDs and archive
hashes remain human-reviewed provenance metadata because CI does not fetch
upstream or prove the commit-to-tree relationship. It rejects any missing,
extra, modified, remoded, symlinked, or special file. Agents can read only exact paths in
`memory/upstream-methodology-index.md`; they cannot list or execute a snapshot.

Bull's operating contract and deterministic implementation remain an original
synthesis. Vendoring is for traceability and on-demand methodological review,
not silent code reuse or activation.

## What was adopted from QuantMind

The useful implemented ideas came primarily from
`quantmind/knowledge/_base.py`, `quantmind/knowledge/paper.py`,
`quantmind/preprocess/_news_types.py`, `quantmind/preprocess/news.py`,
`quantmind/flows/batch.py`, `docs/design/en/news.md`, `docs/library.md`, and
`quantmind/library/`:

- Source observations and agent interpretations are different records.
- Every financial claim needs both an information cutoff (`as_of`) and declared
  observability. Bull records a `published_at` believed trustworthy, or null
  plus the conservative `fetched_at` bound. Validation checks format and order,
  not factual authenticity. Historical filters must apply availability before
  ranking; unknown availability is not permission to assume midnight.
- Collection defines a replayable window, reports completeness, and preserves
  partial failures instead of silently dropping them.
- Stable identities and canonical URLs identify exact or replayed URL
  duplicates. Distinct syndicated URLs still require origin and content-hash
  checks before they can count as independent confirmation.
- Strict, no-extra-field schemas reduce quiet contract drift.
- Deterministic offline validation is separate from optional live source-health
  checks.
- Canonical typed evidence is source of truth; embeddings, projections, filter
  columns, indexes, and rankings are rebuildable derivatives bound to content,
  model, dimension, and schema identities.
- Retrieval may operate at item, tree-root, or node grain, but every hit must
  resolve back to canonical cited evidence. Similarity is relevance, not alpha.

Bull implements those ideas through:

- `schemas/research-packet.schema.json`;
- `bulltrader/research.py` semantic and referential validation;
- profile-isolated `research-evidence.jsonl` ledgers;
- atomically claimed fixed pending packets, retained failure artifacts, plus
  `scripts/research.py append --agent ...` and `validate --agent ...`;
- the mandatory compact playbook in `memory/quant-research-playbook.md`.
- the mandatory upstream operating index in
  `memory/upstream-methodology-index.md`.

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

### QuantMind mechanisms deliberately not activated

QuantMind is a document-acquisition, typed-knowledge, and local-retrieval project
in active migration, not a complete trading research platform. At the reviewed
snapshot:

- graph, factor, and thesis models were placeholders;
- citations were requested from an LLM but not source-span verified;
- some memory, budget, and archive hooks were no-ops;
- the local library uses SQLite plus an embedding provider, but `available_at`
  remains optional and some date-only examples normalize releases to midnight;
- embedding requests lack a complete timeout/cost/retry policy, locking is
  process-local rather than distributed, and exact cosine loads the local index
  in memory;
- no replication, temporal-leakage, investability, or cost filter was evident
  in the reviewed paper-catalog path or its metadata.

Therefore Bull vendors the bytes for audit but does not install, import, or run
the QuantMind package, dump its paper list into agent context, call its
embedding library, or treat extracted/retrieved text as validated investment
knowledge. Its bundled catalog and example database are not market data or a
research corpus for Bull.

## What ATLAS inspired and Bull corrected

The useful conceptual inspiration came from `architecture/overview.md`,
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

### ATLAS mechanisms deliberately not activated

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

Bull therefore vendors the source for audit but does not activate Darwinian
weights, JANUS blending, MiroFish probabilities, autorewrites, automatic agent
spawning, or any advertised trade result. Scenario generation remains a source
of stress-test ideas only.

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
