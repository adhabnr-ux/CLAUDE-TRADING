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

### 2026-05-20 — Credential env vars present but empty

All five credential env vars (`ALPACA_API_KEY_ID`, `ALPACA_API_SECRET_KEY`,
`ALPACA_BASE_URL`, `CALLMEBOT_PHONE`, `CALLMEBOT_APIKEY`) were visible in the
environment but had zero-length values. `env | grep ALPACA` showed them as
existing keys; `printenv` and `awk length()` confirmed empty values. The
cloud environment provisioned the variable *names* but not the *secrets*.
Alpaca and CallMeBot calls both fail. Action taken: stop, no orders placed,
documented here. The human must populate these secrets in the environment
configuration before any routine can function.
