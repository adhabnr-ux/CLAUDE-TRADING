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

- **2026-05-21 (first run):** On strategy initialization, geopolitical headlines caused XOM/CVX to drop ~3% on May 20 (Trump/Iran comments). This is the kind of noise to distinguish from fundamental thesis breaks — the Strait of Hormuz physical disruption was still ongoing; a diplomatic comment is not a resolved deal. Identified it as a potential entry opportunity rather than a sell signal. Watch: if an actual Iran deal is signed and Hormuz traffic normalizes, the energy thesis weakens and position should be reassessed.
- **2026-05-21 (first run):** UNH has strong fundamentals (beat + raised guidance, analysts PT $420–440) but an active DOJ criminal + civil investigation. Chose not to open a position until the investigation situation clarifies. Avoiding potential-headline risk on a day-1 position is prudent — thesis is not broken, just incomplete.
- **2026-05-21 (first run):** HWM at 54× fwd PE is a momentum play more than a value play. Strong growth (19% revenue YoY) partially justifies the premium, but not appropriate as a starter position. Add to watchlist for entry on a pullback to <45× fwd PE or after a sector consolidation.
