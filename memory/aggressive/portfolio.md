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

## Last snapshot — 2026-06-16 MIDDAY (~12:41 PM ET)

| Field | Value |
|---|---|
| Equity | USD 96,060.12 |
| Cash | USD 6,553.24 (6.82%) |
| Long market value | USD 89,506.88 |
| Open positions | 8 |
| last_equity (June 15 EOD) | USD 97,144.23 |
| Intraday P/L vs last_equity | -USD 1,084.11 (-1.115%) — FOMC-day softness; AVGO -3.945%, MRVL -5.565% intraday |
| HWM | USD 101,144.73 |
| Drawdown from HWM | -5.03% (circuit breaker: 20% — NOT triggered; 14.97pp of headroom) |

**Open positions (2026-06-16 midday ~12:41 PM ET):**

| Symbol | Qty | Avg Entry | Midday Price | Market Value | Unrealized P/L | P/L % | -12% Cut Trigger | Buffer |
|---|---|---|---|---|---|---|---|---|
| NVDA | 103 | USD 213.60 | USD 208.72 | USD 21,498.16 | -USD 502.64 | -2.285% | USD 187.97 | 9.715pp |
| META | 23 | USD 630.12 | USD 596.745 | USD 13,725.14 | -USD 767.63 | -5.297% | USD 554.51 | **6.703pp** ✅ |
| AVGO | 34 | USD 406.23 | USD 378.40 | USD 12,865.60 | -USD 946.22 | **-6.851%** | USD 357.48 | **5.149pp ⚠️** |
| MSFT | 28 | USD 426.21 | USD 392.09 | USD 10,978.52 | -USD 955.36 | **-8.005%** | USD 375.06 | **3.995pp ⚠️** |
| AMZN | 36 | USD 247.99 | USD 246.97 | USD 8,890.92 | -USD 36.76 | -0.412% | USD 218.23 | 11.588pp |
| VST | 52 | USD 151.47 | USD 159.635 | USD 8,301.02 | +USD 424.58 | **+5.391% ✅** | USD 133.29 | 17.391pp |
| GOOGL | 16 | USD 370.22 | USD 371.745 | USD 5,947.92 | +USD 24.40 | +0.412% ✅ | USD 325.79 | 12.412pp |
| MRVL | 25 | USD 293.29 | USD 291.69 | USD 7,292.25 | -USD 39.88 | -0.544% | USD 258.09 | 11.456pp |

**Stop audit (2026-06-16 midday): ALL 8 positions confirmed with live 18% trailing stop orders. ✓**

| Symbol | Stop Order ID | HWM | Stop Price | Status |
|---|---|---|---|---|
| NVDA | `54d7d851` | USD 221.60 | USD 181.712 | ✓ live |
| META | `11c3a1bf` | USD 642.38 | USD 526.7516 | ✓ live |
| AVGO | `36f5a45f` | USD 426.48 | USD 349.7136 | ✓ live |
| MSFT | `ef211767` | USD 427.51 | USD 350.5582 | ✓ live |
| AMZN | `b55bef05` | USD 250.43 | USD 205.3526 | ✓ live |
| VST | `5b347be3` | USD 160.2599 (new ATH ✅) | USD 131.4131 | ✓ live — stop ratcheting |
| GOOGL | `e52a43f1` | USD 375.77 (new ATH ✅) | USD 308.1314 | ✓ live — stop ratcheting |
| MRVL | `a9097c8c` | USD 316.99 | USD 259.9318 | ✓ live |

**Sector exposure (midday June 16):**
| Sector | Market Value | % of Portfolio |
|---|---|---|
| Technology — semis (NVDA, AVGO, MRVL) | USD 42,161.76 | 43.9% |
| Technology — hyperscalers (META, MSFT, AMZN, GOOGL) | USD 39,541.58 | 41.2% |
| Utilities/Energy (VST) | USD 8,301.02 | 8.6% |
| Cash | USD 6,553.24 | 6.82% |
_FOMC-day: broad AI-tech softness. MSFT 3.995pp from cut (watchpoint; shareholder lawsuit nuisance, Azure 40% intact). AVGO 5.149pp. VST and GOOGL set new ATH HWMs today. No positions cut. No stops recreated._

