# Routine: Monthly deep review (Cautious Bull)

Runs every Friday evening after the weekly review; the playbook itself exits
unless it is the **first Friday of the calendar month** (no "first Friday"
cron syntax exists, so the gate lives in the playbook).

## Schedule (UTC cron — adjust for US daylight saving)

| Season | Cron |
|--------|------|
| Summer (EDT) | `20 21 * * 5` (5:20 PM ET) |
| Winter (EST) | `20 22 * * 5` (5:20 PM ET) |

Runs 30 minutes after the weekly review. `memory/_lock` is only an advisory
local repository signal; it is not a distributed broker lock.

## Cowork routine prompt

```
Run the Bull monthly deep review. Follow the playbook in
.claude/commands/monthly-review.md exactly. You are Cautious Bull (default
mode). Read memory/control.md first. The playbook self-gates: if today is not
the first Friday of the month, exit quietly. Human-owned config is
authoritative; memory/lessons can only record inactive proposals. Every broker
mutation must use python3 scripts/trade.py. On a proceeding run, reconcile at
startup and end with `--agent bull` (`--repair` only for ACTIVE or RISK_OFF;
read-only for PAUSED), and fail closed on any discrepancy. Never use a raw
broker order, close, cancellation, or stop command. Required environment names
are ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY, ALPACA_BASE_URL,
ALPACA_EXPECTED_ACCOUNT_ID, TRADING_AGENT, TELEGRAM_BOT_TOKEN, and
TELEGRAM_CHAT_ID; TRADING_AGENT must equal `bull`. Finish by running exactly
`python3 scripts/persist_memory.py` with no arguments. Never run Git directly.
```

Type: Remote · repo: this repo · branch `main` · environment `trading` ·
permissions: fixed profile-scoped persistence helper only.
