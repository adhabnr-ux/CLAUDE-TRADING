# Aggressive Bull — Portfolio Snapshot

_Updated by every aggressive routine from live Alpaca data (the **separate**
aggressive paper account). The next agent trusts this as the last known state
but always re-fetches live data before trading._

---

## Inception baseline

| Field | Value |
|---|---|
| Inception date | 2026-06-04 |
| Starting equity | USD 100,000.00 |
| SPY anchor price | 754.18 (June 3, 2026 close) |
| Benchmark (SPY) | tracked from this anchor for all "vs SPY" calculations |

---

## Last snapshot — 2026-06-12 market-open (~9:46 AM ET)

| Field | Value |
|---|---|
| Equity | USD 93,469.93 |
| Cash | USD 13,885.38 |
| Long market value | USD 79,584.55 |
| Open positions | 7 |
| last_equity (prev close June 11) | USD 94,130.22 |
| Today's change vs last_equity | -USD 660.29 (-0.70%) |
| HWM | USD 101,144.73 |
| Drawdown from HWM | -7.59% (circuit breaker: 20% — NOT triggered) |

**Open positions:**

| Symbol | Qty | Avg Entry | Price | Market Value | Unrealized P/L | P/L % | -12% Cut Trigger | Buffer | Trailing Stop Order | Stop Price |
|---|---|---|---|---|---|---|---|---|---|---|
| NVDA | 103 | USD 213.60 | USD 204.09 | USD 21,021.27 | -USD 979.53 | -4.45% | USD 187.97 | 7.55pp | `54d7d851` | USD 181.71 |
| META | 23 | USD 630.12 | USD 563.85 | USD 12,968.55 | -USD 1,524.21 | **-10.52%** | USD 554.51 | **🔴 1.48pp** | `11c3a1bf` | USD 526.75 |
| AVGO | 34 | USD 406.23 | USD 380.50 | USD 12,937.00 | -USD 874.82 | -6.33% | USD 357.48 | 5.67pp | `36f5a45f` | USD 349.71 |
| MSFT | 28 | USD 426.21 | USD 384.34 | USD 10,761.52 | -USD 1,172.36 | **-9.82%** | USD 375.06 | **2.18pp ⚠️** | `ef211767` | USD 350.56 |
| AMZN | 36 | USD 247.99 | USD 235.04 | USD 8,461.26 | -USD 466.42 | -5.22% | USD 218.23 | 6.76pp | `b55bef05` | USD 205.35 |
| VST | 52 | USD 151.47 | USD 147.66 | USD 7,678.32 | -USD 198.12 | -2.52% | USD 133.29 | 9.49pp | `5b347be3` | USD 124.57 |
| GOOGL | 16 | USD 370.22 | USD 356.23 | USD 5,699.68 | -USD 223.84 | -3.78% | USD 325.79 | 8.22pp | `e52a43f1` | USD 304.81 |

**Stop audit (2026-06-12 market-open): ALL 7 positions confirmed with live 18% trailing stop orders. ✓**
_(Stop prices unchanged — no position has made a new high since stops were set; all stops remain at their last-recorded levels.)_

| Symbol | Stop Order ID | Stop Price | HWM | Status |
|---|---|---|---|---|
| NVDA | `54d7d851` | USD 181.71 | USD 221.60 | ✓ live |
| META | `11c3a1bf` | USD 526.75 | USD 642.38 | ✓ live |
| AVGO | `36f5a45f` | USD 349.71 | USD 426.48 | ✓ live |
| MSFT | `ef211767` | USD 350.56 | USD 427.51 | ✓ live |
| AMZN | `b55bef05` | USD 205.35 | USD 250.43 | ✓ live |
| VST | `5b347be3` | USD 124.57 | USD 151.91 | ✓ live |
| GOOGL | `e52a43f1` | USD 304.81 | USD 371.72 | ✓ live |

**Sector exposure summary (journaled decision — intentional concentration):**
| Sector | Market Value | % of Portfolio |
|---|---|---|
| Technology (NVDA, META, AVGO, MSFT, AMZN, GOOGL) | USD 71,849.28 | 76.9% |
| Utilities/Energy (VST) | USD 7,678.32 | 8.2% |
| Cash | USD 13,885.38 | 14.9% |
_Technology overweight is BY DESIGN for Aggressive Bull — concentrated AI-supercycle thesis. VST provides non-correlated diversification via nuclear power PPAs._

**Thesis contracts (2026-06-12 market-open status):**
| Symbol | Invalidation | Review By | Status |
|---|---|---|---|
| NVDA | NVDA loses a major hyperscaler customer OR Q2 FY2027 guide drops below USD 80B | 2026-06-25 | ✓ INTACT — Helix Digital Infrastructure consortium (KKR+NVDA+VST+KIA >USD 10B); -4.45% from entry; analyst target USD 298.42 |
| META | Meta formally confirms equity offering AND management explicitly downgrades AI monetization | **2026-06-17** | ✓ INTACT — no banks hired, no confirmation per WebSearch June 12; ad revenue +33% thesis intact; **-10.52%, 🔴 1.48pp buffer**; review_by June 17 = 3 trading days. Midday MUST check META first. |
| AVGO | AI revenue guide cut below USD 12B for next quarter OR Q3 total revenue miss >10% | 2026-06-25 | ✓ INTACT — AI XPV Platform USD 35B with Apollo/Blackstone; -6.33% from entry; analyst target USD 522 |
| MSFT | Azure growth decelerates below 30% YoY OR Copilot explicitly called underperforming | 2026-06-25 | ✓ INTACT — Azure accelerating, Build 2026 confirmed; **-9.82% from entry, 2.18pp buffer ⚠️**; Xbox memo immaterial |
| AMZN | AWS growth decelerates to <20% YoY OR Trainium adoption fails hyperscaler traction | 2026-06-22 | ✓ INTACT — Claude Fable 5 on Amazon Bedrock; -5.22% from entry; analyst target USD 312.71 |
| VST | Nuclear PPAs with Meta/AWS cancelled or renegotiated; OR material regulatory action vs nuclear fleet | 2026-07-15 | ✓ INTACT — Helix consortium (KKR+NVDA+VST); ex-div June 22; oil -20% from peak (neutral-to-minor headwind vs prior narrative) |
| GOOGL | GCP growth decelerates below 40% YoY OR AI investment plan explicitly cut | 2026-06-25 | ✓ INTACT — GCP +63% YoY; -3.78% from entry; analyst avg target USD 428.15 |

