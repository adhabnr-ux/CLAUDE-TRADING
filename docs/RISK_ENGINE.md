# Risk engine and operating model

## Scope and non-goals

This layer turns an untrusted agent proposal into a bounded paper-trading
request. It is designed to fail closed when required data is absent,
inconsistent, stale, or outside policy. It improves operational safety; it does
not prove that a thesis is true, guarantee an execution price, eliminate model
or software errors, cap realized loss exactly, or guarantee profit.

The broker client accepts only the canonical Alpaca paper endpoint:
`https://paper-api.alpaca.markets`. The market-data feed is IEX. These values
come from `config/risk-policy.json`, not agent prose.

## Authority and trust boundaries

| Layer | Role | May override machine risk? |
|---|---|---|
| `config/risk-policy.json` | Human-owned numeric and system limits | Canonical source |
| `config/instruments.json` | Approved symbols and canonical sectors | Canonical source |
| `config/earnings-calendar.json` | Human-verified earnings records | Canonical source |
| `bulltrader/` | Deterministic parsing, risk, broker, execution | Enforces config |
| `scripts/trade.py` | Authorized mutation interface | No |
| Current research-log JSON plan | Proposed buy/trim/exit intent | No |
| Current research-evidence packet | Declared support or veto for a fresh buy | No |
| Strategy, lessons, prompts, web research | Analysis and context | No |
| Broker | Orders, fills, positions, cash, equity | Operational source of truth |

The language model is inside the untrusted proposal boundary. It cannot waive a
check by explaining why an exception seems reasonable. `TRADING_AGENT` binds
the command to one profile, the authenticated Alpaca account ID must match
`ALPACA_EXPECTED_ACCOUNT_ID`, and the shell read helper `scripts/alpaca.sh`
deliberately rejects mutation commands.

Credentials still confer broker access to any process that can read them. Cloud
environment permissions, secret rotation, branch protection, code review, and
least-privilege execution remain required. The gateway is not a security
sandbox.

## Entry pipeline

`python3 scripts/trade.py buy --agent <bull|aggro> --symbol <SYM>` performs this
sequence:

1. Load schema-versioned policy, instrument master, and trusted earnings
   calendar.
2. Read the latest fenced JSON object from the applicable research log.
3. Require a supported schema version, an `agent` value matching the selected
   account profile, and a same-day, unique `buy` intent for the requested
   symbol. New plans use version 2; version 1 remains legacy-only.
4. Parse and type-check the plan, including whole-share quantity, canonical
   sector, thesis contract, maximum entry, and earnings metadata that must
   exactly match a human-owned record no more than 72 hours old.
5. Reconcile broker positions, open orders, and protective stops. A normal buy
   repairs managed-state drift; `--dry-run` is read-only. Any unresolved issue
   blocks entry.
6. Look up every deterministic entry-attempt ID. If no attempt exists, require
   the latest same-session premarket research packet to be within the
   human-owned freshness limits and contain exactly one candidate for the
   symbol. Its packet ID, canonical content hash, thesis, invalidation, and
   review date must exactly match the version-2 buy plan. Filled or partially
   filled recovery and protective containment do not reopen this new-entry
   gate. A zero-fill attempt found after restart cannot authorize another buy
   attempt; it is contained and the operation stops.
7. Confirm the control switch permits opening exposure.
8. Confirm an active, unblocked account; an open market; and an active, tradable
   US equity.
9. Require a valid positive bid/ask quote no more than 120 seconds old, an ask
   of at least $5, and a midpoint spread no wider than the profile cap. Reject
   when the ask exceeds the planned maximum entry.
10. Calculate a cent-rounded-down limit no more than 0.3% over the ask and never
   above the plan's maximum entry.
11. Re-read broker equity, cash, last equity, portfolio history, positions, open
    and recent orders, and market calendar. Apply every portfolio and event gate,
    including pending buy exposure.
12. Recheck the deterministic `client_order_id` before submitting. If absent,
    submit a day limit order; after an ambiguous submission error, look up the
    same ID before deciding whether submission failed.
13. Poll for at most 75 seconds. Confirm that a still-open order becomes
    terminal after cancellation before another attempt. Make at most two bounded
    entry attempts.
14. For any filled quantity, submit exactly that quantity as a GTC trailing
    stop. If protection submission fails, make at most two idempotent emergency
    market-liquidation attempts and restore protection to any residual holding.
15. Append broker identifiers and execution events. Broker state remains the
    authoritative record.

A non-dry-run rerun that finds a filled entry never buys again. It reports the
already closed position or repairs and verifies stop coverage for an open
position. Once any entry attempt exists, its original share quantity is
immutable; a changed plan cannot resize the in-flight operation.

