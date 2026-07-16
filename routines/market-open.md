# Routine: Market Open

- **Cron (UTC):** `35 13 * * 1-5` summer / `35 14 * * 1-5` winter → 9:35 AM US Eastern
- The routine UI has no timezone picker — crons run in UTC. See the
  daylight-saving note in `README.md`.
- **Repo / branch:** this repo / `main`
- **Environment:** your `trading` cloud environment (all required vars present)

## Prompt to paste into the routine

```
Execute the /market-open command for the Bull trading agent.

All API credentials are environment variables in this cloud environment.
Reference them by these EXACT names: ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY,
ALPACA_BASE_URL, ALPACA_EXPECTED_ACCOUNT_ID, TRADING_AGENT,
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID. TRADING_AGENT must equal `bull`.

Read memory/control.md first. Treat memory/_lock as advisory local repository
coordination only. Human-owned config is authoritative; no memory or lesson can
activate a rule change. Every broker mutation must use python3 scripts/trade.py.
Run startup and final reconciliation with `--agent bull` (`--repair` only for
ACTIVE or RISK_OFF; read-only for PAUSED). Execute only current typed
buy/trim/exit intents from a plan with exactly top-level `schema_version: 2`,
`agent: "bull"`, `plan_date`, and `trades`. Planned trims/exits cannot day-trade
and remain blocked after a same-day buy. Fail closed on any discrepancy; never
use a raw broker order, close, cancellation, or stop command.

Then read only the authorized Bull files in top-level memory/; do not read the
memory/aggressive/ subtree. Follow the playbook in
.claude/commands/market-open.md exactly. When finished, run exactly
`python3 scripts/persist_memory.py` with no arguments. Never run Git directly;
a non-zero persistence result is a failed routine.
```