**CRITICAL watchpoints for remainder of June 12 session:**
1. 🔴 META at -10.52% (USD 563.85) → **1.48pp buffer** to -12% forced cut (USD 554.51). META is -0.81% today. No new equity offering news (no banks hired per June 12 WebSearch). Invalidation NOT triggered. Midday routine MUST check META price FIRST. A 1.7% further decline forces the cut.
2. ⚠️ MSFT at -9.82% (USD 384.34) → **2.18pp buffer** to forced cut (USD 375.06). MSFT down -1.54% today. Xbox memo immaterial. A 2.4% further decline forces the cut.
3. SpaceX IPO (SPCX) trading today — potential tech liquidity absorption.
4. Iran 60-day ceasefire: oil down. Risk-on generally.

---

## Planned next positions

- **No new positions until META buffer widens above 4pp or is resolved.** Cash USD 13,885 maintained as buffer.
- **AMD re-entry**: AMD last held at USD 508.43 entry; cut at USD 440.92 (-13.28%). Re-entry only after AMD recovers above USD 508. Do not average down.
- **MSFT dividend**: USD 0.91/share × 28 = USD 25.48 received June 11 (already in cash).

---

## SPY performance tracker

| Date | Aggro equity | SPY close | Aggro return | SPY return since inception | Alpha |
|---|---|---|---|---|---|
| 2026-06-04 (inception) | 100,000 | 754.18 | 0.00% | 0.00% | 0.00% |
| 2026-06-04 (market-open) | 100,009.58 | — | +0.01% | — | — |
| 2026-06-04 (midday) | 100,911.69 | — | +0.91% | — | — |
| 2026-06-04 (EOD close) | 100,993.61 | 757.16 | +0.99% | +0.40% | **+0.60%** |
| 2026-06-05 (pre-market) | 100,139.18 | — | +0.14% | — | — |
| 2026-06-05 (market-open) | 99,407.74 | — | -0.59% | — | — |
| 2026-06-05 (midday) | 97,571.05 | — | -2.43% | — | — |
| 2026-06-05 (EOD close) | 96,234.84 | 737.41 | -3.77% | -2.22% | **-1.55%** |
| 2026-06-05 (weekly review) | 96,193.58 | 737.45 | -3.81% | -2.22% | **-1.59%** |
| 2026-06-08 (pre-market) | 97,687.25 | — | -2.32% | — | — |
| 2026-06-08 (market-open) | 97,455.37 | — | -2.54% | — | — |
| 2026-06-08 (midday) | 97,033.54 | — | -2.97% | — | — |
| 2026-06-08 (EOD close) | 97,102.72 | 739.22 | -2.90% | -1.98% | **-0.91pp** |
| 2026-06-09 (pre-market) | 97,715.46 | ~742.30 (pre-mkt) | -2.28% | ~-1.57% | **~-0.71pp** |
| 2026-06-09 (market-open) | 98,044.78 | ~746.14 (intraday) | -1.96% | ~-1.07% | **~-0.89pp** |
| 2026-06-09 (midday) | 93,506.59 | ~723.44 (intraday) | -6.49% | ~-4.08% | **~-2.41pp** |
| 2026-06-09 (EOD close) | 95,762.44 | 737.11 | -4.24% | -2.26% | **-1.98pp** |
| 2026-06-10 (pre-market) | 94,388.86 | — | **-5.61%** | — | — |
| 2026-06-10 (market-open) | 94,721.05 | ~737.11 (prev close) | **-5.28%** | -2.26% | **-3.02pp** |
| 2026-06-10 (midday) | 93,840.73 | — | **-6.16%** | — | — |
| 2026-06-10 (EOD close) | 92,912.82 | 725.43 | **-7.09%** | -3.81% | **-3.28pp** |
| 2026-06-11 (pre-market) | 93,604.88 | — | **-6.40%** | — | — |
| 2026-06-11 (market-open) | 93,115.96 | — | **-6.88%** | — | — |
| 2026-06-11 (midday) | 92,974.10 | — | **-7.03%** | — | — |
| 2026-06-11 (EOD close) | **94,155.63** | **737.76** | **-5.84%** | **-2.18%** | **-3.66pp** |
| 2026-06-12 (pre-market) | **94,898.51** | ~741.94 (pre-mkt) | **-5.10%** | ~-1.62% | **~-3.48pp** |
| 2026-06-12 (market-open) | **93,469.93** | ~735.58 (intraday) | **-6.53%** | ~-2.47% | **~-4.06pp** |
