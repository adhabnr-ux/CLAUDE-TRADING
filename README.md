# Bull — guarded autonomous paper-trading agents

Bull runs two scheduled Claude Code research and trading agents against separate
**Alpaca paper accounts**:

- **Cautious Bull** uses tighter concentration, deployment, stop, and drawdown
  limits.
- **Aggressive Bull (AGGRO)** accepts wider limits, but uses the same mandatory
  execution gateway and fail-closed controls.

The objective is to research and test a repeatable process against the S&P 500.
It is not a claim of alpha. No agent, model, strategy, stop order, or software
control can guarantee correct decisions, prevent every loss, or produce a
profit. This repository is intentionally paper-only.

## Safety architecture

Agents may propose trades, but they do not have final execution authority. All
broker mutations must pass through `scripts/trade.py`, a deterministic gateway
that enforces the human control switch, typed same-day plans, the exact Alpaca
paper endpoint, account and market checks, portfolio limits, duplicate-order
protection, and protective-stop coverage.

The authority order is:

1. `config/risk-policy.json`, `config/instruments.json`, and
   `config/earnings-calendar.json` — human-owned, machine-enforced limits,
   symbol metadata, and trusted earnings records.
2. `bulltrader/` and `scripts/trade.py` — deterministic validation, risk,
   execution, idempotency, and reconciliation.
3. A current fenced JSON trade plan in the applicable research log — an agent
   proposal that must satisfy the typed contract.
4. A current schema-validated, symbol/thesis/invalidation/review-date-bound
   declared-evidence packet — required by the fresh-buy gateway, but still
   non-executable, unverified as to source truth, and never order authority.
5. Narrative research, strategies, lessons, and prompts — context only; they
   cannot override the controls above.

Complete reviewed QuantMind and ATLAS source snapshots are checked in for
provenance, but remain below every layer above: they are quarantined read-only
methodology evidence, never executable dependencies, instructions, market data,
signals, performance proof, policy, plans, or orders.

Direct order mutations are disabled in `scripts/alpaca.sh`. The gateway verifies
the configured Alpaca account ID before broker or market-data access and takes a
same-host, per-command operating-system lock keyed by that account. GitHub-hosted runs share
a workflow concurrency group. The `memory/_lock` file remains only an advisory
writing signal.

None of those controls is a cross-host distributed lock for independently
scheduled Claude environments. Broker-side `client_order_id` lookup provides
duplicate resistance for one canonical operation, not general serialization.
Do not overlap external routines for the same account; a durable distributed
lease is still required before calling the paper system operationally mature.

See [Risk engine and operations](docs/RISK_ENGINE.md), the
[quant research integration](docs/QUANT_RESEARCH_INTEGRATION.md), the
[trade-plan schema](schemas/trade-plan.schema.json), and the
[research-packet schema](schemas/research-packet.schema.json).

## Machine-enforced profiles

| Limit | Cautious Bull | AGGRO |
|---|---:|---:|
| Max position | 20% | 35% |
| Max single order | 15% | 20% |
| Minimum cash after a buy | 5% | 2% |
| Max new-buy deployment/day | 25% | 60% |
| Max new positions/week | 3 | 8 |
| Max sector exposure | 60% | 50% |
| Trailing stop | 10% | 18% |
| Midday loss-cut threshold | -7% | -12% |
| Intraday shock breaker | 4% | 6% |
| High-water drawdown breaker | 10% | 20% |
| Max modeled risk at stop/projected position | 1.5% | 3.6% |
| Max quoted spread | 35 bps | 60 bps |
| Max candidate-packet age | 240 min | 240 min |
| Max supporting exchange-market source age | 120 min | 120 min |

Shared gates also require whole shares, an approved instrument and canonical
sector, an active tradable US equity priced at least $5, a fresh IEX quote, a
profile-bounded bid/ask spread, a current-day strict plan envelope, a bounded
entry price, verified earnings metadata, at least three trading sessions until
earnings (the next two sessions are blacked out), and no discretionary same-day
round-trip. A full-position `midday_loss` exit is the sole same-day
risk-reduction exception. Stop percentages model risk for sizing; gaps and
slippage can make realized losses larger. Entry and exit loops are bounded to
two attempts, and a cancellation must be broker-confirmed before continuing.

