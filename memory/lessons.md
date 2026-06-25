# Lessons Learned

_Carried forward across every run. Add a dated line whenever something works
well, fails, or surprises you. Keep the highest-value lessons near the top._

## Trading lessons (recent)

### 2026-06-25 (midday) — NVDA II: GPU compute spot pricing is a real-time leading indicator of AI infrastructure demand health
NVDA's second stop-out (−9.78% in 3 days, June 22–25) was driven in part by GPU compute lease price compression: Nvidia's B200 GPU hourly spot market price fell from $6.11 (May 30) to $4.22 (June 21), a −31% decline in 3 weeks. This reflects rising hardware competition and expanding cloud compute supply, directly threatening GPU premium pricing power. The original thesis assumed AI accelerator monopoly pricing remained intact. GPU spot prices are publicly available in real time (CoreWeave/Lambda spot markets) and provide earlier warning than quarterly earnings. For any future AI infrastructure holding, track GPU spot pricing as a secondary ongoing thesis health metric alongside fundamental catalysts. When GPU spot falls >20% in a month, treat as a thesis watch-flag.

### 2026-06-24 (close) — NVDA: when a stated invalidation condition triggers at close, the next pre-market is the decision point — do not wait for the trailing stop
NVDA's entry plan stated "closes below $200 on volume" as the invalidation condition. At 15:51 ET close it printed $197.75 (−7.34% from entry), breaching both the $200 invalidation level and the −7% forced-cut threshold ($198.48). The trailing stop (at $192.591) had NOT fired. Because the close routine cannot trade, the position stayed open. The lesson: when a named invalidation condition triggers at EOD, log it immediately in the close journal and mandate a hold/exit decision at pre-market the next session. A thesis break is categorically different from a stop-out — it means the original reason for holding is gone, and the stop price is no longer the primary exit signal. Waiting for the stop to fire when the thesis is already broken turns a deliberate strategy position into a passive one.

### 2026-06-19 (weekly review) — From Aggressive Bull: proactive trimming before forced exits preserves capital and reduces peak-to-exit losses
AGGRO made two deliberate 25% trims on June 18 when position buffers narrowed toward the −12% forced-cut thresholds: MSFT trimmed 28→21sh when buffer reached 1.02pp; META trimmed 23→17sh when buffer was 3.60pp. Neither position was forced out — the trim was discretionary and proactive. This is a superior behavior to waiting for an automatic stop or forced cut: it reduces exposure while the thesis is still intact, preserves capital from the most-at-risk slice, and keeps the position alive to recover if the thesis holds. Cautious Bull should codify this: when a position's trailing-stop buffer falls below 2pp above the mandatory-cut trigger, consider a 25% proactive trim. This is not thesis abandonment — it is risk management within an active position. The full exit rule remains unchanged (stop fires → exit all).

### 2026-06-19 (weekly review) — MRVL (Marvell) watch: custom AI silicon thesis materially similar to NVDA's AI infrastructure angle
AGGRO's MRVL position (added June 15, +5.90% in one week) is based on custom AI silicon for hyperscalers — Marvell's ASICs for AWS and Google custom accelerators. This is a structurally valid thesis distinct from GPU sellers like NVDA: custom ASICs are cheaper per unit and carry no Nvidia licensing cost for the hyperscaler, making them a cost-optimization play as the AI buildout matures. Cautious Bull's watchlist does not currently include MRVL. When NVDA is confirmed (Monday June 22 fill) and a 4th position slot opens, MRVL should be researched as the first semi-equipment/ASIC diversifier candidate.

### 2026-06-12 (weekly review) — From Aggressive Bull: tighter stops and diversification outperform wider stops and concentration in volatile macro environments
AGGRO is down -5.95% since June 4 inception vs Cautious Bull -1.13% over the same period — Cautious leads by +4.82pp. The 10% trailing stop on META forced an exit at -6.87%; AGGRO's 18% stop kept META alive but the position is now at -9.88% with only 2.12pp of buffer before the -12% forced cut. The tighter stop was the CORRECT outcome for Cautious Bull: it limited the loss to a known maximum and freed capital. AGGRO's 77% tech concentration amplified every sector selloff (AMD cut at -13.28%; META/MSFT dangerously close to forced exits). Cautious Bull's three-sector spread (healthcare, financials, energy) provided substantially lower drawdown in the same volatile period. Lesson: the 10% stop + diversification approach is not overly conservative — it is structurally superior to wide stops + concentration in macro-shock environments. The advantage of wide stops + concentration only materializes in sustained, low-volatility uptrends. Reserve concentration for when the macro backdrop is clearly trending and rate risk is contained.

### 2026-06-10 — META stop-out: entering high-beta names near macro inflections co-locates the stop with the -7% rule
META entered June 1 into a macro reversal (strong NFP June 5 → delayed rate cuts → multiple compression on high-P/E names). With trailing stop HWM $642.38 and stop $578.142, the stop was co-located with the -7% cut threshold at $577.19. Any thesis-consistent broad-market weakness resulted in a near-maximum-loss automatic exit at $578.00 (−6.87%). Lesson: before initiating a high-multiple name, check the macro calendar for imminent rate-risk events (major payroll, CPI, FOMC) that could create sustained multiple compression. When the stop and the -7% rule are within 1% of each other, the expected-loss on a stop-out is nearly the same as the maximum guardrail loss — that is an unfavorable entry setup.

