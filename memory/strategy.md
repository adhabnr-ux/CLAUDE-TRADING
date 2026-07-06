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

_Watchlist hygiene (updated 2026-07-06 pre-market): entries require date added + catalyst with expiry. Stale entries (4+ weeks, catalyst expired) purged. LRCX and ETN failed their ATR gates yet again July 2 (LRCX 14.11%, catastrophic; ETN 5.52%, narrow) — both gate counters reset to 0/2. LRCX hits the 4-week staleness line ~July 8 — purge at Friday's weekly review if still ungated. Per the 2026-07-03 directive to widen beyond semis, four new non-semi research candidates sourced 2026-07-06: CEG, VRT, NVT, MOD (see below) — none yet diligenced, watchlist-only until a full pre-trade checklist pass._

| Ticker | Sector | Date Added | One-line reason | Catalyst Expiry |
|--------|--------|------------|-----------------|-----------------|
| LLY    | Healthcare | 2026-05-22 | **HELD** 10sh @ $1,093.53 — GLP-1 dominance; Medicare Bridge live since July 1 (USD 50/month, ~20M Medicare patients); Leerink PT $1,232; +10.38% from entry | Review by July 7 (tomorrow) — mandatory decision due; thesis intact as of July 6 pre-market |
| V      | Financials | 2026-06-10 | **HELD** 22sh @ $323.57 — payments infrastructure; OpenAI partnership; Open USD stablecoin consortium (140+ partners); zero sell ratings among 42 analysts; +11.64% from entry | Review by July 28 (earnings ~July 28–Aug 4) |
| VST    | Energy / Utilities | 2026-06-09 (closed 2026-06-30, WIN +7.66%) | **NOT HELD** — pulled back to ~$151–153 (below the $160.20 exit); Wells Fargo Buy July 3; but NEW: FERC colocation-deal scrutiny risk + June 25 technical sell signal + insider selling — fails technical-confirmation entry signal, not a falling-knife buy | Not eligible today — needs a confirmed bottom (reversal + volume) and FERC-risk clarity before re-entry; re-check ATR/technicals each pre-market |
| ETN    | Industrials / AI Power | 2026-06-26 | Eaton electrical equipment — direct critical-path input to hyperscale data centers; BMO Buy July 2; FY26 guidance raised (EPS est. $3.07, +4.07% YoY) | July 2 ATR 5.52% — fails ≤5% gate narrowly again; counter reset to 0/2 as of July 6 pre-market |
| LRCX   | Semi Equipment | 2026-06-08 | AI fab investment wave; Cantor PT $500, Susquehanna $475 (June 29); but July 2 ATR 14.11% — catastrophic single-day fail (−10.2%) on AI-capex demand-destruction fears | Counter reset to 0/2 as of July 6 pre-market; **hits 4-week staleness line ~July 8 — purge candidate at Friday's weekly review if still ungated** |
| CEG    | Utilities / Nuclear | 2026-07-06 | NEW — Constellation Energy; nuclear power, Microsoft Three Mile Island restart PPA; premium pricing power as AI demand grows; July 2 ATR 3.00% ✓ clears gate | Research-only — needs full pre-trade diligence pass (10-K, valuation, thesis) before any entry consideration |
| VRT    | Industrials / AI Cooling | 2026-07-06 | NEW — Vertiv; full power+cooling stack, deep NVIDIA integration; orders +252%, ~USD 13.5B 2026 revenue guide (+28%) | Research-only — needs full pre-trade diligence pass before any entry consideration |
| NVT    | Industrials / AI Cooling | 2026-07-06 | NEW — nVent Electric; liquid cooling distribution + high-density power distribution units; organic orders +65% | Research-only — needs full pre-trade diligence pass before any entry consideration |
| MOD    | Industrials / AI Cooling | 2026-07-06 | NEW — Modine Manufacturing; refocusing around data-center thermal management; Performance Technologies RMT spin-off expected Q4 2026 | Research-only — needs full pre-trade diligence pass before any entry consideration |
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

## Active Macro Watches (updated 2026-07-06 pre-market)

- **FOMC June 16–17 2026 — COMPLETED HAWKISH (finalized):** Rate hold (3.50–3.75%); dot plot: median 3.8% year-end, 9/18 members projecting hike. Next FOMC: est. late July 2026.
- **PCE inflation 4.1% YoY (June 25):** Highest since April 2023. Reinforces higher-for-longer rate regime. 10yr yield last read 4.47-4.49% — **BELOW 4.75% trigger ✓**. Monitor; if closes above 4.75%, halt all new buys.
- **Soft June jobs report (July 3):** Nonfarm payrolls +57K vs +113K expected — reinforces no-hike expectations, broadly supportive backdrop into the week.
- **Iran/US peace deal — holding (60-day agreement from June 18):** Strait of Hormuz open; WTI ~$80/bbl ✓. Peace deal expiry ~August 17 — monitor.
- **SPY ex-dividend June 18 — APPLIED:** $1.76/sh. Total-return benchmark anchor: **$741.20**. Next SPY ex-div est. ~September 2026.
- **LLY — position:** July 6 pre-market $1,207.05 (+10.38% from entry). HWM $1,238.00 / stop $1,114.20, buffer 7.69%. Review_by **tomorrow, 2026-07-07** — mandatory decision due. Conviction A.
- **V — position:** July 6 pre-market $361.225 (+11.64% from entry). HWM $361.86 / stop $325.674, buffer 9.84%. Thesis intact; zero sell ratings among 42 analysts. Review_by 2026-07-28. Conviction B.
- **VST — re-entry review:** Pulled back to ~$151–153 (below the $160.20 exit); NEW FERC colocation-deal regulatory risk + June 25 technical sell signal + insider selling. Fails technical-confirmation entry signal — not eligible today.
- **NVDA — REMOVED FROM WATCHLIST:** Cooling period from the June 25 stop-out — re-eligible July 9 (3 days away).
- **LRCX — ATR gate:** July 2 14.11% (catastrophic fail). Gate counter 0/2. Hits 4-week staleness line ~July 8 — purge candidate at Friday's weekly review if still ungated.
- **ETN — ATR gate:** July 2 5.52% — fails narrowly again. Gate counter reset to 0/2.
- **New candidates sourced 2026-07-06:** CEG, VRT, NVT, MOD — research-only, no diligence done yet.

## Weekly review summary (2026-07-03)

Week 7 (Jun 29–Jul 3): Bull +0.42% vs SPY +2.18% = lagged −1.75pp (pure cash drag on SPY's best week since inception). Since inception: Bull +0.13% vs SPY TR +0.97% = trails −0.84pp (was leading +0.88pp last week). First win banked (VST +7.66%, Jun 30) — win rate now 1/7 (14.3%), profit factor 0.192. Grade: B−. 4th consecutive week of 0 new positions — see Watchlist note above for the pipeline fix. Full detail in `weekly-review.md`.

## Monday Conviction Ratings (last set 2026-07-06 pre-market; next refresh Monday 2026-07-13)

| Symbol | Rating | 3-consecutive-C trigger | Notes |
|--------|--------|------------------------|-------|
| LLY | **A** (unchanged) | N/A | +10.38% from entry; Medicare Bridge confirming; stop buffer 7.69%; review_by tomorrow 2026-07-07 |
| V | **B** (unchanged) | 0/3 weeks at C | +11.64% from entry; thesis intact; zero sell ratings among 42 analysts; review_by 2026-07-28 |
