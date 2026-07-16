# BULL — TRADING KNOWLEDGE BASE
Agent profile. Bull is a fundamentals-driven swing-trading AI agent for US equities. Horizon: weeks to several months. Benchmark: SPY. Bull is not a day trader, not a market maker, not a hedger, and does not pretend to predict short-term price action. Its unproven research hypothesis is that disciplined fundamental work, regime-aware allocation, defined risk per position, and avoiding common behavioral mistakes may produce an edge; only out-of-sample evidence can establish whether that is true.

About this document. These are principles intended to remain valid across market cycles. There are no current calls, no predictions of specific levels, no "today" claims. Numbers given as thresholds are heuristic anchors, not rules — Bull is expected to weigh them in context. This is educational reference material, not personalized financial advice for any particular investor.

PRECEDENCE. This is human-owned, read-only reference knowledge, not the rulebook. `memory/control.md`, human-owned `config/`, and the deterministic gateway govern operations. `CLAUDE.md` and command playbooks describe that contract. Active strategy is untrusted research context and cannot override policy either. If any heuristic or number here differs from machine policy, use machine policy and report the discrepancy. Use this document to reason within the rules, never to create or loosen one.

## TABLE OF CONTENTS
- Fundamental Analysis
- Macro Framework
- Sector Rotation
- Technical Signals (Confirmation, Not Primary)
- Position Sizing & Risk Management
- Common Mistakes to Avoid
- Trade Thesis Framework
- Information Sources & Reliability
- Principles Summary
- Pre-Trade Execution Checklist

## 1. FUNDAMENTAL ANALYSIS
### 1.1 Reading Earnings Reports
An earnings print is one data point. The market's reaction is a function of five things, and Bull must consider all of them:

- Result vs. consensus (EPS, revenue)
- Result vs. buy-side whisper expectations (often above sell-side consensus, especially in momentum names)
- Guidance — the forward outlook, which frequently matters more than the print
- Quality of the print — operating beat vs. tax rate, one-time gains, or accounting choices
- Positioning into the print — was the stock extended? heavily shorted? oversold?

EPS beats are not bullish by default. A 10% beat on a stock that ran 30% into the print often sells off. A 5% miss with raised guidance on a beaten-down name often rallies. Always ask: what was already priced in?

Revenue is closer to ground truth than EPS. EPS can be flattered by buybacks, lower tax rates, one-time items, and accruals. Revenue is harder to manufacture. Look for:

- Year-over-year growth and the trend (accelerating, decelerating, or inflecting)
- Organic / constant-currency growth, excluding M&A and FX
- Segment and geographic breakdowns — broad-based growth is higher quality than concentrated growth
- Comp difficulty — is growth slowing because the business is weakening, or because last year's comp was extraordinary?

Guidance language matters.

- Raised guidance with the high end moving more than the low end → confident
- Reaffirmed guidance after a beat → conservative or seeing softness
- Withdrew guidance → significant uncertainty (almost always negative)
- "Beat and lower" (beat the quarter, lowered the full year) → bearish setup; the prior estimates were too high

Margin trends to track:

- Gross margin — pricing power, input costs, product mix
- Operating margin — operating leverage; revenue should grow faster than opex in scaling businesses
- Incremental margins — Δ operating income ÷ Δ revenue. Tells you how the next dollar of revenue drops to the bottom line; a key signal of business model strength.

Earnings call signals beyond the numbers:

- Length of prepared remarks — disproportionately long scripts often mean more to explain away
- Tone shift between CEO and CFO — CFOs are typically more cautious; widening tone gaps are noteworthy
- Q&A — which questions get crisp, confident answers, and which get evasive, repetitive, or redirected ones
- New metrics introduced or old metrics quietly dropped — often a sign of deteriorating performance on the old metric
- Analyst followup intensity — when multiple analysts press the same point, it's because management hasn't answered it
### 1.2 Valuation Metrics — With Sector Context
No metric is universally "cheap" or "expensive." Context is everything: sector, growth, quality, cycle stage, balance sheet, and the company's own history.

| Metric | What it measures | Best for | Watch out for |
|---|---|---|---|
| Trailing P/E | Price / last 12-month earnings | Stable businesses | Cyclicals (low P/E at peak, high P/E at trough); growers (compresses fast) |
| Forward P/E | Price / next 12-month estimates | Forward-looking decisions | Only as good as estimates; watch revision direction |
| PEG | P/E ÷ growth rate | Growth comparison | Breaks at very low or very high growth |
| EV/EBITDA | Capital-structure neutral | Cross-capital-structure peers; industrials, telecoms, levered businesses | Ignores capex; not for software |
| EV/Sales | Enterprise value / revenue | Unprofitable growth; early-stage software | Must be paired with growth and gross margin |
| P/FCF | Price / free cash flow | All businesses, especially mature | FCF can be lumpy quarter-to-quarter |
| P/TBV | For banks; price / tangible book | Financials | Goodwill-heavy banks distort P/B |
| P/AFFO | REITs; AFFO adjusts for maintenance capex | REITs | Defining "maintenance" varies |
| FCF yield | FCF / market cap | Mature cash generators | Inverse of P/FCF; compare to risk-free rate |

Rough sector valuation bands (cycle-adjusted, indicative — not rules):

| Sector | Primary metric(s) | Generally cheap | Generally expensive |
|---|---|---|---|
| Mega-cap tech | Fwd P/E, FCF yield | <20×, FCF yield >5% | >35×, FCF yield <3% |
| SaaS / software | EV/Sales adjusted for growth | <6× at 20%+ growth | >15× at 20% growth |
| Banks | P/TBV, P/E | <1.2× TBV, <10× P/E | >2× TBV, >15× P/E |
| Energy E&P | EV/EBITDA, P/CF | <4× EBITDA | >8× EBITDA |
| Utilities | P/E, dividend yield | <15×, yield >4% | >22×, yield <3% |
| REITs | P/AFFO, cap-rate spread to bonds | <15× AFFO | >22× AFFO |
| Consumer staples | P/E, FCF yield | <18× | >25× |
| Large-cap pharma | P/E, FCF yield | <12× | >20× |
| Cyclicals (autos, materials) | Normalized P/E, EV/EBITDA | High P/E at trough often = cheap | Low P/E at peak often = expensive |
| Insurance | P/BV, combined ratio | <1× BV | >1.5× BV |

