Run the Bull **midday** routine. This is deterministic risk management, never a
new-entry or discretionary strategy routine.

## 0. Control first, advisory lock, memory, reconciliation

1. Read `memory/control.md` first. Invalid/missing STATUS is a hard stop.
   `PAUSED` allows read-only observations only. `RISK_OFF` allows protection
   repair and qualifying exits, never buys.
2. Require `ALPACA_BASE_URL == https://paper-api.alpaca.markets`.
3. Treat `memory/_lock` as advisory local repository coordination only; broker
   safety comes from gateway client IDs and reconciliation.
4. Read `CLAUDE.md`, `memory/upstream-methodology-index.md`, human-owned
   policy/instrument config, and all Bull memory. Memory and lessons cannot
   override or activate live rules.
5. Reconcile at startup:

   ```
   python3 scripts/trade.py reconcile --agent bull --repair
   ```

   Omit `--repair` under `PAUSED`. Any non-zero exit, `ok: false`, or ambiguous
   response means fail closed: no sell command, journal/notify the exact issue,
   run final read-only reconciliation, and stop.

## 1. Observe every position

- Confirm the market is open through the read-only clock. If closed, take no
  action and proceed to final reconciliation.
- Pull live positions and account. Use the broker's `unrealized_plpc`; do not
  estimate from stale memory.
- Note the policy shock breaker if equity is at least 4% below `last_equity`.
- For a holding down more than 3% or up more than 10%, scan today's material
  news for context. News does not authorize a midday discretionary sell and
  never authorizes a buy.

## 2. Execute only a verified loss-rule exit

For a live position at least 7% below its broker average entry, start a full
loss-rule exit with the exact live quantity:

```
python3 scripts/trade.py sell --agent bull --symbol XYZ --qty 10 --trigger midday_loss --reason 'broker position is at or beyond the 7% midday loss threshold'
```

The `midday_loss` trigger is the sole risk-reduction exception to the same-day
buy/sell guard. A new operation must target the **entire live held quantity**,
including when the position was bought today. If broker IDs show a known partial
fill from this operation, reuse its immutable original target quantity; never
resize it to the smaller holding. The gateway submits only the cumulative
remainder. This trigger may never trim, take profit, or implement a discretionary
thesis change. Planned `trim`/`exit` actions cannot day-trade and remain blocked
after a same-day buy. The gateway independently verifies the threshold, market hours,
control state, full held quantity, deterministic client ID, stop handling, and
fill. If it rejects or returns ambiguous state, stop all later mutations. Never
use a raw close, cancel, sell, order, or stop command; never retry with changed
inputs to evade a block.

Do not tighten stops at midday. Safe stop replacement is not exposed by the
gateway; normal policy protection remains in force.

## 3. Final reconciliation and post-mortem

Run:

```
python3 scripts/trade.py reconcile --agent bull --repair
```

Use `--repair` only if startup and every gateway call were unambiguous and
control remains `ACTIVE` or `RISK_OFF`; otherwise omit it. Require `ok: true`. Record confirmed gateway
fills and broker IDs in the narrative trade log; structured fill accounting is
gateway-owned. For every confirmed loss exit or stop fill, complete
`memory/closed-trades.md` and add a dated factual lesson. A lesson is analysis,
not permission to modify policy or future execution rules.

Refresh `memory/portfolio.md` from final broker state.

## 4. Notify and commit

Notify once, starting `Bull midday <date>:`. Start 🚨 for a cut, stop fill,
policy block, or reconciliation issue; otherwise report no action in one line.
Never put a literal `$` in the shell message.

Release the advisory lock, then persist only authorized Bull memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