**Thesis contracts (updated 2026-06-16 midday):**
| Symbol | Invalidation | Review By | Status |
|---|---|---|---|
| NVDA | NVDA loses a major hyperscaler customer OR Q2 FY2027 guide drops below USD 80B | 2026-06-25 | ✓ INTACT — -2.285% from entry; 9.715pp buffer |
| META | Meta formally confirms equity offering AND management explicitly downgrades AI monetization | 2026-06-24 | ✓ INTACT — -5.297%; buffer 6.703pp ✅; Arete upgraded to Buy/USD 735 |
| AVGO | AI revenue guide cut below USD 12B for next quarter OR Q3 total revenue miss >10% | 2026-06-25 | ✓ INTACT — USD 16B Q3 guide; -6.851% from entry; 5.149pp buffer |
| MSFT | Azure growth decelerates below 30% YoY OR Copilot explicitly called underperforming | 2026-06-25 | ✓ INTACT — Azure +40%; shareholder lawsuit nuisance; -8.005%; 3.995pp buffer ⚠️ |
| AMZN | AWS growth decelerates to <20% YoY OR Trainium adoption fails hyperscaler traction | 2026-06-22 | ✓ INTACT — AWS +28%; -0.412%; 11.588pp buffer. ⚠️ Review June 22 (6 days). |
| VST | Nuclear PPAs with Meta/AWS cancelled or renegotiated; OR material regulatory action vs nuclear fleet | 2026-07-15 | ✓ INTACT — +5.391% ✅; HWM USD 160.26 new ATH; ex-div June 22 |
| GOOGL | GCP growth decelerates below 40% YoY OR AI investment plan explicitly cut | 2026-06-25 | ✓ INTACT — GCP +63%; +0.412%; HWM USD 375.77 new ATH |
| MRVL | MRVL loses major hyperscaler custom chip program OR revenue growth <15% YoY OR CFO transition causes material disruption | 2026-06-29 | ✓ INTACT — S&P 500 inclusion June 22; -0.544% from entry (well within range despite -5.565% today) |

---

## Prior snapshot — 2026-06-16 MARKET OPEN (~9:46 AM ET)

| Field | Value |
|---|---|
| Equity | USD 97,032.20 |
| Cash | USD 6,553.24 (6.75%) |
| Long market value | USD 90,478.96 |
| Open positions | 8 |
| last_equity (June 15 EOD) | USD 97,144.23 |
| Intraday P/L vs last_equity | -USD 112.03 (-0.115%) — minor intraday softness; FOMC in session (hold expected) |
| HWM | USD 101,144.73 |
| Drawdown from HWM | -4.07% (circuit breaker: 20% — NOT triggered; 15.93pp of headroom) |

### Prior snapshot — 2026-06-16 PRE-MARKET (~8:12 AM ET)

| Field | Value |
|---|---|
| Equity | USD 97,030.05 |
| Cash | USD 6,553.24 (6.75%) |
| Long market value | USD 90,476.81 |
| Open positions | 8 |
| last_equity (June 15 EOD) | USD 97,144.23 |
| Pre-market P/L vs last_equity | -USD 114.18 (-0.12%) — minor overnight softness; FOMC in session |
| HWM | USD 101,144.73 |
| Drawdown from HWM | -4.07% (circuit breaker: 20% — NOT triggered; 15.93pp of headroom) |

### Prior snapshot — 2026-06-15 EOD (~4:07 PM ET)

| Field | Value |
|---|---|
| Equity | USD 97,186.26 |
| Cash | USD 6,553.25 (6.74%) |
| Long market value | USD 90,633.01 |
| Open positions | 8 |
| last_equity (prev close June 12 EOD) | USD 94,031.31 |
| Today's P/L | +USD 3,154.95 (+3.356%) — Iran peace deal / Hormuz reopen full risk-on rally |
| HWM | USD 101,144.73 |
| Drawdown from HWM | -3.91% (circuit breaker: 20% — NOT triggered; 16pp of headroom) |

**Open positions (2026-06-16 market-open ~9:46 AM ET):**

| Symbol | Qty | Avg Entry | Open Price | Market Value | Unrealized P/L | P/L % | -12% Cut Trigger | Buffer |
|---|---|---|---|---|---|---|---|---|
| NVDA | 103 | USD 213.60 | USD 209.83 | USD 21,612.49 | -USD 388.31 | -1.765% | USD 187.97 | 10.23pp |
| META | 23 | USD 630.12 | USD 601.50 | USD 13,834.50 | -USD 658.26 | -4.542% | USD 554.51 | **7.46pp** ✅ |
| AVGO | 34 | USD 406.23 | USD 387.97 | USD 13,190.98 | -USD 620.84 | -4.495% | USD 357.48 | 7.50pp |
| MSFT | 28 | USD 426.21 | USD 393.285 | USD 11,011.98 | -USD 921.90 | -7.725% | USD 375.06 | **4.28pp ⚠️** |
| AMZN | 36 | USD 247.99 | USD 247.07 | USD 8,894.52 | -USD 33.16 | -0.371% | USD 218.23 | 11.63pp |
| VST | 52 | USD 151.47 | USD 157.99 | USD 8,215.48 | +USD 339.04 | **+4.304% ✅** | USD 133.29 | 16.31pp |
| GOOGL | 16 | USD 370.22 | USD 367.925 | USD 5,886.80 | -USD 36.72 | -0.620% | USD 325.79 | 11.38pp |
| MRVL | 25 | USD 293.285 | USD 312.13 | USD 7,803.25 | +USD 471.12 | **+6.425% ✅** | USD 258.09 | 18.43pp |

