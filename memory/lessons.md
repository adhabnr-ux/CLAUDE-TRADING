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

- **2026-05-20:** Midday routine aborted — `ALPACA_API_KEY_ID` and `ALPACA_API_SECRET_KEY` were not injected into the cloud environment. Check environment variable configuration before scheduling any routine. The strategy is also uninitialized (pre-market has never run), so the first successful run must be pre-market to set up strategy.md and portfolio.md.
