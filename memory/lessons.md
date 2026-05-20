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
- The Alpaca free-tier data subscription does not allow querying historical SIP data; use the IEX feed for bar data (`?feed=iex`) or rely on the default `bars` command. For broader historical price data, use WebSearch/WebFetch to query financial sites.

## Trading lessons

### 2026-05-20 — Inception week

- **Don't chase post-earnings gaps.** NVDA beat every metric and guided above consensus ($91B Q2), yet the stock slid after-hours. The earnings beat was already priced in. Lesson: after a major earnings beat, wait 1–2 trading days for the market to digest before evaluating entry; the immediate post-earnings reaction often reverses.

- **Rising Treasury yields are the primary equity headwind right now.** The 10Y hit a 16-month high (4.69%) and the 30Y hit an 18-year high (5.20%) this week, causing three consecutive days of S&P 500 declines. Avoid adding new positions on days when Treasury yields are spiking; rate-sensitive sectors (REITs, utilities, long-duration growth) will get hit hardest.

- **Holding cash during a choppy tape is a valid trade.** The S&P 500 fell Mon–Tue on yield anxiety, then bounced Wed. By staying in cash, we avoided the drawdown and preserved 100% capital. A day (or week) with no trades can be the right call.

- **System initialization must happen in sequence.** strategy.md was NOT_INITIALIZED when the first weekly review ran — this is a process gap. The correct order is: pre-market → market-open → midday → close → weekly-review. Subsequent routines depend on the strategy and portfolio snapshot being written by earlier routines.

- **Q1 2026 earnings season was exceptionally strong** (84% beat rate, +28% YoY EPS, record 13.4% net margins). This does not automatically justify buying everything — much of the good news is already priced in at a 20.9x forward P/E. Look for names that beat AND were not priced for perfection.