`--dry-run` executes the current preflight and returns approval metrics without
submitting an order. It is a point-in-time check, not a reservation: price,
cash, orders, control status, or market state can change before a later command.

## Buy gates

All gates are conjunctive; one failure blocks the order.

- `ACTIVE` control state. `RISK_OFF` and `PAUSED` block new exposure.
- Exact paper endpoint, profile-bound command, present credentials, and an
  authenticated account ID matching the configured fingerprint.
- Current-day typed plan and one exact symbol/action match.
- Approved non-benchmark symbol with the plan's canonical sector.
- Whole-share positive quantity; specific thesis and invalidation; review date
  not before the plan date.
- For buys: positive maximum entry and a timezone-aware earnings record whose
  date, verification timestamp, and HTTPS source exactly match the human-owned
  calendar; the trusted verification must be no more than 72 hours old.
- Active, unblocked account; market open; active tradable US equity.
- Fresh valid bid/ask quote; minimum stock price; profile spread cap; bounded
  entry price.
- Intraday loss from `last_equity` strictly below the profile shock breaker.
- Drawdown from one-year portfolio-history high water strictly below the
  profile drawdown breaker.
- Projected position, single order, modeled risk at stop for the projected
  position, cash reserve, sector, daily deployment, and weekly new-position
  limits. Open buy quantities count against projected position, cash, and
  sector exposure.
- No buy after a same-day sell of the same symbol.
- More than the configured number of trading sessions before earnings. With the
  current value of two, zero, one, or two trading days to earnings are blocked.
- Earnings verification cannot be timestamped in the future. An empty trusted
  calendar blocks every buy.

### Current profiles

| Gate | Bull | AGGRO |
|---|---:|---:|
| Position/equity | 20% | 35% |
| Single order/equity | 15% | 20% |
| Cash after buy/equity | >=5% | >=2% |
| New-buy deployment/day | 25% | 60% |
| New positions/week | 3 | 8 |
| Sector/equity | 60% | 50% |
| Trailing stop | 10% | 18% |
| Modeled risk at stop/projected position | 1.5% | 3.6% |
| Quoted bid/ask spread | 35 bps | 60 bps |
| Intraday shock | 4% | 6% |
| High-water drawdown | 10% | 20% |

Position, order, stop-risk, cash, sector, daily-deployment, and spread limits
permit their exact boundary and reject a breach. Intraday shock and drawdown
breakers activate at or above their boundary. The loss-cut exit is eligible at
or below its negative threshold. Percent calculations use current equity,
broker market values, applicable pending/recent orders, and proposed limit
notional. These are risk constraints, not target allocations.

## Exit pipeline

`scripts/trade.py sell` permits two trigger types:

- `planned`: the exact symbol and quantity must match a current-day typed `trim`
  or `exit` intent. An `exit` must equal the entire held quantity.
- `midday_loss`: the broker-reported unrealized percentage must be at or below
  the profile threshold (-7% Bull, -12% AGGRO), and the requested quantity must
  equal the entire live holding for a new operation. The loss test is
  deterministic; the required reason is still narrative.

For a new operation, both require an approved symbol, a market-open clock, an
existing long position, a positive whole-share quantity no larger than the
holding, a specific reason, and a clean repair-mode reconciliation. A planned
sell is blocked after a buy fill in the same symbol that day. If any immutable
sell operation already partially filled, a rerun uses the original target
quantity so deterministic IDs can recover cumulative progress; it must not
resize the request to the reduced holding. A qualifying full-position
`midday_loss` exit is the explicit risk-reduction exception and may close a
same-day buy; this can count as a day trade and remains subject to
broker/account restrictions. `ACTIVE` and `RISK_OFF` allow eligible exits;
`PAUSED` blocks them.

Before submitting the idempotent market sell, the gateway cancels each open
trailing stop and confirms that it is terminal. It then refreshes the position;
if the stop already closed it, no market sell is sent, and an unsafe quantity
mismatch blocks the request. The gateway makes at most two attempts and submits
only the cumulative unfilled remainder. It returns cumulative fill, target,
remaining target, and all broker/client IDs. A rerun recovers those same orders
by client ID. In a `finally` path the gateway repairs stop coverage for any
remaining position; if that fails, it attempts an emergency flatten and
protects any residual.

This sequencing reduces conflicting sell orders but creates a brief unprotected
window after exit stops are confirmed canceled and before residual protection is
restored. It cannot guarantee fill price and must remain paper-only.

## Idempotency

Each entry attempt, protective stop, repair, exit, and emergency liquidation
uses a deterministic, length-bounded `client_order_id` derived from canonical
intent or event data. Before submission, the gateway asks the broker for that
ID. A routine crash after broker acceptance can therefore recover the accepted
order instead of relying on a Markdown `EXECUTED` marker.

