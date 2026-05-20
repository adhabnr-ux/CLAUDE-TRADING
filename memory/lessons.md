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

### 2026-05-20 — First run: credential issue
- All five env vars (ALPACA_API_KEY_ID, ALPACA_API_SECRET_KEY, ALPACA_BASE_URL,
  CALLMEBOT_PHONE, CALLMEBOT_APIKEY) are present in the environment but set to
  empty strings. The alpaca.sh script correctly rejects the empty credentials
  and exits with an error. Per guardrails, no orders were placed and no
  notification could be sent.
- **Action needed by human**: populate the environment variables with valid
  Alpaca paper-account credentials and CallMeBot details before the next
  routine runs. Until then, every routine will be research-only.
- Strategy initialization (strategy.md) was completed from web research alone.
  The inception portfolio equity baseline could not be confirmed from live data;
  assumed Alpaca paper default of $100,000. Confirm and correct on the first
  successful account fetch.
- SPY benchmark anchor set to ~$738 (May 18 2026 close) — confirm this against
  live data on the next routine.
