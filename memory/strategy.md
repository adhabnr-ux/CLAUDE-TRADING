# Trading Strategy

**STATUS: ACTIVE**
**Initialized:** 2026-05-21

---

## Thesis

The S&P 500 is at all-time highs on the back of 15–28% YoY earnings growth and
a stable Fed (funds rate 3.5–3.75%, on hold). Real GDP grew 2% in Q1 2026.
Valuation is stretched (forward P/E ~20.9x vs. 18.9 ten-year avg), so selective
stock picking—not closet indexing—is required to beat SPY.

Three durable tailwinds drive our edge:
1. **AI infrastructure spend** — hyperscaler capex is still accelerating.
   Semiconductor equipment, networking chips, and enterprise software with deep
   AI integration are structural winners.
2. **Real-economy rotation** — investors are broadening beyond pure AI plays
   into industrials, energy, and consumer defensives that benefit indirectly
   from the AI buildout and cost-conscious spending.
3. **Healthcare secular growth** — GLP-1 drug demand plus aging demographics
   create durable revenue streams; several names trade at reasonable valuations
   despite strong earnings momentum.

We stay fully in US large/mid-cap equities (no options, no penny stocks, no
margin, no crypto, no shorting). We try to beat SPY through selective, high-
conviction positions—not volume of trades.

---

## Universe

- US-listed stocks, market cap ≥ $5 B, price ≥ $5.
- Liquid names: average daily volume ≥ 500 K shares.
- Broad ETFs are eligible as defensive placeholders, but we prefer individual
  stocks for alpha.
- All guardrails in CLAUDE.md must be respected at all times.

---

## Entry Signals

Open a new position only when **at least two** of these apply:
1. Strong recent earnings momentum: beat + raise or analyst upgrades.
2. Clear catalyst in the next 1–6 months (product launch, new contract, sector
   re-rating, earnings).
3. Reasonable valuation — PEG ratio < 2.5, or at a discount vs. peers on
   NTM P/E or EV/FCF.
4. Technical confirmation: stock is above its 50-day moving average and not
   extended > 10% above it (avoid chasing blow-off moves).
5. Macro tailwind: sector trend is intact and no major contrary catalyst looms.

Write a thesis sentence before every buy. If you can't write one, don't trade.

**Technical-gate discipline:** Do not invent volatility/ATR "gates" or cooldown
periods beyond what's written here. If a name needs to cool off after a
stop-out, cap it at **2 weeks**, not 4+. If waiting for lower volatility before
entry, cap it at **2 consecutive sessions** of a reasonable ATR (≤5% of price),
not 3+ sessions at a stricter threshold. A day with no trades is fine; a name
sitting in self-imposed purgatory for weeks on end is not the intent of this
strategy — this is a swing strategy, not a wait-for-perfection strategy.

---

## Sizing

| Conviction | Starting size | Max scale-up |
|------------|---------------|--------------|
| Starter    | 7–9% of portfolio | Stay ≤ 20% |
| High       | 10–12% of portfolio | Stay ≤ 20% |

- Never enter at > 15% in a single order.
- Scale up only after an initial position confirms (holds above entry, catalyst
  progressing, no thesis breaks).
- Hard cap: 20% per position (CLAUDE.md).

---

## Exit Signals

In priority order:
1. **Trailing stop triggers** (10% trailing stop, placed immediately after entry).
2. **−7% rule** (close at midday if position is more than 7% below entry).
3. **Thesis break** — miss + lower guidance, key catalyst fails, or sector
   reversal. Exit within one session.
4. **Valuation stretched** — position has re-rated to > 35× NTM P/E with no new
   catalyst and is now > 25% of portfolio mark-to-market (trim to 20%).
5. **Macro deterioration** — Fed pivot to hikes, recession signals, or major
   geopolitical shock that reverses risk appetite.
6. **Earnings gap-down override:** If a held stock gaps down >8% on earnings,
   do NOT execute a pre-planned scale-up even if the literal trigger conditions
   are met. The market's verdict overrides a pre-stated formula. Exit gracefully
   via trailing stop. Never add to a falling knife on a gap-down earnings day.
   _(Lesson from AVGO Jun 4 2026: scale-up plan had two technical conditions
   met, but a −15% gap is unambiguously negative market confirmation.)_

Do NOT sell on day-to-day noise. Sell on thesis changes.

---

## Cash Policy