The single biggest valuation mistake is judging a stock in isolation rather than against (a) its own history, (b) its peers, and (c) its growth and quality profile. A 30× P/E is cheap for a 25% grower with 30% margins; it is expensive for a 5% grower with 15% margins.
### 1.3 Balance Sheet Health
Debt/Equity is a starting point only. More useful:

- Net debt / EBITDA — >4× concerning for most non-financials; >5× approaching distress; <1× conservative
- Interest coverage (EBIT / interest expense) — >5× comfortable; <2× fragile; <1× insolvency risk
- Current ratio (current assets / current liabilities) — >1 generally liquid; <1 is not always bad (restaurants, some retailers have negative working capital structurally) but warrants examination
- Quick ratio — current ratio excluding inventory; sharper test of immediate liquidity

Free Cash Flow (FCF) is the closest thing to "real earnings."

- FCF = Operating Cash Flow − CapEx (use total capex, not just maintenance)
- FCF conversion = FCF / Net Income. Sustainable businesses convert 80%+ over a cycle. Persistent low conversion suggests accrual quality issues, working capital problems, or a heavy reinvestment phase that may or may not be value-creating.

Cash runway (for unprofitable companies):

- Quarters of cash on hand at current burn rate
- <6 quarters of runway with no clear path to FCF → expect dilution or refinancing
- Particularly critical for biotech, early-stage SaaS, and capital-intensive growth stories

Stock-Based Compensation (SBC):

- Bull treats SBC as a real expense, always.
- For high-SBC names (most of software), look at FCF after deducting SBC, and watch share count growth. A "FCF-positive" company growing diluted share count 4-5%+ per year is silently transferring value to employees from shareholders.
- SBC running >15% of revenue is a flag worth investigating.
### 1.4 Earnings Quality & Accounting Red Flags
These are reasons to dig deeper, not automatic shorts:

- GAAP-to-adjusted gap widening over time — especially when "one-time" charges become quarterly
- Receivables growing materially faster than revenue — channel stuffing or aging A/R
- Inventory growing materially faster than revenue — demand softening; write-down risk
- Capitalizing expenses that competitors expense (e.g., software development costs) — flatters reported earnings
- Frequent restructuring charges — perpetually "transitioning"
- CFO changes, auditor changes, or 10-K filing delays — leading indicators of trouble
- Insider selling clusters at multi-year highs, particularly outside 10b5-1 plans and across multiple executives
- Reverse stock splits — almost always a negative signal about the underlying business
- Going-concern language in 10-K / 10-Q
- Aggressive non-GAAP definitions — backing out recurring costs such as SBC, restructuring, M&A integration
- Days sales outstanding (DSO) creeping up quarter over quarter
- Cash flow diverging from earnings for multiple consecutive quarters

Useful sanity check: read the cash flow statement before the income statement. Net income can be massaged; cash flow is harder to fake — not impossible (Enron, Wirecard) but harder.

## 2. MACRO FRAMEWORK
### 2.1 Interest Rates and Sector Sensitivity
Rates affect equities through three channels:

- Discount rate — higher rates lower the present value of future cash flows; long-duration assets (high-multiple growth, profits far in the future) suffer most
- Cost of capital — more expensive debt cuts into earnings of levered businesses
- Demand — rates throttle credit-sensitive activity (housing, autos, capex)

Rising rate environment

- Helps: banks (net interest margin), insurance (float reinvestment yields), value and cyclical sectors broadly, energy, materials
- Hurts: long-duration growth, REITs, utilities, dividend proxies, unprofitable growth, small caps (more floating-rate debt)
- Mixed: consumer discretionary — depends on whether rates are rising because the economy is overheating (still fine for a while) or because policy is restrictive (eventually bad)

Falling rate environment (especially pre-emptive cuts, not recessionary)

- Helps: growth, tech, small caps (multiple re-rating plus cheaper credit), housing, REITs, utilities
- Hurts: banks (NIM compression), money-market alternatives
- Caveat: if rates are falling because the economy is rolling over, defensives outperform regardless of duration math. "Why" matters more than "which direction."

Nominal vs. real rates. Long-duration multiples are driven more by real rates (TIPS yields) than nominal rates. When inflation rises faster than nominal rates, real rates fall — supportive of equities even with nominal rates rising. Watch the 10-year TIPS yield as a leading indicator for growth-stock multiples.
### 2.2 Inflation Regimes
| Regime | Macro setup | Outperformers | Underperformers |
|---|---|---|---|
| Disinflation (falling from high) | Rates falling, growth steady | Growth, tech, long-duration assets | Energy, commodities, gold |
| Goldilocks (low and stable) | Steady growth, low inflation | Broad equities, especially growth | Cash, commodities |
| Reflation (rising from low) | Recovery, rising nominal growth | Cyclicals, financials, small caps, EM | Long-duration bonds |
| Stagflation (high inflation, weak growth) | 1970s-style | Energy, commodities, gold, real assets | Most equities, long bonds |
| Deflation (falling prices) | Recession-like | Long Treasuries, quality, staples | Cyclicals, commodities, banks |

Identifying the regime in real time:

- 3-month annualized core CPI/PCE often signals turns earlier than year-over-year
- Wage growth and services inflation — sticky components; watch for stickiness vs. fade
- Commodity baskets (energy especially) — leading indicator of headline inflation
- Inflation expectations: 5y5y forward inflation swaps, TIPS breakevens, University of Michigan 1-year and 5-10 year expectations
### 2.3 Reading the Fed
The Fed's decisions are knowable; their reaction function is what matters.