This is duplicate resistance, not a mathematical exactly-once guarantee.
Correctness also depends on broker retention and API semantics, stable canonical
inputs, credential/account isolation, and no order submission outside the
gateway. Never alter a plan and retry merely to obtain a different ID after an
ambiguous result; reconcile first. A later attempt ID appearing without every
earlier attempt is treated as an unresolved broker-history break and blocks
recreation of the missing order.

### Order-status handling

Only `filled`, `canceled`, `expired`, and `rejected` are treated as terminal.
Statuses including `stopped`, `done_for_day`, `calculated`, `pending_cancel`,
and `pending_replace` remain unresolved/open for this system even when their
names sound final. A timeout must not be converted into a retry until the
broker confirms a terminal state.

## Reconciliation and stop coverage

Run reconciliation at the start and end of every routine. It is read-only under
`PAUSED`; scheduled routines use repair mode under `ACTIVE` or `RISK_OFF`:

```bash
python3 scripts/trade.py reconcile --agent bull --repair
python3 scripts/trade.py reconcile --agent aggro --repair
```

It compares the account, broker positions, and open orders with the system's
managed-state invariants. It reports blocked/suspended/inactive or invalid
accounts, unmanaged non-protective open orders, orphan stops, instruments absent
from the approved master, short/zero positions, incorrect trail percentage or
time-in-force, stop over-coverage, and incomplete coverage.

`--repair` normalizes managed order state. For simple under-coverage it submits
only the missing share quantity:

```bash
python3 scripts/trade.py reconcile --agent bull --repair
```

Repair is a broker mutation. It is allowed in `ACTIVE` and `RISK_OFF` and
blocked in `PAUSED`. It leaves unmanaged non-protective orders and orphan stops
untouched and reports them as unresolved. It adds only missing protection and
uses broker PATCH replacement for invalid or over-covered managed stops so the
prior stop remains live if replacement fails. A fully redundant stop is canceled
only when other live stops already cover the holding. Repair also attempts to
flatten forbidden shorts and unknown held non-equities. An unknown long US
equity is protected but remains an unresolved instrument-policy issue.

Any unresolved issue exits nonzero. Stop coverage is an operational check, not
a guaranteed loss boundary: a trailing stop can trigger or fill through its
reference level during gaps, volatility, latency, or illiquidity.

## Control-state matrix

| Operation | ACTIVE | RISK_OFF | PAUSED |
|---|---:|---:|---:|
| Read broker state | Yes | Yes | Yes |
| Read-only reconcile | Yes | Yes | Yes |
| New buy | Eligible | Blocked | Blocked |
| Planned/midday exit | Eligible | Eligible | Blocked |
| Managed-stop/forbidden-holding containment | Eligible | Eligible | Blocked |

Invalid, missing, or unreadable status blocks mutations. `NOTE:` and `QUERY:`
are communication fields and never create trade authority.

## Plan contract

The plan is the unique newest-dated fenced `json` object in:

- Bull: `memory/research-log.md`
- AGGRO: `memory/aggressive/research-log.md`

It must match `schemas/trade-plan.schema.json`. The execution parser applies
the same critical checks independently; the JSON schema assists authors and CI
but is not the execution authority.

The top-level envelope contains exactly `schema_version`, `agent`, `plan_date`,
and `trades`; unknown fields fail. Each intent contains exactly its typed common
fields. A version-2 `buy` accepts and requires the four entry/earnings fields
plus `research_packet_id` and `research_packet_sha256`; `trim` and `exit` reject
all six. The selected profile must match `agent`, and one symbol may have only
one action in a plan.

The following is a **structural illustration only**. Its placeholder earnings
source is not in the checked-in trusted calendar, so it cannot authorize a buy.
An executable buy must copy all three earnings values exactly from a fresh
human-owned calendar record.

```json
{
  "schema_version": 2,
  "agent": "bull",
  "plan_date": "2026-07-16",
  "trades": [
    {
      "action": "buy",
      "symbol": "ETN",
      "qty": 10,
      "sector": "Industrials",
      "thesis": "Data-center power demand supports durable multi-quarter growth.",
      "invalidation": "Management cuts organic-growth guidance.",
      "review_by": "2026-08-14",
      "max_entry_price": "425.00",
      "earnings_date": "2026-08-05",
      "earnings_verified_at": "2026-07-16T08:00:00-04:00",
      "earnings_source": "https://calendar.example.invalid/etn",
      "research_packet_id": "bull:2026-07-16:premarket:example",
      "research_packet_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    },
    {
      "action": "trim",
      "symbol": "V",
      "qty": 5,
      "sector": "Financials",
      "thesis": "Reduce concentration while retaining the long-term payment thesis.",
      "invalidation": "Position remains above its approved concentration band.",
      "review_by": "2026-07-31"
    }
  ]
}
```