- **Hard minimum:** 5% cash at all times (CLAUDE.md).
- **Target:** 25–40% cash until the portfolio has 6–8 positions; then 10–20%.
- **Build steadily:** max 25% of portfolio in new buys per day.
- **Raise cash** if broad market VIX spikes above 35 or if we have > 3
  positions down more than 5% simultaneously.

---

## Watchlist

_Watchlist hygiene (updated 2026-06-26 weekly review): entries require date added + catalyst with expiry. Stale entries (4+ weeks, catalyst expired) purged. NVDA removed after second stop-out + GPU spot compression. LRCX gate fully reset. ETN added as AI power infrastructure candidate._

| Ticker | Sector | Date Added | One-line reason | Catalyst Expiry |
|--------|--------|------------|-----------------|-----------------|
| LLY    | Healthcare | 2026-05-22 | **HELD** 10sh @ $1,093.53 — GLP-1 dominance; Medicare Bridge July 1 confirmed (USD 50/month, ~20M Medicare patients); Leerink PT $1,232; LLY +11.11% from entry | Review by July 1 — MANDATORY pre-mkt June 30 hold/trim/exit decision |
| V      | Financials | 2026-06-10 | **HELD** 22sh @ $323.57 — payments infrastructure; OpenAI partnership; stablecoin capabilities; showing defensive strength in AI selloff | Review by July 28 (earnings Q3 FY26) |
| VST    | Energy / Utilities | 2026-06-09 | **HELD** 40sh @ $148.81 — nuclear operator; Helix Digital Infrastructure (KKR+NVDA preferred power partner); +9.78% from entry; 5% trail; stop buffer 1.86% CRITICAL ⚠️⚠️ | Review by July 7 |
| ETN    | Industrials / AI Power | 2026-06-26 | Eaton electrical equipment — direct critical-path input to hyperscale data centers scaling with AI GPU density; AGGRO added June 25 at $419.54; +42% analyst PT upside | Gate loosened per 2026-07-01 strategy update: need 2 consecutive ≤5% ATR sessions, re-check from July 1; catalyst: AI capex supercycle, ongoing |
| LRCX   | Semi Equipment | 2026-06-08 | AI fab investment wave; Citi PT raised to $450 (from $315); ATR gate reset by June 26 selloff | Gate loosened per 2026-07-01 strategy update: need 2 consecutive ≤5% ATR sessions (was 3×≤3%), re-check from July 1; catalyst: AI equipment cycle, no hard expiry |
| MSFT   | Tech / Enterprise AI | 2026-05-22 | Azure AI platform compounding; stop-outs June 5; re-evaluate when PCE trend reverses or stock re-bases cleanly; July 23 earnings next catalyst | Re-evaluate July 23+ (earnings); not near-term |
| COST   | Consumer Defensive | 2026-05-29 | Membership model loyalty; defensive in high-PCE environment; Q4 earnings mid-August | Re-evaluate July+ (pre-earnings) |
| PWR    | Industrials | 2026-06-12 | Quanta Services; grid/data-center infrastructure buildout; Q1 EPS +31.4% beat; PT upgrades TD Cowen $775 / Citi $837; ATR elevated + insider selling $123M flag; P/E ~95 | Re-evaluate late July; needs ATR normalization + insider selling to abate |
| JNJ    | Healthcare | 2026-05-22 | Defensive quality compounder; resilient earnings; reasonable valuation; inflation-resistant | Ongoing; no hard expiry |
| WMT    | Consumer Defensive | 2026-05-22 | Market-share gains from cost-conscious consumer; AI supply-chain edge; defensive in inflation environment | Ongoing; no hard expiry |

_Purged from watchlist (2026-06-26 weekly review):_
- **NVDA:** REMOVED — second trailing stop in 5 weeks (June 5: −3.36%; June 25: −9.78%). GPU B200 hourly spot price −31% in 3 weeks ($6.11→$4.22) is a fundamental margin-pressure concern. Re-add only when: (a) GPU spot prices recover above $5.50/hr OR (b) confirmed major new hyperscaler deployment catalyst; cooling period capped at 2 weeks from June 25 per 2026-07-01 strategy update (was 4 weeks) — re-eligible July 9.