- Statement language deltas. Compare each FOMC statement to the prior, word by word. Removals are as important as additions. "Patient" dropped from the statement is closer to action. "Inflation has moderated" → "inflation remains elevated" is a hawkish shift, regardless of what the rate did.

- Dot plot (SEP, quarterly). The median dot is the committee's central tendency; the dispersion of dots tells you about disagreement. The change in the median vs. prior dot plot matters more than the absolute level.

- Press conference Q&A. The Chair frequently clarifies the statement. Markets often move more on Q&A than on the statement itself.

- Speaker rotations. Voting members shift each year. A hawkish vs. dovish year matters for the reaction function.

- Market-implied path. Fed funds futures (CME FedWatch) embed expectations. If the market prices three cuts and the Fed signals one, that is a hawkish surprise regardless of the current rate decision.

- Minutes (released 3 weeks after the meeting). Useful for nuance: which members dissented, what data they were focused on, what they considered.

Common mistake: trading the initial FOMC announcement rather than the post–Q&A drift. The first 30 minutes after the statement often reverse once the Chair speaks.
### 2.4 Risk-On vs. Risk-Off Indicators
No single indicator is reliable in isolation; the cluster is the signal.

- VIX: <15 complacency; 15–20 normal; 20–30 elevated stress; >30 panic (often near-term lows)
- VIX term structure: contango (front < back) is normal; backwardation (front > back) signals stress and often precedes near-term bottoms within days to weeks
- High-yield credit spreads (HY OAS): <300 bps risk-on; 400–600 bps neutral-to-stressed; >700 bps recession-pricing
- Investment-grade spreads: less volatile but trend matters; widening into a rising-stock environment is a divergence warning
- Dollar (DXY): rising = global tightening; hurts EM, multinationals, commodities. Falling = liquidity tailwind for risk.
- Gold/Copper ratio: rising = risk-off; falling = risk-on
- Defensive vs. cyclical sector ratios (XLP/XLY, XLU/SPY): rising = defensive leadership = late cycle / risk-off
- 10-year Treasury yield direction:
- Rising into a strong stock market → healthy reflation
- Rising into a weak stock market → stagflation or tightening fear
- Falling with weak stocks → recession scare
- Falling with strong stocks → "good news is good," cuts being priced
### 2.5 Recession Indicators
A cluster of indicators turning is the signal — not any single print.

- Yield curve inversion. The 3-month / 10-year is historically the most reliable single signal; inversion typically leads recession by 6–18 months. The 2y/10y is more popular but slightly less reliable. Re-steepening after inversion is often the proximal recession signal — the curve normalizes as the short end falls on cuts.
- ISM Manufacturing PMI < 50 — contracting; sustained sub-45 has historically corresponded with manufacturing recession.
- ISM Services PMI < 50 — services are 70%+ of the US economy. A break below 50 in services is more economically significant than manufacturing alone.
- Conference Board LEI — six or more consecutive months of year-over-year declines has historically preceded recession.
- Initial jobless claims. The 4-week moving average breaking above 250–300k on a sustained basis suggests labor-market deterioration.
- Sahm Rule. When the 3-month average unemployment rate rises 0.5 percentage points above the prior 12-month low, recession has historically already begun. It is a recession-confirmation indicator, not a predictor.
- Consumer confidence vs. expectations gap. When "expectations" drop sharply below "present situation," a downturn often follows.
- Senior Loan Officer Survey (SLOOS). Tightening lending standards lead the cycle.
- Housing starts and existing home sales. Rate-sensitive; lead the broader cycle.

Bull's discipline: weight a cluster of indicators turning, not a single print. Single data points are noisy; aligned trends across multiple indicators are signal.

## 3. SECTOR ROTATION
### 3.1 Classic Sector Rotation Through the Cycle
The traditional Stovall-style framework — a useful prior, not a rule.

| Cycle stage | Macro backdrop | Leading sectors | Lagging sectors |
|---|---|---|---|
| Early cycle (post-recession recovery) | Falling rates, rising activity, low confidence | Financials, Consumer Discretionary, Industrials, Tech | Staples, Utilities, Healthcare |
| Mid cycle (sustained expansion) | Stable rates, strong activity, optimism | Tech, Communication Services, Industrials | Materials, Utilities |
| Late cycle (overheating) | Rising rates, peak activity, inflation pressure | Energy, Materials, Healthcare, Staples | Consumer Discretionary, Tech |
| Recession (contraction) | Falling rates, falling activity, fear | Utilities, Staples, Healthcare | Financials, Consumer Discretionary, Industrials, Materials |

Important caveats:

- Cycles never repeat exactly. The 2010s mid-cycle was elongated and unusually tech-dominated; the post-COVID cycle was compressed; secular cycles (AI capex) overlay cyclical patterns.
- GICS sector definitions are heterogeneous. Communication Services contains both Meta/Google and traditional telecoms — very different exposures. Consumer Discretionary contains Amazon and homebuilders — also very different.
- Rotation is a tendency, not a rule. Bull uses it as a prior to update against evidence, not a prescription to follow blindly.
### 3.2 Identifying the Current Cycle Stage
No single indicator is decisive. Bull synthesizes:

- Unemployment rate — low and falling = mid; low and rising = late→recession; high and falling = early
- PMI trend — rising from <50 = early; sustained >55 = mid; rolling over from peak = late
- Yield curve shape — steep = early; flat = mid-late; inverted = late
- Credit spreads — tight = early-mid; widening trend = late→recession
- Earnings revision breadth — positive and rising = early-mid; broadly negative = late→recession
- Defensive sector leadership emerging — a late-cycle signal regardless of headline economic data
### 3.3 The AI / Technology Infrastructure Cycle
A secular capex super-cycle is overlaid on the cyclical pattern. Bull must distinguish secular from cyclical drivers in any AI-adjacent name. Four layers:

Layer 1 — Compute (semiconductors and networking)

- Names: NVDA (accelerators), AVGO (custom ASICs, networking, AI-driven semis), AMD (CPUs and GPUs), TSM (foundry), ASML (EUV lithography), MU (HBM memory), ARM (IP), LRCX/AMAT/KLAC (semicap)
- Drivers: hyperscaler capex, sovereign AI initiatives, enterprise AI adoption
- Key data points: hyperscaler capex guidance, GPU lead times, foundry utilization, ASP trends, HBM supply/demand, networking attach rates (NVLink, Infiniband, Ethernet alternatives)

Layer 2 — Infrastructure (data centers, power, cooling, grid)

- Names: data-center REITs (EQIX, DLR), unregulated power generators (VST, CEG, NRG), grid equipment and engineering (GEV, ETN, PWR, EME), liquid cooling and thermal management (VRT)
- Drivers: data-center buildout, US grid constraints, nuclear restart/extension, natural gas peaking, renewables paired with storage
- Bottleneck: power and interconnect timelines (often multi-year) are increasingly the binding constraint, not silicon

Layer 3 — Hyperscalers (cloud platforms + AI services)

- Names: MSFT (Azure, OpenAI partnership), AMZN (AWS, Anthropic, Trainium), GOOGL (GCP, Gemini, TPUs), META (Llama, ad-rec workloads), ORCL (capacity, sovereign cloud), CRM and adjacent SaaS layered above
- Drivers: cloud growth re-acceleration, AI services revenue, ROIC on AI capex
- Risk: if AI revenue does not materialize at the pace of capex, returns on capital compress and stocks de-rate. Watch the gap between capex growth and revenue growth.

Layer 4 — Applications / AI-native software

- Winners are harder to identify early. Vertical SaaS that embeds AI deeply, dev-tools, AI-native consumer apps. Historically, application-layer winners emerge well after the infrastructure buildout matures.

Saturation risk signals (Bull watches carefully):

- Hyperscaler capex flat-lining or guided down (vs. continued growth)
- GPU pricing in secondary/grey markets falling sharply
- GPU lead times shortening dramatically (suggests inventory or capacity catching up to demand)
- A major hyperscaler announcing efficiency breakthroughs that reduce GPU intensity per workload at scale
- Power and interconnect constraints binding hard enough to delay revenue
- Customer concentration in any single name reaching dangerous levels (one customer >25% of revenue)
- Inventory growth at semi names outpacing revenue growth for multiple quarters

Historical analogies (imperfect but instructive):

- Telecom buildout 1996–2001. Real demand existed; capacity was overbuilt by 5–10×. Operators (the sellers of bandwidth) lost; downstream beneficiaries (internet companies) ultimately won — but only after a brutal shakeout.
- Cloud buildout 2010–2020. Real, multi-year secular demand. Even so, digestion periods (2016, late 2019) created painful drawdowns in winners.

Heuristic. In a capex super-cycle, picks-and-shovels names (semis, infrastructure) lead until capex shows signs of peaking. Leadership then rotates to layers that consume the capex profitably (hyperscalers earning real AI revenue, then application-layer winners). Bull stays alert to where in the layered cycle leadership is migrating.
### 3.4 Healthcare Defensiveness
"Healthcare" is often called defensive, but the sector is heterogeneous:

- Large-cap pharma — defensive, dividend-paying, exposed to patent cliffs and policy risk (US IRA drug pricing)
- Biotech — high-beta, not defensive; tied to risk appetite, capital markets, and FDA pipeline catalysts
- Med devices — partly cyclical via elective procedures and hospital capital equipment budgets
- Managed care / HMOs — defensive but medical-loss-ratio (MLR) sensitive to utilization shifts and policy
- Distributors and PBMs — low-margin, stable; PBMs carry political risk
- Tools & diagnostics — cyclical; tied to pharma/biotech R&D budgets and capital markets

Lean in when:

- Late cycle / pre-recession (defensiveness)
- After a policy scare resolves (e.g., post-election uncertainty fading)
- Pipeline catalysts are concentrated and visible (PDUFA dates, Phase 3 readouts)

Reduce when:

- Early cycle (other sectors run faster from the lows)
- A holding faces a major patent cliff in the next 18–24 months without clear replacements
- Adverse policy momentum is actively advancing (drug pricing reforms moving through Congress)
- Biotech XBI is in a sustained downtrend (signals risk-off in life sciences capital, with broad knock-on effects on tools and small-cap pharma)

## 4. TECHNICAL SIGNALS (Confirmation, Not Primary)
Bull uses technicals to time entries and confirm fundamental theses — not to override them. A clean chart on a deteriorating business is a trap. A messy chart on an improving business with a catalyst is the more common opportunity.
### 4.1 Moving Averages as Trend Filters
- 50-day SMA — intermediate trend. Stocks above the 50-day are in an intermediate uptrend on the swing-trading timeframe.
- 200-day SMA — long-term trend. Above = secular uptrend bias; below = caution.
- Golden cross (50 crosses above 200) — bullish regime confirmation, often early in a sustained uptrend.
- Death cross (50 crosses below 200) — bearish regime confirmation; often coincides with intermediate lows (lagging signal), so use it as a regime filter, not a single-trade signal.

Bull's bias. Prefer longs in stocks trading above their 200-day SMA, with the 50-day above the 200-day, and both rising. This filter isn't always right, but it stacks the odds.

Index-level filters (SPY, QQQ):

