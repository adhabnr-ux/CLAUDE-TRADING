# Lessons Learned

_Carried forward across every run. Add a dated line whenever something works
well, fails, or surprises you. Keep the highest-value lessons near the top._

## Operating lessons (seed)

- Always run `./scripts/alpaca.sh clock` before trading; do nothing if the
  market is closed.
- After any order, re-fetch `positions` and `orders` to confirm the fill before
  journaling or notifying.
- Notional (dollar-based) buys can produce fractional shares — fractional
  positions cannot use trailing-stop orders. To guarantee a trailing stop is
  possible, prefer whole-share quantities for new positions.
- If a credential env var is missing, stop immediately and notify — never guess.
- Commit and push to `main` at the end of every run, or the next agent loses
  this run's work.

## Trading lessons

### 2026-05-20 — market-open aborted: missing credentials
- `ALPACA_API_KEY_ID`, `ALPACA_API_SECRET_KEY`, and `ALPACA_BASE_URL` were all
  unset in the cloud environment. No clock check, no trades, no notifications.
- **Action required:** inject the three Alpaca env vars (and optionally
  `CALLMEBOT_PHONE` / `CALLMEBOT_APIKEY`) into the environment before the next
  routine runs.
- Note: strategy.md is still NOT_INITIALIZED and research-log.md has no
  pre-market research. The pre-market routine must run first with valid
  credentials before market-open can execute meaningfully.