### 2026-06-10 — V (Visa) CFO 10b5-1 confirmation: always verify Form 4 transaction type before labeling insider selling as bearish
The Visa CFO's May 12 sale of 10,639 shares ($3.46M, 51.9% of holdings) was initially flagged as a bearish open-market discretionary sale and blocked the V buy for two weeks. SEC filing review confirms the transaction was under a pre-arranged Rule 10b5-1 plan — scheduled months in advance, NOT a discretionary sale. Two weeks of correct deferral turned into two weeks of unnecessary delay once the 10b5-1 status was confirmed. Lesson: always verify whether an insider sale was executed under a 10b5-1 plan before treating it as a conviction-level bearish signal. A plan-based sale is structurally different from a discretionary sale.

### 2026-06-03 — Regulatory headwinds (EU cloud rules) silently eroded AMZN below the -7% threshold
AMZN drifted from entry $269.13 to the -7% cut threshold ($250.29) over 12 days with no single catalyst. European cloud regulation pressures (AWS government contract risk) and heavy capex cycle created sustained downward drift. The position hit the guardrail not with a bang but a slow grind. Lesson: before entry, explicitly score structural regulatory headwinds (EU, DOJ, FTC scrutiny) as a negative entry signal — not just a "risk to monitor." A position facing both capex headwinds and regulatory uncertainty requires higher conviction to justify the entry.

### 2026-06-09 — Cash cushion compressed the since-inception gap by over half in one day
SPY had its biggest intraday swing since inception: opened $743.63, peaked $746.90, crashed to a low of $722.59 (-2.9% from open), then recovered to close $733.06 (-0.84% from prior close). Bull with 73.7% cash fell only -0.20%. The since-inception gap narrowed from -0.96% to -0.36% in a single session — cash drag hurts in up markets but repeatedly pays off in volatile/down sessions. This is the second major down-day demonstration since the Jun 5 NFP shock. META showed notable relative strength: +0.15% on a day SPY fell -0.84% and hit a -2.9% intraday low, suggesting some support is forming near the $578-580 stop level. Still, the 1.39% stop buffer remains the primary risk going into Wednesday.

## Operating lessons (seed)

- Always run `./scripts/alpaca.sh clock` before trading; do nothing if the
  market is closed.
- After any order, re-fetch `positions` and `orders` to confirm the fill before
  journaling or notifying.
- Notional (dollar-based) buys can produce fractional shares — fractional
  positions cannot use trailing-stop orders. To guarantee a trailing stop is
  possible, prefer whole-share quantities for new positions.
- If a credential env var is missing, stop immediately and notify — never guess.
- Push your work with `git push origin HEAD:main` at the end of every run. A
  routine runs on a temporary working branch, so a plain push to `main` is a
  no-op and the next agent loses this run's work.
- Never put a literal `$` in a `notify.sh` message — the shell mangles it.
  Write `USD`/plain numbers and single-quote the argument.

## Trading lessons

### 2026-06-05 (weekly review) — From Aggressive Bull: faster deployment + wider stops in volatile markets
Aggro Bull launched June 4 and deployed 79% of capital across 6 positions in just 2 days (NVDA, META, AVGO, AMD, MSFT, VST). By June 5 EOD it is −3.77% while SPY fell −2.20% from its inception anchor — alpha −1.57%. Cautious Bull over the same 2 days fell less. The lesson: rapid full deployment into a volatile market amplifies drawdown risk. Aggro's 18% trailing stops kept all 6 positions alive (AMD most stressed at −8.39%, still inside −12% threshold), while Cautious Bull's 10% stops triggered on NVDA and MSFT — Aggro has more positions alive for a recovery, Cautious Bull has more cash protection. Neither is universally better; the trade-off is real. One actionable idea from Aggro: **VST (Vistra Energy)** — nuclear power operator with long-term PPAs to Meta and AWS for AI data-center electricity. It held up far better than semis on the June 5 selloff (−2.00% vs NVDA −4.36%). Non-correlated to AI semi selling. Worth researching for Cautious Bull as a diversifier.

### 2026-06-05 — High cash during a broad market selloff provides strong relative protection
SPY fell −2.41% today (strong NFP print pushed rate-cut expectations out). Bull fell only −0.97%, outperforming by +1.44% — entirely because 79% of the portfolio was in cash. The since-inception performance gap vs SPY narrowed from −3.08% at midday to −1.06% at close, driven almost entirely by SPY's large down day. Lesson: cash drag hurts in bull markets but provides real protection in downturns. The build-phase high-cash posture is correct and has now demonstrated its protective value. Do not rush to deploy capital just to reduce cash drag in up markets — the protection has tangible value.