**Stop audit (2026-06-16 market-open): ALL 8 positions confirmed with live 18% trailing stop orders. ✓**
_(All positions show qty_available=0, confirming trailing stop orders hold all shares.)_

| Symbol | Stop Order ID | Stop Price | HWM | Status |
|---|---|---|---|---|
| NVDA | `54d7d851` | USD 181.71 | USD 221.60 | ✓ live |
| META | `11c3a1bf` | USD 526.75 | USD 642.38 | ✓ live |
| AVGO | `36f5a45f` | USD 349.71 | USD 426.48 | ✓ live |
| MSFT | `ef211767` | USD 350.56 | USD 427.51 | ✓ live |
| AMZN | `b55bef05` | USD 205.35 | USD 250.43 | ✓ live |
| VST | `5b347be3` | USD 130.03 | USD 158.57 (new HWM today ✅) | ✓ live — stop ratcheting |
| GOOGL | `e52a43f1` | USD 305.85 | USD 372.99 | ✓ live |
| MRVL | `a9097c8c` | USD 256.64 | USD 312.98 (new HWM ✅) | ✓ live — stop ratcheting |

**Sector exposure summary (2026-06-16 market-open — intentional concentration):**
| Sector | Market Value | % of Portfolio |
|---|---|---|
| Technology — semis (NVDA, AVGO, MRVL) | USD 42,607 | 43.9% |
| Technology — hyperscalers (META, MSFT, AMZN, GOOGL) | USD 39,628 | 40.8% |
| Utilities/Energy (VST) | USD 8,215 | 8.5% |
| Cash | USD 6,553 | 6.75% |
_Semi-group (NVDA+AVGO+MRVL) at 43.9% — within 50% cap. Three positions in profit: MRVL +6.43%, VST +4.30%. META buffer 7.46pp (safe zone). MSFT 4.28pp (watchpoint; FOMC pressure). Cash 6.75% above 2% floor. FOMC in session — no deployment today._

**Thesis contracts (updated 2026-06-16 pre-market):**
| Symbol | Invalidation | Review By | Status |
|---|---|---|---|
| NVDA | NVDA loses a major hyperscaler customer OR Q2 FY2027 guide drops below USD 80B | 2026-06-25 | ✓ INTACT — -0.71% from entry; 11.29pp buffer; Annual Meeting June 24 (not earnings); bond issuance minor |
| META | Meta formally confirms equity offering AND management explicitly downgrades AI monetization | 2026-06-24 | ✓ INTACT — buffer 6.32pp; no offering confirmed; thesis contract renewed June 15 |
| AVGO | AI revenue guide cut below USD 12B for next quarter OR Q3 total revenue miss >10% | 2026-06-25 | ✓ INTACT — Q3 guide ~USD 16B; AI XPV Platform; -2.99% from entry; 9.01pp buffer |
| MSFT | Azure growth decelerates below 30% YoY OR Copilot explicitly called underperforming | 2026-06-25 | ✓ INTACT — Azure +40%; Quantum milestone (Quantinuum); Citi USD 605 watch; -6.97% from entry; 5.03pp buffer |
| AMZN | AWS growth decelerates to <20% YoY OR Trainium adoption fails hyperscaler traction | 2026-06-22 | ✓ INTACT — AWS +28%; Prime Day June 23-26; -0.14% from entry; 11.86pp buffer. ⚠️ Review June 22 (6 days). |
| VST | Nuclear PPAs with Meta/AWS cancelled or renegotiated; OR material regulatory action vs nuclear fleet | 2026-07-15 | ✓ INTACT — Helix consortium; ex-div June 22; +1.81% from entry ✅; 15.51pp buffer; oil USD 83 (narrative not fundamental) |
| GOOGL | GCP growth decelerates below 40% YoY OR AI investment plan explicitly cut | 2026-06-25 | ✓ INTACT — GCP +63% YoY; USD 1.5B Alabama data center expansion; -0.30% from entry (near-flat); 11.70pp buffer |
| MRVL | MRVL loses major hyperscaler custom chip program OR revenue growth <15% YoY OR CFO transition causes material disruption | 2026-06-29 | ✓ INTACT — S&P 500 inclusion June 22 catalyst; +3.93% from entry ✅; 14.93pp buffer; B. Riley target USD 345 |

