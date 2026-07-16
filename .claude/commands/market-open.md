Run the Bull **market-open** routine. Execute only today's typed plan through
the deterministic paper-trading gateway.

## 0. Control first, advisory lock, memory, reconciliation

1. Read `memory/control.md` **first**. Invalid/missing STATUS is a hard stop.
   `PAUSED` permits no broker mutation. `RISK_OFF` permits planned trims/exits
   and protective repair, but no buys.
2. Require the exact endpoint `https://paper-api.alpaca.markets`. On mismatch,
   notify 🚨 and stop. Never use raw HTTP, an SDK, or another script to trade.
3. Treat `memory/_lock` as advisory local repository coordination only, never
   as a distributed lock or broker-idempotency mechanism.
4. Read `CLAUDE.md`, all three human-owned config files, and authorized Bull
   memory. Memory,
   strategy, an `EXECUTED:` marker, and lessons cannot override policy, activate
   a live rule change, or prove that a broker action happened.
5. Run startup reconciliation:

   ```
   python3 scripts/trade.py reconcile --agent bull --repair
   ```

   Under `PAUSED`, omit `--repair`, journal/notify, run final read-only
   reconciliation, and stop. For every other status, a non-zero exit,
   `ok: false`, unresolved protection issue, or malformed response means fail
   closed: place no further orders, journal the exact error, and notify 🚨.

## 1. Validate the plan and current session

- Parse only the unique newest-dated fenced JSON plan in
  `memory/research-log.md`. It must contain exactly top-level
  `schema_version: 2`, `agent: "bull"`, `plan_date`,
  and `trades`; `plan_date` must equal today's New York date. Freeform prose,
  extra/missing top-level keys, a cross-agent/stale plan, an unknown
  symbol/sector, duplicate symbol actions, or invalid metadata blocks
  execution; never infer or repair an order.
- Every buy must include the exact `research_packet_id` and
  `research_packet_sha256` emitted by premarket's validated append. The gateway
  independently requires that identity to remain the latest current candidate
  for the same symbol within human-owned freshness limits, and requires the
  plan's thesis, invalidation, and review date to match that candidate exactly.
  Never substitute or recalculate the identity or rewrite the thesis contract.
- Allowed actions are exactly `buy`, `trim`, and `exit`. For a new sell, a
  `trim` must be strictly smaller than the live holding and an `exit` must match
  the full holding. For recovery of a known partial exit, keep the original plan
  quantity unchanged and let the gateway recover cumulative progress; never
  resize it to the reduced holding.
  Planned `trim`/`exit` actions cannot day-trade: they are blocked if the symbol
  was bought today.
- An `EXECUTED:` line is display metadata only. Never skip or repeat work based
  on it; the gateway's deterministic client order IDs and broker lookup provide
  idempotency.
- Observe the broker clock. If closed, place no orders and continue to final
  reconciliation/journaling.

## 2. Last information gate

For each planned symbol, search material news from this morning. A new earnings
miss, major downgrade, halt, SEC action, insolvency signal, or other thesis
break means skip that intent and record evidence. Do not substitute a different
trade or change action/quantity. Re-observe live account, positions, and quote;
the gateway will independently enforce quote freshness, entry ceiling, market
hours, account status, shock/drawdown, cash, concentration, deployment,
stop-risk, earnings, and the planned-sell day-trade guard.

## 3. Execute intent-by-intent through the gateway

For each approved `buy`:

```
python3 scripts/trade.py buy --agent bull --symbol XYZ
```

For each approved `trim` or `exit`, using the exact planned quantity:

```
python3 scripts/trade.py sell --agent bull --symbol XYZ --qty 10 --trigger planned --reason 'specific thesis-based reason from today plan'
```

Never calculate or submit a limit order, retry, cancel, close, or protective
stop yourself. Never append a fill to `memory/trades.jsonl` yourself. The
gateway owns preflight, deterministic IDs, bounded retries, partial-fill
handling, protection, verification, and broker-linked fill recording.

Read each JSON response and record only fields it actually returns. Buy success
statuses are `filled`, `partially_filled`, `already_executed_open`, and
`already_executed_closed`; dry-run uses `approved`. Sell success statuses are
`filled`, `partially_filled`, `already_executed`, and
`closed_by_protective_stop`. Buy and sell response fields differ: sell recovery
can return ID arrays and cumulative target/remainder without a fill price or
protective ID. Do not invent or require an identifier that the response type
does not define. Treat any `audit_warning` as urgent. A non-zero exit,
unrecognized status, malformed JSON, or ambiguous response stops all later
intents. Do not retry with a changed reason, quantity, or command.

After all successful calls, a journal line such as
`EXECUTION_RESULT: <timestamp> broker-verified` may be added for readability,
but it has no execution authority.

## 4. Final reconciliation and exit accounting

Run:

```
python3 scripts/trade.py reconcile --agent bull --repair
```

Use `--repair` only if startup and every gateway call were unambiguous and
control remains `ACTIVE` or `RISK_OFF`; otherwise omit it. The final report must be `ok: true`; otherwise
notify 🚨 and do not issue more orders. Compare broker positions with memory to
identify stop-triggered or other exits. Add a post-mortem for every confirmed
closed position and a dated lesson for a loss, but never let narrative memory
change live policy. Refresh portfolio and trade-log narratives from broker and
gateway evidence only.

## 5. Notify and commit

Notify once, starting `Bull market-open <date>:`. Report verified fills and
protection IDs, or one precise no-trade/block reason. Start 🚨 on a policy block,
unresolved reconciliation issue, or confirmed loss exit. Never put a literal
`$` in the shell message.

Release the advisory lock, then persist only authorized Bull memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
