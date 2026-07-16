Run the **Aggressive Bull midday** routine in AGGRESSIVE MODE. This is
deterministic risk management, never a new-entry or discretionary strategy run.

## 0. Control first, advisory lock, memory, reconciliation

1. Read shared `memory/control.md` first. Invalid/missing STATUS is a hard stop.
   `PAUSED` allows read-only observations only; `RISK_OFF` allows protection
   repair and qualifying exits, never buys.
2. Require `ALPACA_BASE_URL == https://paper-api.alpaca.markets`.
3. Treat `memory/_lock` as advisory local repository coordination only; client
   IDs and broker reconciliation provide safety.
4. Read `CLAUDE.md`, human-owned config, Aggressive profile/memory, shared
   knowledge-base, and Aggro ledger rows. Profile, strategy, memory, and lessons
   cannot override or activate live policy.
5. Reconcile at startup:

   ```
   python3 scripts/trade.py reconcile --agent aggro --repair
   ```

   Omit `--repair` under `PAUSED`. Any non-zero exit, `ok: false`, or ambiguous
   output means fail closed: issue no sell, journal/notify, run final read-only
   reconciliation, and stop.

## 1. Observe every position

- Confirm the broker clock is open; if closed, take no action and proceed to
  final reconciliation.
- Pull live account/positions and use broker `unrealized_plpc`, not memory math.
- Note a shock day when equity is at least 6% below `last_equity`.
- Scan material news for positions down more than 5% or up more than 15% for
  context only. News does not authorize a discretionary midday sell or any buy.

## 2. Execute only a verified loss-rule exit

For a live position at least 12% below broker average entry, start a full
loss-rule exit using exact live quantity:

```
python3 scripts/trade.py sell --agent aggro --symbol XYZ --qty 10 --trigger midday_loss --reason 'broker position is at or beyond the 12% midday loss threshold'
```

The `midday_loss` trigger is the sole risk-reduction exception to the same-day
buy/sell guard. A new operation must target the **entire live held quantity**,
including when the position was bought today. If broker IDs show a known partial
fill from this operation, reuse its immutable original target quantity; never
resize it to the smaller holding. The gateway submits only the cumulative
remainder. This trigger may never trim, take profit, or implement a discretionary
thesis change. Planned `trim`/`exit` actions cannot day-trade and remain blocked
after a same-day buy. The gateway independently verifies trigger, clock, control,
full held quantity, deterministic ID, stop handling, and fill. On rejection or
ambiguity, stop all later mutations. Never use a raw close, cancel, sell, order,
or stop command; never alter inputs to evade a block.

Do not tighten stops at midday. Safe stop replacement is not exposed by the
gateway; normal 18% machine protection remains in force.

## 3. Final reconciliation and post-mortem

Run:

```
python3 scripts/trade.py reconcile --agent aggro --repair
```

Use `--repair` only if startup and every gateway call were unambiguous and
control remains `ACTIVE` or `RISK_OFF`; otherwise omit it. Require `ok: true`. Record confirmed gateway
fills/broker IDs in Aggressive narrative logs. Structured fill accounting is
gateway-owned. Complete an Aggressive closed-trade post-mortem and factual loss
lesson for every confirmed loss exit/stop fill. Lessons are not live rules.
Refresh Aggressive portfolio memory from final broker state.

## 4. Notify and commit

Notify once, starting `🔥 AGGRO Bull midday <date>:`. Start 🚨 for a cut, stop
fill, policy block, or reconciliation issue; otherwise one-line no action.
Never put a literal `$` in the shell message.

Release the advisory lock, then persist only authorized AGGRO memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
