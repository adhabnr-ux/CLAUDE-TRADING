# Routine: Aggressive Bull — Market Open

- **Cron (UTC):** `45 13 * * 1-5` summer / `45 14 * * 1-5` winter → 9:45 AM US Eastern
- Staggered 10 min after Cautious Bull's market-open. The routine UI has no
  timezone picker — crons run in UTC. See the daylight-saving note in `README.md`.
- **Repo / branch:** this repo / `main`
- **Environment:** your `trading-aggressive` cloud environment (aggressive Alpaca
  account keys + the same Telegram vars)

## Prompt to paste into the routine

```
Execute the /aggro-market-open command. You are AGGRESSIVE MODE — the Aggressive
Bull trading agent on its OWN separate Alpaca paper account.

All API credentials are environment variables in this cloud environment.
Reference them by these EXACT names: ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY,
ALPACA_BASE_URL, ALPACA_EXPECTED_ACCOUNT_ID, TRADING_AGENT,
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID. TRADING_AGENT must equal `aggro`.

Read memory/control.md first. Treat memory/_lock as advisory local repository
coordination only. Human-owned config is authoritative; profile/memory/lessons
cannot activate rule changes. Every broker mutation must use python3
scripts/trade.py. Run startup and final reconciliation with `--agent aggro`
(`--repair` only for ACTIVE or RISK_OFF; read-only for PAUSED). Execute only
current typed buy/trim/exit intents from a plan with exactly top-level
`schema_version: 2`, `agent: "aggro"`, `plan_date`, and `trades`. Planned
trims/exits cannot day-trade and remain blocked after a same-day buy. Fail closed
on any discrepancy; never use a raw broker order, close, cancellation, or stop
command.

Then read memory/aggressive/profile.md and every file in memory/aggressive/.
Follow the playbook in .claude/commands/aggro-market-open.md
exactly. When finished, run exactly `python3 scripts/persist_memory.py` with no
arguments. Never run Git directly; a non-zero persistence result is a failed routine.
```