A genuinely new buy also needs the latest same-session candidate packet and an
exact plan match on packet ID/hash, symbol, thesis, invalidation, and review
date. Packet validation checks declared structure and freshness; it does not
verify that a URL exists, content was fetched, a publisher is independent, or a
claim is true. See the integration document for the explicit trust boundary.

## Repository map

```text
CLAUDE.md                    Agent operating constitution
config/
  risk-policy.json          Canonical system and per-agent limits
  instruments.json          Human-reviewed symbol and sector master
  earnings-calendar.json    Human-verified earnings dates (empty blocks buys)
bulltrader/
  alpaca.py                 Exact-endpoint broker client
  plan.py                   Typed plan parser
  research.py               Evidence-packet and provenance validator
  risk.py                   Pre-trade and control checks
  execution.py              Idempotent execution, protection, reconciliation
scripts/
  trade.py                  Only authorized order-mutation entry point
  alpaca.sh                 Read-only broker and market-data inspection
  persist_memory.py         Fixed profile-scoped journal publisher
  research.py               Fixed pending-packet append and profile validation
memory/                     Cautious state plus shared human control
memory/aggressive/          AGGRO state and profile-scoped ledgers
memory/quant-research-playbook.md  Shared immutable research protocol
memory/upstream-methodology-index.md  Curated QuantMind/ATLAS operating rules
.claude/commands/           Scheduled routine playbooks
routines/                   Routine schedules and launch prompts
schemas/                    Plan/evidence schemas and experiment draft checklist
third_party/                Pinned, tree-verified, quarantined upstream sources
scripts/verify_upstream_snapshots.py  Upstream snapshot integrity verifier
tests/                      Policy, risk, idempotency, and protection tests
docs/index.html             GitHub Pages performance dashboard
```

Every scheduled run should read `memory/control.md` first and reconcile broker
state before making a decision. The broker is the source of truth for orders,
fills, positions, cash, and equity; Markdown files are journals, not a ledger.

## Human controls

Edit `memory/control.md` through GitHub:

- `STATUS: ACTIVE` — new entries, exits, and protective-order repairs are
  eligible, subject to every other gate.
- `STATUS: RISK_OFF` — no new buys; exits and protective-order repairs remain
  eligible.
- `STATUS: PAUSED` — all broker mutations, including repair orders, are blocked;
  read-only reconciliation is allowed.
- `NOTE: ...` — operating context for both agents; never an order instruction.
- `QUERY: ...` — request an answer in the next report; never an order
  instruction.

## Operator commands

```bash
# Read-only broker inspection
./scripts/alpaca.sh account
./scripts/alpaca.sh positions
./scripts/alpaca.sh orders open

# Detect mismatches without changing broker state
TRADING_AGENT=bull python3 scripts/trade.py reconcile --agent bull
TRADING_AGENT=aggro python3 scripts/trade.py reconcile --agent aggro

# Repair managed stops and contain forbidden holdings (blocked while PAUSED)
TRADING_AGENT=bull python3 scripts/trade.py reconcile --agent bull --repair

# Validate a same-day planned buy without submitting it
TRADING_AGENT=bull python3 scripts/trade.py buy --agent bull --symbol ETN --dry-run

# Append an already-prepared fixed pending packet, then validate the ledger
TRADING_AGENT=bull python3 scripts/research.py append --agent bull
TRADING_AGENT=aggro python3 scripts/research.py append --agent aggro
python3 scripts/research.py validate --agent bull
python3 scripts/research.py validate --agent aggro

# Execute only a matching, fully validated plan intent
TRADING_AGENT=bull python3 scripts/trade.py buy --agent bull --symbol ETN
TRADING_AGENT=bull python3 scripts/trade.py sell --agent bull --symbol ETN --qty 10 \
  --trigger planned --reason "Thesis invalidated after a confirmed guidance cut"
```

Completed order results include broker order identifiers; reconciliation returns
issue and repair summaries. Expected plan, policy, risk, and broker rejections
emit a JSON `blocked` result and exit nonzero. Never work around a rejection
with raw HTTP calls; investigate the input, policy, account, or broker state
instead.

`reconcile --repair` is a mutation command. Besides adding/replacing managed
protective stops, it may emergency-flatten a short or an unknown held asset that
the broker confirms is not an allowed long US equity. It leaves unmanaged
orders and orphan stops untouched and reports them as unresolved for a human.

