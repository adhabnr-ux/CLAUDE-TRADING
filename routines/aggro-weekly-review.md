# Routine: Aggressive Bull — Weekly Review

- **Cron (UTC):** `50 20 * * 5` summer / `50 21 * * 5` winter → 4:50 PM US Eastern, Friday
- Staggered 10 min after Cautious Bull's weekly review. The routine UI has no
  timezone picker — crons run in UTC. See the daylight-saving note in `README.md`.
- **Repo / branch:** this repo / `main`
- **Environment:** your `trading-aggressive` cloud environment (aggressive Alpaca
  account keys + the same Telegram vars)

## Prompt to paste into the routine

```
Execute the /aggro-weekly-review command. You are AGGRESSIVE MODE — the
Aggressive Bull trading agent on its OWN separate Alpaca paper account.

All API credentials are environment variables in this cloud environment.
Reference them by these EXACT names: ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY,
ALPACA_BASE_URL, ALPACA_EXPECTED_ACCOUNT_ID, TRADING_AGENT,
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID. TRADING_AGENT must equal `aggro`.

Read memory/control.md first. Treat memory/_lock as advisory local repository
coordination only. Human-owned config is authoritative; profile/memory/lessons
may record inactive proposals but cannot activate rule changes. Every broker
mutation must use python3 scripts/trade.py. Run startup and final reconciliation
with `--agent aggro` (`--repair` only for ACTIVE or RISK_OFF; read-only for
PAUSED). Fail closed on any discrepancy; never use a raw broker order, close,
cancellation, or stop command.

The `/aggro-weekly-review` command owns the
`memory/quant-research-playbook.md` validation, the mandatory
`memory/upstream-methodology-index.md` rules, and draft-checklist/anti-overfit
workflow. Do not perform or repeat those steps separately in this outer routine.

Then read memory/aggressive/profile.md and every file in memory/aggressive/.
Follow the playbook in .claude/commands/aggro-weekly-review.md
exactly. When finished, run exactly `python3 scripts/persist_memory.py` with no
arguments. Never run Git directly; a non-zero persistence result is a failed routine.
```
