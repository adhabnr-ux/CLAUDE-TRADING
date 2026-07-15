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
   extended > 10% above it (avoid chasing blow-off moves). **A close must be
   at least 0.5% above the 50-day MA to count as "above" it** — a same-day
   noise-level crossing (e.g. +0.05%) does not confirm. This is the one
   fixed number for this signal; do not tighten it further ad hoc per name
   (codified 2026-07-10 after ETN sat in noise-level-crossing limbo for two
   sessions with no written threshold to apply).
5. Macro tailwind: sector trend is intact and no major contrary catalyst looms.

Write a thesis sentence before every buy. If you can't write one, don't trade.

**Pullback-watch protocol (added 2026-07-10):** when a candidate passes
signals #1, #2, #3, and #5 but fails only #4 (technical/extension), log an
explicit pullback target price (its 50-day MA at diligence time) in the
watchlist row instead of re-running a full diligence pass every session.
Future pre-markets just check the live price against the stored target;
promote to a buy candidate automatically once price reaches it, provided the
other signals still hold (re-verify #1/#2/#3/#5 briefly, not from scratch).
This was added after six consecutive diligenced names (LRCX, ETN, CEG, VRT,
NVT, ABBV) all failed only the technical-extension gate — the pipeline is
finding real theses, just too late in their run-up.

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

_Watchlist hygiene (updated 2026-07-15 pre-market): entries require date added + catalyst with expiry. Stale entries (4+ weeks, catalyst expired) purged. **ETN PROMOTED 2026-07-15** — July 14 close $415.65 cleared its 50-day MA ($405.09) by +2.606%, clearing both the 0.5%-minimum-separation floor and the 10%-extension ceiling for the first time since diligence began; ATR 2.967% (under the 3% halved-sizing threshold); signals #1/#2/#3/#5 re-verified (Q1 2026 record sales $7.5B +17% YoY, AI-data-center power-infrastructure catalyst intact, 25-analyst Buy consensus mean PT $455.79, industrials/AI-capex macro tailwind intact); earnings confirmed July 31 (outside 2-day window). Buy plan written for today's market-open — see research-log.md. **CAT held since 2026-07-13** (see row below). **MOD diligenced 2026-07-14 — NOT PROMOTED** (fails technical −13.02% below 50-day MA and the hard ATR gate 5.42%; genuine RMT spin-off completion risk). **COST received its first-ever full pre-trade diligence pass 2026-07-15** — fundamentals pass (Q3 beat: sales +11.6%, comp sales +9.8%, membership fee income +10.7%) but FAILS valuation (P/E ~47-49x vs. its own 10-yr avg ~39x and peer low-20s multiples — no discount, no PEG relief at this multiple) and FAILS technical confirmation (−6.158% below 50-day MA); no fresh near-term catalyst (next earnings confirmed Sept 24, 2026, not "mid-August" as previously logged — corrected). Not promoted. CEG/VRT/NVT re-checked 2026-07-15: CEG 50-day MA $271.27 vs July 14 close $256.41 = −5.476% below (was −5.44% July 14); VRT 50-day MA $324.23 vs close $303.67 = −6.342% below (worse than −5.84% July 14); NVT 50-day MA $166.01 vs close $161.80 = −2.537% below (improved from −4.61% July 14). None reclaimed their 50-day MA; no promotions.

| Ticker | Sector | Date Added | One-line reason | Catalyst Expiry |
|--------|--------|------------|-----------------|-----------------|
| LLY    | Healthcare | 2026-05-22 | **HELD** 10sh @ $1,093.53 — GLP-1 dominance; Medicare Bridge live since July 1 (USD 50/month, ~20M Medicare patients); FDA PreCheck pilot selection (new July 7); Leerink PT $1,232; +11.66% from entry | Review by 2026-07-21 (renewed 2026-07-07 — HOLD decision, thesis intact) |
| V      | Financials | 2026-06-10 | **HELD** 22sh @ $323.57 — payments infrastructure; OpenAI partnership; Open USD stablecoin consortium (140+ partners); zero sell ratings among 42 analysts; +7.82% from entry (pulled back from +11.64% on July 6 profit-taking/sector rotation, not thesis-related) | Review by July 28 (earnings) |
| VST    | Energy / Utilities | 2026-06-09 (closed 2026-06-30, WIN +7.66%) | **NOT HELD** — pulled back to ~$151–153 (below the $160.20 exit); Wells Fargo Buy July 3; but NEW: FERC colocation-deal scrutiny risk + June 25 technical sell signal + insider selling — fails technical-confirmation entry signal, not a falling-knife buy | Not eligible today — needs a confirmed bottom (reversal + volume) and FERC-risk clarity before re-entry; re-check ATR/technicals each pre-market |
| ETN    | Industrials / AI Power | 2026-06-26 | Eaton electrical equipment — direct critical-path input to hyperscale data centers; Q1 2026 record sales $7.5B (+17% YoY), adj EPS $2.81 record; 25-analyst Buy consensus, mean PT $455.79 (+13.5% upside) | **PROMOTED 2026-07-15** — July 14 close $415.65 is +2.606% above its 50-day MA ($405.09), clearing the 0.5% separation floor and the 10% extension ceiling; ATR 2.967% (under the 3% halving threshold). Earnings confirmed July 31, 2026 (outside 2-day window). Buy plan written for 2026-07-15 market-open. |
| CEG    | Utilities / Nuclear | 2026-07-06 | Constellation Energy; nuclear power, Microsoft Three Mile Island restart PPA; premium pricing power as AI demand grows; **full diligence pass 2026-07-07: Q1 beat (EPS $4.49), FY26 guide affirmed, PEG 1.19, analyst consensus Buy — but FAILS technical confirmation (11.55% below 50-day MA, confirmed downtrend since July 1-2 selloff)** | Not eligible — needs to reclaim 50-day MA or show a clear reversal/basing pattern before re-consideration |
| VRT    | Industrials / AI Cooling | 2026-07-06 | Vertiv; full power+cooling stack, deep NVIDIA integration; **full diligence pass 2026-07-08: FY26 guide raised to USD13.5-14.0B (+30% organic), backlog >USD15B, PEG 1.36, ROE 45.1%/ROIC 32.1%, healthy balance sheet (current ratio 1.49, D/E 0.77) — but FAILS technical confirmation (~6.1% below approx 50-day MA, USD305.625 vs ~USD325.37) AND the ATR gate (6.15% July 7, above 5% cap)** | Not eligible — needs to reclaim 50-day MA and post 2 consecutive ATR-gate-clearing sessions (≤5%) before re-consideration |
| NVT    | Industrials / AI Cooling | 2026-07-06 | nVent Electric; liquid cooling distribution + high-density power distribution units; **full diligence pass 2026-07-09: FY26 adj. EPS guide raised to USD 4.45-4.55, backlog USD 2.6B, PEG 1.18, D/E 43.9%, interest coverage 6.7x — passes fundamentals/valuation/ATR gate (3.015%) but FAILS technical confirmation (−5.82% below ~50-day MA of USD 164.44)** | Not eligible — needs to reclaim its 50-day MA before re-consideration |
| MOD    | Industrials / AI Cooling | 2026-07-06 | Modine Manufacturing; **full diligence pass 2026-07-14: NOT PROMOTED.** FY26 record year (Q4 net sales +47% YoY, data-center sales +78%, USD 4B hyperscale capacity agreement), FY27 guide net sales +20-35% — fundamentals genuinely strong. But fails technical confirmation (−13.02% below 50-day MA) and the hard ATR gate (5.42% > 5% cap) | Not eligible — needs ATR back under 5% for consecutive sessions, price to stabilize/reclaim the 50-day MA, and concrete progress on the Gentherm RMT deal's approval conditions (Gentherm shareholder vote, regulatory clearance, IRS tax opinion) before re-consideration |
| ABBV   | Healthcare | 2026-07-09 | AbbVie; 52-week high July 2 on 340B drug-pricing reform tailwind (shifts margin to drug developers from hospitals); USD 10.9B Apogee Therapeutics acquisition expands immunology pipeline | **Full diligence pass 2026-07-10: Q1 beat (EPS 2.65 vs 2.59 est., rev 15.0B vs 14.72B est.), 340B/Apogee catalysts real and advancing, PEG 0.41-0.91 (cheap vs LLY/JNJ/MRK) — but FAILS entry signal #4 (extended +13% above ~50-day MA of ~$222, over the 10% not-extended gate) and FY26 EPS guidance was trimmed to 13.91-14.11 (below the 14.25 Street consensus) on July 9, one day before this review — undercuts the beat+raise signal; interest coverage ~3.33x is also weak vs. healthcare peers.** Not promoted — needs to pull back toward its 50-day MA; guidance figures need primary-source (AbbVie IR) verification before re-consideration |
| CAT    | Industrials | 2026-07-09 | Caterpillar; Q1 beat/raise (rev USD 17.42B, adj. EPS USD 5.50, +20% vs. est), FY26/FY27 estimates revised up (Zacks: +29.4%/+24.4% YoY), dividend hiked 8%, Zacks Rank #1; July 7 Skycatch acquisition (AI-powered mining digital-twin tech) + American Intelligence & Power 2GW hyperscale-AI power alliance extend the AI-infrastructure angle; headwind: USD 2.2-2.4B 2026 tariff costs compressing Resource Industries margins ~500bp | **Full diligence pass 2026-07-13: PROMOTED to buy candidate.** 5/5 entry signals clear — earnings momentum (Q1 beat), catalyst (Skycatch + AI-power alliance), valuation (PEG ~1.27-1.6, under the 2.5 gate, though P/E 46-47x trailing is a premium vs. peer avg ~31.2x/industry ~26.5x — passes via PEG only, not peer-discount), technical (50-day MA USD 925.64, July 10 close USD 951.67 = +2.81% above, clears both the 10% extension ceiling and the 0.5% separation floor), macro (industrials/AI-capex tailwind, XLI +12.5% YTD). ATR 3.219% (20-day) is just over the 3% halved-sizing threshold — sized at half a starter position. Caveats: stock +167% over 52 weeks near highs, high beta (1.60), one analyst source flags ~18% overvaluation risk post-Skycatch, insider selling ongoing (Group President sold ~12.6K sh in May, no July Form 4 found yet). Next earnings confirmed Aug 4, 2026 (outside 2-day window). See today's research-log entry and trade-log for the executed plan. |
| MSFT   | Tech / Enterprise AI | 2026-05-22 | Azure AI platform compounding; stop-outs June 5; re-evaluate when PCE trend reverses or stock re-bases cleanly; July 23 earnings next catalyst | Re-evaluate July 23+ (earnings); not near-term |
| COST   | Consumer Defensive | 2026-05-29 | Membership model loyalty; defensive in high-PCE environment; Q3 beat May 28 (sales +11.6%, comp sales +9.8%, membership fee income +10.7%) | **Full diligence pass 2026-07-15: NOT PROMOTED.** Fundamentals genuinely strong but FAILS valuation (P/E ~47-49x vs. 10-yr avg ~39x and peer low-20s multiples, no PEG relief) and FAILS technical confirmation (−6.158% below 50-day MA). Next earnings confirmed Sept 24, 2026 (corrected from prior "mid-August" estimate). Not eligible — needs valuation to compress toward historical range and price to reclaim the 50-day MA. |
| PWR    | Industrials | 2026-06-12 | Quanta Services; grid/data-center infrastructure buildout; Q1 EPS +31.4% beat; PT upgrades TD Cowen $775 / Citi $837; ATR elevated + insider selling $123M flag; P/E ~95 | Re-evaluate late July; needs ATR normalization + insider selling to abate |
| JNJ    | Healthcare | 2026-05-22 | Defensive quality compounder; resilient earnings; reasonable valuation; inflation-resistant | Ongoing; no hard expiry |
| WMT    | Consumer Defensive | 2026-05-22 | Market-share gains from cost-conscious consumer; AI supply-chain edge; defensive in inflation environment | Ongoing; no hard expiry |

_Purged from watchlist (2026-07-10 weekly review):_
- **LRCX:** REMOVED — added 2026-06-08, hit the 4-week watchlist-staleness line without ever clearing its entry gate. Failed its ATR gate 3+ times, most recently July 9 (5.466%) on a chase-y analyst-PT-hike pop (TD Cowen $340→$400, Mizuho $380→$400), not fresh fundamentals — LRCX was already ~56% above its 200-day MA before that move. CEO Timothy Archer sold ~USD11.7M stock July 2. Fundamental AI-fab-investment thesis is not broken, but re-entry needs a fresh diligence pass and a genuinely calm technical setup, not an automatic re-add.

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

## Active Macro Watches (updated 2026-07-15 pre-market)

- **July 15 pre-market:** S&P 500 futures +0.18% on cooling inflation (July-hike odds fell to 17% from 42%) ahead of today's PPI print; PayPal +on ~USD53B takeover-offer reports; chip stocks broadly higher. 10yr yield 4.57% (below the 4.75% halt trigger); WTI ~USD79.64-80.58/bbl (below the USD100 halt trigger) despite ongoing Strait-of-Hormuz tension. Neither macro halt trigger close to tripping. Risk-on, constructive tape.
- **CAT — position:** July 15 pre-market USD936.80 (−0.839% from entry). FY2026 revenue outlook raised (low double-digit growth); record USD63B backlog; Power and Energy segment +41% on hyperscaler AI-data-center capex — thesis-confirming, not new since the July 13 diligence. Valuation debate (P/E ~38x vs 5-yr avg 19x; Michael Burry short, already known since July 1) unchanged. Ex-div July 20 (USD1.63/sh). review_by 2026-08-03 not due. HOLD.
- **LLY — position:** July 15 pre-market USD1,152.58 (+5.400% from entry, down from +8.09% July 13 peak). July 14 close was −3.10% on sector-wide rotation out of high-multiple metabolic-health/growth names into cyclicals — not company-specific, no thesis break. Bernstein PT raised to USD1,385, UBS to USD1,425, Guggenheim to USD1,273 (all positive, all recent). Stop buffer wide (HWM USD1,249.45, stop USD1,124.505). review_by 2026-07-21 not due. HOLD. Conviction A.
- **V — position:** July 15 pre-market USD355.51 (+9.871% from entry). ACE Money Transfer partnership (July 13, already known) and a new AI Financial Assistant product; consensus Buy, median PT ~USD401-410. No thesis-breaking news. review_by 2026-07-28 not due. HOLD. Conviction B.
- **Iran/Israel ceasefire status July 13:** Ceasefire effectively over per multiple sources; fresh US strikes on Iran retaliation for Strait of Hormuz tanker attacks. WTI ~$71-75/bbl, Brent ~$72-79/bbl this week — both well below the $100 halt-trigger despite the volatility. 10yr not yet re-checked this run (prior read ~4.54-4.58%, below 4.75% trigger). S&P 500 futures modestly higher pre-market (+0.4%) on cooling global inflation prints (France 1.8%) despite the geopolitical overhang. June CPI lands tomorrow, July 14 — last major inflation read before the July 29 FOMC.
- **Industrials sector strength (XLI +12.5% YTD, +13.3% 6mo)** — power/AI-capex-adjacent names outperforming; supports the CAT diligence catalyst read below.
- **Healthcare sector rotation continues** — multiple healthcare names at 52-week highs (ALHC, HCSG, MRNA) alongside LLY; a defensive-growth rotation theme, consistent with LLY's continued strength.
- **Iran ceasefire remains broken — market shrugging it off (July 10):** Fresh US-Iran strikes continued this week; Strait of Hormuz shipping is near a standstill (~13 vessels/24h vs. ~110/day pre-war). Despite the escalation, stocks rallied Thursday (S&P 500 +0.81% to 7,543.64, Nasdaq +1.30%) as oil fell — WTI ~$71.93 (down from an intraweek high of ~$76.70), Brent similar, both well below the $100 halt-trigger. 10yr yield eased to ~4.54-4.58% (below the 4.75% halt trigger) for a second session as falling oil reduced inflation-tightening fears. No halt triggered, but Hormuz disruption is a live tail risk worth re-checking each session given how fast oil has swung this week (69→76.70→72). June CPI (last major inflation read before the July 29 FOMC) lands Tuesday July 14 — watch for a hawkish surprise.
- **Iran conflict escalates further — fresh US airstrikes (July 9):** The US launched new strikes overnight (80+ targets: air defense, command/control, radar, anti-ship missile capability, small boats); Tehran retaliated against Gulf countries. Some shipping insurers are advising a pause on Strait of Hormuz voyages. Oil choppy but still well below the $100 halt-trigger (Brent ~$77-79, WTI ~$72-74). 10yr yield 4.587-4.59% (4-week high) — still below the 4.75% halt trigger but trending the wrong way. Monitor closely — if WTI closes above $100 or the 10yr closes above 4.75%, halt all new buys.
- **FOMC June 16–17 2026 — COMPLETED HAWKISH (finalized):** Rate hold (3.50–3.75%); dot plot: median 3.8% year-end, 9/18 members projecting hike. Next FOMC: est. late July 2026.
- **PCE inflation 4.1% YoY (June 25):** Highest since April 2023. Reinforces higher-for-longer rate regime.
- **Soft June jobs report (July 3):** Nonfarm payrolls +57K vs +113K expected — reinforces no-hike expectations; drove a rotation out of mega-cap growth/tech into cyclical value in the prior week.
- **SPY ex-dividend June 18 — APPLIED:** $1.76/sh. Total-return benchmark anchor: **$741.20**. Next SPY ex-div est. ~September 2026.
- **LLY — position:** July 10 pre-market $1,221.50 (+11.702% from entry). HWM $1,249.45 / stop $1,124.505, buffer 7.941%. No new company-specific news since July 9; presenting 16 abstracts at AAIC (Alzheimer's conference) July 12-15. review_by 2026-07-21 not due. HOLD. Conviction A.
- **V — position:** July 10 pre-market $349.245 (+7.943% from entry). HWM $364.21 / stop $327.789, buffer 6.143%. Launched Visa Threat Intelligence Platform (VTIP, fraud/cyber detection) — incremental positive, not thesis-moving. review_by 2026-07-28. Conviction B.
- **VST — re-entry review:** Not re-checked today (no held position, no near-term catalyst change).
- **NVDA — off watchlist, cooling period expired July 9** — not proactively re-added; would need a fresh diligence pass to re-enter consideration.
- **LRCX — ATR gate FAILED July 9 (5.466%)** on a chase-y ~6-7% pop (analyst PT hikes + broad semi relief rally, no fresh fundamentals); gate counter reset to 0/2. Technical confirmation strengthened to +7.88% above 50-day MA. Hit the 4-week staleness line — purge/keep decision at today's 2026-07-10 weekly review.
- **ETN — re-checked 2026-07-14:** 50-day MA $405.45, last close (July 13) $402.76 = **−0.66% below** — reversed back below the MA (was +0.37% above July 10) on Monday's broad semiconductor-led risk-off selloff. Not promoted — separation lost, not gained.
- **CEG diligence completed 2026-07-07, re-checked 2026-07-14:** 50-day MA now $272.40, last close $257.57 = **−5.44% below** (improved from −8.0% July 10) — still fails technical confirmation. ATR 3.30% would clear.
- **VRT diligence completed 2026-07-08, re-checked 2026-07-14:** 50-day MA now $324.73, last close $305.77 = **−5.84% below** (worse than −1.82% July 10 — lost ground Monday). ATR 5.15% still fails the 5% gate.
- **NVT diligence completed 2026-07-09, re-checked 2026-07-14:** 50-day MA now $165.63, last close $158.00 = **−4.61% below** (worse than −2.58% July 10 — lost ground Monday). ATR 3.56% clears.
- **MOD: full diligence pass completed 2026-07-14 — NOT PROMOTED.** See Watchlist table row above for details.
- **ABBV diligence completed 2026-07-10:** fundamentals/valuation pass (PEG 0.41-0.91) but FAILS technical confirmation (+13% extended above 50-day MA) and FY26 guidance was trimmed below Street consensus July 9 — not promoted. Not re-checked today (no diligence-queue slot; MOD took today's slot).
- **CAT: full diligence pass completed 2026-07-13 — PROMOTED, bought 4sh @ $944.73 same day.** Held position now; +0.42% above its 50-day MA as of July 13 close (separation compressed from +2.81% at entry).

## Weekly review summary (2026-07-10)

Week 8 (Jul 6–10): Bull −0.525% vs SPY +1.353% = lagged −1.879pp (AI/semi trade rallied hard — Meta custom-chip news, SK Hynix IPO — while an 80%-cash, non-tech book sat out). Since inception: Bull −0.396% vs SPY TR +2.391% = trails −2.787pp, the worst since-inception reading yet (was −0.84pp last review). Zero trades this week; win rate/profit factor unchanged (1/7, 14.3%, 0.192). Grade: C+. LRCX purged (4-week staleness, repeated ATR-gate failures). Codified a 0.5% minimum-separation rule for entry signal #4 and added a "pullback-watch" protocol after 6 consecutive diligenced names failed only the technical-extension gate — see Entry Signals section above. Full detail in `weekly-review.md`.

## Weekly review summary (2026-07-03)

Week 7 (Jun 29–Jul 3): Bull +0.42% vs SPY +2.18% = lagged −1.75pp (pure cash drag on SPY's best week since inception). Since inception: Bull +0.13% vs SPY TR +0.97% = trails −0.84pp (was leading +0.88pp last week). First win banked (VST +7.66%, Jun 30) — win rate now 1/7 (14.3%), profit factor 0.192. Grade: B−. 4th consecutive week of 0 new positions — see Watchlist note above for the pipeline fix. Full detail in `weekly-review.md`.

## Monday Conviction Ratings (last set 2026-07-13 pre-market; next refresh Monday 2026-07-20)

| Symbol | Rating | 3-consecutive-C trigger | Notes |
|--------|--------|------------------------|-------|
| LLY | **A** (unchanged) | N/A | +8.09% from entry ($1,182.00); JPMorgan PT raised to $1,400 (July 7); no negative news; stop buffer 4.85%; review_by 2026-07-21 |
| V | **B** (unchanged) | 0/3 weeks at C | +7.86% from entry ($349.00); securities-fraud suit dismissed July 9; Barclays/Wells Fargo/UBS all Buy; stop buffer 6.08%; review_by 2026-07-28 |

### Previous ratings (2026-07-06 pre-market)

| Symbol | Rating | 3-consecutive-C trigger | Notes |
|--------|--------|------------------------|-------|
| LLY | **A** (unchanged) | N/A | +10.38% from entry; Medicare Bridge confirming; stop buffer 7.69%; review_by tomorrow 2026-07-07 |
| V | **B** (unchanged) | 0/3 weeks at C | +11.64% from entry; thesis intact; zero sell ratings among 42 analysts; review_by 2026-07-28 |