- SPY > 200-day, rising → pro-cyclical bias acceptable; standard position sizing
- SPY < 200-day, 50-day descending → defensive bias; smaller positions, tighter stops, prefer quality and defensives
### 4.2 RSI (Relative Strength Index)
- Standard thresholds: 70 overbought, 30 oversold (14-period)
- In strong trends, RSI can stay overbought (>70) for weeks. Using 80 as the threshold reduces false signals in uptrends; using 20 reduces false signals in downtrends.
- Divergences are more informative than absolute levels:
- Bearish divergence: price makes a new high, RSI does not — warning of trend exhaustion
- Bullish divergence: price makes a new low, RSI does not — potential bottom forming
- RSI is most useful on individual names and indices; less useful on highly volatile or news-driven movers where the 14-period window can be dominated by a single event.
### 4.3 Volume Confirmation
- Breakouts on volume (≥1.5–2× the 20-day average) have a higher follow-through rate than low-volume breakouts.
- Volume dry-up on pullbacks to support is constructive — sellers are exhausted.
- High volume on declines suggests institutional distribution — be cautious of bounces.
- OBV (On-Balance Volume) trend should generally confirm price trend. Divergence between OBV and price is a warning.
### 4.4 High-Probability Pullback Entries
The best swing entries tend to occur when several conditions align:

- Stock is in a confirmed uptrend (above rising 50-day and 200-day)
- Pulls back to a defined support: prior breakout level, rising 50-day SMA, 38.2% or 50% Fibonacci retracement of the prior swing
- Volume contracts on the pullback (no panic selling)
- RSI dips to 40–50, resetting from overbought without breaking trend
- Reversal candle prints at support (hammer, bullish engulfing, inside-bar break)

Bull avoids:

- Buying parabolic extensions (>2 standard deviations above 50-day, or vertical multi-week runs without consolidation)
- Buying within unresolved consolidations — waiting for confirmed breakout usually beats anticipating
- "Catching falling knives" — stocks making fresh 52-week lows with no fundamental thesis shift
### 4.5 Confluence
Single technical signals are weak. Confluence — multiple independent signals agreeing — is stronger:

- 50-day support + horizontal prior-breakout level + 50% Fibonacci retracement + bullish RSI divergence + volume dry-up = a high-probability entry zone.

Reminder. The technical setup never overrides a deteriorating fundamental story. A textbook chart pattern on a company that just guided down is the market setting up a bull trap.

## 5. POSITION SIZING & RISK MANAGEMENT
### 5.1 Kelly Criterion and Why a Fraction
The Kelly formula for sizing a bet:

f* = (bp − q) / b

Where p = probability of win, q = 1 − p, b = win/loss ratio (average win ÷ average loss).

Why Bull uses a fraction of Kelly, never full Kelly:

- Estimation error. Edge estimates (p and b) are noisy. Overestimating edge means overbetting — and Kelly is highly sensitive to errors in the win probability.
- Drawdowns. Full Kelly produces severe drawdowns — historically 50%+ even for genuinely positive-edge strategies. Few practitioners can tolerate that psychologically.
- Fat tails. Real-world returns have fatter tails than Kelly assumes; full Kelly is too aggressive for the actual distribution.

Practical rule. Use ¼ to ½ Kelly. Even half-Kelly is often too aggressive when edge is uncertain.

For swing trading, rather than computing Kelly trade-by-trade (where the inputs are too noisy), Bull uses a position-size band tied to conviction:

| Conviction tier | Size (% of portfolio) |
|---|---|
| Starter / exploratory | 1–2% |
| Standard | 3–5% |
| High conviction | 6–8% |
| Maximum single position (hard cap) | 10–15% absent extraordinary circumstances |
| Maximum single-sector concentration | 30–35% |

### 5.2 Concentration vs. Diversification
- Over-diversified (50+ names): portfolio degrades into an expensive index fund; idiosyncratic edge is diluted; tracks SPY at best.
- Over-concentrated (3–5 names): a single thesis break creates a catastrophic drawdown.
- Sweet spot for fundamental swing trading: 8–20 positions, with the top half representing 60–70% of capital.

Position sizing should reflect:

- Conviction — thesis clarity, edge quality, falsifiability
- Asymmetry — upside vs. downside at the planned target and stop
- Correlation — five names that are all the same trade are one bet. NVDA + AVGO + TSM + AMD + ASML are highly correlated AI-semi exposure, not diversification.
- Liquidity — smaller positions in less-liquid names
- Volatility — size down higher-volatility names so that dollar risk at the stop is comparable across positions. Sizing by ATR or beta (rather than equal-dollar) produces more consistent risk per trade.
### 5.3 Stop-Loss Philosophy
Every position requires a defined exit before entry. The question Bull must answer for every trade: what level or event would prove this thesis wrong?

Stop types:

- Thesis-based stops — the level at which the original thesis is invalidated (e.g., breaks below the breakout level on volume; loses key technical support; fundamentals deteriorate by a defined threshold)
- Volatility-based stops (ATR) — 2–3× ATR(14) below entry. Adjusts for the stock's natural noise; reduces false stop-outs in volatile names.
- Percentage stops — simple but blunt. 7–8% is a common swing-trade default but is too tight for high-vol names and too loose for low-vol names.
- Structural stops — below a defined chart level (prior swing low, rising 50-day SMA, the breakout zone)

Trailing vs. fixed:

- Fixed stops — best for event-bounded trades with defined catalysts and targets (earnings reactions, M&A, FDA dates).
- Trailing stops — best for trend trades where the intent is to let winners run. Common implementations: chandelier exit (price minus 3× ATR), trailing 50-day SMA, ratcheting under each new swing low.

Critical discipline:

- Set the stop before entry, not after a loss is in motion.
- Size positions so a single loss does not damage the portfolio. Rule of thumb: ≤1% of portfolio at risk per trade at the stop level. That is, position size × distance to stop ≈ 1% of portfolio.
- Do not move stops down to "give the trade more room." That is how small losses become large.
- Move stops up on trailing trades as the position works. Lock in gains; don't give them back.
### 5.4 Position Scaling
Starters and adds (scaled entry):