_Previously purged (still excluded):_
- **AVBO:** Trailing stop gap-fill June 4 (−2.10%). Re-evaluate 4+ weeks post-gap digestion (earliest late July).
- **AMZN:** Closed June 3 per −7% rule (−7.39%). EU regulatory headwinds ongoing.
- **META:** Closed June 10 per trailing stop (−6.87%). Re-evaluate when PCE trend reverses and stock re-bases above $620.
- **XOM:** No specific near-term catalyst; energy sector stable but no alpha driver.
- **UNH:** Regulatory overhang; re-evaluate monthly review.

---

## Benchmarking

- Benchmark: SPY total return.
- Inception SPY price (2026-05-21): $739.44.
- Measure performance weekly (Friday review) and monthly.
- If we lag SPY by > 5% over any rolling 4-week window, review and adjust
  sector weights and position theses before adding new names.

## Active Macro Watches (updated 2026-06-26 weekly review)

- **FOMC June 16–17 2026 — COMPLETED HAWKISH (finalized):** Rate hold (3.50–3.75%); dot plot: median 3.8% year-end, 9/18 members projecting hike. Next FOMC: est. late July 2026.
- **PCE inflation 4.1% YoY (June 25) — NEW HAWKISH SIGNAL:** Highest since April 2023. Kevin Warsh hawkish comments. Reinforces higher-for-longer rate regime. 10yr yield ~4.44-4.49% range — **BELOW 4.75% trigger ✓**. Monitor; if closes above 4.75%, halt all new buys.
- **Iran/US peace deal — holding (60-day agreement from June 18):** Strait of Hormuz open; WTI ~$80/bbl ✓. Peace deal expiry ~August 17 — monitor.
- **AI/tech selloff week of June 23-26:** OpenAI IPO delay + valuation concerns drove Nasdaq −4%+. Chip names hardest hit. LRCX ATR gate fully reset. Sector rotation into healthcare, industrials, defensives favors current Bull portfolio.
- **SPY ex-dividend June 18 — APPLIED:** $1.76/sh. Total-return benchmark anchor: **$741.20**. Next SPY ex-div est. ~September 2026.
- **LLY — position:** June 26 close $1,215.00 (+11.11% from entry). HWM $1,215.76 / stop $1,094.18. **Medicare Bridge July 1 TOMORROW** — **MANDATORY HOLD/TRIM/EXIT DECISION AT PRE-MARKET JUNE 30.** Buffer 9.69% excellent. Review_by July 1.
- **V — position:** June 26 close $336.00 (+3.84% from entry). HWM $339.94 / stop $305.95. Thesis intact; defensive strength in AI selloff. Review_by July 28 (Q3 FY26 earnings).
- **VST — position:** June 26 close $163.75 (+9.78% from entry). 5% trail HWM $168.77 / stop $160.33. **BUFFER 1.86% CRITICAL ⚠️⚠️** — stop may fire Monday open if VST gaps down. Thesis intact. Review_by July 7.
- **NVDA — REMOVED FROM WATCHLIST:** Second stop-out June 25 (−9.78%). GPU spot compression not resolved. Minimum 4-week cooling period.
- **LRCX — ATR GATE FULLY RESET:** −10%+ on June 26. Fresh 3 consecutive ≤3% sessions needed from June 29. June 29 ATR 8.76% = session 1/3 FAILS; gate counter 0/3. **Earliest entry July 9+**.
- **ETN — NEW WATCHLIST ADDITION:** AGGRO added June 25 at $419.54. AI power infrastructure. ATR elevated post-selloff. Earliest entry week of July 7+.
- **GOOGL Dow Jones inclusion — effective June 29 (Monday):** Positive for passive flows; watch for momentum.

## Monday Conviction Ratings (updated 2026-06-29 pre-market)

| Symbol | Rating | 3-consecutive-C trigger | Notes |
|--------|--------|------------------------|-------|
| LLY | **A** | N/A | +12.48% from entry; AT Leerink PT $1,232; Medicare Bridge launches July 1 TOMORROW; stop buffer 11.05% healthy; HOLD decision made; review_by 2026-07-07 |
| V | **B** | 0/3 weeks at C | +4.07% from entry; thesis intact; defensive strength in AI selloff; July 28 earnings gate; review_by 2026-07-28 |
| VST | **A** | N/A | +10.20% from entry; Helix+Cogentrix intact; 5% trail; stop buffer 2.23% CRITICAL ⚠️⚠️ — improved from 1.86% Friday but still narrow; thesis conviction unchanged; review_by 2026-07-07; earnings Aug 6 |
