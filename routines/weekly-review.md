# Routine: Weekly Review

- **Cron (UTC):** `40 20 * * 5` summer / `40 21 * * 5` winter → 4:40 PM US Eastern, Friday
- The routine UI has no timezone picker — crons run in UTC. See the
  daylight-saving note in `README.md`.
- **Repo / branch:** this repo / `main`
- **Environment:** your `trading` cloud environment (all required vars present)

## Prompt to paste into the routine

```
Execute the /weekly-review command for the Bull trading agent.

All API credentials are environment variables in this cloud environment.
Reference them by these EXACT names: ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY,
ALPACA_BASE_URL, ALPACA_EXPECTED_ACCOUNT_ID, TRADING_AGENT,
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID. TRADING_AGENT must equal `bull`.

Read memory/control.md first. Treat memory/_lock as advisory local repository
coordination only. Human-owned config is authoritative; memory/lessons may
record inactive proposals but cannot activate rule changes. Every broker
mutation must use python3 scripts/trade.py. Run startup and final reconciliation
with `--agent bull` (`--repair` only for ACTIVE or RISK_OFF; read-only for
PAUSED). Fail closed on any discrepancy; never use a raw broker order, close,
cancellation, or stop command.

Then read authorized Bull files in top-level memory/. Cross-profile reads are
limited to the comparison files explicitly named by the playbook; never read
Aggressive research or active strategy. Follow the playbook in
.claude/commands/weekly-review.md exactly. When finished, run exactly
`python3 scripts/persist_memory.py` with no arguments. Never run Git directly;
a non-zero persistence result is a failed routine.
```