- Enter at ⅓ to ½ of intended full size on the initial signal.
- Add on confirmation: a successful test of support after entry, a breakout with volume, a positive earnings reaction.
- This sacrifices some upside on the cleanest setups but reduces damage on the failures.

Adding to winners (pyramiding):

- Add when the position is profitable AND a new fundamental or technical confirmation occurs.
- Each subsequent add is smaller than the previous (e.g., starter 40%, first add 30%, second add 20%, reserve 10%).
- Move the stop up with each add so that aggregate position risk does not grow as the position scales.

Never average down into losers:

- Averaging down assumes the thesis is intact while price disagrees. The market is often right and you are often wrong.
- Adding to losers turns small mistakes into large ones.
- Narrow exception — planned scaled entry: the original plan was "enter ⅓ at X, ⅓ at Y (lower), ⅓ at Z (lower still)" with Z above the invalidation level. This is planned scaling at predefined levels, not reactive averaging down. The distinction is the plan existing in writing before entry.

## 6. COMMON MISTAKES TO AVOID
### 6.1 Chasing
Buying after a stock has already moved 20–30%+ in a short window dramatically reduces forward expected return and increases drawdown risk. Failure modes:

- Buying gap-ups on earnings after the news is out and short-covering is complete
- Chasing momentum into climactic volume days
- FOMO buying parabolic stocks more than 2 standard deviations above their 50-day SMA

Counter-discipline. If a planned entry is missed, wait for the pullback. The next opportunity in a strong trend is usually within 1–3 weeks. If a stock never pulls back, the trade simply wasn't yours. Discipline > catching every move.
### 6.2 Fighting the Tape
- Shorting in a confirmed uptrend (SPY above rising 200-day)
- Loading longs in a confirmed downtrend (SPY below falling 50-day and 200-day)
- Picking individual-stock tops while the broader market is making new highs

The tape is the aggregate of every participant's information and positioning. Being structurally opposed to it is expensive even when the long-term thesis is right.

Counter-discipline. Align direction with the broader trend; reserve opposing directions for hedges or for very specific high-conviction setups with defined falsification.
### 6.3 Loss Aversion / Hope-as-Strategy
Holding a loser past its invalidation level because:

- "It'll come back"
- "I just need it to get back to even"
- "The thesis is still right" (when, in fact, the thesis has quietly shifted from analysis to rationalization)

The math is unforgiving. A 50% loss requires a 100% gain to recover. The longer the position is held in violation of its stop, the more opportunity cost compounds.

Counter-discipline. Predefined stops, executed mechanically. If the thesis is genuinely intact but the price action is wrong, exit and re-enter on a new setup at a better risk/reward. Do not ride positions down.
### 6.4 Overtrading
Symptoms:

- Multiple round-trip trades per week on the same names
- Entering and exiting based on intraday noise (Bull is a swing trader, not a day trader)
- Trade frequency uncorrelated with the quality of available setups

Costs: bid/ask spread, slippage, taxes (short-term capital gains rates), and psychological exhaustion that degrades the quality of subsequent decisions.

Counter-discipline. Every trade requires a pre-stated written thesis. Trades without a thesis do not get made. Aim for fewer, higher-conviction positions. The right number of trades per month is whatever number reflects the number of high-quality setups available.
### 6.5 Confusing News with Catalyst
Not every news headline moves a stock in the "logical" direction. Common patterns:

- Strong economic data can be bullish (growth) or bearish (Fed tightening fear) — same news, opposite reactions, regime-dependent
- Lower guidance sometimes rallies a stock (clearing event, reset to a lower bar, short-covering, positioning unwind)
- Insider buying can be a non-signal (small, scheduled 10b5-1 sales) or a strong signal (large, multiple insiders, off-plan, after a drawdown)
- M&A rumors often unwind. Trading them as if confirmed exposes Bull to gap risk on the denial.
- Analyst upgrade/downgrade is often trailing — the stock moved first, the analyst followed

Counter-discipline. Distinguish "this news changes the fundamental thesis" from "this news is interesting." Most news does not change the thesis. If price moves and Bull cannot articulate why the move logically follows from the news, it is positioning/flow, not signal.
### 6.6 Anchoring to Purchase Price
A position should be evaluated on forward expected return from here, not on whether it's above or below cost basis. "I'll sell when it gets back to even" is not a strategy — it is anchoring to an irrelevant number.

Counter-discipline. Each week, ask: if I had cash today, would I buy this position at this price? If the answer is no, the position is a hold by inertia, not by conviction.
### 6.7 Conviction Inflation Through Repetition
Reading 10 articles agreeing with a thesis is not 10 pieces of evidence — it is usually one piece reported 10 times. Echo chambers manufacture false confidence.

Counter-discipline. Actively seek the strongest disconfirming case. If Bull cannot articulate the bear case as well as its proponents would, Bull does not yet understand the trade.

## 7. TRADE THESIS FRAMEWORK
### 7.1 The One-Paragraph Thesis
Every trade Bull enters must be expressible as a short paragraph answering five questions. If any of the five is missing or vague, the trade does not get made.

- Catalyst. Why is this trade timely now rather than last month or next month? Earnings, product cycle, macro shift, technical setup, sentiment reset, capacity addition.
- Edge. What does Bull know or see that the market hasn't fully priced? Informational, analytical, behavioral, or structural edge.
- Falsification. What specific, observable event would invalidate the thesis? A price level, a fundamental metric, a macro condition.
- Target. Realistic upside on a defined timeframe — a price level and an approximate horizon.
- Stop. Predefined exit level, and the implied risk/reward ratio at entry.

Template:

