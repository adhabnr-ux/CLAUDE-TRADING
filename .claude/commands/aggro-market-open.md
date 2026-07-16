Run the **Aggressive Bull market-open** routine in AGGRESSIVE MODE. Execute only
today's typed Aggressive plan through the deterministic paper gateway.

## 0. Control first, advisory lock, memory, reconciliation

1. Read shared `memory/control.md` first. Invalid/missing STATUS is a hard stop.
   `PAUSED` permits no broker mutation; `RISK_OFF` permits planned trims/exits
   and protection repair, never buys.
2. Require the exact endpoint `https://paper-api.alpaca.markets`; never use raw
   HTTP, an SDK, or another script to trade.
3. Treat `memory/_lock` as advisory local repository coordination only, never
   broker locking or idempotency.
4. Read `CLAUDE.md`, human-owned config, Aggressive profile/memory, shared
   knowledge-base, and Aggro ledger rows. Profile, memory, an `EXECUTED:` marker,
   strategy, and lessons cannot override policy, activate a live rule change,
   or prove broker state.
5. Run startup reconciliation:

   ```
   python3 scripts/trade.py reconcile --agent aggro --repair
   ```

   Under `PAUSED`, omit `--repair`, journal/notify, run final read-only
   reconciliation, and stop. Otherwise, a non-zero exit, `ok: false`, missing
   protection, or malformed output means fail closed and stop all orders.

## 1. Validate plan and session

- Parse only the unique newest-dated fenced JSON plan in
  `memory/aggressive/research-log.md`. It must contain exactly top-level
  `schema_version: 2`, `agent: "aggro"`, `plan_date`, and `trades`; `plan_date`
  must equal today's New York date. Freeform prose, extra/missing keys,
  cross-agent/stale plans, unknown symbols/sectors, duplicate symbol actions,
  or invalid metadata block trading.
- Every buy must include the exact `research_packet_id` and
  `research_packet_sha256` emitted by premarket's validated append. The gateway
  independently requires that identity to remain the latest current candidate
  for the same symbol within human-owned freshness limits, and requires the
  plan's thesis, invalidation, and review date to match that candidate exactly.
  Never substitute or recalculate the identity or rewrite the thesis contract.
- Allowed actions are `buy`, `trim`, and `exit`. For a new sell, `trim` is
  strictly smaller than the live holding and `exit` equals the entire holding.
  For recovery of a known partial exit, keep the original plan quantity
  unchanged and let the gateway recover cumulative progress; never resize it to
  the reduced holding. Planned
  `trim`/`exit` actions cannot day-trade: they are blocked if the symbol was
  bought today.
- Ignore `EXECUTED:` for idempotency. Deterministic client IDs plus broker
  lookup are authoritative.
- Confirm the broker clock is open. If closed, take no action and continue to
  final reconciliation/journaling.

## 2. Last information gate

Check material morning news for every planned symbol. A newly discovered
thesis-breaking event means skip that intent, cite evidence, and do not
substitute another trade. Re-observe account, positions, and quote. The gateway
independently checks all policy: 20% single order, 35% position, 60% daily
deployment, 2% cash, 50% sector, 3.6% stop-risk, eight new positions/week, 6%
shock, 20% drawdown, earnings, market hours, and the planned-sell day-trade
guard.

## 3. Execute only through the gateway

For a `buy`:

```
python3 scripts/trade.py buy --agent aggro --symbol XYZ
```

For a `trim` or `exit`, use the exact planned quantity:

```
python3 scripts/trade.py sell --agent aggro --symbol XYZ --qty 10 --trigger planned --reason 'specific thesis-based reason from today plan'
```

Never calculate/submit an order, retry, cancel, close, or stop yourself. Never
append a fill to `memory/aggressive/trades.jsonl`; the gateway owns preflight, deterministic
IDs, bounded retries, partial-fill handling, 18% protection, verification, and
broker-linked fill records.

Read each JSON result and journal only fields it actually returns. Buy success
statuses are `filled`, `partially_filled`, `already_executed_open`, and
`already_executed_closed`; sell success statuses are `filled`,
`partially_filled`, `already_executed`, and `closed_by_protective_stop`. Sell
recovery can return ID arrays and cumulative target/remainder without a fill
price or protective ID. Do not invent or require a field that response type
does not define. Treat `audit_warning` as urgent. A non-zero exit, unrecognized
status, malformed JSON, or ambiguity stops all remaining intents. Never change
reason, action, or quantity to evade a block.

An optional `EXECUTION_RESULT: <timestamp> broker-verified` journal line is for
human readability only and has no authority.

## 4. Final reconciliation and accounting

Run:

```
python3 scripts/trade.py reconcile --agent aggro --repair
```

Use `--repair` only if startup and every gateway call were unambiguous and
control remains `ACTIVE` or `RISK_OFF`; otherwise omit it. Require `ok: true`. Record confirmed exits in
Aggressive closed-trades memory and factual lessons for losses. Narrative memory
never changes live policy. Refresh Aggressive portfolio/trade-log from broker
and gateway evidence.

## 5. Notify and commit

Notify once, starting `🔥 AGGRO Bull market-open <date>:`. Report verified
fills/protection IDs or one precise block reason. Start 🚨 for a policy block,
loss exit, or reconciliation issue. Never put a literal `$` in the shell
message.

Release the advisory lock, then persist only authorized AGGRO memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