## Schedule

| Routine | Cautious | AGGRO | Purpose |
|---|---|---|---|
| Pre-market | 8:00 AM ET | 8:10 AM ET | Research and typed plan |
| Market open | 9:35 AM ET | 9:45 AM ET | Reconcile and execute eligible plans |
| Midday | 12:30 PM ET | 12:40 PM ET | Reconcile and enforce loss-cut rules |
| Close | 4:10 PM ET | 4:20 PM ET | Post-close broker snapshot and benchmark report |
| Weekly review | 4:40 PM Fri | 4:50 PM Fri | Process and performance review |
| Monthly review | 5:20 PM first Fri | — | Drift and sizing review |

Routine schedules are configured outside this repository. Confirm their time
zone and daylight-saving behavior in the cloud scheduler. The close routines
must run after the regular session; a 3:50 PM snapshot is not an end-of-day
performance observation.

## Setup and validation

1. Create separate Alpaca **paper** accounts for Cautious and AGGRO and record
   each account's exact ID from the authenticated account response.
2. In each cloud environment set `ALPACA_API_KEY_ID`,
   `ALPACA_API_SECRET_KEY`, `ALPACA_EXPECTED_ACCOUNT_ID`,
   `ALPACA_BASE_URL`, and `TRADING_AGENT`. Use `TRADING_AGENT=bull` for
   Cautious and `TRADING_AGENT=aggro` for AGGRO. The URL must be exactly
   `https://paper-api.alpaca.markets`; a missing value or credential/account-ID
   mismatch fails closed. A coordinated swap of both credentials and expected
   ID is still an environment-assignment risk.
3. Populate `config/earnings-calendar.json` through human review using dated
   HTTPS source records. The checked-in calendar is intentionally empty, so all
   new buys remain blocked until a plan exactly matches a fresh trusted entry.
4. Configure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` before enabling
   scheduled reports. They are optional only for manual read-only CLI checks.
5. Connect each routine to the correct account environment and reviewed commit.
   Pin a reviewed model in the scheduler; the repository cannot validate a
   model choice configured only in the Claude cloud UI. If using the optional
   GitHub/Groq runner, set the repository variable `GROQ_MODEL`; that runner
   refuses silent model fallback. Groq exposes search discovery but no trusted
   content fetch, so its append process is machine-blocked from accepting
   `candidate` research; it may record only `hold`, `watch`, or `avoid`, and it
   must not create a fresh-buy plan.
6. Run the repository checks before enabling or changing a routine:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q bulltrader runner.py scripts/trade.py \
  scripts/research.py scripts/persist_memory.py \
  scripts/verify_upstream_snapshots.py .claude/hooks/validate_agent_tool.py
python3 scripts/verify_upstream_snapshots.py
bash -n scripts/*.sh
```

GitHub Actions runs these checks plus JSON/schema validation on pushes and pull
requests. The rollout branch is checked in as `STATUS: PAUSED`. Keep every
schedule disabled and run read-only reconciliation separately for both paper
accounts. Populate the trusted earnings calendar, review every reconciliation
issue, and confirm notification/persistence failures are visible. A `--dry-run`
is still read-only and can run while `ACTIVE`, but its approval is only a
point-in-time observation. Human activation comes last; it is not part of this
change.

## Strategy changes

Agents may append research-backed proposals to the
[Cautious queue](memory/strategy-proposals.md) or
[AGGRO queue](memory/aggressive/strategy-proposals.md). They must not rewrite
the machine policy or silently activate a lesson. A human reviews evidence,
testing, conflicts, rollback criteria, and the proposed diff before changing
`config/` or execution code. Draft prose uses the fields in the
[strategy-experiment schema](schemas/strategy-experiment.schema.json) as a
checklist. The schema permits only `DRAFT` and `REJECTED`; it does not register,
run, validate, or promote an experiment. Unknown inputs remain `UNKNOWN`; a
short P/L window or higher in-sample Sharpe is not promotion evidence.

## Disclaimer

This is an educational paper-trading experiment, not financial advice or a
production trading system. Paper fills, liquidity, latency, slippage, corporate
actions, data quality, and outages can differ materially from live markets.
Keep it paper-only unless it undergoes independent security, reliability,
model-risk, compliance, and live-capital readiness reviews.
