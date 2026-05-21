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

- **2026-05-21 inception:** 2026 is a sector-rotation year. Energy (+22% YTD),
  Industrials (+16%), Consumer Staples (+13%) are leading SPY. Start cautiously:
  3 positions on Day 1, stay well within 25% daily deployment cap, keep ~75%
  cash to deploy gradually over coming weeks. Build conviction before sizing up.
- **2026-05-21:** Energy plays (CVX/XOM) carry geopolitical reversal risk —
  oil premium from Iran conflict could unwind fast. Size accordingly and watch
  the Middle East tape daily in pre-market.
- **2026-05-21:** CAT already up 57% YTD — avoid chasing extended names on
  inception day. Better to wait for a pullback or use future position slots.