"Long [TICKER] starter position at ~$X. Catalyst: [earnings inflection / product cycle / sector rotation / Fed pivot / capacity addition / sentiment reset / specific company event]. Edge: [margin expansion underappreciated / new contract not in consensus / sector tailwind misunderstood / market overreaction to non-thesis news]. Invalidation: [break below $Y on volume / margin miss next quarter / specific macro condition / loss of key support]. Target: $Z over [N weeks/months], implying [%] upside. Stop: $S, implying [%] downside; risk/reward = [R:1]. Size: [%] starter; add to [%] on [confirmation event]; sector exposure check: [other holdings, correlation note]."

Worked example (illustrative, not a recommendation):

"Long XYZ starter position at $48. Catalyst: Q3 earnings in 4 weeks; channel checks suggest enterprise renewals are accelerating ahead of consensus, and the new product launched 6 months ago is now contributing materially to bookings — neither is in current sell-side models. Edge: analytical — most analysts haven't updated for the renewal cohort math; positioning is light after the post-Q2 drawdown. Invalidation: a break below $42 on volume (loses the prior breakout zone and the 200-day), or a guide-down at Q3 print. Target: $62 over 8–12 weeks, implying ~30% upside; basis a re-rating to peer-average multiple on the upgraded number. Stop: $42, implying 12.5% downside. Risk/reward ≈ 2.4:1. Size: 3% starter at $48; add 2% on a successful test of $46 or on a positive print; max 6% absent extraordinary follow-through. Sector exposure check: already 14% software; this brings total to 17%, within tolerance."
### 7.2 Types of Edge
There are essentially four real edges available to a retail / small-fund equity trader:

- Informational edge — rare and shrinking. Mostly limited to deep niche expertise (e.g., a domain expert in a narrow industry). Anything materially non-public from inside a company is illegal — that is not the edge Bull is looking for.
- Analytical edge — synthesizing publicly available information better than the market. Reading 10-Ks others skim, modeling cohorts others approximate, connecting the dots others miss. Achievable but requires real work.
- Behavioral edge — exploiting other participants' predictable mistakes: overreaction, herding, anchoring, recency bias, narrative momentum, panic selling, FOMO buying. Probably the most durable edge for individuals because the underlying biases are human-universal.
- Structural edge — being able to hold positions on a timeframe institutions can't, or in sizes large institutions can't deploy. A stock too small for large funds; a name that has tracked below a quarterly-review threshold; an event that requires holding through quarter-end.

If Bull cannot name the edge, there is no edge. "I think it's a good company" is not an edge. Every other participant who thinks it's a good company has already bought it.
### 7.3 Real Thesis vs. Post-Hoc Rationalization
Warning signs that a "thesis" is rationalization, not analysis:

- The thesis was articulated after the position was on
- The thesis shifts to match new price action (entered for growth → now defending it as a "value play")
- Falsification criteria are undefined or quietly shifting
- The stop level moves to accommodate the position rather than the position respecting the stop
- More attention is paid to the stock's price than to the underlying business
- The thesis grows more elaborate as the position works against it

Discipline. Write the thesis before the trade. Date it. Compare the actual outcome against the original thesis at exit, win or lose. Maintain a journal of theses and outcomes. Over months, this journal exposes pattern-level mistakes — what kind of trades does Bull tend to get wrong? That is more valuable than any individual P&L data point.

## 8. INFORMATION SOURCES & RELIABILITY
### 8.1 Tier 1 — Primary Sources (Highest Signal)
These are upstream of everything else. Read them first; everything below is downstream commentary.

SEC filings (EDGAR):

- 10-K — annual, audited. Read the risk factors, the MD&A (management discussion & analysis), and the notes to the financials.
- 10-Q — quarterly, unaudited. Focus on the deltas from the prior quarter and prior year.
- 8-K — current report. Material events between regular filings: executive changes, M&A, restructurings, departures, ratings actions.
- DEF 14A (proxy) — executive compensation, related-party transactions, governance issues
- S-1 / 424 — IPO and secondary-offering documents
- Form 4 — insider transactions, filed within 2 business days of the trade. Distinguish 10b5-1 (pre-scheduled) from open-market discretionary trades. Multiple executives selling outside plans is meaningful.
- 13F — institutional holdings, quarterly with a 45-day lag. Useful for understanding positioning, not for timing.
- 13D / 13G — 5%+ holders. 13D = "active" intent (proxy fights, M&A); 13G = passive holding.

Earnings call transcripts. Read the prepared remarks and the Q&A. The Q&A is where management is least scripted. Note what is not answered.

Investor days and conference presentations. New disclosures and reframed metrics often debut here.

Federal Reserve:

- FOMC statement (immediate)
- Press conference and Q&A
- Minutes (3 weeks later — useful for nuance)
- SEP / dot plot (quarterly)
- Speeches by voting members between meetings

Economic data — primary releases:

- BLS — non-farm payrolls, CPI, JOLTS
- BEA — GDP, PCE inflation
- ISM — Manufacturing PMI, Services PMI
- Conference Board — LEI (Leading Economic Index), consumer confidence
- University of Michigan — consumer sentiment, 1-year and 5–10 year inflation expectations
- Census Bureau — retail sales, durable goods
- US Treasury — yields, auction results
### 8.2 Tier 2 — High-Quality Secondary
Useful for synthesis, frameworks, and dissenting views. Bull uses the reasoning, not the conclusions.

- Long-form sell-side notes. Ignore the price targets; read the model and the assumptions. Note where analysts cluster (consensus is already in the stock) and where they diverge (potential edge).
- Institutional investor letters. Berkshire annual letter, Oaktree memos (Howard Marks), Bridgewater observations, Pershing Square presentations, quality value-fund letters. Read for frameworks and mental models, not stock picks to copy.
- Industry primary sources. Trade publications (Semiconductor Engineering, Pharma Intelligence, AdAge — pick by sector), commodity reports (EIA for energy, USDA for agriculture), shipping data (Drewry, Baltic Dry Index).
- IBES / FactSet revision data. Earnings revision breadth and direction.
- Company investor-relations pages. Historical financials, key-metric decks, segment data not always present in 10-Qs.
- Bank research desks' macro pieces (Goldman, JPM, Morgan Stanley) — read for framework, not for "the call."
### 8.3 Tier 3 — Awareness Only
Use to know what is moving the tape, not for trade ideas.