The parser selects by maximum `plan_date`, not file position, because historical
logs have used both prepend and append conventions. Multiple supported-schema
plans on the newest date, or any malformed fenced JSON block, fail closed.

An empty `trades` array is valid and is preferable to inventing a low-quality
trade. New plans use `schema_version: 2`; `agent` must match the gateway profile.
Version 1 is parsed only for legacy continuity and cannot authorize a genuinely
new buy because it has no research identity. It has no scheduled-playbook path;
all scheduled plans require version 2. Plans may contain at most 12 intents. A
symbol may appear only once per plan, regardless of action.

New packet appends use the current human-owned market-source age. Whole-ledger
validation uses the immutable schema-v1 ceiling of 1,440 minutes so tightening
today's policy does not invalidate accepted history. Execution then applies the
current tighter limit again. Pending packets are atomically renamed to a unique
claim before validation; a failed claim is restored only when doing so cannot
overwrite a newer producer's packet. Its claim link is retained for audit and
blocks persistence. An exact retry that consumes the same inode removes both
links; a distinct retained claim requires human inspection and explicit cleanup,
never blind deletion by an agent.

## Audit data and recovery

- `memory/execution-events.jsonl` for Bull and
  `memory/aggressive/execution-events.jsonl` for AGGRO receive reconciliation,
  approval, submission, protection, completion, and failure events. Appends are
  flushed and synced, but a telemetry-write failure does not interrupt an
  in-progress broker-protection path.
- `memory/trades.jsonl` for Bull and `memory/aggressive/trades.jsonl` for AGGRO
  receive structured fills with broker identifiers. They are not a complete
  double-entry or transactional lifecycle ledger.
- `memory/performance.csv` for Bull and
  `memory/aggressive/performance.csv` for AGGRO contain profile-scoped daily
  snapshots. Historical mixed rows were split without changing their values.
- Research logs and portfolio Markdown are reports. They can lag or conflict
  after a crash and must never be used to infer that an order did or did not
  reach the broker.

After a timeout, crash, conflicting report, or unexpected position:

1. Set `STATUS: PAUSED` if preserving broker state for investigation is safer.
2. Inspect `account`, `positions`, and `orders` with `scripts/alpaca.sh`.
3. Run read-only reconciliation and save its output.
4. Search the broker order list by returned client/broker identifiers; do not
   resubmit with modified inputs.
5. Resolve unknown instruments, over-coverage, or account mismatch manually.
6. Move to `RISK_OFF` if exits or stop repair are required, then perform the
   minimum reviewed action through `scripts/trade.py`.
7. Reconcile again and document the incident.

## Known limitations before any live-capital consideration

- No strategy in this repository has established future alpha. Backtests,
  walk-forward validation, realistic costs, capacity analysis, and independent
  model-risk review are not supplied by this control layer.
- Research packets are structurally validated declarations. The current code
  does not fetch and attest source content, verify publisher ownership or source
  tier, require a captured content hash, or independently detect prompt
  injection. Declared completeness and distinct hosts are not proof of complete
  coverage or source independence. Until trusted acquisition exists, this is a
  fail-closed governance scaffold, not verified investment evidence.
- Human earnings-calendar content can still be wrong. The gateway requires an
  exact match to the fresh human-owned record; it does not independently prove
  that the human-selected source is correct.
- The quoted-spread gate uses one top-of-book IEX observation. It does not model
  depth, volume participation, impact, queue priority, or future liquidity.
- Paper fills do not reproduce live liquidity, queue priority, impact, or
  slippage. Trailing stops do not guarantee a price or exact maximum loss.
- The append-only files are useful evidence but not a transactional database.
  A same-host per-command account lock and GitHub workflow concurrency do not serialize
  independent cloud hosts. Concurrent runs, repository writes, and failed
  pushes can still strand journal state behind broker reality. `_lock` is not
  distributed.
- Broker/API outages, stale portfolio history, corporate actions, symbol
  changes, and eventual consistency require operator intervention.
- The allowlisted instrument master is intentionally narrow and needs human
  review for additions and sector changes.
- Audit-file writes are local to a routine checkout until committed and pushed;
  a crash or repository conflict can leave them behind broker reality.
- Cloud secrets and permissions can bypass application-level intent if the
  surrounding environment is compromised.
- The gateway fingerprints the account against an environment-owned expected
  ID. A coordinated swap of both credentials and expected ID can still pass;
  environment assignment is not an independent profile registry.

Keep the system on paper accounts. A move toward live capital would require a
separate, explicit project with legal/compliance review, an independent account
registry, cross-host serialization, independent risk controls, durable
transactional storage, observability and alerting, disaster recovery,
adversarial testing, staged capital limits, and a human kill switch outside the
agent runtime.