**Week 3 conviction ratings (pre-market June 16):**
| Symbol | Rating | Notes |
|---|---|---|
| NVDA | **A** | Core AI GPU thesis; 11.29pp buffer; Annual Meeting June 24 (not earnings); bond issuance minor |
| AVGO | **A** | AI XPV Platform; Q3 USD 16B guide; 9.01pp buffer |
| AMZN | **A** | AWS +28%; Prime Day June 23-26; 11.86pp buffer; review_by June 22 (6 days) |
| GOOGL | **A** | GCP +63%; USD 1.5B Alabama data center; 11.70pp buffer |
| VST | **A** | Helix consortium; ex-div June 22; +1.81% in profit ✅; 15.51pp buffer; oil at USD 83 (PPAs fixed-rate) |
| MRVL | **A** | S&P 500 inclusion June 22; Jensen Huang "next trillion-dollar co."; +3.93% ✅; 14.93pp buffer |
| META | **B** | Ad +33%; no offering confirmed; 6.32pp buffer (safe zone); review_by June 24 |
| MSFT | **B** | Azure +40%; Quantum milestone (Quantinuum); 5.03pp buffer; review_by June 25 |

**No C-rated positions.**

**Key notes for Week 3 (market-open June 16):**
1. MRVL: S&P 500 inclusion June 22 — index funds must own by June 20 close. "Massive news" confirmed (Motley Fool June 16). FY2028 outlook raised to USD 16.5B.
2. FOMC in session June 16–17. Expected hold at 3.50–3.75%. First meeting under new Chair Kevin Warsh. Decision tomorrow. MSFT softness (-1.62% intraday) reflects FOMC growth-multiple compression — not a thesis break.
3. Iran deal SIGNED: Full Hormuz reopening + 60-day nuclear talks. Oil Brent USD 83. Macro overhang fully resolved.
4. VST ex-dividend June 22 (USD 0.229/share × 52 = USD 11.91 incoming to cash). New HWM USD 158.57 today — stop ratcheting up.
5. AMZN review_by June 22 — pre-market June 22 must include explicit hold/trim/exit decision.
6. META buffer: 7.46pp (comfortable; well above 4pp threshold). MSFT: 4.28pp (watchpoint — midday must check).
7. AMD re-entry: blocked until AMD recovers above USD 508.43.
8. No trades today: FOMC uncertainty + stop audit passed 8/8 + all 8 theses intact.

---

## Planned next positions

- **MRVL entered June 15 market-open**: 25 shares @ USD 293.29; 18% trailing stop `a9097c8c`; review_by June 29. Up +5.0% on Day 1.
- **AMD re-entry**: AMD cut at USD 440.92 (-13.28%). Re-entry only after AMD recovers above USD 508.43. Do not average down.
- **Cash at 6.74%** — above 2% floor; no immediate deployment pressure. 8 positions open, 1/8 new positions used Week 3.
- **Dividends received:** MSFT USD 0.91/share × 28 = USD 25.48 (June 11); GOOGL USD 0.22/share × 16 = USD 3.52 (June 15); META USD 0.525/share × 23 = USD 12.08 (June 15). All in cash.
- **Next thesis contracts due:** AMZN review_by June 22 (pre-market June 22 must include explicit hold/trim/exit decision and contract renewal); VST ex-dividend June 22; META review_by June 24.

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
| 2026-06-12 (midday) | **93,959.99** | — | **-6.04%** | — | — |
| 2026-06-12 (EOD close) | **94,051.73** | **741.02** | **-5.95%** | **-1.75%** | **-4.20pp** |
| 2026-06-12 (weekly review) | **94,070.42** | **741.75** | **-5.93%** | **-1.65%** | **-4.28pp** |
| 2026-06-15 (pre-market) | **95,643.72** | ~**760+** (est, Iran ceasefire risk-on +1%) | **-4.36%** | ~**+0.77%** (est) | **~-5.13pp** (est) |
| 2026-06-15 (market-open) | **~96,202** | ~**760** (Iran ceasefire +~2.5%) | **~-3.80%** | ~**+0.77%** (est) | **~-4.57pp** (est) |
| 2026-06-15 (midday) | **97,007.87** | **756.15** | **-2.99%** | **+0.26%** | **-3.25pp** |
| 2026-06-15 (EOD close) | **97,186.26** | **754.83** | **-2.814%** | **+0.086%** | **-2.90pp** |
| 2026-06-16 (pre-market) | **97,030.05** | ~**763** (est, futures +1.22%) | **-2.970%** | ~**+1.17%** (est) | **~-4.14pp** (est; SPY futures driving benchmark up) |
| 2026-06-16 (market-open) | **97,032.20** | ~**763+** (est; Iran deal + FOMC) | **-2.968%** | ~**+1.17%** (est) | **~-4.14pp** (est) |
| 2026-06-16 (midday) | **96,060.12** | **753.07** | **-3.940%** | **-0.147%** | **-3.793pp** |