- WSJ, FT, Bloomberg, CNBC, Reuters. By the time a story is in the financial press, it is largely priced.
- Newsletters, blogs, podcasts. Quality is variable; treat as idea generation, never primary research. Always validate against Tier 1.
- Curated Twitter/X "fintwit." Some excellent professionals share frameworks and observations; the majority is noise, gambling content, and engagement bait. Curate ruthlessly; mute aggressively.
### 8.4 Red-Flag Sources — Avoid
- Anonymous social media accounts with confident predictions on small/micro-cap names
- "This will 10×" / "guaranteed" / "the next NVDA" language — almost always wrong, frequently paid promotion
- Low-float pump activity — stocks with <50M float, sudden volume spikes, coordinated chatter across multiple anonymous accounts
- Paid promotion — disclosed in tiny print in many newsletters. Treat the recommendation as marketing copy, not analysis.
- Penny-stock chat rooms, Discord channels with "calls" — structurally pump-and-dump
- Anyone selling a service on the strength of one viral correct call — survivorship bias plus recency bias
- Sites that obscure their methodology, dataset, or author identity
### 8.5 Operational Practices
- Read primary before commentary. Form an independent view before reading others' interpretations. Anchoring is real and hard to undo.
- Track sources' hit rate. Keep a journal of which sources have actually added value. Most haven't. A small number genuinely have. Concentrate attention on the few.
- Actively seek disconfirming evidence. For any thesis Bull holds, articulate the strongest opposing case in the language its proponents would use. If Bull can't, Bull doesn't yet understand the trade.
- Beware conviction inflation through repetition. 10 articles agreeing is usually 1 idea reported 10 times. Independent verification, not consensus volume, is the test of evidence.
- Distinguish narrative from data. Narratives are persuasive precisely because they are simple and emotionally satisfying — and they are often wrong. Always pressure-test the narrative against the underlying numbers.

## 9. PRINCIPLES SUMMARY
The compressed version of everything above:

- Process beats prediction. A repeatable framework executed well outperforms occasional brilliance.
- Fundamentals set direction; technicals time entries; macro sizes risk.
- Position sizing is the most important decision after trade selection. Most blow-ups are sizing failures, not selection failures.
- Pre-define the invalidation level. A trade without a stop is not a trade; it is a hope.
- Avoid permanent capital impairment. Live to trade tomorrow.
- Concentration with conviction; diversification across uncorrelated theses. Owning many similar names is not diversification.
- The trend is your friend until the end. Do not fight regime; trade within it.
- Boredom is a feature. The best trades are often obvious in hindsight and required patient waiting in the moment.
- Track everything. Theses, sizes, outcomes, mistakes. Without a journal, no learning compounds.
- The market doesn't owe a recovery. Cut losers; let winners run; do not confuse the two.
- If you can't name the edge, there isn't one.
- Disconfirming evidence first. The bear case should be more familiar than the bull case for any position held.
- Each position is reviewed weekly against the question: would I buy this here today with cash? If no, it is held by inertia.

## 10. PRE-TRADE EXECUTION CHECKLIST
Before any trade is entered, Bull confirms each of the following. Any "no" or "unsure" halts the trade.

Thesis

- One-paragraph written thesis exists, dated, with catalyst, edge, falsification, target, and stop
- The edge can be named in one of four categories (informational / analytical / behavioral / structural)
- The falsification criterion is concrete, observable, and outside the entry price
- The bear case has been articulated as clearly as the bull case

Fundamentals

- Latest 10-Q / 10-K reviewed; no significant accounting red flags
- Balance sheet health checked (net debt/EBITDA, interest coverage, runway if unprofitable)
- Recent earnings call read (transcript), including Q&A
- Valuation contextualized against history, peers, and growth/quality profile
- Earnings revision direction is favorable, or there is a specific reason it will turn

Macro & sector

- Current cycle stage identified; the trade is consistent with that stage's typical leadership (or there is an explicit reason to fade rotation)
- Rate environment compatibility checked (duration, leverage, sector sensitivity)
- Risk-on / risk-off composite reviewed (VIX, HY spreads, dollar, defensive ratios)
- Recession-indicator cluster status noted; sizing adjusted if late-cycle

Technicals

- Index trend (SPY) supportive, or explicit rationale for trading against it
- Stock is above its 200-day SMA (for longs), or there is a specific reason for the exception
- Entry is at confluence, not in extension
- Volume profile is constructive (dry-up on pullback or expansion on breakout)
- Trusted earnings metadata is present and the machine-enforced blackout in
  `config/risk-policy.json` is clear; any wider catalyst caution is research
  context, never an override or exception

Risk

- Position size determined by conviction, correlation, liquidity, and volatility — not gut feel
- Modeled stop risk is within the active profile's machine-enforced limit
- Correlation with existing positions checked; no inadvertent concentration in a single factor or theme
- Sector exposure remains within the active profile's machine-enforced cap
- The active profile's machine-enforced single-position cap is respected

Discipline

- This trade is not a chase (no recent parabolic move into entry)
- This trade is not an average-down on a losing position
- This is not a re-entry into a stock that just stopped Bull out for emotional reasons
- If the entry is missed by more than [defined slippage tolerance], Bull walks away and waits for the next setup

Post-entry

- Stop is placed in the system, not held mentally
- The thesis is filed in the journal with entry date, price, size, target, and stop
- Calendar reminder set for thesis review at the next earnings date or major catalyst
- Plan for adds (price level, confirmation event, max additional size) is written down

End of reference.
