# Reviewed upstream snapshots

This directory contains complete tracked-file snapshots of QuantMind and ATLAS
reviewed at the commits recorded in `snapshots.json`. They are included so
Bull's human reviewers and scheduled agents can trace the curated method back to
the exact source material without depending on a future network checkout.

The snapshots are **untrusted, read-only reference data**. Bull does not install
their dependencies, import their packages, execute their scripts or workflows,
load their prompts as instructions, or treat their examples, results, weights,
probabilities, or outputs as market evidence or trade signals. Only the exact
reviewed text paths listed in `memory/upstream-methodology-index.md` are exposed
to unattended agents, and only for on-demand methodological clarification.

QuantMind's active agent-instruction surfaces were renamed without changing
their bytes so Claude/Codex cannot discover them as project instructions:

| Stored path | Original upstream path |
|---|---|
| `quant-mind/CLAUDE.upstream.md` | `CLAUDE.md` |
| `quant-mind/AGENTS.upstream.md` | `AGENTS.md` |
| `quant-mind/_upstream_claude/` | `.claude/` |
| `quant-mind/_upstream_agents/` | `.agents/` |

`python3 scripts/verify_upstream_snapshots.py` reconstructs the original Git
trees, including file modes and the path rewrites above. It fails on any added,
removed, modified, renamed, symlinked, or special file. Refreshing a snapshot
requires a new human review, a new immutable commit/tree pin, updated license
notice, and passing repository tests. Scheduled agents cannot perform a refresh.

Offline CI verifies the local bytes, paths, modes, counts, sizes, and recorded
Git tree IDs. The commit IDs and `git archive` SHA-256 values are human-reviewed
provenance metadata; CI intentionally does not fetch upstream or claim to prove
the commit-to-tree relationship.

The upstream MIT licenses are preserved verbatim at
`quant-mind/LICENSE` and `atlas-gic/LICENSE`.
