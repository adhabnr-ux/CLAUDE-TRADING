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

- **2026-05-21:** Market-open ran before pre-market on the very first run. No pre-market plan existed (strategy.md STATUS: NOT_INITIALIZED, research-log.md empty). Correct action: place no trades, update portfolio snapshot, notify, commit. Pre-market must run first to initialize strategy and produce a trade plan.