### 2026-06-05 — Trailing stops that trigger intraday protect against afternoon continuation
NVDA and MSFT stops triggered mid-session today (~11:20 AM and ~12:08 PM ET). Both stocks would have fallen further in the afternoon broad-market selloff. The stops that seemed painful at midday (-3.36% and -0.70% from entry) actually prevented worse realized losses. This is trailing-stop discipline working as designed. Never second-guess a triggered stop by wishing you could have held.

### 2026-06-04 — Trailing stops do not protect against gap-down risk on earnings; scale-up plans must require positive market reaction
AVGO's trailing stop was set at $445.50 (HWM $495.00). The stock gapped from ~$479 close to ~$409
overnight after earnings — completely through the stop level. The stop executed at market price, not
at $445.50. This is called gap risk: when a stock opens below your stop, the stop fills at the opening
market price, potentially well below the stop level. Three lessons: (1) Trailing stops protect against
gradual declines, not overnight gaps. Accept this as a structural limitation of the product. (2) The
scale-up plan called for adding 8–10 shares, and technically both AI-revenue conditions were met
($10.8B > $10.7B guide; Q3 $16.0B > $11.5B threshold). But the spirit of the plan was "add on
confirmation with positive market reaction." A −15% gap is unambiguously negative confirmation. Never
execute a scale-up plan when the stock gaps down on earnings even if the technical trigger conditions
are literally met — the market's verdict overrides the pre-stated formula. (3) Pre-earnings stops
should be held with full awareness that gap risk exists; raising stops before an earnings event trades
one risk (slow decline protected) for another (false stop-out in normal volatility). The existing
policy of waiving the +15% tighten rule pre-earnings is correct.

### 2026-06-03 — Earnings beat thresholds must be anchored to what management GUIDED, not to stale buy-side bars
AVGO's pre-market research originally used ">$5B AI revenue" as the scale-up trigger — taken from
market commentary at the time. But in its Q1 March report Broadcom itself GUIDED Q2 AI semiconductor
revenue of $10.7B (+140% YoY). The real bar for a "beat" is whether the actual print exceeds the
company's own guidance. Writing "AI revenue >$5B" without refreshing against the company's own
prior guidance was sloppy. Always check management guidance for the period before defining the
earnings trigger threshold. An in-line $10.7B is NOT a beat relative to guide; only exceeding it is.

### 2026-05-29 — Pre-stating strong-beat thresholds for earnings skips is essential
MRVL (EPS $0.80 vs $0.85 threshold; revenue $2.418B vs $2.5B) and COST (EPS $4.93 vs $5.10;
renewal 89.7% vs >90%) were both correctly skipped because specific, pre-stated quantitative
thresholds existed before the prints. Without those thresholds, there is a risk of rationalizing
entry on any beat. Writing the invalidation criterion before the event — not after — is what
makes the skip defensible. Always set specific numeric thresholds in the research log before
earnings; "strong beat" without numbers is not a criterion.

### 2026-05-29 — Cash drag is real but correct during the build phase
The since-inception gap (Bull +1.26% vs SPY +2.33% = −1.07%) is almost entirely explained by
60% cash during a 2.33% SPY run. The right response is NOT to rush deployment — it is to
deploy disciplined, high-conviction positions one per week until 6-8 are held. The gap will
mechanically narrow as positions are added. Forcing entries to "keep up with SPY" risks
permanent capital impairment, which is worse than temporary drag.

### 2026-05-25 — Holiday pre-market: research and plan ahead, don't skip
When the market is closed (e.g., Memorial Day), the pre-market routine still adds value: it
forces a structured review of weekend news, resets the weekly cap count, and ensures the
market-open routine on the first trading day has a clear, pre-written plan. A holiday pre-market
run with no trades is still a full, successful routine — the deliverable is the plan, not the order.

### 2026-05-22 — Opening-minute entries on strong gap-up days
The pre-market routine must run at 8:00 AM ET. A run at 1:40 PM is too late
for same-day execution — the market opens at 9:30 and plans must be ready.
A missed morning costs an entire trading day. If the routine is late, accept
the missed session and target the next valid open; do not attempt to rush or
cut corners.

### 2026-05-22 — Opening-minute entries on strong gap-up days
All three initial positions (AVGO, MSFT, AMZN) were filled at 9:36 AM on a
day when SPY opened and continued higher. All three ended the day below
entry. On days when SPY gaps up >0.5% at the open and the planned names are
already bid, consider placing limit orders ~0.2–0.4% below the opening
quote rather than market orders. The spread between "plan price" and "fill
price" matters over many trades. Alternatively, wait 5–10 minutes for the
opening rush to settle before executing.

### 2026-05-22 — Cash drag is intentional, not a mistake
A 75%-cash portfolio will lag a rising market. This is the correct posture
for an early-stage build in a stretched-valuation environment with elevated
yields and geopolitical uncertainty. Do not rush to deploy capital to "keep
up with SPY" in the first weeks. Selective, high-conviction entries beat
forced deployment.
