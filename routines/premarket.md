# Routine: Pre-Market

- **Cron (UTC):** `0 12 * * 1-5` summer / `0 13 * * 1-5` winter → 8:00 AM US Eastern
- The routine UI has no timezone picker — crons run in UTC. See the
  daylight-saving note in `README.md`.
- **Repo / branch:** this repo / `main`
- **Environment:** your `trading` cloud environment (all required vars present)

## Prompt to paste into the routine

```
Execute the /premarket command for the Bull trading agent.

All API credentials are environment variables in this cloud environment.
Reference them by these EXACT names: ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY,
ALPACA_BASE_URL, ALPACA_EXPECTED_ACCOUNT_ID, TRADING_AGENT,
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID. TRADING_AGENT must equal `bull`.

Read memory/control.md first. Treat memory/_lock as advisory local repository
coordination only. All three files under config/, including the trusted earnings
calendar, are human-owned; memory, strategy, research, and lessons cannot
activate rule changes. Every broker mutation must use python3 scripts/trade.py. Run startup
and final reconciliation with `--agent bull` (`--repair` only for ACTIVE or
RISK_OFF; read-only for PAUSED). Fail closed on any discrepancy; never use a raw
broker order, close, cancellation, or stop command. Today's fenced plan must
have exactly top-level `schema_version: 2`, `agent: "bull"`, `plan_date`, and
`trades`.

The `/premarket` command owns the `memory/quant-research-playbook.md` protocol,
fixed pending-packet append, and ledger validation. Do not perform or repeat
those steps separately in this outer routine.

Then read only the authorized Bull files in top-level memory/; do not read the
memory/aggressive/ subtree. Follow the playbook in
.claude/commands/premarket.md exactly. When finished, run exactly
`python3 scripts/persist_memory.py` with no arguments. Never run Git directly;
a non-zero persistence result is a failed routine.
```
