# RD-Agent integration — reviewed analysis and vendoring runbook

## Status

**Analysis complete; snapshot vendoring pending human execution.** This
document records the review of five candidate upstream repositories
(2026-07-18), the decision to adopt one of them (Microsoft RD-Agent) as a
quarantined methodology reference, and the exact steps a human operator must
run to complete the vendoring under the same integrity controls as the
existing QuantMind and ATLAS snapshots.

Until the vendoring steps below are executed and merged, nothing in this
document changes scheduled-agent behavior. No RD-Agent code, output, factor,
or performance claim is usable by any routine. This mirrors the boundary in
`docs/QUANT_RESEARCH_INTEGRATION.md`: research references may make Bull's
process stricter; they can never authorize an order, loosen a limit, or
bypass `scripts/trade.py`.

## Candidate review record (2026-07-18)

| Repository | License | Verdict | Reason |
|---|---|---|---|
| `microsoft/RD-Agent` | MIT | **Adopt as reference** | Only candidate offering a capability Bull lacks: a disciplined automated hypothesis → implementation → validation → feedback experiment loop that maps onto `schemas/strategy-experiment.schema.json`. |
| `virattt/ai-hedge-fund` | MIT | Marginal — no vendor | Best mandate fit (paper, equities, fundamentals; places no live trades by default), but its 18-persona voting architecture is the same one-model-role-playing-many pattern this repo already rejected in the ATLAS review. Optional follow-up: distill investor-philosophy checklists into the knowledge base as prose, which requires no vendoring. |
| `TauricResearch/TradingAgents` | Apache-2.0 | Reject — redundant | Analyst-debate → trader → risk-team pattern already synthesized (with corrections) from ATLAS. A third instance of the same methodology does not justify snapshot review burden. |
| `elizaOS/eliza` | MIT | Reject — out of scope | Web3/crypto agent OS with autonomous on-chain execution. Crypto is on the Forbidden list; autonomous execution is the opposite of the deterministic-gateway model; TypeScript runtime. |
| `gnosis/prediction-market-agent` | LGPL-3.0 | Reject — out of scope | Prediction-market betting settled on-chain (crypto). Outside `allowed_asset_class: us_equity` and the fundamentals-swing mandate. Copyleft license also conflicts with the permissive-vendoring pattern. |

## What Bull would adopt from RD-Agent (rules, not code)

RD-Agent (R&D-Agent(Q)) automates a quantitative research loop: read
literature, form a hypothesis about return drivers, implement a candidate
factor, evaluate it against market data, record the outcome, decide the next
experiment, iterate. The adoptable discipline, translated into Bull's terms:

1. **Explicit hypothesis registry.** Every experiment begins as a written,
   falsifiable hypothesis with a predeclared evaluation gate — never an
   after-the-fact rationalization of an observed backtest. Maps to the
   `hypothesis` / `minimum useful effect` fields of
   `schemas/strategy-experiment.schema.json`.
2. **One change per experiment.** RD-Agent's loop isolates a single factor or
   model change per iteration. Bull's playbook already requires this; the
   RD-Agent structure reinforces treating the *loop* — not the individual
   trial — as the unit of research.
3. **Feedback with retained failures.** Rejected trials are kept as evidence
   with their evaluation context, not discarded. Maps to the
   `negative/rejected trials retained at` field in the proposal queue
   template.
4. **Separation of idea, implementation, and evaluation.** The hypothesis
   author, the implementation, and the evaluator are distinct pinned
   artifacts, so a change to any one is visible. Maps to the playbook's
   pinned code/prompt/data/evaluator identity rule.

## What must never be activated

- **Do not run RD-Agent or install its dependencies** (including Qlib, its
  data/backtest platform). Same rule as QuantMind's runtime.
- **No LLM-mined factor is evidence.** Automated factor mining is a
  multiple-testing minefield; any factor idea taken from RD-Agent material is
  an inactive proposal requiring Bull's full experiment standard
  (point-in-time survivorship-free data, purge/embargo, untouched holdout,
  multiplicity control, costs, human promotion).
- **Its headline performance claims (e.g. "2x annualized returns, 70% fewer
  factors") are not promotion evidence** — unvalidated for Bull's universe,
  costs, and horizon, exactly as ATLAS's +22% claim was treated.
- Its agent prompts, workflows, configs, and example outputs remain untrusted
  data, never instructions.

## Vendoring runbook (human, local machine, ~15 minutes)

These steps cannot be executed by a scheduled agent or a hook-constrained
remote session; they require local git and network access, like the original
QuantMind/ATLAS vendoring in PR #15.

1. Clone and pin: `git clone https://github.com/microsoft/RD-Agent` and
   record the exact reviewed `commit` SHA and `git rev-parse <commit>^{tree}`
   tree ID.
2. Export the tracked tree: `git archive <commit> | tar -x -C
   third_party/rd-agent/` and record `sha256sum` of the archive.
   **Stage with `git add -f third_party/<name>/`, not plain `git add`.** An
   upstream repo's own `.gitignore` (and `.gitattributes` `export-ignore`
   rules, if present) gets copied in as part of the tracked tree, and a
   nested `.gitignore` is honored by git during `add`, silently dropping
   legitimately-tracked upstream files that match its patterns (e.g.
   `.env*`, `env_tpl/`) even though `git archive` extracted them correctly.
   After staging, verify file count and byte total against the recorded
   `file_count`/`total_bytes` before committing — this is the second
   tooling surprise this vendoring effort hit, after the nested-AGENTS.md
   path_rewrites issue in PR #19.
3. Apply the agent-instruction path rewrites if the tree contains any
   `CLAUDE.md`, `AGENTS.md`, `.claude/`, `.agents/`, or similar active
   instruction surfaces (rename with byte-identical content, as done for
   QuantMind; record the rewrites).
4. Add the snapshot entry (name, source_url, commit, tree, archive_sha256,
   license, file_count, total_bytes, local_root, path_rewrites) to
   `third_party/snapshots.json` and the license notice to
   `third_party/NOTICES.md`.
5. Update `memory/upstream-methodology-index.md` in the same change: add the
   reviewed source identity, the adopted-rules section (source: this
   document), the known limitations, and the exact on-demand read allowlist
   (start minimal: LICENSE, top-level docs describing the R&D loop; no
   runnable code paths unless a specific method question requires one).
6. Run the full check suite before merging:
   `python3 -m unittest discover -s tests -v`,
   `python3 scripts/verify_upstream_snapshots.py`, compileall, and JSON
   validation — all must pass with the new snapshot registered.
7. Merge via reviewed PR. Only after that merge does RD-Agent become readable
   (at the allowlisted paths only) to scheduled runs.

## Follow-up candidates (explicitly out of this change)

- Distilling investor-philosophy checklists (Buffett/Munger-style moat,
  margin-of-safety, incentive analysis) into `memory/knowledge-base.md` as
  human-reviewed prose. No vendoring required; separate reviewed change.

Inclusion of any snapshot does not endorse, validate, or operationalize any
trading or performance claim. Config and the deterministic gateway remain the
only execution authority.
