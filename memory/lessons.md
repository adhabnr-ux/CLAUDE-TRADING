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

- **2026-05-20 (inception):** Energy sector (XOM -3.9%, CVX -3.0%, COP -2.2%) had a broad
  selloff even while the broader market (SPY +1.0%) recovered. Do not enter a sector on
  a day when the whole sector is in a bearish reversal — wait for at least one stabilizing
  session before entering.
- **2026-05-20 (inception):** GE Aerospace (+5.2%) and AMD (+8.1%) had single-day outsized
  moves. Never chase a stock up >4% on the same day — wait for consolidation. There will
  always be another entry.
- **2026-05-20 (inception):** Starting with 2 positions (~17% of portfolio) in week 1 is
  appropriate. Rising yields and stretched valuations argue for caution; deploying 25% on
  day 1 would be overaggressive for a fresh account.
