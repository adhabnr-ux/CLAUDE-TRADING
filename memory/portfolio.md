# Portfolio Snapshot

_Updated by every routine from live Alpaca data. The next agent trusts this as
the last known state, but always re-fetches live data before trading._

**Last updated:** 2026-07-06 15:51 ET (close routine; `is_open: true` at run time, next_close 16:00 ET — full trading day; stop audit 3/3 PASS; LLY $1,204.565 +10.153% / V $357.14 +10.375%; no trades; Bull TRAILS SPY since inception by −2.007pp — gap widened sharply as SPY rallied on a broad tech/semi bounce that LLY/V, non-tech names, did not participate in)
**Inception:** 2026-05-21 — starting equity $100,000.00 | SPY anchor price $739.44
**SPY total-return anchor (post-June 18 ex-div $1.76):** **$741.20**
**Cumulative SPY dividends since inception (quarterly tracker):** $1.76/sh (June 18 ex-div); next SPY ex-div est. ~September 2026.

---

## Account (close routine, 2026-07-06 ~15:51 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,924.58 |
| Cash | $80,023.72 (80.08%) |
| Long market value | $19,900.86 |
| Buying power | ~$80,023.72 (cash) / $375,817.29 (margin, unused) |
| Last equity (July 2 close, carried through July 3 holiday/weekend) | $100,129.68 |

## Open positions (close routine, 2026-07-06 ~15:51 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,204.565 | $12,045.65 | +$1,110.31 (+10.153%) | 12.06% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $90.365 (7.50%) ✓ |
| V | 22 | $323.57 | $357.14 | $7,857.08 | +$738.54 (+10.375%) | 7.86% | 66033918 (22sh), HWM $364.21, stop $327.789 ✓ — buffer $29.351 (8.22%) ✓ |

**Sector exposure (close July 6):**
- Healthcare (LLY): $12,045.65 = 12.06% | Financials (V): $7,857.08 = 7.86% | Cash: $80,023.72 = 80.08%
- No sector above 60% cap ✓

**Close July 6 notes (~15:51 ET; stop audit 3/3 PASS; 0 trades; no cuts; no tightenings; SPY's strong tech/semi-driven rally left LLY/V behind):**
- **Live-switch guard:** `ALPACA_BASE_URL` contains "paper" ✓.
- **Lock:** was `{}` — acquired and will be released cleanly.
- **Control switch:** STATUS ACTIVE, no `NOTE:`/`QUERY:` to acknowledge.
- **Market clock:** `is_open: true` at run time (~15:51 ET), `next_close: 16:00 ET` — full trading day, not a half-day.
- **Today P/L:** $99,924.58 vs last_equity $100,129.68 = **−$205.10 (−0.2049%)** | SPY $751.96 vs $744.86 (July 2 close, carried) = **+0.9531%** | Bull underperformed SPY by **−1.158pp today**.
- **Shock check:** −0.2049% — no shock ✓ (threshold −4%).
- **Drawdown circuit breaker:** $99,924.58 vs HWM $101,384.21 = **−1.4396%** — NOT triggered ✓ (8.560pp headroom; not near the −10% level).
- **LLY** $1,204.565 (+10.153% from entry, −0.775% today): No new news since this morning's Medicare Bridge confirmation; thesis intact. HWM $1,238 not touched today — no ratchet. Buffer 7.50% ✓. **review_by tomorrow (2026-07-07) — mandatory hold/trim/exit decision due at next pre-market.** Conviction A (unchanged).
- **V** $357.14 (+10.375% from entry, −1.378% today): Modest pullback despite the broad tape's strength — no negative news, thesis (payments infrastructure, Open USD stablecoin consortium) intact. Buffer 8.22% ✓. review_by 2026-07-28 not due. Conviction B (unchanged).
- **No cuts** (−7% rule): both positions far above threshold (gains) ✓.
- **No discretionary tightenings** (+15% trigger = LLY $1,257.56 / V $372.10): neither reached ✓.
- **Stop audit (step 5):** 3/3 trailing stops confirmed live via `orders open` (LLY 7sh `d4147484` + 3sh `25989fb5` = 10sh; V 22sh `66033918`) — matches held quantities exactly. No missing stops, nothing to recreate.
- **Exit reconciliation:** No fills today (position quantities unchanged from market-open: LLY 10sh, V 22sh) — nothing to reconcile against closed-trades.md; ledger remains current (VST June 30 win is the latest entry).
- **Market close context (July 6):** US stocks rallied broadly — Nasdaq +1.2%, S&P 500 +0.8%, Dow topped 53,000 for the first time, as tech-sector pressure eased and oil fell post-holiday; a rebound in AI-trade sentiment (despite MU/AMD/INTC still down 4-5.5% intraday before partial recovery) and a Dell +7.7% pop on a White House event drove the tape. This is a tech/semi-led rally that neither LLY (healthcare) nor V (financials) directly participates in — consistent with today's relative underperformance; no thesis-relevant news for either holding.
- **Trades today:** 0.
- **Since inception:** Bull −0.0754% ($99,924.58) vs SPY TR **+1.9312%** ($751.96 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY by −2.0066pp** (was −0.930pp at pre-market; gap widened −1.077pp today, driven almost entirely by SPY's tech/semi-led +0.95% session vs Bull's diversified, non-tech book slipping −0.20%).
- **Race scoreboard:** Bull −0.08% | AGGRO −7.96% (2026-07-06 midday snapshot, equity $92,044.48, since its own June 4 inception) | SPY +1.93% (since Bull's May 21 inception, total return) — Bull leads AGGRO by ~7.88pp.
- **Friday watchdog:** N/A — today is Monday.

---

## Account (midday routine, 2026-07-06 ~12:33 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,861.28 |
| Cash | $80,023.72 (80.14%) |
| Long market value | $19,837.56 |
| Buying power | ~$80,023.72 (cash) / $375,640.05 (margin, unused) |
| Last equity (July 3 close, carried over holiday) | $100,129.68 |

## Open positions (midday routine, 2026-07-06 ~12:33 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,201.59 | $12,015.90 | +$1,080.56 (+9.881%) | 12.03% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $87.39 (7.27%) ✓ |
| V | 22 | $323.57 | $355.53 | $7,821.66 | +$703.12 (+9.877%) | 7.83% | 66033918 (22sh), HWM $364.21, stop $327.789 ✓ — buffer $27.741 (7.805%) ✓ |

**Sector exposure (midday July 6):**
- Healthcare (LLY): $12,015.90 = 12.03% | Financials (V): $7,821.66 = 7.83% | Cash: $80,023.72 = 80.14%
- No sector above 60% cap ✓

**Midday July 6 notes (~12:33 ET; stop audit 3/3 PASS; no trades — no cuts, no tightenings):**
- **Live-switch guard:** `ALPACA_BASE_URL` contains "paper" ✓.
- **Lock:** was `{}` — acquired and will be released cleanly.
- **Control switch:** STATUS ACTIVE, no `NOTE:`/`QUERY:` to acknowledge.
- **Market clock:** `is_open: true` ✓.
- **Shock check:** $99,861.28 vs last_equity $100,129.68 = **−$268.40 (−0.268%)** — no shock ✓ (threshold −4%).
- **Drawdown circuit breaker:** $99,861.28 vs HWM $101,384.21 = **−1.502%** — NOT triggered ✓ (8.498pp headroom).
- **News-scan gate:** LLY +9.881%, V +9.877% — both just under the +10% trigger; no scan run.
- **No cuts** (−7% rule): both positions far above threshold (both are gains) ✓.
- **No discretionary tightenings** (+15% trigger = LLY $1,257.56 / V $372.10): neither reached ✓.
- **Stop audit (step 5):** 3/3 trailing stops present and correctly sized (LLY 7sh + 3sh = 10sh; V 22sh) — matches held quantities exactly. No missing stops.
- **Exit reconciliation:** no fills since market-open — nothing to reconcile against closed-trades.md.
- **Trades today:** 0.
- **LLY review_by tomorrow (2026-07-07):** mandatory hold/trim/exit decision due at next pre-market.

## Account (market-open routine, 2026-07-06 ~09:36 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,868.79 |
| Cash | $80,023.72 (80.13%) |
| Long market value | $19,845.07 |
| Buying power | ~$80,023.72 (cash) / $375,661.08 (margin, unused) |
| Last equity (July 3 close, carried over holiday) | $100,129.68 |

## Open positions (market-open routine, 2026-07-06 ~09:36 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,201.615 | $12,016.15 | +$1,080.81 (+9.884%) | 12.03% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $87.415 (7.27%) ✓ |
| V | 22 | $323.57 | $355.82 | $7,828.04 | +$709.50 (+9.967%) | 7.84% | 66033918 (22sh), HWM $364.21, stop $327.789 ✓ — buffer $28.031 (7.88%) ✓ |

**Sector exposure (market-open July 6):**
- Healthcare (LLY): $12,016.15 = 12.03% | Financials (V): $7,828.04 = 7.84% | Cash: $80,023.72 = 80.13%
- No sector above 60% cap ✓

**Market-open July 6 notes (~09:36 ET; stop audit 3/3 PASS; no trades — today's plan was empty):**
- **Live-switch guard:** `ALPACA_BASE_URL` contains "paper" ✓.
- **Lock:** `memory/_lock` was `{}` — no stale lock; acquired and released cleanly.
- **Control switch:** STATUS ACTIVE, no `NOTE:`/`QUERY:` to acknowledge.
- **Plan check:** today's plan block (`plan_date: 2026-07-06`, `trades: []`) confirmed current — pre-market already elected zero new positions (LRCX/ETN fail ATR gates, VST fails technical confirmation + FERC overhang, CEG/VRT/NVT/MOD undiligenced). No prior EXECUTED line — first run today.
- **Market clock:** `is_open: true` ✓.
- **Breaking-news gate:** no planned trades — N/A.
- **Shock check:** $99,868.79 vs last_equity $100,129.68 = **−$260.89 (−0.2606%)** — no shock ✓ (threshold −4%).
- **Drawdown circuit breaker:** $99,868.79 vs HWM $101,384.21 = **−1.4947%** — NOT triggered ✓.
- **Stop audit (step 5):** 3/3 trailing stops present and correctly sized (LLY 7sh + 3sh = 10sh; V 22sh) — matches held quantities exactly. No missing stops.
- **Exit reconciliation:** no fills since pre-market — nothing to reconcile against closed-trades.md.
- **Trades today:** 0.
- **LLY review_by tomorrow (2026-07-07):** mandatory hold/trim/exit decision due at next pre-market.

## Account (pre-market July 6, 2026 — live Alpaca data ~08:07 ET)

| Metric | Value |
|--------|-------|
| Equity | $100,041.17 |
| Cash | $80,023.72 (80.00%) |
| Long market value | $20,017.45 |
| Buying power | ~$80,023.72 (cash) / $376,143.74 (margin, unused) |
| Last equity (July 3 close, carried over holiday) | $100,129.68 |

## Open positions (pre-market July 6, 2026 — live Alpaca data ~08:07 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,207.05 | $12,070.50 | +$1,135.16 (+10.38%) | 12.06% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $92.85 (7.69%) ✓ |
| V | 22 | $323.57 | $361.225 | $7,946.95 | +$828.41 (+11.64%) | 7.94% | 66033918 (22sh), HWM $361.86, stop $325.674 ✓ — buffer $35.551 (9.84%) ✓ |

**Sector exposure (pre-market July 6):**
- Healthcare (LLY): $12,070.50 = 12.06% | Financials (V): $7,946.95 = 7.94% | Cash: $80,023.72 = 80.00%
- No sector above 60% cap ✓

**Trailing stop status (pre-market July 6 — confirmed via Alpaca live orders ~08:07 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $92.85 = 7.69%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $361.86, stop $325.674 ✓ (buffer $35.551 = 9.84%)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions; none missing)

**Pre-market July 6 notes (~08:07 ET — Monday; stop audit 3/3 PASS; no trades, market not yet open):**
- **Shock check:** $100,041.17 vs last_equity $100,129.68 = **−$88.51 (−0.088%)** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $100,041.17 vs HWM $101,384.21 = **−1.325%** — NOT triggered ✓ (8.675pp headroom; CB trigger USD 91,245.79)
- **LLY** $1,207.05 (+10.38% from entry): No new news since Friday's Medicare Bridge confirmation; thesis intact. Review_by **tomorrow (2026-07-07)** — mandatory decision due at next pre-market. Conviction A (Monday refresh, unchanged).
- **V** $361.225 (+11.64% from entry): No new news since Thursday's 52-week high; Open USD stablecoin build-out continuing. review_by 2026-07-28 not due. Conviction B (Monday refresh, unchanged).
- **LRCX/ETN ATR gates:** Both failed again July 2 (LRCX 14.11% catastrophic, ETN 5.52% narrow) — gate counters reset to 0/2. Not eligible today.
- **VST re-entry:** Fails technical-confirmation signal (downtrend, new FERC regulatory risk, insider selling) — not eligible today.
- **New watchlist research candidates:** CEG, VRT, NVT, MOD sourced today (non-semi AI-power/cooling names) — research-only, no diligence yet.
- **Cash-drag check:** Cash 80.00%, well above the 25–40% target band for a 2-position book. No qualifying entry today — deliberate decision, documented in research-log.md.
- **Trades today:** 0 planned (market not yet open).
- **Since inception:** Bull +0.0412% ($100,041.17) vs SPY TR +0.9711% ($744.86 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY −0.930pp** (essentially unchanged from Thursday's −0.841pp; small extended-hours give-back, no new SPY session)

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-07-06)** | **$99,924.58 (−0.0754%)** | **SPY $751.96 + $1.76 div = +1.9312% TR** | **Bull TRAILS SPY −2.0066pp** |
| Pre-market (2026-07-06) | $100,041.17 (+0.0412%) | SPY $744.86 + $1.76 div = +0.9711% TR | Bull TRAILS SPY −0.930pp |
| Close (2026-07-03, MARKET HOLIDAY) | $100,129.68 (+0.1297%) | SPY $744.86 + $1.76 div = +0.9711% TR | Bull TRAILS SPY −0.8414pp |

---

## Account (market-open routine, 2026-07-03 ~09:36 ET — MARKET HOLIDAY, no trading day)

| Metric | Value |
|--------|-------|
| Equity | $100,129.68 |
| Cash | $80,023.72 (79.91%) |
| Long market value | $20,105.96 |
| Buying power | ~$80,023.72 (cash) / $376,391.57 (margin, unused) |
| Last equity | $100,129.68 |

## Open positions (market-open routine, 2026-07-03 ~09:36 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,213.91 | $12,139.10 | +$1,203.76 (+11.01%) | 12.13% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ |
| V | 22 | $323.57 | $362.13 | $7,966.86 | +$848.32 (+11.92%) | 7.96% | 66033918 (22sh), HWM $361.86, stop $325.674 ✓ |

**Sector exposure:** Healthcare (LLY) 12.13% | Financials (V) 7.96% | Cash 79.91% — no sector above 60% cap ✓

**Market-open routine notes (2026-07-03 ~09:36 ET):**
- **Live-switch guard:** `ALPACA_BASE_URL` contains "paper" ✓.
- **Lock:** no stale lock found; acquired and released cleanly.
- **Control switch:** `memory/control.md` STATUS: ACTIVE. No `NOTE:`/`QUERY:` line to acknowledge.
- **Plan check:** today's plan block in research-log.md (`plan_date: 2026-07-03`, `trades: []`) confirmed current — pre-market already decided to stay in cash for the July 4 holiday closure (LRCX/ETN ATR gates both reset to 0/2 after the semi-sector selloff; no other watchlist name qualified). Not a stale/prior-day plan.
- **Market clock:** `is_open: false` — `next_open: 2026-07-06T09:30:00-04:00`. Per playbook step 1, no trades possible; skipped steps 2–4 (breaking-news gate, shock re-check, trade execution — none applicable with an empty plan and closed market).
- **Shock check:** equity $100,129.68 vs last_equity $100,129.68 = 0.00% — no shock ✓ (no new session has closed since pre-market).
- **Stop audit (step 5):** compared live positions vs open orders — 3/3 trailing stops present and correctly sized (LLY 7sh + 3sh = 10sh total; V 22sh), matching held quantities exactly. No missing stops, nothing to recreate. Identical to the pre-market audit — no session has elapsed.
- **Exit reconciliation:** no fills since pre-market (market closed) — nothing to reconcile against closed-trades.md.
- **Trades today:** 0 (market closed).
- **Since inception:** Bull +0.1297% ($100,129.68) vs SPY TR +0.8413% ($743.90 + $1.76 div vs $739.44 anchor, unchanged — market closed) → **Bull TRAILS SPY −0.712pp** (unchanged from pre-market).

---

## Account (midday routine, 2026-07-03 ~12:34 ET — MARKET HOLIDAY, no trading day)

| Metric | Value |
|--------|-------|
| Equity | $100,129.68 |
| Cash | $80,023.72 (79.91%) |
| Long market value | $20,105.96 |
| Buying power | ~$80,023.72 (cash) / $376,391.57 (margin, unused) |
| Last equity | $100,129.68 |

## Open positions (midday routine, 2026-07-03 ~12:34 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,213.91 | $12,139.10 | +$1,203.76 (+11.01%) | 12.13% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ |
| V | 22 | $323.57 | $362.13 | $7,966.86 | +$848.32 (+11.92%) | 7.96% | 66033918 (22sh), HWM $361.86, stop $325.674 ✓ |

**Sector exposure:** Healthcare (LLY) 12.13% | Financials (V) 7.96% | Cash 79.91% — no sector above 60% cap ✓

**Midday routine notes (2026-07-03 ~12:34 ET):**
- **Live-switch guard:** `ALPACA_BASE_URL` contains "paper" ✓.
- **Lock:** no stale lock found; acquired and released cleanly.
- **Control switch:** `memory/control.md` STATUS: ACTIVE. No `NOTE:`/`QUERY:` line to acknowledge.
- **Market clock:** `is_open: false` — `next_open: 2026-07-06T09:30:00-04:00`. Per playbook step 1, journaled "market closed, no action" and skipped directly to step 7 (journal) / step 8 (notify).
- **Shock check:** equity $100,129.68 vs last_equity $100,129.68 = 0.00% — no shock ✓ (no new session has closed since market-open).
- **Stop audit:** compared live positions vs open orders — 3/3 trailing stops present and correctly sized (LLY 7sh + 3sh = 10sh total; V 22sh), matching held quantities exactly. No missing stops, nothing to recreate. Identical to the market-open audit — no session has elapsed.
- **News scan:** not run — no new session has closed since market-open, so no new price move to trigger the >3%-down / >10%-up news-scan gate.
- **Exit reconciliation:** no fills since market-open (market closed) — nothing to reconcile against closed-trades.md.
- **Trades today:** 0 (market closed).
- **Since inception:** Bull +0.1297% ($100,129.68) vs SPY TR +0.8413% ($743.90 + $1.76 div vs $739.44 anchor, unchanged — market closed) → **Bull TRAILS SPY −0.712pp** (unchanged from market-open).

---

## Account (pre-market July 3, 2026 — live Alpaca data ~08:06 ET; MARKET HOLIDAY)

| Metric | Value |
|--------|-------|
| Equity | $100,129.68 |
| Cash | $80,023.72 (79.91%) |
| Long market value | $20,105.96 |
| Buying power | ~$80,023.72 (cash) / $376,391.57 (margin, unused) |
| Last equity (carried, market closed) | $100,129.68 |

## Open positions (pre-market July 3, 2026 — live Alpaca data ~08:06 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,213.91 | $12,139.10 | +$1,203.76 (+11.01%) | 12.13% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $99.71 (8.21%) ✓ |
| V | 22 | $323.57 | $362.13 | $7,966.86 | +$848.32 (+11.92%) | 7.96% | 66033918 (22sh, HWM $361.86 ⬆️ auto-ratcheted, stop $325.674 ⬆️) ✓ — buffer $36.456 (10.07%) ✓ |

**Sector exposure (pre-market July 3):**
- Healthcare (LLY): $12,139.10 = 12.13% | Financials (V): $7,966.86 = 7.96% | Cash: $80,023.72 = 79.91%
- No sector above 60% cap ✓

**Trailing stop status (pre-market July 3 — confirmed via Alpaca live orders ~08:06 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $99.71 = 8.21%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM **$361.86** ⬆️ (auto-ratcheted from $360.84), stop **$325.674** ⬆️ (up from $324.756) ✓ (buffer $36.456 = 10.07%)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions; none missing)

**Pre-market July 3 notes (~08:06 ET — MARKET HOLIDAY, no trading; stop audit 3/3 PASS; plan for Monday July 6 is empty):**
- **Shock check:** $100,129.68 vs last_equity $100,129.68 = **$0.00 (0.00%)** — no shock ✓ (threshold −4%; no new session has closed)
- **Drawdown circuit breaker:** $100,129.68 vs HWM $101,384.21 = **−1.237%** — NOT triggered ✓ (8.763pp headroom; CB trigger USD 91,245.79)
- **LLY** $1,213.91 (+11.01% from entry): No new news since the July 1 Medicare Bridge launch; thesis intact, Leerink PT $1,232 stands. review_by 2026-07-07 not yet due. HOLD. Conviction A.
- **V** $362.13 (+11.92% from entry, new 52-week high): Rallied +3.15% July 2 on strong Q2 growth commentary and Piper Sandler support; Visa Destinations + stablecoin pilot (~USD 7B run rate) build out. Thesis intact. review_by 2026-07-28 not due. HOLD. Conviction B.
- **Market context:** Broad market (SPY, Dow) closed at fresh highs July 2 heading into the holiday, but the semiconductor sector (SOX) fell ~12% over two days on AI-capex demand-destruction fears after reports Meta is building an internal cloud business to resell excess AI compute. This hit LRCX directly (−10.2% July 2) and reset both LRCX and ETN's ATR gates to 0/2. No impact on held LLY/V (neither is semi-exposed).
- **Cash-drag check:** Cash 79.91%, well above target for a 2-position book. No qualifying candidate for Monday — LRCX/ETN gates both reset by the semi selloff; no other watchlist name clears entry signals. Staying in cash into the weekend is deliberate, not a default.
- **Trades today:** 0 (market closed).
- **Since inception:** Bull +0.1297% ($100,129.68) vs SPY TR +0.8413% ($743.90 + $1.76 div vs $739.44 anchor, unchanged — market closed) → **Bull TRAILS SPY −0.712pp**

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-07-03, MARKET HOLIDAY)** | **$100,129.68 (+0.1297%)** | **SPY $744.86 + $1.76 div = +0.9711% TR** | **Bull TRAILS SPY −0.8414pp** |
| Pre-market (2026-07-03) | $100,129.68 (+0.1297%) | SPY $743.90 (intraday est.) + $1.76 div = +0.8413% TR | Bull TRAILS SPY −0.712pp |
| Close (2026-07-02) | $100,016.50 (+0.0165%) | SPY $743.90 (intraday est.) + $1.76 div = +0.842% TR | Bull TRAILS SPY −0.825pp |

---

## Account (close July 3, 2026 — live Alpaca data ~15:51 ET — MARKET HOLIDAY, no trading day)

| Metric | Value |
|--------|-------|
| Equity | $100,129.68 |
| Cash | $80,023.72 (79.91%) |
| Long market value | $20,105.96 |
| Buying power | ~$80,023.72 (cash) / $376,391.57 (margin, unused) |
| Last equity | $100,129.68 |

## Open positions (close July 3, 2026 — live Alpaca data ~15:51 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,213.91 | $12,139.10 | +$1,203.76 (+11.01%) | 12.13% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ |
| V | 22 | $323.57 | $362.13 | $7,966.86 | +$848.32 (+11.92%) | 7.96% | 66033918 (22sh), HWM $361.86, stop $325.674 ✓ |

**Sector exposure:** Healthcare (LLY) 12.13% | Financials (V) 7.96% | Cash 79.91% — no sector above 60% cap ✓

**Close routine notes (2026-07-03 ~15:51 ET):**
- **Live-switch guard:** `ALPACA_BASE_URL` contains "paper" ✓.
- **Lock:** no stale lock found; acquired and released cleanly.
- **Control switch:** `memory/control.md` STATUS: ACTIVE. No `NOTE:`/`QUERY:` line to acknowledge.
- **Market clock:** `is_open: false` all day — `next_open: 2026-07-06T09:30:00-04:00`. No trades possible.
- **Today P/L:** $0.00 (0.00%) — market never traded.
- **Drawdown circuit breaker:** $100,129.68 vs HWM $101,384.21 = −1.237% — NOT triggered ✓ (8.763pp headroom).
- **Stop audit:** 3/3 PASS, unchanged from midday.
- **Exit reconciliation:** no fills today — nothing new for closed-trades.md.
- **Market context (July 2 close, most recent session):** Dow +~1.1% to a fresh record; Nasdaq −0.8% on chip-sector weakness; SPY little changed. June payrolls soft (+57K vs +113K expected). No impact on LLY/V theses.
- **Since inception:** Bull +0.1297% ($100,129.68) vs SPY TR +0.9711% ($744.86 official close + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY −0.8414pp**.
- **Race scoreboard:** Bull +0.13% | AGGRO −9.33% (2026-07-03 midday snapshot, equity $90,674.09, market closed/unchanged) | SPY +0.97% — Bull leads AGGRO by ~9.46pp.
- **Friday watchdog:** newest weekly-review.md entry (week ending 2026-06-26) is exactly 7 days old — not stale, no flag today (weekly review runs separately at 16:30 ET).
- **Trades today:** 0 (market closed all day).

---

## Account (close July 2, 2026 — live Alpaca data ~15:55 ET)

| Metric | Value |
|--------|-------|
| Equity | $100,016.50 |
| Cash | $80,023.72 (80.01%) |
| Long market value | $19,992.78 |
| Buying power | ~$80,023.72 (cash) / $376,074.66 (margin, unused) |
| Last equity (July 1 Alpaca close) | $99,664.88 |

## Open positions (close July 2, 2026 — live Alpaca data ~15:55 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,205.65 | $12,056.50 | +$1,121.16 (+10.25%) | 12.06% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $91.45 (7.59%) ✓ |
| V | 22 | $323.57 | $360.83 | $7,938.26 | +$819.72 (+11.51%) | 7.94% | 66033918 (22sh, HWM $360.84 ⬆️ auto-ratcheted intraday, stop $324.756 ⬆️) ✓ — buffer $36.074 (10.00%) ✓ |

**Sector exposure (close July 2):**
- Healthcare (LLY): $12,056.50 = 12.06% | Financials (V): $7,938.26 = 7.94% | Cash: $80,023.72 = 80.01%
- No sector above 60% cap ✓

**Trailing stop status (close July 2 — confirmed via Alpaca live orders ~15:55 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $91.45 = 7.59%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM **$360.84** ⬆️ (auto-ratcheted from $359.65 at midday), stop **$324.756** ⬆️ (up from $323.685) ✓ (buffer $36.074 = 10.00%)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions; none missing)

**Close July 2 notes (~15:55 ET — stop audit 3/3 PASS; 0 trades; no cuts; no tightenings; soft NFP print, Fed comments constructive, chip-sector selloff continues, Financials/Comm Services led):**
- **Today P/L:** +$351.62 (+0.353%) | SPY −0.351% ($746.5225 → $743.90) | Bull outperformed SPY by +0.704pp today
- **Shock check:** $100,016.50 vs last_equity $99,664.88 = **+$351.62 = +0.353%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $100,016.50 vs HWM $101,384.21 = **−1.349%** — NOT triggered ✓ (8.651pp headroom; CB trigger USD 91,245.79)
- **LLY** $1,205.65 (+10.25% from entry, +1.17% today): Continued strength post-Medicare-Bridge-launch; no new news since midday's confirmatory scan (CHMP Jaypirca EU backing, Medicare Bridge live, Leerink PT $1,232). HWM $1,238 not yet exceeded — no ratchet. Buffer 7.59% ✓. review_by 2026-07-07 not due. HOLD. Conviction A.
- **V** $360.83 (+11.51% from entry, +2.78% today): Extended gains into the close as Financials led the tape (sector +2.2%) on the soft-jobs/steady-Fed read. HWM auto-ratcheted to $360.84 (from $359.65), stop tightened to $324.756 (from $323.685). No new negative news; Bernstein Buy initiation + "Open USD" stablecoin consortium catalyst (from midday scan) stands. Not yet at the +15% tighten-trail trigger ($372.10). review_by 2026-07-28 not due. HOLD. Conviction B.
- **No cuts** (−7% rule): both positions far above threshold ✓
- **No discretionary tightenings** (+15% trigger = LLY $1,257.56 / V $372.10): neither reached ✓ (V closest at +11.51%)
- **Stop audit:** 3/3 live trailing-stop orders confirmed (LLY 7sh + 3sh, V 22sh) — matches held quantities exactly. No missing stops, nothing to recreate.
- **Market context (July 2):** June nonfarm payrolls came in well below consensus (+57K vs +113K expected; unemployment 4.2% vs 4.3% forecast) — a soft print that broke a three-month hot streak and reinforced the case for the Fed to hold rates steady. Fed Chair Warsh reiterated that inflation risks have eased substantially. The Dow rose ~0.8% to a fresh record; the S&P 500 fell −0.3% and the Nasdaq fell −1.2%, dragged by a continuing chip-sector selloff (Info Tech sector −2.6%). Financials (+2.2%) and Communication Services (+2.4%) led. Neither LLY's nor V's thesis is affected by today's chip-specific weakness; V directly benefited from the Financials-sector rotation. Market closed Friday July 3 for Independence Day; reopens Monday July 6.
- **Exit reconciliation:** No exits today. closed-trades.md remains current (VST June 30 win is the latest entry). No new lessons.md entry required — nothing notable beyond routine housekeeping.
- **Trades today:** 0.
- **Since inception:** Bull +0.0165% ($100,016.50) vs SPY TR +0.8417% ($743.90 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY −0.825pp** (was −0.685pp at midday; SPY firmed modestly into the close (742.85→743.90) while Bull's own gain, though the day's strongest single-day outperformance driver was V, didn't fully offset — gap widened slightly from midday but remains far narrower than market-open's −1.739pp)

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-07-02)** | **$100,016.50 (+0.0165%)** | **SPY $743.90 + $1.76 div = +0.842% TR** | **Bull TRAILS SPY −0.825pp** |
| Midday (2026-07-02) | $100,014.58 (+0.0146%) | SPY $742.85 + $1.76 div = +0.699% TR | Bull TRAILS SPY −0.685pp |

---

## Account (midday July 2, 2026 — live Alpaca data ~12:34 ET)

| Metric | Value |
|--------|-------|
| Equity | $100,014.58 |
| Cash | $80,023.72 (80.01%) |
| Long market value | $19,990.09 |
| Buying power | ~$80,023.72 (cash) / $376,069.29 (margin, unused) |
| Last equity (July 1 Alpaca close) | $99,664.88 |

## Open positions (midday July 2, 2026 — live Alpaca data ~12:34 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,207.955 | $12,079.55 | +$1,144.21 (+10.46%) | 12.08% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $93.755 (7.76%) ✓ |
| V | 22 | $323.57 | $359.57 | $7,910.54 | +$792.00 (+11.13%) | 7.91% | 66033918 (22sh, HWM $359.65 ⬆️ auto-ratcheted intraday, stop $323.685 ⬆️) ✓ — buffer $35.885 (9.98%) ✓ |

**Sector exposure (midday July 2):**
- Healthcare (LLY): $12,079.55 = 12.08% | Financials (V): $7,910.54 = 7.91% | Cash: $80,023.72 = 80.01%
- No sector above 60% cap ✓

**Trailing stop status (midday July 2 — confirmed via Alpaca live orders ~12:34 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $93.755 = 7.76%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM **$359.65** ⬆️ (auto-ratcheted from $356.60), stop **$323.685** ⬆️ (up from $320.94) ✓ (buffer $35.885 = 9.98%)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions; none missing)

**Midday July 2 notes (~12:34 ET — stop audit 3/3 PASS; 0 trades; no cuts; no tightenings; NFP print drove a broad SPY dip while LLY/V held gains on company-specific catalysts):**
- **Shock check:** $100,014.58 vs last_equity $99,664.88 = **+$349.70 = +0.351%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $100,014.58 vs HWM $101,384.21 = **−1.351%** — NOT triggered ✓ (8.649pp headroom; CB trigger USD 91,245.79)
- **Macro:** June nonfarm payrolls (8:30 AM ET) appears to have come in soft/mixed — SPY fell from market-open's $748.91 to $742.85 at midday, a −0.81% intraday move. Broad tape pulled back on the print while Bull's two holdings (company-specific catalysts, not macro-sensitive) continued to rally — a favorable divergence day.
- **LLY** $1,207.955 (+10.46% from entry, +1.36% today): Crossed the +10%-from-entry news-scan trigger. Scan found: Friday's CHMP (EU) backing of Jaypirca for CLL across all lines, Medicare GLP-1 Bridge program details (up to 20M Medicare Part D patients, $50/month, launched July 1), and Leerink's PT raise to $1,232 (from $1,119) — all confirmatory, not new since pre-market/market-open. No thesis break. HWM $1,238 not yet exceeded (current price still below it) — no ratchet. Buffer 7.76% ✓. review_by 2026-07-07 not due. HOLD. Conviction A.
- **V** $359.57 (+11.13% from entry, +2.42% today): Crossed the +10%-from-entry news-scan trigger. Scan found: Bernstein initiated/reiterated a Buy rating, and Visa joined 140+ partners to launch "Open USD," a consortium stablecoin positioned against USDC/USDT — a genuine incremental catalyst extending the stablecoin/tokenization thesis already on file. No negative news. HWM auto-ratcheted intraday to $359.65 (from $356.60), stop tightened to $323.685 (from $320.94). Buffer 9.98% ✓. Not yet at the +15% tighten-trail trigger ($372.10). review_by 2026-07-28 not due. HOLD. Conviction B.
- **No cuts** (−7% rule): both positions far above threshold ✓
- **No discretionary tightenings** (+15% trigger = LLY $1,257.56 / V $372.10): neither reached ✓ (V closest at +11.13%)
- **Stop audit:** 3/3 live trailing-stop orders confirmed (LLY 7sh + 3sh, V 22sh) — matches held quantities exactly. No missing stops, nothing to recreate.
- **No new positions** — midday routine manages existing risk only, per playbook.
- **Trades today:** 0.
- **Since inception:** Bull +0.0146% ($100,014.58) vs SPY TR +0.699% ($742.85 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY −0.685pp** (narrowed sharply from −1.739pp at market-open as SPY sold off on the NFP print while LLY/V held their gains)

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Midday (2026-07-02)** | **$100,014.58 (+0.0146%)** | **SPY $742.85 + $1.76 div = +0.699% TR** | **Bull TRAILS SPY −0.685pp** |
| **Market-open (2026-07-02)** | **$99,779.89 (−0.220%)** | **SPY $748.91 + $1.76 div = +1.519% TR** | **Bull TRAILS SPY −1.739pp** |

---

## Account (market-open July 2, 2026 — live Alpaca data ~09:36 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,779.89 |
| Cash | $80,023.72 (80.20%) |
| Long market value | $19,756.17 |
| Buying power | ~$80,023.72 (cash) / $375,412.16 (margin, unused) |
| Last equity (July 1 Alpaca close) | $99,664.88 |

## Open positions (market-open July 2, 2026 — live Alpaca data ~09:36 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,194.375 | $11,943.75 | +$1,008.41 (+9.22%) | 11.97% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $80.175 (6.71%) ✓ |
| V | 22 | $323.57 | $355.11 | $7,812.42 | +$693.88 (+9.75%) | 7.83% | 66033918 (22sh, HWM $356.60 ⬆️ auto-ratcheted intraday, stop $320.94 ⬆️) ✓ — buffer $34.17 (9.63%) ✓ |

**Sector exposure (market-open July 2):**
- Healthcare (LLY): $11,943.75 = 11.97% | Financials (V): $7,812.42 = 7.83% | Cash: $80,023.72 = 80.20%
- No sector above 60% cap ✓

**Trailing stop status (market-open July 2 — confirmed via Alpaca live orders ~09:36 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $80.175 = 6.71%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $356.60 ⬆️ (ratcheted from $353.36), stop $320.94 ⬆️ (up from $318.024) ✓ (buffer $34.17 = 9.63%)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions; none missing)

**Market-open July 2 notes (~09:36 ET — stop audit 3/3 PASS; 0 trades; plan was empty; V new intraday HWM/stop ratchet):**
- **Plan check:** Today's plan block in research-log.md (`plan_date: 2026-07-02`) is empty — pre-market decided to stay in cash (LRCX ATR gate failed again 8.40%, ETN gate 1/2, no other watchlist name qualified, NFP report 8:30 AM ET added event risk). Nothing to execute; breaking-news gate (step 2) and trade execution (step 4) skipped as not applicable.
- **Shock check:** $99,779.89 vs last_equity $99,664.88 = **+$115.01 = +0.115%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,779.89 vs HWM $101,384.21 = **−1.583%** — NOT triggered ✓ (8.417pp headroom; CB trigger USD 91,245.79)
- **LLY** $1,194.375 (+9.22% from entry, +0.22% today): Holding post-Medicare-Bridge-launch gains, modestly positive on the open. No new news since pre-market. Buffer 6.71% ✓. Thesis intact, review_by 2026-07-07 not yet due. HOLD. Conviction A.
- **V** $355.11 (+9.75% from entry, +1.15% today): Strong open, HWM auto-ratcheted to $356.60 (from $353.36), stop tightened to $320.94 (from $318.024). No negative news; Piper Sandler Overweight (June 29) stands. Thesis intact. HOLD. Conviction B. review_by 2026-07-28.
- **No trades today** — plan was empty; no positions to execute.
- **Since inception:** Bull −0.220% ($99,779.89) vs SPY TR +1.519% ($748.91 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY −1.739pp**

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Market-open (2026-07-02)** | **$99,779.89 (−0.220%)** | **SPY $748.91 + $1.76 div = +1.519% TR** | **Bull TRAILS SPY −1.739pp** |
| **Pre-market (2026-07-02)** | **$99,717.72 (−0.282%)** | **SPY ~$746.75 + $1.76 div = +1.227% TR** | **Bull TRAILS SPY ~−1.509pp** |

---

## Account (pre-market July 2, 2026 — live Alpaca data ~08:06 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,717.72 |
| Cash | $80,023.72 (80.25%) |
| Long market value | $19,694.00 |
| Buying power | ~$80,023.72 (cash) / $375,238.08 (margin, unused) |
| Last equity (July 1 Alpaca close) | $99,664.88 |

## Open positions (pre-market July 2, 2026 — live Alpaca data ~08:06 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,192.80 | $11,928.00 | +$992.66 (+9.08%) | 11.96% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $78.60 (6.59%) ✓ |
| V | 22 | $323.57 | $353.00 | $7,766.00 | +$647.46 (+9.10%) | 7.79% | 66033918 (22sh, HWM $353.36, stop $318.024) ✓ — buffer $34.976 (9.91%) ✓ |

**Sector exposure (pre-market July 2):**
- Healthcare (LLY): $11,928.00 = 11.96% | Financials (V): $7,766.00 = 7.79% | Cash: $80,023.72 = 80.25%
- No sector above 60% cap ✓

**Trailing stop status (pre-market July 2 — confirmed via Alpaca live orders ~08:06 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $78.60 = 6.59%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $353.36, stop $318.024 ✓ (buffer $34.976 = 9.91%)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions)

**Pre-market July 2 notes (~08:06 ET — stop audit 3/3 PASS; no trades, market not yet open; no new positions planned):**
- **Shock check:** $99,717.72 vs last_equity $99,664.88 = **+$52.84 = +0.053%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,717.72 vs HWM $101,384.21 = **−1.644%** — NOT triggered ✓ (8.356pp headroom; CB trigger USD 91,245.79)
- **Macro (pre-market ~08:06 ET):** Semiconductor/memory-chip selloff (Micron −8%, SanDisk −10%, Western Digital −7% on July 1 — DRAM antitrust class action + Citi demand-softening note) dominated the tape, but the broad market was only mildly lower (S&P −0.22%, Dow −0.03%, Nasdaq −0.66%). Today's key event: June nonfarm payrolls at 8:30 AM ET (fcst +115K, unemployment 4.3%); yesterday's soft ADP (+98K vs +110K) adds two-way surprise risk. 10yr yield 4.44% — **BELOW 4.75% gate ✓**. No new positions ahead of the jobs data.
- **LLY** $1,192.80 (+9.08% from entry): No new news since the Medicare Bridge launch (July 1); stock holding gains, modestly positive pre-market. Leerink PT $1,232 unchanged. Next earnings Aug 5. Thesis intact, review_by 2026-07-07 not yet due. HOLD. Conviction A.
- **V** $353.00 (+9.10% from entry): No negative news; Piper Sandler Overweight (June 29) stands. Next earnings July 28. Thesis intact. review_by 2026-07-28 not due. HOLD. Conviction B.
- **LRCX ATR gate:** July 1 session H $414.33 / L $381.47 / C $391.36 = **8.40% ATR** ⚠️ FAILS again — hit directly by the memory-chip selloff. Gate counter stays **0/2** under the July 1 reset. Not eligible today.
- **ETN ATR gate:** July 1 session H $423.36 / L $405.215 / C $412.16 = **4.40% ATR** ✓ — first qualifying session under the July 1 reset. Gate counter **1/2**. Needs one more ≤5% session (today) to clear; not eligible for entry today regardless. New catalyst: added to Russell 1000 Growth / Russell Top 200 Growth / Russell 3000E Growth indices; FY26 EPS guidance raised to USD 13.00–13.50.
- **Cash-drag check:** Cash at 80.25%, well above the 10–20% target band, elevated 6+ weeks. No qualifying entry today: LRCX failed its ATR gate again; ETN is 1/2 through its gate and cannot be bought until a second clean session completes; no other watchlist name clears its entry signals; and today carries major macro-event risk (NFP at 8:30 AM ET). Staying in cash today is the correct, deliberate call, not a default.
- **Trades today:** 0 (pre-market only; market not yet open).
- **Since inception:** Bull −0.282% ($99,717.72) vs SPY TR ~+1.227% (~$746.75 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY ~−1.509pp**

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Pre-market (2026-07-02)** | **$99,717.72 (−0.282%)** | **SPY ~$746.75 + $1.76 div = +1.227% TR** | **Bull TRAILS SPY ~−1.509pp** |
| **Close (2026-07-01)** | **$99,626.38 (−0.374%)** | **SPY $746.5225 + $1.76 div = +1.196% TR** | **Bull TRAILS SPY −1.569pp** |

---

## Account (close July 1, 2026 — live Alpaca data ~15:51 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,626.38 |
| Cash | $80,023.72 (80.33%) |
| Long market value | $19,602.66 |
| Buying power | ~$80,023.72 (cash) / $374,982.33 (margin, unused) |
| Last equity (June 30 Alpaca close) | $99,566.00 |

## Open positions (close July 1, 2026 — live Alpaca data ~15:51 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,189.76 | $11,897.60 | +$962.26 (+8.80%) | 11.94% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $75.56 (6.35%) ✓ |
| V | 22 | $323.57 | $350.23 | $7,705.06 | +$586.52 (+8.24%) | 7.74% | 66033918 (22sh, HWM $353.36, stop $318.024) ✓ — buffer $32.206 (9.20%) ✓ |

**Sector exposure (close July 1):**
- Healthcare (LLY): $11,897.60 = 11.94% | Financials (V): $7,705.06 = 7.74% | Cash: $80,023.72 = 80.33%
- No sector above 60% cap ✓

**Trailing stop status (close July 1 — confirmed via Alpaca live orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $75.56 = 6.35%; LLY at $1,189.76 < HWM — no ratchet today)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $353.36, stop $318.024 ✓ (buffer $32.206 = 9.20%; V at $350.23 < HWM $353.36 — no ratchet today; midday's new-HWM ratchet stands)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions; none missing)

**Close July 1 notes (~15:51 ET — stop audit 3/3 PASS; 0 trades; no cuts; no tightenings; choppy flat session on soft ADP print):**
- **Today P/L:** +$60.38 (+0.0607%) | SPY −0.0331% ($746.77 → $746.5225) | Bull outperformed SPY by +0.094pp today
- **Shock check:** $99,626.38 vs last_equity $99,566.00 = **+$60.38 = +0.061%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,626.38 vs HWM $101,384.21 = **−1.734%** — NOT triggered ✓ (8.266pp headroom; CB trigger USD 91,245.79)
- **LLY** $1,189.76 (+8.80% from entry, −0.807% today): Continued mild give-back after yesterday's Medicare Bridge launch — consistent with the "sell the news" pattern flagged since pre-market. HWM $1,238 not touched; no ratchet. Buffer 6.35% ✓. Thesis intact, no new negative news, review_by 2026-07-07 not due. HOLD. Conviction A.
- **V** $350.23 (+8.24% from entry, +1.907% today): Extended the midday rally into the close; new intraday high but did not clear the midday-set HWM $353.36, so no further ratchet. No new catalyst beyond the already-known stablecoin initiative and June 29 Piper Sandler Overweight. Thesis intact. HOLD. Conviction B. review_by 2026-07-28.
- **No cuts** (−7% rule): both positions well above threshold ✓
- **No tightenings** (+15% trigger = LLY $1,257.56 / V $372.10): neither triggered ✓
- **Market context (July 1):** Choppy, essentially flat session — SPY closed $746.5225 vs June 30's $746.77 (−0.03%). ADP private payrolls came in soft at +98K (vs +110K expected), and ISM Manufacturing PMI plus Fed Chair Warsh's Sintra remarks were the other data points investors weighed; none produced a decisive directional move. Neither LLY's nor V's thesis is affected by today's macro prints.
- **Monthly housekeeping (first trading day of July):** research-log.md and trade-log.md entries dated before 2026-06-01 (2026-05-21 through 2026-05-29) archived to `memory/archive/2026-05.md`, with a one-line pointer left at the top of each log. Quarterly dividend housekeeping (Jun/Sep/Dec) not due this month.
- **Exit reconciliation:** No exits today. closed-trades.md remains current (VST June 30 win is the latest entry). No new lessons.md entry required — nothing notable beyond routine housekeeping.
- **Trades today:** 0.
- **Since inception:** Bull −0.374% ($99,626.38) vs SPY TR +1.196% ($746.5225 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY −1.569pp** (was −1.845pp at midday; V's afternoon strength narrowed the gap)

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-07-01)** | **$99,626.38 (−0.374%)** | **SPY $746.5225 + $1.76 div = +1.196% TR** | **Bull TRAILS SPY −1.569pp** |
| **Midday (2026-07-01)** | **$99,693.47 (−0.307%)** | **SPY $749.05 + $1.76 div = +1.538% TR** | **Bull TRAILS SPY −1.845pp** |

---

## Account (midday July 1, 2026 — live Alpaca data ~12:33 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,693.47 |
| Cash | $80,023.72 (80.27%) |
| Long market value | $19,669.75 |
| Buying power | ~$80,023.72 (cash) / $375,170.18 (margin, unused) |
| Last equity (June 30 Alpaca close) | $99,566.00 |

## Open positions (midday July 1, 2026 — live Alpaca data ~12:33 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,190.375 | $11,903.75 | +$968.41 (+8.86%) | 11.94% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $76.175 (6.40%) ✓ |
| V | 22 | $323.57 | $353.00 | $7,766.00 | +$647.46 (+9.10%) | 7.79% | 66033918 (22sh, HWM $353.36 ⬆️ NEW HWM, stop $318.024 ⬆️) ✓ — buffer $34.976 (9.91%) ✓ |

**Sector exposure (midday July 1):**
- Healthcare (LLY): $11,903.75 = 11.94% | Financials (V): $7,766.00 = 7.79% | Cash: $80,023.72 = 80.27%
- No sector above 60% cap ✓

**Trailing stop status (midday July 1 — confirmed via Alpaca live orders ~12:33 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $76.175 = 6.40%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM **$353.36** ⬆️ (auto-ratcheted from $345.81), stop **$318.024** ⬆️ (up from $311.229) ✓ (buffer $34.976 = 9.91%)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions; none missing)

**Midday July 1 notes (~12:33 ET — stop audit 3/3 PASS; 0 trades; no cuts; no tightenings; V strong intraday rally, new HWM):**
- **Shock check:** $99,693.47 vs last_equity $99,566.00 = **+$127.47 = +0.128%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,693.47 vs HWM $101,384.21 = **−1.668%** — NOT triggered ✓ (8.332pp headroom; CB trigger USD 91,245.79)
- **LLY** $1,190.375 (+8.86% from entry, −0.755% today): Continued mild pullback, consistent with the post-Medicare-Bridge-launch "sell the news" pattern already flagged at pre-market/market-open. Not down >3% from entry or up >10%, so no news-scan trigger — no new information to reassess. Buffer 6.40% (widened slightly from market-open's 6.22% as the price ticked up since 09:37). Thesis intact, review_by 2026-07-07 not due. HOLD. Conviction A.
- **V** $353.00 (+9.10% from entry, +2.89% today): Strong intraday rally to a new high; HWM auto-ratcheted to $353.36, trailing stop tightened to $318.024 (was $311.229). Not yet past the +10%-from-entry news-scan trigger, but given the size of today's move a precautionary scan was run: no new catalyst found beyond the already-known stablecoin initiative and the June 29 Piper Sandler Overweight initiation — no thesis break, nothing new specifically driving today's strength. Approaching but below the +15% tighten trigger ($372.10). HOLD. Conviction B. review_by 2026-07-28.
- **No cuts** (−7% rule): both positions well above threshold ✓
- **No tightenings** (+15% trigger = LLY $1,257.56 / V $372.10): neither triggered ✓
- **No new positions** — midday routine manages existing risk only, per playbook.
- **Trades today:** 0.
- **Since inception:** Bull −0.307% ($99,693.47) vs SPY TR +1.538% ($749.05 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY −1.845pp**

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Midday (2026-07-01)** | **$99,693.47 (−0.307%)** | **SPY $749.05 + $1.76 div = +1.538% TR** | **Bull TRAILS SPY −1.845pp** |
| **Market-open (2026-07-01)** | **$99,427.40 (−0.573%)** | **SPY $743.08 + $1.76 div = +0.730% TR** | **Bull TRAILS SPY −1.303pp** |

---

## Account (market-open July 1, 2026 — live Alpaca data ~09:37 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,427.40 |
| Cash | $80,023.72 (80.48%) |
| Long market value | $19,403.68 |
| Buying power | ~$80,023.72 (cash) / $374,425.18 (margin, unused) |
| Last equity (June 30 Alpaca close) | $99,566.00 |

## Open positions (market-open July 1, 2026 — live Alpaca data ~09:37 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,188.10 | $11,881.00 | +$945.66 (+8.65%) | 11.95% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $73.90 (6.22%) ✓ |
| V | 22 | $323.57 | $341.94 | $7,522.68 | +$404.14 (+5.68%) | 7.57% | 66033918 (22sh, HWM $345.81, stop $311.229) ✓ — buffer $30.711 (8.98%) ✓ |

**Sector exposure (market-open July 1):**
- Healthcare (LLY): $11,881.00 = 11.95% | Financials (V): $7,522.68 = 7.57% | Cash: $80,023.72 = 80.48%
- No sector above 60% cap ✓

**Trailing stop status (market-open July 1 — confirmed via Alpaca live orders ~09:37 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $73.90 = 6.22%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $345.81, stop $311.229 ✓ (buffer $30.711 = 8.98%)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions; no fills since pre-market, no missing stops)

**Market-open July 1 notes (~09:37 ET — stop audit 3/3 PASS; 0 trades, none planned; market open confirmed via clock endpoint):**
- **Plan check:** Today's plan block in research-log.md (`plan_date: 2026-07-01`) is empty — pre-market decided to stay in cash given elevated macro-event risk (ADP/ISM/Fed Chair Warsh) and no watchlist name clearing its ATR gate. Nothing to execute; breaking-news gate (step 2) and trade execution (step 4) skipped as not applicable.
- **Shock check:** $99,427.40 vs last_equity $99,566.00 = **−$138.60 = −0.139%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,427.40 vs HWM $101,384.21 = **−1.930%** — NOT triggered ✓ (8.070pp headroom; CB trigger USD 91,245.79)
- **LLY** $1,188.10 (+8.65% from entry, −0.95% since June 30 close): Pulling back further after Medicare Bridge launch today — consistent with the "sell the news" pattern already flagged pre-market; no negative news found. Stop buffer 6.22% — narrower than pre-market's 7.31% but still clear of the 10% trail. Thesis intact, review_by 2026-07-07 not due. HOLD. Conviction A.
- **V** $341.94 (+5.68% from entry, −0.34% since June 30 close): Modest pullback, no negative news. Stop buffer 8.98% ✓. Thesis intact. HOLD. Conviction B. review_by 2026-07-28.
- **No trades today** — plan was empty; no positions to execute.
- **Since inception:** Bull −0.573% ($99,427.40) vs SPY TR +0.730% ($743.08 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY −1.303pp**

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Market-open (2026-07-01)** | **$99,427.40 (−0.573%)** | **SPY $743.08 + $1.76 div = +0.730% TR** | **Bull TRAILS SPY −1.303pp** |
| **Pre-market (2026-07-01)** | **$99,596.72 (−0.403%)** | **SPY $746.65 + $1.76 div = +1.213% TR** | **Bull TRAILS SPY −1.616pp** |

---

## Account (pre-market July 1, 2026 — live Alpaca data ~08:10 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,596.72 |
| Cash | $80,023.72 (80.35%) |
| Long market value | $19,573.00 |
| Buying power | ~$80,023.72 (cash) / $374,899.28 (margin, unused) |
| Last equity (June 30 Alpaca close) | $99,566.00 |

## Open positions (pre-market July 1, 2026 — live Alpaca data ~08:10 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,202.04 | $12,020.40 | +$1,085.06 (+9.92%) | 12.07% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $87.84 (7.31%) ✓ |
| V | 22 | $323.57 | $343.30 | $7,552.60 | +$434.06 (+6.10%) | 7.58% | 66033918 (22sh, HWM $345.81, stop $311.229) ✓ — buffer $32.071 (9.34%) ✓ |

**Sector exposure (pre-market July 1):**
- Healthcare (LLY): $12,020.40 = 12.07% | Financials (V): $7,552.60 = 7.58% | Cash: $80,023.72 = 80.35%
- No sector above 60% cap ✓

**Trailing stop status (pre-market July 1 — confirmed via Alpaca live orders ~08:10 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $87.84 = 7.31%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $345.81, stop $311.229 ✓ (buffer $32.071 = 9.34%)
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 positions)

**Pre-market July 1 notes (~08:10 ET — stop audit 3/3 PASS; no trades, market not yet open; no new positions planned):**
- **Shock check:** $99,596.72 vs last_equity $99,566.00 = **+$30.72 = +0.031%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,596.72 vs HWM $101,384.21 = **−1.763%** — NOT triggered ✓ (8.237pp headroom; CB trigger USD 91,245.79)
- **Macro (pre-market ~08:10 ET):** S&P 500 futures modestly lower (~−0.38%) after Tuesday's best first-half close in years (S&P 500 index 7,499.36, +0.79%). ADP employment (fcst 118K) at 7:15 AM ET, ISM Manufacturing PMI (fcst 53.8) at 9:00 AM ET, and Fed Chair Kevin Warsh speaking on a central-bank panel (with Lagarde/Bailey/Macklem) at the ECB's Sintra forum at 8:00 AM ET — all three land before/around the open. 10yr yield steady at 4.47% — **BELOW 4.75% gate ✓**. Elevated event-risk day; no new positions until data/speech risk clears.
- **LLY** $1,202.04 (+9.92% from entry): Medicare GLP-1 Bridge program **launches TODAY** ($50/month copay for ~20M Medicare Part D patients, Zepbound/Foundayo/Wegovy). This is the confirmatory event behind the June 26 +7.13% rally (already priced in ahead of the formal launch); Leerink PT $1,232 (raised June 25). No new negative news. Next earnings Aug 5. Thesis intact, no invalidation triggered, review_by 2026-07-07 not yet due — no action required today; will assess actual post-launch reaction (utilization data, any commentary) at midday/close. HOLD. Conviction A.
- **V** $343.30 (+6.10% from entry): No negative news. Piper Sandler initiated Overweight (June 29). Visa Destinations (10 markets) and stablecoin initiative continue to build out. Thesis intact. review_by 2026-07-28 not due. HOLD. Conviction B.
- **LRCX ATR gate:** June 29 8.55% (fail), June 30 5.47% (fail, just above the loosened 5% threshold) — gate counter **0/2** fresh sessions under the 2026-07-01 strategy update. Not eligible today.
- **ETN ATR gate:** June 29 2.43% ✓, June 30 4.15% ✓ (both would clear the loosened ≤5% threshold), but the 2026-07-01 strategy update explicitly resets the count to start from July 1 sessions only — pre-update sessions don't carry over. Gate counter **0/2** as of today. Earliest clearance July 2 close if today's session is also ≤5%.
- **Cash-drag check:** Cash at 80.35%, well above the 10–20% target band and above it for multiple weeks. No qualifying entry today: LRCX and ETN both fail the (reset) ATR gate; no other watchlist name (MSFT, COST, JNJ, WMT, PWR) clears its entry gate today; and today carries elevated macro event risk (ADP/ISM/Fed Chair Warsh) before the open. Staying in cash today is the correct, deliberate call, not a default — will re-assess LRCX/ETN gates at every session this week as fresh ≤5% sessions accumulate.
- **Trades today:** 0 (pre-market only; market not yet open).
- **Since inception:** Bull −0.403% ($99,596.72) vs SPY TR +1.213% ($746.65 + $1.76 div vs $739.44 anchor) → **Bull TRAILS SPY −1.616pp**

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Pre-market (2026-07-01)** | **$99,596.72 (−0.403%)** | **SPY $746.65 + $1.76 div = +1.213% TR** | **Bull TRAILS SPY −1.616pp** |
| **Close (2026-06-30)** | **$99,654.56 (−0.345%)** | **SPY $746.72 + $1.76 div = +1.223% TR** | **Bull TRAILS SPY −1.568pp** |


## Account (close June 30, 2026 — live Alpaca data ~15:50 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,654.56 |
| Cash | $80,023.74 (80.30%) — VST stop sale proceeds (40sh × $160.20 = $6,408.00) credited; VST $9.20 dividend still NOT credited as of this run |
| Long market value | $19,630.82 |
| Buying power | ~$80,023.74 (cash) / $375,061.26 (margin, unused — cash account in practice) |
| Last equity (June 29 Alpaca close) | $99,926.54 |

## Open positions (close June 30, 2026 — live Alpaca data ~15:50 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,208.46 | $12,084.60 | +$1,149.26 (+10.51%) | 12.13% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $94.26 (7.80%) ✓ |
| V | 22 | $323.57 | $342.99 | $7,545.78 | +$427.24 (+6.00%) | 7.57% | 66033918 (22sh, HWM $345.81, stop $311.229) ✓ — buffer $31.76 (9.26%) ✓ |

**VST CLOSED:** Trailing stop c8b43d32 filled 13:48 ET June 30 @ $160.20 — P/L +$455.60 (+7.66%) — **WIN** (first win on record). 21 days held. See closed-trades.md.

**Sector exposure (close June 30):**
- Healthcare (LLY): $12,084.60 = 12.13% | Financials (V): $7,545.78 = 7.57% | Cash: $80,023.74 = 80.30%
- No sector above 60% cap ✓ (utilities/energy sector exposure zeroed out with VST exit)

**Trailing stop status (close June 30 — confirmed via Alpaca live orders ~15:50 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $94.26 = 7.80%; LLY at $1,208.46 < HWM — no ratchet today)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $345.81, stop $311.229 ✓ (buffer $31.76 = 9.26%; V at $342.99 < HWM — no ratchet)
- VST (c8b43d32): **FILLED** 13:48 ET @ $160.20 — position closed, stop no longer applicable
**Stop audit: 3/3 PASS ✓** (3 live trailing-stop orders across 2 remaining positions; VST's stop consumed by its own fill, not a missing-stop condition)

**Close June 30 notes (~15:50 ET — stop audit 3/3 PASS; 0 new trades; VST stop fill = first win; end-of-Q2 session):**
- **Today P/L:** −$271.98 (−0.272%) | SPY +$5.85 (+0.79%) from $740.87 → $746.72 | Bull underperformed SPY by −1.06pp today (VST exit + LLY −1.75% sell-the-news pressure into Medicare Bridge launch, vs. broad-market quarter-end strength)
- **Shock check:** $99,654.56 vs last_equity $99,926.54 = **−$271.98 = −0.272%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,654.56 vs HWM $101,384.21 = **−1.706%** — NOT triggered ✓ (8.294pp headroom; CB trigger USD 91,245.79)
- **⭐ VST stop-out (WIN):** Trailing stop c8b43d32 (5% trail) fired 13:48 ET at $160.20 — HWM $168.77. P/L +$455.60 (+7.66%). Entry June 9 @ $148.81, held 21 days. Thesis (Helix+Cogentrix nuclear PPAs) never broke; the 5% tightened trail (applied after the position cleared +15% gain) captured the win during the AI-selloff buffer compression instead of round-tripping further. Post-mortem in closed-trades.md ✓; lessons.md entry added (win, not a loss, but a notable process validation) ✓.
- **LLY** $1,208.46 (+10.51% from entry, −1.75% today): Continued "sell the news" pressure into tomorrow's Medicare Bridge launch (July 1). News scan from midday confirmed thesis intact (Mounjaro/Zepbound revenue +56% YoY, raised FY guidance, Innovent + 4E Therapeutics deals). HWM $1,238 not touched today — no ratchet. Buffer 7.80% ✓. HOLD. Conviction A. review_by 2026-07-07 (pre-market July 1 should assess post-bridge-launch reaction).
- **V** $342.99 (+6.00% from entry, +0.39% today): Modest gain on quarter-end flows; thesis intact. Buffer 9.26% ✓. HOLD. Conviction B (0/3 C-weeks). review_by 2026-07-28.
- **Market context (June 30, end of Q2):** SPY closed $746.72 (+0.79%), extending Monday's rally (Dow closed above 52,000 for the first time; US-Iran ceasefire holding, Strait of Hormuz reopened) into the final session of what is shaping up to be the best quarter for the S&P 500 and Nasdaq in six years. Tech/communication-services led; GOOGL's first week as a Dow component continued to draw passive flows. No negative news for LLY or V theses; the LLY weakness is sell-the-news positioning, not fundamental.
- **LRCX ATR gate:** Today's range H $436.97 / L $414.01 / C $435.50 = $22.96 = **5.27% ATR** ⚠️ — session FAILS (>3% threshold). Gate counter resets to **0/3** again. Fresh 3 consecutive ≤3% sessions needed starting July 1. Earliest entry pushed to July 9+ at best, more realistically later given the repeated resets.
- **Exit reconciliation:** VST exit fully reconciled — closed-trades.md ✓ (WIN entry added), lessons.md ✓ (win lesson added; no loss-lesson required since this was a winning trade). LLY and V held, no other exits.
- **Trades today:** 1 (VST trailing-stop exit; 0 new entries — close routine does not place orders).
- **Since inception:** Bull −0.345% vs SPY TR +1.223% → **Bull TRAILS SPY −1.568pp** (was −1.378pp at midday; SPY's end-of-quarter strength plus the VST exit and LLY pre-event softness widened the gap modestly)

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-06-30)** | **$99,654.56 (−0.345%)** | **SPY $746.72 + $1.76 div = +1.223% TR** | **Bull TRAILS SPY −1.568pp** |
| **Midday (2026-06-30)** | **$99,771.24 (−0.229%)** | **SPY $746.18 + $1.76 div = +1.149% TR** | **Bull TRAILS SPY −1.378pp** |

---

## Account (midday June 30, 2026 — live Alpaca data ~12:32 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,771.24 |
| Cash | $73,615.74 (73.80%) — VST div $9.20 payable today, not yet credited |
| Long market value | $26,155.50 |
| Buying power | ~$73,615.74 |
| Last equity (June 29 Alpaca close) | $99,926.54 |

## Open positions (midday June 30, 2026 — live Alpaca data ~12:32 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,209.485 | $12,094.85 | +$1,159.51 (+10.60%) | 12.12% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $95.285 (7.88%) ✓ |
| V | 22 | $323.57 | $343.315 | $7,552.93 | +$434.39 (+6.10%) | 7.57% | 66033918 (22sh, HWM $345.81, stop $311.229) ✓ — buffer $32.086 (9.35%) ✓ |
| VST | 40 | $148.81 | $162.74 | $6,509.60 | +$557.20 (+9.36%) | 6.53% | c8b43d32 (40sh, 5% trail, HWM $168.77, stop $160.3315) ✓ — buffer $2.4085 (1.48%) ⚠️ CRITICAL (improved from 0.76% at open) |

**Sector exposure (midday June 30):**
- Healthcare (LLY): $12,094.85 = 12.12% | Financials (V): $7,552.93 = 7.57% | Utilities/Energy (VST): $6,509.60 = 6.53% | Cash: $73,615.74 = 73.78%
- No sector above 60% cap ✓

**Trailing stop status (midday June 30 — confirmed via Alpaca live orders ~12:32 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $95.285 = 7.88%; LLY at $1,209.49 < HWM — no ratchet today)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $345.81, stop $311.229 ✓ (buffer $32.086 = 9.35%; V at $343.315 < HWM — no ratchet)
- VST (c8b43d32): 40sh — 5% trail, HWM $168.77, stop $160.3315 ✓ (buffer $2.4085 = 1.48% ⚠️ CRITICAL — improved from 0.76% at market-open; VST recovering +0.22% intraday)
**Stop audit: 4/4 PASS ✓**

**Midday June 30 notes (~12:32 ET — stop audit 4/4 PASS; 0 trades; no cuts; no tightenings; end-of-quarter SPY rally):**
- **Shock check:** $99,771.24 vs last_equity $99,926.54 = **−$155.30 = −0.155%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,771.24 vs HWM $101,384.21 = **−1.593%** — NOT triggered ✓ (8.407pp headroom; CB trigger USD 91,245.79)
- **LLY** $1,209.485 (+10.60% from entry, −1.66% today): "Sell the news" pressure ahead of Medicare Bridge launch July 1. News scan confirms THESIS INTACT: Mounjaro $8.7B (+125% YoY), Zepbound $4.1B (+80% YoY), total Q2 revenue $19.8B (+56%), full-year guidance raised $82-85B. Innovent China deal for Verzenios; 4E Therapeutics acquisition (non-opioid pain). No thesis break — today's selling is pre-event caution, not fundamental deterioration. HWM $1,238 not exceeded; no ratchet. Buffer 7.88% comfortable ✓. HOLD. Conviction A. review_by 2026-07-07.
- **V** $343.315 (+6.10% from entry, +0.49% today): Outperforming today — defensive financials + end-of-quarter flows. HWM $345.81 — V at $343.315 approaching HWM. Buffer 9.35% ✓. Thesis intact. HOLD. Conviction B (0/3 C-weeks). review_by 2026-07-28.
- **VST** $162.74 (+9.36% from entry, +0.22% today): Stop buffer recovered from ultra-critical 0.76% to 1.48% as VST rebounds intraday. Dividend $9.20 payable today (not yet credited). News scan: Buy consensus, analyst fair value ~$225, Q1 net income $980M reaffirmed, Cogentrix acquisition intact. No negative news. HOLD with 5% trailing stop. Conviction A. review_by 2026-07-07. Earnings Aug 6 (outside 2-day window ✓).
- **No cuts** (−7% rule): all positions well above threshold ✓
- **No tightenings** (+15% trigger = LLY $1,257.56 / V N/A / VST $171.13): none triggered ✓
- **News scan (LLY >10% from entry):** Thesis confirmed; sell-the-news temporary pressure. Medicare Bridge is an 18-month program — fundamental driver intact.
- **End-of-quarter context:** SPY +0.718% today to $746.18 — last trading day of Q2 window dressing + index rebalancing boosting broad market. Bull's defensive positioning (healthcare pulling back on sell-the-news; utilities/financials steady) underperforming SPY's tech-led quarter-end rally. Expected divergence on Q2 end day.
- **VST dividend:** $9.20 ($0.23/sh × 40sh) payable today June 30 — not yet reflected in cash. May credit EOD. Close routine should confirm.
- **LRCX ATR gate:** Session 2/3 attempt today June 30. Need ≤3% ATR range for session to count. Today's range: $746.6 - $740.9 for SPY; LRCX data available at close. Assess at close routine.
- **Since inception:** Bull −0.229% vs SPY TR +1.149% → **Bull TRAILS SPY −1.378pp** (end-of-quarter SPY rally widens gap; cash drag + LLY sell-the-news)

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Midday (2026-06-30)** | **$99,771.24 (−0.229%)** | **SPY $746.18 + $1.76 div = +1.149% TR** | **Bull TRAILS SPY −1.378pp** |
| **Market-open (2026-06-30)** | **$99,699.27 (−0.301%)** | **SPY $740.87 + $1.76 div = +0.431% TR est.** | **Bull TRAILS SPY est. −0.732pp** |
| **Close (2026-06-29)** | **$99,940.72 (−0.059%)** | **$740.87 + $1.76 div = +0.431% TR** | **Bull TRAILS SPY −0.490pp** |

---

## Account (market-open June 30, 2026 — live Alpaca data ~09:36 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,699.27 |
| Cash | $73,615.74 (73.91%) |
| Long market value | $26,083.53 |
| Buying power | ~$73,615.74 |
| Last equity (June 29 Alpaca close) | $99,926.54 |

## Open positions (market-open June 30, 2026 — live Alpaca data ~09:36 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,213.76 | $12,137.65 | +$1,202.31 (+10.99%) | 12.17% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $99.56 (8.20%) ✓ |
| V | 22 | $323.57 | $340.36 | $7,487.92 | +$369.38 (+5.19%) | 7.51% | 66033918 (22sh, HWM $345.81, stop $311.229) ✓ — buffer $29.13 (8.55%) ✓ |
| VST | 40 | $148.81 | $161.56 | $6,462.40 | +$510.00 (+8.57%) | 6.48% | c8b43d32 (40sh, 5% trail, HWM $168.77, stop $160.3315) ✓ — buffer $1.23 (0.76%) ⚠️⚠️ ULTRA CRITICAL |

**Sector exposure (market-open June 30):**
- Healthcare (LLY): $12,137.65 = 12.17% | Financials (V): $7,487.92 = 7.51% | Utilities/Energy (VST): $6,462.40 = 6.48% | Cash: $73,615.74 = 73.84%
- No sector above 60% cap ✓

**Trailing stop status (market-open June 30 — confirmed via Alpaca live orders ~09:36 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $99.56 = 8.20%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $345.81, stop $311.229 ✓ (buffer $29.13 = 8.55%)
- VST (c8b43d32): 40sh — 5% trail, HWM $168.77, stop $160.3315 ✓ (buffer $1.23 = 0.76%) ⚠️⚠️ ULTRA CRITICAL
**Stop audit: 4/4 PASS ✓**

**Market-open June 30 notes (~09:36 ET — stop audit 4/4 PASS; 0 trades; pre-market did not run; VST stop at knife-edge 0.76%):**
- **Shock check:** $99,699.27 vs last_equity $99,926.54 = **−$227.27 = −0.227%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,699.27 vs HWM $101,384.21 = **−1.664%** — NOT triggered ✓ (8.336pp headroom)
- **Pre-market did NOT run today:** No June 30 plan in research-log.md. Plan stale. No new trades placed per playbook.
- **⚠️⚠️ VST ULTRA CRITICAL:** $161.56 → stop $160.3315 = buffer $1.23 (0.76%). Down 0.50% intraday. Stop may fire any moment. Thesis intact (Helix+Cogentrix nuclear PPAs). Do NOT override stop. If fires → exit = +8.57% gain = first WIN. Close/midday must record exit if fired.
- **LLY** $1,213.76 (+10.99% from entry): Down 1.31% today from $1,229.93 yesterday. Medicare Bridge launches TOMORROW July 1 — possible "sell the news" pressure today. Pre-market June 29 HOLD decision stands (review_by 2026-07-07). Buffer 8.20% comfortable ✓.
- **V** $340.36 (+5.19% from entry): Down 0.38% intraday. Thesis intact. Buffer 8.55% ✓.
- **VST dividend $9.20:** Payable today — may credit to cash later today. Currently cash unchanged at $73,615.74.
- **LRCX ATR gate:** Session 2/3 today (June 30). Need ≤3% ATR range. Gate counter 0/3 after June 29 failed (8.76%). Assess at close.
- **Since inception:** Bull −0.301% vs SPY TR est. +0.431% → **Bull TRAILS SPY est. −0.732pp**

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Market-open (2026-06-30)** | **$99,699.27 (−0.301%)** | **SPY $740.87 + $1.76 div = +0.431% TR est.** | **Bull TRAILS SPY est. −0.732pp** |
| **Close (2026-06-29)** | **$99,940.72 (−0.059%)** | **$740.87 + $1.76 div = +0.431% TR** | **Bull TRAILS SPY −0.490pp** |

---

## Account (close June 29, 2026 — live Alpaca data ~15:51 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,940.72 |
| Cash | $73,615.74 (73.66%) |
| Long market value | $26,324.98 |
| Buying power | ~$73,615.74 |
| Last equity (June 26 Alpaca close) | $99,633.60 |

## Open positions (close June 29, 2026 — live Alpaca data ~15:51 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,228.07 | $12,280.70 | +$1,345.36 (+12.30%) | 12.29% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 ✓ — buffer $113.87 (9.27%) ✓ |
| V | 22 | $323.57 | $342.515 | $7,535.33 | +$416.79 (+5.86%) | 7.54% | 66033918 (22sh, HWM $345.81, stop $311.229) ✓ — buffer $31.29 (9.15%) ✓ |
| VST | 40 | $148.81 | $162.66 | $6,506.40 | +$554.00 (+9.31%) | 6.51% | c8b43d32 (40sh, 5% trail, HWM $168.77, stop $160.3315) ✓ — buffer $2.33 (1.43%) ⚠️⚠️ CRITICAL |

**Sector exposure (close June 29):**
- Healthcare (LLY): $12,280.70 = 12.29% | Financials (V): $7,535.33 = 7.54% | Utilities/Energy (VST): $6,506.40 = 6.51% | Cash: $73,615.74 = 73.66%
- No sector above 60% cap ✓

**Trailing stop status (close June 29 — confirmed via Alpaca live orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $113.87 = 9.27%; LLY closed $1,228.07 < HWM — no new ratchet)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $345.81, stop $311.229 ✓ (buffer $31.29 = 9.15%; V closed $342.515 < HWM $345.81 — no ratchet)
- VST (c8b43d32): 40sh — 5% trail, HWM $168.77, stop $160.3315 ✓ (buffer $2.33 = 1.43% ⚠️⚠️ CRITICAL — worsened from midday 2.40%; VST −0.50% this afternoon)
**Stop audit: 4/4 PASS ✓**

**Close June 29 notes (~15:51 ET — stop audit 4/4 PASS; 0 trades; SPY +1.09% tech rally; Bull underperformed; VST buffer ⚠️⚠️ more critical):**
- **Today P/L:** +$307.12 (+0.308%) | SPY +$8.005 (+1.093%) from $732.865 → $740.87 | Bull underperformed SPY by −0.785pp today
- **Shock check:** $99,940.72 vs last_equity $99,633.60 = **+$307.12 = +0.308%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,940.72 vs HWM $101,384.21 = **−1.424%** — NOT triggered ✓ (8.576pp headroom; CB trigger USD 91,245.79)
- **⭐ LLY** $1,228.07 (+12.30% from entry, +1.65% today): HWM $1,238.00 not exceeded today. **Medicare Bridge July 1 TOMORROW — MANDATORY pre-market June 30 hold/trim/exit decision.** Stop buffer 9.27% ✓. Below +15% tighten trigger ($1,257.56). HOLD. Conviction A. review_by 2026-07-07.
- **V** $342.515 (+5.86% from entry, +1.87% today): Strong on tech/Nasdaq recovery. V closed $342.515 < HWM $345.81 — no ratchet today. Stop buffer 9.15% ✓. Thesis intact. HOLD. Conviction B (0/3 C-weeks). review_by 2026-07-28.
- **VST** $162.66 (+9.31% from entry, **−0.50% today**) ⚠️⚠️: Stop buffer 1.43% CRITICAL — worse than midday (2.40%). Utilities lagged tech rally. Thesis intact (Helix+Cogentrix, nuclear PPAs). VST dividend USD 9.20 payable TOMORROW June 30. Do NOT override stop. HOLD with stop. Conviction A. review_by 2026-07-07.
- **Market context (June 29):** S&P 500 +1.1%, Nasdaq +1.8% on US-Iran peace talks resuming and Supreme Court protecting Fed governor Lisa Cook's position (Fed independence signal). GOOGL Dow Jones inclusion drove broad tech strength. Bull's defensive healthcare/financials/utilities lagged the tech-led recovery. Cash drag + low-beta portfolio = underperformed on a strong tech day.
- **Since inception:** Bull −0.059% vs SPY TR +0.431% → **Bull TRAILS SPY −0.490pp** (reversed from +0.344pp lead at June 26 close; SPY +1.093% vs Bull +0.308% swung the race −0.785pp today)
- **LRCX ATR gate:** Today H $414.98 / L $379.10 / C $409.645 = range $35.88 = **8.76% ATR** ⚠️ — session 1/3 FAILS. Gate counter reset to **0/3**. Earliest entry now July 9+ (need 3 consecutive ≤3% sessions starting June 30).
- **VST dividend:** USD 9.20 payable TOMORROW June 30 — cash credit expected.
- **Exit reconciliation:** No exits today. All 3 positions held. closed-trades.md current ✓.
- **Trades today:** 0.

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-06-29)** | **$99,940.72 (−0.059%)** | **$740.87 + $1.76 div = +0.431% TR** | **Bull TRAILS SPY −0.490pp** |
| **Midday (2026-06-29)** | **$99,842.69 (−0.157%)** | **SPY ~$737–738 midday + $1.76 div ≈ −0.028% TR** | **Bull roughly tracking SPY** |
| **Market-open (2026-06-29)** | **$99,998.76 (−0.001%)** | **SPY $737.47 + $1.76 div = −0.028% TR** | **Bull LEADS SPY +0.027pp** |
| **Close (2026-06-26)** | **$99,692.61 (−0.307%)** | **$732.865 + $1.76 div = −0.651% TR** | **Bull LEADS SPY +0.344pp ✓** |

---

## Account (midday June 29, 2026 — live Alpaca data ~12:32 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,842.69 |
| Cash | $73,615.74 (73.74%) |
| Long market value | $26,226.95 |
| Buying power | ~$73,615.74 |
| Last equity (June 26 Alpaca close) | $99,633.60 |

## Open positions (midday June 29, 2026 — live Alpaca data ~12:32 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,215.14 | $12,151.40 | +$1,216.06 (+11.12%) | 12.17% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00, stop $1,114.20 — buffer $100.94 (8.31%) ✓ |
| V | 22 | $323.57 | $341.125 | $7,504.75 | +$386.21 (+5.43%) | 7.52% | 66033918 (22sh, HWM **$345.81** ⬆️ NEW HWM ratcheted, stop **$311.229** ⬆️) ✓ — buffer $29.90 (8.77%) ✓ |
| VST | 40 | $148.81 | $164.27 | $6,570.80 | +$618.40 (+10.39%) | 6.58% | c8b43d32 (40sh, 5% trail, HWM $168.77, stop $160.3315) ✓ — buffer $3.94 (2.40%) ⚠️⚠️ CRITICAL |

**Sector exposure (midday June 29):**
- Healthcare (LLY): $12,151.40 = 12.17% | Financials (V): $7,504.75 = 7.52% | Energy/Utilities (VST): $6,570.80 = 6.58% | Cash: $73,615.74 = 73.74%
- No sector above 60% cap ✓

**Trailing stop status (midday June 29 — confirmed via Alpaca live orders ~12:32 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00, stop $1,114.20 ✓ (buffer $100.94 = 8.31%)
- LLY (25989fb5): 3sh — HWM $1,238.00, stop $1,114.20 ✓
- V (66033918): 22sh — HWM **$345.81** ⬆️ (ratcheted from $340.94), stop **$311.229** ⬆️ ✓ (buffer $29.90 = 8.77%)
- VST (c8b43d32): 40sh — 5% trail, HWM $168.77, stop $160.3315 ✓ (buffer $3.94 = 2.40% ⚠️⚠️ CRITICAL)
**Stop audit: 4/4 PASS ✓**

**Midday June 29 notes (~12:32 ET — stop audit 4/4 PASS; 0 trades; LLY ATH thesis confirmed; V HWM ratcheted; VST dividend tomorrow):**
- **Shock check:** $99,842.69 vs last_equity $99,633.60 = **+$209.09 = +0.210%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,842.69 vs HWM $101,384.21 = **−1.52%** — NOT triggered ✓ (8.48pp headroom)
- **⭐ LLY** $1,215.14 (+11.12% from entry): Hit all-time high today per news scan; weight-loss drug (Foundayo oral) accelerating; avg analyst PT $1,294 (17% upside). HWM $1,238 (set at open). Medicare Bridge July 1 TOMORROW. Stop buffer 8.31% ✓. Below +15% tighten trigger ($1,257.56). HOLD. Conviction A. review_by 2026-07-07.
- **V** $341.125 (+5.43% from entry): V HWM auto-ratcheted to $345.81 today (up from $340.94), stop improved $305.946→$311.229. Buffer 8.77% ✓. Thesis intact. HOLD. Conviction B (0/3 C-weeks). review_by 2026-07-28.
- **VST** $164.27 (+10.39% from entry) ⚠️⚠️: Stop buffer 2.40% CRITICAL (slightly improved from 2.27% at market-open). Thesis intact (Helix+Cogentrix+AI power demand). MS PT $210 (minor cut from $212 on June 24 = noise). Dividend $0.23/sh payable TOMORROW June 30. Do NOT manually override stop. HOLD with stop. Conviction A. review_by 2026-07-07.
- **News scan (positions >10% from entry — LLY, VST):** Both thesis-confirmed. LLY ATH on weight-loss sales; VST Helix/AI power intact. No thesis breaks found.
- **No cuts, no tightenings, no new positions** — all positions within guardrails ✓
- **LRCX ATR gate:** Session 1/3 in progress (started at market-open; confirm pass/fail at close). Earliest entry July 7+.
- **VST dividend reminder:** $0.23/sh × 40sh = $9.20 payable June 30 — will show as cash addition.

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Midday (2026-06-29)** | **$99,842.69 (−0.157%)** | **SPY ~$737–738 midday + $1.76 div ≈ −0.028% TR** | **Bull roughly tracking SPY** |
| **Market-open (2026-06-29)** | **$99,998.76 (−0.001%)** | **SPY $737.47 + $1.76 div = −0.028% TR** | **Bull LEADS SPY +0.027pp** |
| **Close (2026-06-26)** | **$99,692.61 (−0.307%)** | **$732.865 + $1.76 div = −0.651% TR** | **Bull LEADS SPY +0.344pp ✓** |

---

## Account (market-open June 29, 2026 — live Alpaca data ~09:36 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,998.76 |
| Cash | $73,615.74 (73.62%) |
| Long market value | $26,383.02 |
| Buying power | ~$73,615.74 |
| Last equity (June 26 Alpaca close) | $99,633.60 |

## Open positions (market-open June 29, 2026 — live Alpaca data ~09:36 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,233.30 | $12,333.00 | +$1,397.66 (+12.78%) | 12.33% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,238.00 ⬆️ NEW HWM (ratcheted above $1,215.76 Friday; ABOVE Leerink PT $1,232), stop $1,114.20 — buffer $119.10 (9.66%) ✓ |
| V | 22 | $323.57 | $340.20 | $7,484.31 | +$365.77 (+5.14%) | 7.48% | 66033918 (22sh, HWM $340.94, stop $306.846) ✓ — buffer $33.35 (9.80%) ✓ |
| VST | 40 | $148.81 | $164.06 | $6,562.40 | +$610.00 (+10.25%) | 6.56% | c8b43d32 (40sh, 5% trail, HWM $168.77, stop $160.3315) ✓ — buffer $3.73 (2.27%) ⚠️⚠️ CRITICAL — improved from 1.86% Friday, but still narrow |

**Sector exposure (market-open June 29):**
- Healthcare (LLY): $12,333.00 = 12.33% | Financials (V): $7,484.31 = 7.48% | Energy/Utilities (VST): $6,562.40 = 6.56% | Cash: $73,615.74 = 73.62%
- No sector above 60% cap ✓

**Trailing stop status (market-open June 29 — confirmed via Alpaca live orders ~09:36 ET):**
- LLY (d4147484): 7sh — HWM $1,238.00 ⬆️, stop $1,114.20 ✓ (buffer $119.10 = 9.66%; new HWM above Leerink PT $1,232)
- LLY (25989fb5): 3sh — HWM $1,238.00 ⬆️, stop $1,114.20 ✓
- V (66033918): 22sh — HWM $340.94, stop $306.846 ✓ (buffer $33.35 = 9.80%)
- VST (c8b43d32): 40sh — 5% trail, HWM $168.77, stop $160.3315 ✓ (buffer $3.73 = 2.27% ⚠️⚠️ CRITICAL)
**Stop audit: 4/4 PASS ✓**

**Market-open June 29 notes (~09:36 ET — stop audit 4/4 PASS; 0 trades; GOOGL Dow inclusion driving SPY rally):**
- **Shock check:** $99,998.76 vs last_equity $99,633.60 = **+$365.16 = +0.37%** — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,998.76 vs HWM $101,384.21 = **−1.366%** — NOT triggered ✓ (8.634pp headroom)
- **⭐ LLY** $1,233.30 (+12.78% from entry): New HWM $1,238.00 — ABOVE Leerink PT $1,232. Medicare Bridge launches TOMORROW (July 1). Stop at $1,114.20 (9.66% buffer) ✓. Conviction A. review_by 2026-07-07.
- **VST** $164.06 (+10.25% from entry): Stop buffer 2.27% — improved marginally from 2.23% pre-market. Still CRITICAL. VST dividend payment tomorrow ($0.23/sh × 40 = $9.20). Thesis intact. HOLD with stop. Conviction A.
- **V** $340.20 (+5.14% from entry): Defensive thesis intact; gaining with GOOGL-Dow rally. HWM $340.94 nearly touched. Stop buffer 9.80% healthy ✓. Conviction B.
- **No new positions:** Plan was empty; all guardrails confirmed. LRCX ATR gate session 1/3 in progress (2.45% ATR early trading ≤3% threshold — confirm at close). Next entry window earliest July 7.
- **SPY:** $737.47 — rallying +1.12% on GOOGL Dow Jones inclusion. Lead compressed vs Friday.

## Monday conviction ratings (June 29, 2026 — unchanged from pre-market)

| Symbol | Rating | 3-consecutive-C trigger | Notes |
|--------|--------|------------------------|-------|
| LLY | **A** | N/A | +12.78% from entry; new HWM $1,238 above Leerink PT $1,232; Medicare Bridge launches TOMORROW |
| V | **B** | 0/3 weeks at C | +5.14% from entry; defensive strength; GOOGL-Dow rally; July 28 earnings gate |
| VST | **A** | N/A | +10.25% from entry; Helix+Cogentrix intact; 5% trail stop buffer 2.27% CRITICAL ⚠️⚠️ |

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Market-open (2026-06-29)** | **$99,998.76 (−0.001%)** | **SPY $737.47 + $1.76 div = −0.028% TR** | **Bull LEADS SPY +0.027pp** |
| **Close (2026-06-26)** | **$99,692.61 (−0.307%)** | **$732.865 + $1.76 div = −0.651% TR** | **Bull LEADS SPY +0.344pp ✓** |

---

## Account (close June 26, 2026 — live Alpaca data ~15:51 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,692.61 |
| Cash | $73,615.74 (73.87%) |
| Long market value | $26,076.87 |
| Buying power | ~$73,615.74 |
| Last equity (June 25 Alpaca close) | $98,874.88 |

## Open positions (close June 26, 2026 — live Alpaca data ~15:51 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,211.575 | $12,115.75 | +$1,180.41 (+10.79%) | 12.15% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,215.76 ⬆️ NEW HIGH (was $1,207.589), stop $1,094.184 ⬆️ ✓ — buffer $117.39 (9.69%) ✓ |
| V | 22 | $323.57 | $337.46 | $7,424.12 | +$305.58 (+4.29%) | 7.44% | 66033918 (22sh, HWM $339.94, stop $305.946) ✓ — buffer $31.51 (9.34%) ✓ |
| VST | 40 | $148.81 | $163.37 | $6,534.80 | +$582.40 (+9.78%) | 6.55% | c8b43d32 (40sh, 5% trail, HWM $168.77, stop $160.3315) ✓ — buffer $3.04 (1.86%) ⚠️⚠️ CRITICAL: VST fell −2.62% today; stop at risk Mon open |

**Sector exposure (close June 26):**
- Healthcare (LLY): $12,115.75 = 12.15% | Financials (V): $7,424.12 = 7.44% | Energy/Utilities (VST): $6,534.80 = 6.55% | Cash: $73,615.74 = 73.87%
- No sector above 60% cap ✓

**Trailing stop status (close June 26 — confirmed via Alpaca live orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM $1,215.76 ⬆️ (auto-ratcheted from $1,207.589 during afternoon session), stop $1,094.184 ⬆️ ✓ (buffer $117.39 = 9.69%)
- LLY (25989fb5): 3sh — HWM $1,215.76, stop $1,094.184 ✓
- V (66033918): 22sh — HWM $339.94, stop $305.946 ✓ (buffer $31.51 = 9.34%; today's high below HWM — no ratchet)
- VST (c8b43d32): 40sh — 5% trail, HWM $168.77, stop $160.3315 ✓ (buffer $3.04 = 1.86% ⚠️⚠️ — down from 3.37% at midday; VST continued decline afternoon)
**Stop audit: 4/4 PASS ✓**

**Close June 26 notes (~15:51 ET — stop audit 4/4 PASS; 0 trades; LLY ⭐ new HWM; VST buffer ⚠️⚠️; Bull LEADS SPY):**
- **Today P/L:** +$817.73 (+0.827%) | SPY +$1.295 (+0.177%) | Bull outperformed SPY by +0.650pp today
- **Shock check:** +$817.73 (+0.827%) vs last_equity $98,874.88 — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,692.61 vs HWM $101,384.21 = **−1.669%** — NOT triggered ✓ (8.331pp headroom; CB trigger USD 91,245.79)
- **⭐ LLY** $1,211.575 (+10.79% from entry, +7.44% today): Medicare Bridge July 1 launch confirmed at USD 50/month Medicare pricing — thesis-confirming rally. HWM auto-ratcheted again to $1,215.76 (new position all-time high). Stop improved $1,086.83→$1,094.184. Buffer 9.69% excellent. ⚠️ **PRE-MARKET JUNE 30 MANDATORY hold/trim/exit decision (Monday — 1 trading day away).** HOLD. Conviction A. review_by 2026-07-01.
- **V** $337.46 (+4.29% from entry, +2.10% today): Outperformed market in tech sell-off — defensive financials thesis intact. HWM $339.94 — stop buffer 9.34% comfortable. HOLD. Conviction B (0/3 C-weeks). review_by 2026-07-28.
- **VST** $163.37 (+9.78% from entry, **−2.62% today**) ⚠️⚠️: Down significantly in risk-off tech selloff (AI valuation concerns + OpenAI IPO delay). Thesis unchanged (Helix+Cogentrix, nuclear PPAs). Stop buffer **CRITICAL at 1.86%** (USD 3.04 above stop $160.3315). Stop has NOT fired. Monday open — if VST opens below $160.33 the stop fires. STRONG HOLD (thesis intact) but stop may trigger naturally. review_by 2026-07-07.
- **Market context (June 26):** Tech sell-off on AI valuation concerns + OpenAI IPO delay. S&P 500 −0.5% from intraday high; Nasdaq -4% on the week. Chip stocks down 10% (LRCX, Sandisk, WD) — LRCX ATR gate reset by today's large move; now needs fresh 3 consecutive ≤3% sessions, earliest entry July 7+. Defensives (healthcare, financials) outperformed, supporting Bull's positions.
- **LRCX:** Down ~10% today — ATR gate definitively reset. New earliest entry estimate: July 7+ (need 3 consecutive ≤3% sessions from Monday June 29).
- **Exit reconciliation:** No exits today. All 3 positions held. closed-trades.md current ✓.
- **Friday watchdog:** Last weekly-review.md entry is June 19 (exactly 7 days ago — NOT more than 7 days). Watchdog NOT triggered. Weekly review scheduled today at 4:30 PM ET.
- **Trades today:** 0. Week of June 23 position slots: all 3 slots unused (LRCX ATR gate reset; PWR deferred).

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-06-26)** | **$99,692.61 (−0.307%)** | **$732.865 + $1.76 div = −0.651% TR** | **Bull LEADS SPY +0.344pp ✓** |
| **Midday (2026-06-26)** | **$99,680.86 (−0.319%)** | **$734.30 + $1.76 div = −0.457% TR** | **Bull LEADS SPY +0.138pp ✓** |
| **Market-open (2026-06-26)** | **$99,155.92 (−0.844%)** | **$728.68 + $1.76 div = −1.217% TR** | **Bull LEADS SPY +0.373pp ✓** |
| **Pre-mkt (2026-06-26)** | **$98,723.49 (−1.277%)** | **$733.33 close + $1.76 div = −0.588% TR** | **Bull TRAILED SPY ~0.689pp** |

---

## Account (midday June 26, 2026 — live Alpaca data ~12:34 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,680.86 |
| Cash | $73,615.74 (73.87%) |
| Long market value | $26,065.12 |
| Buying power | ~$73,615.74 |
| Last equity (June 25 Alpaca close) | $98,874.88 |

## Open positions (midday June 26, 2026 — live Alpaca data ~12:34 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,198.76 | $11,987.60 | +$1,052.26 (+9.62%) | 12.03% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,207.589 ⬆️ NEW HIGH, stop $1,086.8301 ⬆️ (was $1,064.457) ✓ — buffer $111.93 (9.34%) ✓ |
| V | 22 | $323.57 | $338.18 | $7,439.96 | +$321.42 (+4.52%) | 7.47% | 66033918 (22sh, HWM $339.94, stop $305.946) ✓ — buffer $32.234 (9.54%) ✓ |
| VST | 40 | $148.81 | $165.91 | $6,636.40 | +$684.00 (+11.49%) | 6.66% | c8b43d32 (40sh, 5% trail, HWM $168.77, stop $160.3315) ✓ — buffer $5.5785 (3.37%) ⚠️ monitoring |

**Sector exposure (midday June 26):**
- Healthcare (LLY): $11,987.60 = 12.03% | Financials (V): $7,439.96 = 7.47% | Energy/Utilities (VST): $6,636.40 = 6.66% | Cash: $73,615.74 = 73.87%
- No sector above 60% cap ✓

**Trailing stop status (midday June 26 — confirmed via Alpaca live orders ~12:34 ET):**
- LLY (d4147484): 7sh — HWM $1,207.589 ⬆️ (auto-ratcheted from $1,182.73), stop $1,086.8301 ⬆️ ✓ (buffer $111.93 = 9.34%)
- LLY (25989fb5): 3sh — HWM $1,207.589, stop $1,086.8301 ✓
- V (66033918): 22sh — HWM $339.94, stop $305.946 ✓ (buffer $32.234 = 9.54%; today's high below HWM — no ratchet)
- VST (c8b43d32): 40sh — 5% trail, HWM $168.77, stop $160.3315 ✓ (buffer $5.5785 = 3.37% ⚠️ — down from 3.91% at market-open; today's high below HWM — no ratchet)
**Stop audit: 4/4 PASS ✓**

**Midday June 26 notes (~12:34 ET — no cuts; no tightenings; stop audit 4/4 PASS; Bull leads SPY):**
- **Shock check:** +$805.98 (+0.815%) vs last_equity $98,874.88 — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,680.86 vs HWM $101,384.21 = **−1.681%** — NOT triggered ✓ (8.319pp headroom)
- **LLY** $1,198.76 (+9.62% from entry, +6.30% today) ⭐: HWM auto-ratcheted to $1,207.589 (new intraday high), stop improved $1,064.457→$1,086.8301. Buffer 9.34% comfortable. Medicare Bridge July 1 (Monday) — large rally today is thesis-confirming (bridge details positive, Leerink PT $1,232). NOT at +15% tighten trigger ($1,257.56) — no tighten needed. ⚠️ **Pre-market June 30 MANDATORY hold/trim/exit decision (1 trading day away — Monday June 29 pre-market should draft the decision framework).** HOLD. Conviction A.
- **V** $338.18 (+4.52% from entry, +2.32% today): Visa Destinations platform showing commercial traction. HWM $339.94 — stop buffer 9.54% comfortable. Thesis intact. HOLD. Conviction B (0/3 C-weeks). review_by 2026-07-28.
- **VST** $165.91 (+11.49% from entry, −1.11% today) ⭐⭐: Down today in risk-off tape; news scan confirms thesis intact (Helix+Cogentrix, 20 analysts Strong Buy, consensus PT $222.89). Stop buffer 3.37% — narrow but improved from pre-market 2.90%. NOT at +15% tighten trigger ($171.13). STRONG HOLD. Conviction A. review_by 2026-07-07.
- **SPY** $734.30 (+0.13% today from $733.33 close): Mild recovery from morning risk-off — market broadly constructive in afternoon.
- **No cuts, no tightenings, no new positions** — all positions within guardrails ✓

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Midday (2026-06-26)** | **$99,680.86 (−0.319%)** | **$734.30 + $1.76 div = −0.457% TR** | **Bull LEADS SPY +0.138pp ✓** |
| **Market-open (2026-06-26)** | **$99,155.92 (−0.844%)** | **$728.68 + $1.76 div = −1.217% TR** | **Bull LEADS SPY +0.373pp ✓** |
| **Pre-mkt (2026-06-26)** | **$98,723.49 (−1.277%)** | **$733.33 close + $1.76 div = −0.588% TR** | **Bull TRAILED SPY ~0.689pp** |

---

## Account (market-open June 26, 2026 — live Alpaca data ~09:37 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,155.92 |
| Cash | $73,615.74 (74.24%) |
| Long market value | $25,540.18 |
| Buying power | ~$73,615.74 |
| Last equity (June 25 Alpaca close) | $98,874.88 |

## Open positions (market-open June 26, 2026 — live Alpaca data ~09:37 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,148.94 | $11,489.40 | +$554.06 (+5.07%) | 11.59% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,182.73, stop $1,064.457 ✓ — buffer $84.48 (7.36%) |
| V | 22 | $323.57 | $335.71 | $7,385.62 | +$267.08 (+3.75%) | 7.45% | 66033918 (22sh, HWM $339.94, stop $305.946) ✓ — buffer $29.76 (8.86%) |
| VST | 40 | $148.81 | $166.8615 | $6,674.46 | +$722.06 (+12.13%) | 6.73% | c8b43d32 (40sh, 5% trail, HWM $168.77, stop $160.3315) ✓ — buffer $6.53 (3.91%) ⚠️ monitoring |

**Sector exposure (market-open June 26):**
- Healthcare (LLY): $11,489.40 = 11.59% | Financials (V): $7,385.62 = 7.45% | Energy/Utilities (VST): $6,674.46 = 6.73% | Cash: $73,615.74 = 74.24%
- No sector above 60% cap ✓

**Trailing stop status (market-open June 26 — confirmed via Alpaca live orders ~09:37 ET):**
- LLY (d4147484): 7sh — HWM $1,182.73, stop $1,064.457 ✓ (buffer $84.48 = 7.36%; today's high $1,151.27 < HWM — no ratchet)
- LLY (25989fb5): 3sh — HWM $1,182.73, stop $1,064.457 ✓
- V (66033918): 22sh — HWM $339.94, stop $305.946 ✓ (buffer $29.76 = 8.86%; today's high $336.59 < HWM — no ratchet)
- VST (c8b43d32): 40sh — 5% trail, HWM $168.77, stop $160.3315 ✓ (buffer $6.53 = 3.91% ⚠️ — improved from pre-mkt 2.90%; today's high $167.05 < HWM — no ratchet)
**Stop audit: 4/4 PASS ✓**

**Market-open June 26 notes (~09:37 ET — stop audit 4/4 PASS; no trades; all positions positive; Bull leads SPY):**
- **Shock check:** +$281.04 (+0.284%) vs last_equity $98,874.88 — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $99,155.92 vs HWM $101,384.21 = **−2.198%** — NOT triggered ✓ (7.802pp headroom)
- **LLY** $1,148.94 (+5.07% from entry, +1.88% today): Strong session; Leerink PT $1,232 Outperform; Medicare Bridge July 1 TOMORROW. ⚠️ **Pre-market June 30 MANDATORY hold/trim/exit decision.** Buffer 7.36% healthy. Earnings Aug 5-6 ✓. Conviction **A**. HOLD.
- **V** $335.71 (+3.75% from entry, +1.57% today): Visa Destinations global rollout gaining traction. Showing relative strength (broad market weak on SPY −0.63%). HWM $339.94 — stop buffer 8.86% comfortable. HOLD. Conviction **B** (0/3 C-weeks). review_by 2026-07-28.
- **VST** $166.8615 (+12.13% from entry, −0.54% today) ⭐⭐: Minor pullback; Helix + Cogentrix intact; MS PT $212 / Seaport PT $230. Stop buffer 3.91% — monitoring but improved from pre-market. STRONG HOLD unless stop fires. Conviction **A**. review_by 2026-07-07.
- **SPY** $728.68 (−0.63% today): Risk-off broad market from Asian semiconductor contagion. Our healthcare/financials/energy positions holding up well — all three positive.
- **Bull LEADS SPY:** $99,155.92 (−0.844%) vs SPY TR $730.44 / $739.44 = −1.217%. **Bull LEADS by +0.373pp** — first lead vs benchmark since inception. LLY +5.07% and V +3.75% driving outperformance in risk-off tape.
- **No trades:** Plan was empty; no trades placed or needed. Cash drag continues but correct posture.
- **LRCX/PWR:** LRCX ATR gate reset (8.88% June 25). Need fresh 3 consecutive ≤3% sessions from June 29. PWR still deferred.

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Market-open (2026-06-26)** | **$99,155.92 (−0.844%)** | **$728.68 + $1.76 div = −1.217% TR** | **Bull LEADS SPY +0.373pp ✓** |
| **Pre-mkt (2026-06-26)** | **$98,723.49 (−1.277%)** | **$733.33 close + $1.76 div = −0.588% TR** | **Bull TRAILED SPY ~0.689pp** |
| **Close (2026-06-25)** | **$98,925.93 (−1.074%)** | **$733.33 + $1.76 div = −0.588% TR** | **Bull TRAILED SPY ~0.486pp** |

---

## Account (close June 25, 2026 — live Alpaca data ~15:51 ET)

| Metric | Value |
|--------|-------|
| Equity | $98,925.93 |
| Cash | $73,615.76 (74.42%) |
| Long market value | $25,310.17 |
| Buying power | ~$73,615.76 |
| Last equity (June 24 close) | $98,825.19 |

## Open positions (close June 25, 2026 — live Alpaca data ~15:51 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,130.32 | $11,303.20 | +$367.86 (+3.36%) | 11.43% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,182.73, stop $1,064.457 ✓ — buffer $65.86 (5.83%) |
| V | 22 | $323.57 | $331.60 | $7,295.20 | +$176.66 (+2.48%) | 7.37% | 66033918 (22sh, HWM $339.94, stop $305.946) ✓ — buffer $25.65 (7.74%) |
| VST | 40 | $148.81 | $167.825 | $6,713.00 | +$760.60 (+12.78%) | 6.79% | c8b43d32 (40sh, 5% trail, HWM $168.77 ⬆️, stop $160.332) ✓ — buffer $7.49 (4.47%) ⭐⭐ TIGHTENED 5% trail |

**NVDA CLOSED:** Trailing stop dcba7429 filled 09:59 AM ET June 25 @ $192.546 — P/L −$688.86 (−9.78%). 3 days. See closed-trades.md.

**Sector exposure (close June 25):**
- Healthcare (LLY): $11,303.20 = 11.43% | Financials (V): $7,295.20 = 7.37% | Energy/Utilities (VST): $6,713.00 = 6.79% | Cash: $73,615.76 = 74.42%
- No sector above 60% cap ✓

**Trailing stop status (close June 25 — confirmed via Alpaca live orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM $1,182.73, stop $1,064.457 ✓ (buffer $65.86 = 5.83%)
- LLY (25989fb5): 3sh — HWM $1,182.73, stop $1,064.457 ✓
- V (66033918): 22sh — HWM $339.94, stop $305.946 ✓ (buffer $25.65 = 7.74%)
- VST (c8b43d32): 40sh — 5% trail, HWM $168.77 ⬆️ (new high today), stop $160.332 ✓ (buffer $7.49 = 4.47%)
**Stop audit: 4/4 PASS ✓**

**Close June 25 notes (~15:51 ET — stop audit 4/4 PASS; 0 trades; 🚨 NVDA stop captured by midday):**
- **Today P/L:** +$100.74 (+0.102%) | SPY −0.091% (USD 731.57) | Bull outperformed SPY by +0.193pp today
- **Shock check:** +$100.74 (+0.102%) vs last_equity $98,825.19 — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $98,925.93 vs HWM $101,384.21 = **−2.425%** — NOT triggered ✓ (7.575pp headroom; CB trigger USD 91,245.79)
- **🚨 NVDA stop-out (captured midday):** Trailing stop fired 09:59 AM ET. −$688.86 (−9.78%). Post-mortem and lesson in closed-trades.md + lessons.md ✓.
- **⭐⭐ VST:** +3.04% today, +12.78% from entry. HWM auto-ratcheted to $168.77 (new position high today). 5% trailing stop c8b43d32 stop $160.332. Buffer 4.47%. Thesis intact (Helix Digital Infrastructure + Cogentrix). STRONG HOLD. review_by 2026-07-07.
- **LLY** $1,130.32: +3.36% from entry, +1.17% today. Medicare Bridge July 1 in **4 trading days** (closes June 26, 29, 30 → July 1). ⚠️ **PRE-MARKET JUNE 30 MANDATORY hold/trim/exit decision.** Buffer 5.83%. HOLD.
- **V** $331.60: +2.48% from entry, −0.19% today. Thesis intact. HOLD. review_by 2026-07-28.
- **Market context (June 25):** Micron +17% post-earnings beat (USD 50B Q3 revenue vs USD 43.2B estimate) lifted semi sentiment; Qualcomm +9% on non-handset revenue expansion. But Apple −6.5% (iPhone/Mac price hikes from memory cost pressures) dragged tech. PCE inflation 4.1% YoY (highest since April 2023) was hawkish macro surprise. Net: healthcare (LLY +1.17%) and energy/utilities (VST +3.04%) outperformed, supporting Bull's positions.
- **LRCX ATR:** Session 3/3 attempt June 25 — pre-market June 26 must confirm if gate passes; if yes, entry eligible as early as Monday June 29.
- **Exit reconciliation:** NVDA stop-out fully reconciled in closed-trades.md (midday June 25 ✓). No other exits. All 3 remaining positions held.
- **Trades today:** 0.

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-06-25)** | **$98,925.93 (−1.074%)** | **$731.57 + $1.76 div = −0.826% TR** | **Bull TRAILS SPY ~0.248pp** (improved from −0.348pp at midday; VST +3.04% + LLY +1.17% recovery) |
| **Midday (2026-06-25)** | **$99,029.80 (−0.970%)** | **~$733.08 + $1.76 div = −0.622% TR** | **Bull TRAILS SPY ~0.348pp** |

---

## Account (midday June 25, 2026 — live Alpaca data ~12:31 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,029.80 |
| Cash | $73,615.76 (74.34%) |
| Long market value | $25,414.04 |
| Buying power | ~$73,615.76 |
| Last equity (June 24 close) | $98,825.19 |

## Open positions (midday June 25, 2026 — live Alpaca data ~12:31 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,130.82 | $11,308.20 | +$372.86 (+3.41%) | 11.42% | d4147484 (7sh) + 25989fb5 (3sh), HWM $1,182.73, stop $1,064.457 ✓ — buffer $66.36 (5.87%) |
| V | 22 | $323.57 | $335.90 | $7,389.80 | +$271.26 (+3.81%) | 7.46% | 66033918 (22sh, HWM $339.94 ⬆️, stop $305.946) ✓ — buffer $29.95 (8.92%) |
| VST | 40 | $148.81 | $167.915 | $6,716.60 | +$764.20 (+12.84%) | 6.78% | c8b43d32 (40sh, HWM $168.25, stop $159.84) ✓ — buffer $8.08 (4.80%) ⭐⭐ TIGHTENED to 5% trail |

**NVDA CLOSED:** Trailing stop dcba7429 filled 09:59 AM ET June 25 @ $192.546 — P/L −$688.86 (−9.78%). 3 days. See closed-trades.md.

**Sector exposure (midday June 25):**
- Healthcare (LLY): $11,308.20 = 11.42% | Financials (V): $7,389.80 = 7.46% | Energy/Utilities (VST): $6,716.60 = 6.78% | Cash: $73,615.76 = 74.34%
- No sector above 60% cap ✓

**Trailing stop status (midday June 25 — confirmed via Alpaca live orders ~12:31 ET):**
- LLY (d4147484): 7sh — HWM $1,182.73, stop $1,064.457 ✓ (buffer $66.36 = 5.87%)
- LLY (25989fb5): 3sh — HWM $1,182.73, stop $1,064.457 ✓
- V (66033918): 22sh — HWM $339.94 ⬆️, stop $305.946 ✓ (buffer $29.95 = 8.92%) — ratcheted from $336.82
- VST (c8b43d32): 40sh — HWM $168.25, stop $159.84 ✓ (buffer $8.08 = 4.80%) ⭐⭐ NEW 5% trailing stop
**Stop audit: 4/4 PASS ✓**

**Midday June 25 notes (~12:31 ET — 🚨 NVDA stop fill; VST tightened; stop audit 4/4 PASS):**
- **🚨 NVDA TRAILING STOP FIRED:** 09:59 AM ET. Filled 33sh @ $192.546. P/L −$688.86 (−9.78%). Held 3 days. Drivers: GPU B200 spot $6.11→$4.22 (−31%/3wks), $410.6M insider selling, AI trade cooling. Thesis invalidation ($200 close) triggered June 24. Stop executed correctly.
- **⭐⭐ VST TIGHTENED:** HWM hit $171.35 (+15.12% from entry), crossing trigger $171.13. Cancelled 10% stop c4c200a5 ($154.215), placed 5% trailing stop c8b43d32 (stop $159.84). Floor improved +$5.63/sh.
- **LLY** $1,130.82: +3.41% from entry. Buffer $66.36 (5.87%). Medicare Bridge July 1 in 4 days — HOLD. Pre-market June 30 decision REQUIRED. review_by 2026-07-01.
- **V** $335.90: +3.81% from entry. HWM ratcheted to $339.94. Thesis intact. HOLD. review_by 2026-07-28.
- **Drawdown circuit breaker:** −2.32% vs HWM — NOT triggered ✓
- **LRCX ATR:** Tracking session 3/3 attempt today (June 25). Pre-market June 26 or Monday June 29 should confirm if gate passes. PWR still deferred.

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Midday (2026-06-25)** | **$99,029.80 (−0.970%)** | **~$733.08 + $1.76 div = −0.622% TR** | **Bull TRAILS SPY ~0.348pp** |
| **Market-open (2026-06-25)** | **$99,127.33 (−0.873%)** | **~$737.34 + $1.76 div = −0.046% TR** | **Bull TRAILS SPY ~0.827pp** |

---

## Account (market-open June 25, 2026 — live Alpaca data ~09:36 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,127.33 |
| Cash | $67,261.73 (67.85%) |
| Long market value | $31,865.60 |
| Buying power | ~$67,261.73 |
| Last equity (June 24 close) | $98,825.19 |

## Open positions (market-open June 25, 2026 — live Alpaca data ~09:36 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,117.50 | $11,175.00 | +$239.66 (+2.19%) | 11.27% | d4147484 (7sh) + 25989fb5 (3sh), HWM **$1,182.73**, stop **$1,064.457** ✓ — buffer $53.04 (4.75%) |
| NVDA | 33 | $213.421 | $198.93 | $6,564.69 | −$478.16 (−6.79%) | 6.62% | dcba7429 (33sh, HWM **$213.99**, stop **$192.591**) ✓ — buffer $6.34 (3.19%) ⚠️ CRITICAL: $0.45 above -7% threshold $198.48; midday MUST cut if ≤$198.48 |
| V | 22 | $323.57 | $333.555 | $7,338.21 | +$219.67 (+3.09%) | 7.40% | 66033918 (22sh, HWM **$336.8199**, stop **$303.138**) ✓ — buffer $30.42 (9.12%) |
| VST | 40 | $148.81 | $169.92 | $6,796.80 | +$844.40 (+14.19%) | 6.86% | c4c200a5 (40sh, HWM **$170.50**, stop **$153.45**) ✓ — buffer $16.47 (9.69%) ⭐⭐ HELIX+COGENTRIX; tighten trigger $171.13 |

**Sector exposure (market-open June 25):**
- Healthcare (LLY): $11,175.00 = 11.27% | Tech/AI Semi (NVDA): $6,564.69 = 6.62% | Financials (V): $7,338.21 = 7.40% | Energy/Utilities (VST): $6,796.80 = 6.86% | Cash: $67,261.73 = 67.85%
- No sector above 60% cap ✓

**Trailing stop status (market-open June 25 — confirmed via Alpaca live orders ~09:36 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $53.04 = 4.75%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- NVDA (dcba7429): 33sh — HWM **$213.99**, stop **$192.591** ✓ (buffer $6.34 = 3.19%) ⚠️ NARROW — only USD0.45 above forced-cut threshold
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $30.42 = 9.12%)
- VST (c4c200a5): 40sh — HWM **$170.50**, stop **$153.45** ✓ (buffer $16.47 = 9.69%) ⭐⭐
**Stop audit: 5/5 PASS ✓**

**Market-open June 25 notes (~09:36 ET — NVDA ⚠️ critical; VST ⭐⭐ strong; 0 trades):**
- **⚠️ NVDA CRITICAL:** Current USD198.93, only USD0.45 above forced-cut threshold USD198.48 (−7% from entry $213.421). Pre-market HOLD decision stands (Micron blowout confirms AI thesis). **Midday MUST cut if ≤USD198.48 at 12:30 ET — no exceptions.**
- **⭐⭐ VST STRONG:** +14.19% from entry, +4.33% today. HWM USD170.50; +15% tighten trigger at USD171.13 (USD1.21 away). Midday should tighten stop to 5% trail if USD171.13 hit.
- **LLY** USD1,117.50 (+2.19% from entry). Medicare Bridge July 1 in 4 trading days — HOLD. Pre-market June 30 mandatory decision required.
- **V** USD333.555 (+3.09% from entry). Stablecoin platform talks (Visa/Mastercard/Stripe) — thesis intact. HOLD.
- **LRCX:** ATR gate still failing (4.15% June 24; 3.08% June 23). Earliest entry June 30+.
- **Drawdown circuit breaker:** $99,127.33 vs HWM $101,384.21 = −2.226% — NOT triggered ✓
- **Today's trades:** 0. Cash 67.85% — above target band (25-40%), explicitly justified.

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Market-open (2026-06-25)** | **$99,127.33 (−0.873%)** | **~$737.34 + $1.76 div = −0.046% TR** | **Bull TRAILS SPY ~0.827pp** |
| **Pre-mkt (2026-06-25)** | **$98,902.39 (−1.098%)** | **futures +0.1%; est −0.636% TR** | **Bull TRAILS SPY ~0.46pp est** |
| **Close (2026-06-24)** | **$98,724.14 (−1.276%)** | **$732.24 + $1.76 div = −0.736% TR** | **Bull TRAILS SPY ~0.54pp** |

---

## Account (close June 24, 2026 — live Alpaca data ~15:51 ET)

| Metric | Value |
|--------|-------|
| Equity | $98,724.14 |
| Cash | $67,261.73 (68.15%) |
| Long market value | $31,462.41 |
| Buying power | ~$67,261.73 |
| Last equity (June 23 close) | $98,656.01 |

## Open positions (close June 24, 2026 — live Alpaca data ~15:51 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,114.33 | $11,143.30 | +$207.96 (+1.90%) | 11.28% | d4147484 (7sh, HWM **$1,182.73**, stop **$1,064.457**) ✓; 25989fb5 (3sh, same) ✓ — buffer $49.87 (4.48%) |
| NVDA | 33 | $213.421 | $197.75 | $6,525.75 | −$517.14 (**−7.34%**) | 6.61% | dcba7429 (33sh, HWM **$213.99**, stop **$192.591**) ✓ — buffer $5.16 (2.61%) ⚠️ BELOW USD200 INVALIDATION + USD198.48 THRESHOLD |
| V | 22 | $323.57 | $331.84 | $7,300.48 | +$181.94 (+2.56%) | 7.40% | 66033918 (22sh, HWM **$336.8199**, stop **$303.138**) ✓ — buffer $28.70 (8.65%) |
| VST | 40 | $148.81 | $162.42 | $6,496.80 | +$544.40 (+9.15%) | 6.58% | c4c200a5 (40sh, HWM **$170.50**, stop **$153.45**) ✓ — buffer $8.97 (5.52%) ⭐⭐ HELIX+COGENTRIX |

**Sector exposure (close June 24):**
- Healthcare (LLY): $11,143.30 = 11.28% | Tech/AI Semi (NVDA): $6,525.75 = 6.61% | Financials (V): $7,300.48 = 7.40% | Energy/Utilities (VST): $6,496.80 = 6.58% | Cash: $67,261.73 = 68.15%
- No sector above 60% cap ✓

**Trailing stop status (close June 24 — confirmed via Alpaca live orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $49.87 = 4.48%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- NVDA (dcba7429): 33sh — HWM **$213.99**, stop **$192.591** ✓ (buffer $5.16 = 2.61%) ⚠️ THESIS BREAK — closed below USD200 invalidation
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $28.70 = 8.65%)
- VST (c4c200a5): 40sh — HWM **$170.50**, stop **$153.45** ✓ (buffer $8.97 = 5.52%)
**Stop audit: 5/5 PASS ✓**

**Close June 24 notes (~15:51 ET — ⚠️ NVDA thesis break; 0 trades; stop audit 5/5 PASS):**
- **Today P/L:** +$68.13 (+0.069%) | SPY ~−0.336% (Alpaca) | Bull outperformed by +0.405pp (cash cushion absorbing continued semi weakness)
- **Shock check:** +$68.13 (+0.069%) vs last_equity $98,656.01 — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $98,724.14 vs HWM $101,384.21 = **−2.625%** — NOT triggered ✓ (7.375pp headroom)
- **⚠️ NVDA THESIS BREAK — CRITICAL:** Closed USD 197.75 = **−7.343% from entry** ($213.421). BOTH conditions triggered:
  1. **USD 200 invalidation** (stated at entry: "closes below $200 on volume") → **TRIGGERED**
  2. **USD 198.48 forced-cut threshold** (−7% from entry) → was $200.41 at midday (above threshold); fell further after midday to $197.75; close routine cannot trade
  - Trailing stop $192.591 has NOT fired (buffer $5.16 = 2.61%)
  - Annual Meeting Jensen Huang keynote did NOT reverse selling; chip sector under 3-day pressure (KOSPI contagion + hyperscaler AI ROI concerns)
  - **PRE-MARKET JUNE 25 MANDATORY:** explicit hold/exit/trim decision required BEFORE open. If NVDA is below $198.48 at midday June 25, the −7% rule MUST cut the position.
  - Micron earnings tonight (after bell) — key AI memory read-through for NVDA thesis; could move materially.
- **LLY** $1,114.33: +1.90% from entry; +0.655% today. Defensive healthcare outperforming. Medicare Bridge July 1 in 5 trading days — HOLD. review_by 2026-07-01.
- **V** $331.84: +2.56% from entry; +1.023% today. Strong; thesis intact. HOLD. review_by 2026-07-28.
- **VST** $162.42: +9.15% from entry; +0.018% today. Flat in risk-off; Helix+Cogentrix thesis intact. Buffer 5.52%. HOLD. review_by 2026-07-07.
- **Market context (June 24):** S&P 500 attempted recovery (+0.35%, Nasdaq +0.62%) after Tuesday's −1.44% selloff. GOOGL +0.5% on Dow Jones index inclusion (effective June 29). AI/chip names stayed under pressure — NVDA −1.14% intraday. Micron earnings after close are a key DRAM/HBM demand read-through for AI semi thesis.
- **Exit reconciliation:** No exits today. All 4 positions held. closed-trades.md current ✓.
- **LRCX ATR tracking:** June 24 = potential session 2/3. Pre-mkt June 25 must calculate LRCX ATR to confirm progress toward Monday June 29 entry gate.
- **Trades today:** 0.

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-06-24)** | **$98,724.14 (−1.276%)** | **$732.24 + $1.76 div = −0.736% TR** | **Bull TRAILS SPY ~0.54pp** (improved from −0.89pp at June 23 close) |
| **Midday (2026-06-24)** | **$98,841.34 (−1.159%)** | **~−0.401% TR est** | **Bull TRAILS SPY ~0.76pp est** |

---

## Account (midday June 24, 2026 — live Alpaca data ~12:32 ET)

| Metric | Value |
|--------|-------|
| Equity | $98,841.34 |
| Cash | $67,261.73 (68.05%) |
| Long market value | $31,579.61 |
| Buying power | ~$67,261.73 |
| Last equity (June 23 close) | $98,656.01 |

## Open positions (midday June 24, 2026 — live Alpaca data ~12:32 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,109.12 | $11,091.20 | +$155.86 (+1.43%) | 11.22% | d4147484 (7sh, HWM **$1,182.73**, stop **$1,064.457**) ✓; 25989fb5 (3sh, same) ✓ — buffer $44.66 (4.03%) |
| NVDA | 33 | $213.421 | $200.41 | $6,613.53 | −$429.36 (−6.10%) | 6.69% | dcba7429 (33sh, HWM **$213.99**, stop **$192.591**) ✓ — buffer $7.82 (3.90%) ⚠️ approaching USD198.48 forced-cut threshold |
| V | 22 | $323.57 | $331.59 | $7,294.98 | +$176.44 (+2.48%) | 7.38% | 66033918 (22sh, HWM **$336.8199**, stop **$303.138**) ✓ — buffer $28.45 (8.59%) |
| VST | 40 | $148.81 | $164.35 | $6,574.00 | +$621.60 (+10.44%) | 6.65% | c4c200a5 (40sh, HWM **$170.50**, stop **$153.45**) ✓ — buffer $10.90 (6.63%) ⭐⭐ HELIX+COGENTRIX |

**Sector exposure (midday June 24):**
- Healthcare (LLY): $11,091.20 = 11.22% | Tech/AI Semi (NVDA): $6,613.53 = 6.69% | Financials (V): $7,294.98 = 7.38% | Energy/Utilities (VST): $6,574.00 = 6.65% | Cash: $67,261.73 = 68.05%
- No sector above 60% cap ✓

**Trailing stop status (midday June 24 — confirmed via Alpaca live orders ~12:32 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $44.66 = 4.03%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- NVDA (dcba7429): 33sh — HWM **$213.99**, stop **$192.591** ✓ (buffer $7.82 = 3.90%) ⚠️ monitoring
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138**  ✓ (buffer $28.45 = 8.59%)
- VST (c4c200a5): 40sh — HWM **$170.50**, stop **$153.45** ✓ (buffer $10.90 = 6.63%)
**Stop audit: 5/5 PASS ✓**

**Midday June 24 notes (~12:32 ET — no cuts, no tightenings; stop audit 5/5 PASS):**
- **Shock check:** $98,841.34 vs last_equity $98,656.01 = +$185.33 (+0.188%) — no shock ✓ (threshold −4%)
- **Drawdown circuit breaker:** $98,841.34 vs HWM $101,384.21 = **−2.50%** — NOT triggered ✓
- **LLY** $1,109.12: +1.43% from entry; Berenberg PT $1,135; retatrutide Phase 3 positive; thesis intact. Medicare Bridge July 1 in 6 days — HOLD. Conviction **A**. review_by 2026-07-01.
- **NVDA** $200.41: −6.10% from entry ⚠️. Annual Meeting Jensen Huang keynote in progress (noon ET). No fundamental thesis break (KOSPI chip selloff contagion only; no NVDA-specific negative). −7% forced-cut threshold $198.48 = $1.93 away from current. HOLD — rule NOT triggered. USD 200 invalidation (close below $200 on volume) monitoring. Conviction **B**. review_by 2026-07-22.
- **V** $331.59: +2.48% from entry; +0.95% today; OpenAI/stablecoin thesis intact. HOLD. Conviction **B**. review_by 2026-07-28.
- **VST** $164.35: +10.44% from entry; +1.21% today ⭐⭐. News scan (>10% threshold): Wells Fargo Buy, Seaport PT $230, 18 analysts Strong Buy / 0 Sell. Thesis-driven appreciation; HELIX+COGENTRIX intact. +15% tighten trigger at $171.13 NOT reached. STRONG HOLD. Conviction **A**. review_by 2026-07-07.
- **No cuts, no tightenings, no new positions** — all positions within guardrails.

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Midday (2026-06-24)** | **$98,841.34 (−1.159%)** | **~$734.71 (June 23 close) + $1.76 div = ~−0.401% TR est** | **Bull TRAILS SPY ~0.76pp est** |
| **Market-open (2026-06-24)** | **$98,860.37 (−1.140%)** | **~$734.71 + $1.76 div = ~−0.401% TR** | **Bull TRAILS SPY ~0.74pp est** |

---

## Account (market-open June 24, 2026 — live Alpaca data ~09:36 ET)

| Metric | Value |
|--------|-------|
| Equity | $98,860.37 |
| Cash | $67,261.73 (68.04%) |
| Long market value | $31,611.68 |
| Buying power | ~$67,261.73 |
| Last equity (June 23 close) | $98,656.01 |

## Open positions (market-open June 24, 2026 — live Alpaca data ~09:36 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,129.27 | $11,292.70 | +$357.36 (+3.27%) | 11.42% | d4147484 (7sh, HWM **$1,182.73**, stop **$1,064.457**) ✓; 25989fb5 (3sh, same) ✓ — buffer $64.81 (5.74%) |
| NVDA | 33 | $213.421 | $200.72 | $6,623.76 | −$419.13 (−5.95%) | 6.70% | dcba7429 (33sh, HWM **$213.99**, stop **$192.591**) ✓ — buffer $8.13 (4.04%) ⚠️ USD 200 invalidation $0.72 ABOVE GATE |
| V | 22 | $323.57 | $328.61 | $7,229.42 | +$110.88 (+1.56%) | 7.31% | 66033918 (22sh, HWM **$336.8199**, stop **$303.138**) ✓ — buffer $25.47 (7.75%) |
| VST | 40 | $148.81 | $161.645 | $6,465.80 | +$513.40 (+8.62%) | 6.54% | c4c200a5 (40sh, HWM **$170.50**, stop **$153.45**) ✓ — buffer $8.20 (5.07%) ⭐⭐ HELIX+COGENTRIX |

**Sector exposure (market-open June 24):**
- Healthcare (LLY): $11,292.70 = 11.42% | Tech/AI Semi (NVDA): $6,623.76 = 6.70% | Financials (V): $7,229.42 = 7.31% | Energy/Utilities (VST): $6,465.80 = 6.54% | Cash: $67,261.73 = 68.04%
- No sector above 60% cap ✓

**Trailing stop status (market-open June 24 — confirmed via Alpaca live orders):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $64.81 = 5.74%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- NVDA (dcba7429): 33sh — HWM **$213.99**, stop **$192.591** ✓ (buffer $8.13 = 4.04%) ⚠️ monitoring
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $25.47 = 7.75%)
- VST (c4c200a5): 40sh — HWM **$170.50**, stop **$153.45** ✓ (buffer $8.20 = 5.07%)
**Stop audit: 5/5 PASS ✓**

**Market-open June 24 notes:**
- **Market context:** S&P 500 futures +0.13% at open (bargain-hunting after KOSPI 2-day chip selloff). Micron +4.5% pre-mkt (earnings beat) = positive AI semi readthrough. NVDA Annual Meeting 9AM PT (noon ET) — Jensen Huang keynote, Blackwell/Vera production update; bullish catalyst.
- **LLY** USD1,129.27: +2.00% today, +3.27% from entry. Berenberg raised PT to $1,135; retatrutide Phase 3 data positive. Medicare Bridge July 1 in 7 days — explicit hold/trim/exit decision REQUIRED at pre-market June 30. HOLD.
- **NVDA** USD200.72: +0.34% today, still −5.95% from entry. ⚠️ USD200 invalidation $0.72 above gate. No fundamental thesis break; KOSPI HBM4 contagion only; Annual Meeting is bullish thesis-affirming event. Midday MUST apply −7% rule if NVDA at/below USD198.48. HOLD.
- **V** USD328.61: +0.04% today, +1.56% from entry. Thesis intact; July 28 earnings gate. HOLD.
- **VST** USD161.645: −0.46% today, +8.62% from entry. Pure risk-off residual pullback; Helix + Cogentrix thesis most compelling. HOLD.
- **Shock check:** +$204.36 (+0.207%) — no shock ✓
- **Drawdown circuit breaker:** $98,860.37 vs HWM $101,384.21 = **−2.49%** — NOT triggered ✓
- **No trades:** plan empty (LRCX ATR gate failing session 1/3; NVDA Annual Meeting event risk; PWR deferred; no other qualified candidates)

## Monday conviction ratings (June 24, 2026)

| Symbol | Rating | 3-consecutive-C trigger | Notes |
|--------|--------|------------------------|-------|
| LLY | **A** | N/A | +3.27% from entry; Medicare Bridge July 1 in 7 days; Berenberg PT $1,135; thesis intact |
| NVDA | **B** | 0/3 weeks at C | +0.34% today; USD 200 invalidation $0.72 above gate; Annual Meeting noon ET bullish; starter position |
| V | **B** | 0/3 weeks at C | +1.56% from entry; thesis intact; July 28 earnings gate |
| VST | **A** | N/A | +8.62% from entry; Helix + Cogentrix closed; thesis most compelling |

**Upcoming catalysts:**
- **NVDA Annual Meeting June 24 9AM PT** (today — Jensen Huang keynote; Blackwell/Vera production ramp; bullish catalyst)
- **LLY Medicare GLP-1 Bridge effective July 1** (7 days — explicit hold/trim/exit decision REQUIRED at pre-market June 30)
- **NVDA $200 invalidation monitoring** (active — closes below $200 on volume = thesis break; midday −7% threshold $198.48)
- **VST thesis review_by July 7** (13 days)
- **NVDA review_by July 22** (28 days)
- **V Q3 FY26 earnings July 28** (34 days — thesis review_by date)
- **NVDA earnings August 26** (63 days — outside 2-day window ✓)
- **LRCX ATR gate tracking:** session 1/3 (June 23 ATR 3.08%); need sessions June 24 + 25 also ≤3% for entry June 29+

**Week of June 23 — new position slots:**
- **Slot 1:** LRCX — ATR gate tracking (session 1/3); earliest entry June 29 (Monday)
- **Slot 2:** PWR — ATR elevated + insider selling; re-evaluate June 29+
- **Slot 3:** MRVL — research candidate from AGGRO lessons; research when calmer

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Market-open (2026-06-24)** | **$98,860.37 (−1.140%)** | **~$734.71 + $1.76 div = ~−0.401% TR (recovering from June 23 close)** | **Bull TRAILS SPY ~0.74pp est** (recovering as LLY +2.0% and NVDA +0.34% recover from KOSPI selloff) |
| **Close (2026-06-23)** | **$98,711.58 (−1.289%)** | **$734.71 + $1.76 div = −0.401% TR** | **Bull TRAILS SPY ~0.89pp** |

## Account (pre-market June 24, 2026 — live Alpaca data ~08:02 ET)

| Metric | Value |
|--------|-------|
| Equity | $98,773.54 |
| Cash | $67,261.73 (68.12%) |
| Long market value | $31,511.81 |
| Buying power | ~$67,261.73 |
| Last equity (June 23 close) | $98,711.58 |

## Open positions (pre-market June 24, 2026 — live Alpaca data ~08:02 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,111.00 | $11,110.00 | +$175.47 (+1.60%) | 11.25% | d4147484 (7sh, HWM **$1,182.73**, stop **$1,064.457**) ✓; 25989fb5 (3sh, same) ✓ — buffer $46.54 (4.19%) |
| NVDA | 33 | $213.421 | $201.50 | $6,649.50 | −$393.40 (−5.59%) | 6.73% | dcba7429 (33sh, HWM **$213.99**, stop **$192.591**) ✓ — buffer $8.91 (4.42%) ⚠️ USD 200 invalidation $1.50 ABOVE GATE |
| V | 22 | $323.57 | $329.00 | $7,238.00 | +$120.06 (+1.68%) | 7.33% | 66033918 (22sh, HWM **$336.8199**, stop **$303.138**) ✓ — buffer $25.86 (7.86%) |
| VST | 40 | $148.81 | $162.80 | $6,512.00 | +$559.60 (+9.40%) | 6.59% | c4c200a5 (40sh, HWM **$170.50**, stop **$153.45**) ✓ — buffer $9.35 (5.75%) ⭐⭐ HELIX+COGENTRIX |

**Sector exposure (pre-market June 24):**
- Healthcare (LLY): $11,110.00 = 11.24% | Tech/AI Semi (NVDA): $6,649.50 = 6.73% | Financials (V): $7,238.00 = 7.33% | Energy/Utilities (VST): $6,512.00 = 6.59% | Cash: $67,261.73 = 68.12%
- No sector above 60% cap ✓

**Trailing stop status (pre-market June 24 — confirmed via Alpaca live orders):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $46.54 = 4.19%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- NVDA (dcba7429): 33sh — HWM **$213.99**, stop **$192.591** ✓ (buffer $8.82 = 4.38%) ⚠️ USD 200 invalidation WATCH
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $25.18 = 7.67%)
- VST (c4c200a5): 40sh — HWM **$170.50**, stop **$153.45** ✓ (buffer $9.35 = 5.75%)
**Stop audit: 5/5 PASS ✓**

**Pre-market June 24 notes:**
- **Market context:** S&P 500 futures +0.13% stabilizing after KOSPI 2-day selloff. 10yr Treasury 4.49% — BELOW 4.75% gate ✓. WTI ~$80/bbl ✓. Iran peace deal holding. NVDA Annual Meeting 9AM PT (noon ET) — bullish catalyst; Jensen Huang keynote.
- **NVDA** USD 201.50 pre-market: +$1.46 (+0.73%) from June 23 close USD 200.04. ⚠️ USD 200 invalidation is $1.50 above gate. Thesis intact (no NVDA-specific fundamental event; KOSPI HBM4 contagion only). Annual Meeting today is bullish catalyst. HOLD; midday -7% threshold = USD 198.48.
- **LLY** USD 1,111.00: +1.60% from entry. Medicare Bridge July 1 in 7 days; explicit hold/trim/exit decision REQUIRED at pre-market June 30. Cathie Wood/ARK accumulated. HOLD.
- **V** USD 329.00: +1.68% from entry. Thesis intact; July 28 earnings gate. HOLD.
- **VST** USD 162.80: +9.40% from entry ⭐⭐. Helix + Cogentrix thesis strongest. HOLD.
- **Shock check:** +$117.53 (+0.119%) from last_equity — below 4% threshold ✓
- **Drawdown circuit breaker:** $98,773.54 vs HWM $101,384.21 = **−2.576%** — NOT triggered ✓
- **No trades planned:** LRCX ATR 3.08% (gate failing; need 3 consecutive ≤3%); NVDA Annual Meeting intraday risk; PWR deferred; cash drag explicitly accepted pending ATR resolution.

## Monday conviction ratings (June 23, 2026)

| Symbol | Rating | 3-consecutive-C trigger | Notes |
|--------|--------|------------------------|-------|
| LLY | **A** | N/A | +1.60% from entry; Medicare Bridge July 1 in 7 days; Cathie Wood buying; thesis intact |
| NVDA | **B** | 0/3 weeks at C | +0.683% pre-mkt recovery; USD 200 invalidation $1.41 above gate; Annual Meeting today; starter position |
| V | **B** | 0/3 weeks at C | +1.68% from entry; thesis intact; July 28 earnings gate |
| VST | **A** | N/A | +9.24% from entry; Helix + Cogentrix closed; thesis most compelling |

**Upcoming catalysts:**
- **LLY Medicare GLP-1 Bridge effective July 1** (7 days — explicit hold/trim/exit decision REQUIRED at pre-market June 30)
- **NVDA Annual Meeting June 24 9AM PT** (today — Jensen Huang keynote; bullish catalyst)
- **VST thesis review_by July 7** (13 days)
- **NVDA $200 invalidation monitoring** (active — closes below $200 on volume = thesis break)
- **NVDA −7% midday threshold $198.48** (midday routine MUST apply rule if triggered)
- **NVDA review_by July 22** (28 days)
- **V Q3 FY26 earnings July 28** (34 days — thesis review_by date)
- **NVDA earnings August 26** (63 days — outside 2-day window ✓)

**Week of June 23 — new position slots:**
- **Slot 1:** LRCX — ATR reset by chip selloff; need 3 consecutive ≤3% sessions; earliest June 30+
- **Slot 2:** PWR — ATR elevated + insider selling; re-evaluate June 30+
- **Slot 3:** MRVL — research candidate from AGGRO lessons; research when calmer

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-06-23)** | **$98,711.58 (−1.289%)** | **$734.71 + $1.76 div = −0.401% TR** | **Bull TRAILS SPY ~0.89pp** (improved from −1.87pp; cash cushion absorbed KOSPI chip selloff) |
| **Market-open (2026-06-23)** | **$98,662.85 (−1.337%)** | **$733.035 + $1.76 div = −0.628% TR** | **Bull TRAILS SPY ~0.71pp** (improved sharply from −1.87pp as SPY falls −1.51% today) |
| **Pre-mkt (2026-06-23)** | **$98,743.65 (−1.257%)** | **$744.69 + $1.76 div; futures −1.43%** | **Bull TRAILS SPY ~2.21pp est** |
| **Close (2026-06-22)** | **$99,078.33 (−0.922%)** | **$744.69 + $1.76 div = +0.948% TR** | **Bull TRAILS SPY ~1.87pp** |

## Account (pre-market June 23, 2026 — live Alpaca data ~08:03 ET)

| Metric | Value |
|--------|-------|
| Equity | $98,743.65 |
| Cash | $67,261.73 (68.11%) |
| Long market value | $31,481.92 |
| Buying power | ~$357,196 |
| Last equity (June 22 close) | $99,043.58 |

## Open positions (pre-market June 23, 2026 — live Alpaca data ~08:03 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,109.00 | $11,090.00 | +$154.66 (+1.41%) | 11.23% | d4147484 (7sh, HWM **$1,182.73**, stop **$1,064.457**) ✓; 25989fb5 (3sh, same) ✓ — buffer $44.54 (4.01%) |
| NVDA | 33 | $213.421 | $203.90 | $6,728.70 | −$314.19 (−4.46%) | 6.82% | dcba7429 (33sh, HWM **$213.99**, stop **$192.591**) ✓ — buffer $11.31 (5.55%) ⚠️ WATCH USD 200 invalidation |
| V | 22 | $323.57 | $328.45 | $7,225.89 | +$107.35 (+1.51%) | 7.32% | 66033918 (22sh, HWM **$336.8199**, stop **$303.138**) ✓ — buffer $25.31 (7.72%) |
| VST | 40 | $148.81 | $160.95 | $6,437.99 | +$485.59 (+8.16%) | 6.52% | c4c200a5 (40sh, HWM **$170.50**, stop **$153.45**) ✓ — buffer $7.50 (4.66%) ⭐⭐ HELIX+COGENTRIX |

**Sector exposure (pre-market June 23):**
- Healthcare (LLY): $11,090 = 11.23% | Tech/AI Semi (NVDA): $6,728.70 = 6.82% | Financials (V): $7,225.89 = 7.32% | Energy/Utilities (VST): $6,437.99 = 6.52% | Cash: $67,261.73 = 68.11%
- No sector above 60% cap ✓

**Trailing stop status (pre-market June 23 — confirmed via Alpaca live orders ~08:03 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $44.54 = 4.01%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- NVDA (dcba7429): 33sh — HWM **$213.99**, stop **$192.591** ✓ (buffer $11.31 = 5.55%) ⚠️ monitoring
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $25.31 = 7.72%)
- VST (c4c200a5): 40sh — HWM **$170.50**, stop **$153.45** ✓ (buffer $7.50 = 4.66%)
**Stop audit: 5/5 PASS ✓**

**Pre-market June 23 notes:**
- **RISK-OFF session:** KOSPI −9.99% (circuit breakers triggered) — Samsung −12.3%, SK Hynix −12.5% on AI-chip profit-taking. S&P futures −1.43%. Contagion to US semis.
- **NVDA** $203.90 (pre-mkt): −4.46% from entry. KOSPI chip selloff contagion — NOT a fundamental break in NVDA thesis (Vera Rubin launched at ISC HPC 2026; earnings Aug 26 confirmed). **Watch $200 close invalidation** and **$198.48 midday −7% rule.** Buffer 5.55%. HOLD.
- **VST** $160.95 (pre-mkt): −3.77% from $167.26 close. Pure risk-off profit-taking. No negative catalyst — Helix + Cogentrix intact; Wells Fargo/Goldman/Bernstein all Buy. Buffer 4.66% to stop $153.45. STRONG HOLD.
- **LLY** $1,109 (pre-mkt): +0.63% — defensive healthcare holding up well in risk-off. Medicare Bridge July 1 in 8 days — explicit decision required June 30 pre-market.
- **V** $328.45 (pre-mkt): +0.57% — defensive financials; thesis intact.
- **Shock check:** −$299.93 (−0.303%) — no shock ✓
- **Drawdown circuit breaker:** $98,743.65 vs HWM $101,384.21 = **−2.60%** — NOT triggered ✓
- **No trades planned today:** risk-off, no qualified candidates (LRCX ATR elevated by chip selloff; PWR deferred)

**Upcoming catalysts:**
- **LLY Medicare GLP-1 Bridge effective July 1** (8 days — explicit hold/trim/exit decision REQUIRED at pre-market June 30)
- **VST thesis review_by July 7** (14 days)
- **NVDA review_by July 22** (29 days) — $200 invalidation monitoring ongoing
- **V Q3 FY26 earnings July 28** (35 days — thesis review_by date)
- **NVDA earnings August 26** (64 days — outside 2-day window ✓)

**Week of June 22 — new position slots:**
- **Slot 1:** NVDA — FILLED June 22 ✓
- **Slot 2:** LRCX — pending ≤3% ATR for 3 consecutive sessions (reset by today's chip selloff; earliest week of June 29)
- **Slot 3:** PWR — pending ATR normalization + insider selling abates; re-evaluate June 29+

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Pre-mkt (2026-06-23)** | **$98,743.65 (−1.257%)** | **$744.69 + $1.76 div; futures −1.43%** | **Bull TRAILS SPY ~2.21pp est** |
| **Close (2026-06-22)** | **$99,078.33 (−0.922%)** | **$744.69 + $1.76 div = +0.948% TR** | **Bull TRAILS SPY ~1.87pp** |
| **Midday (2026-06-22)** | **$99,201.16 (−0.799%)** | **$744.42 + $1.76 div = +0.91% TR** | **Bull TRAILS SPY ~1.71pp** |
| **Market-open (2026-06-22)** | **$99,204.85 (−0.795%)** | **$747.47 + $1.76 div = +1.323% TR** | **Bull TRAILS SPY ~2.12pp** |
| **Pre-mkt (2026-06-22)** | **$99,057.63 (−0.942%)** | **$747.47 close + $1.76 div = +1.323% TR (futures flat ~−0.1%)** | **Bull TRAILS SPY ~2.26pp est** |
| **Pre-mkt (2026-06-19)** | **$99,039.61 (−0.960%)** | **$747.47 close + $1.76 div = +1.323% total-return** | **Bull TRAILS SPY ~2.28pp** |
| **Close (2026-06-18)** | **$99,074.81 (−0.925%)** | **$747.47 + $1.76 div = +1.323% total-return** | **Bull TRAILS SPY ~2.25pp** |
| **Midday (2026-06-18)** | **$99,203.28 (−0.797%)** | **~$741.20 anchor (total-return incl $1.76 div)** | **Bull TRAILS SPY ~1.70pp est.** |
| **Market-open (2026-06-18)** | **$99,166.19 (−0.834%)** | **$744.55 pre-mkt (+0.929% total-return incl $1.76 div)** | **Bull TRAILS SPY ~1.76pp** |
| **Close (2026-06-17)** | **$99,151.19 (Alpaca last_equity)** | **$741.02 (Alpaca daily bar close, +0.213% price only / +0.451% total-return incl $1.76 div)** | **Bull TRAILS SPY ~1.29pp (total-return)** |
| **Pre-mkt (2026-06-18)** | **$99,128.29 (−0.872%)** | **$744.55 pre-mkt (+0.929% total-return incl $1.76 div)** | **Bull TRAILS SPY ~1.80pp** |
| **Close (2026-06-16)** | **$99,209.83** | **$751.01 (close, +1.564% since inception)** | **Bull TRAILS SPY ~2.35pp** |

## Notes

**Close June 23, 2026 — EOD summary (~15:50 ET):**
- **Market context:** KOSPI chip selloff day 2 — contagion spread to US semis. SPY −1.34% (USD 734.71); NVDA among hardest hit. Bull −0.34% (equity USD 98,711.58) on 68% cash. Since-inception gap narrowed from −1.87pp to −0.89pp in one session.
- **Today P/L:** −$332 = −0.34% | SPY −1.34% | Bull outperformed by +1.00pp — cash acting as ballast.
- **Race scoreboard:** Bull −1.29% | AGGRO ~−6.53% (midday est) | SPY TR −0.40% | Bull leads AGGRO by ~5.2pp.
- **NVDA ⚠️ CRITICAL:** Closed ~USD 201.97 — only 0.99% above USD 200 invalidation. No fundamental thesis break. Pre-market June 24 MUST explicitly decide: HOLD vs trim vs exit if approaches USD 200 again. Do NOT wait for the stop at USD 192.59 if USD 200 is repeatedly tested.
- **LLY:** Medicare Bridge July 1 = 7 trading days. Explicit hold/trim/exit decision REQUIRED pre-market June 30 before the bridge activates.
- **VST ⭐⭐:** +9.21% from entry; strongest position; Helix + Cogentrix thesis most compelling. Stop comfortable at 5.58% buffer.
- **V:** +1.47%; financials defensive; thesis intact.
- **Upcoming: week of June 23** — LRCX/PWR still gated (ATR reset by chip selloff; earliest June 30+). MRVL research candidate pending calmer entry.

**Close June 22, 2026 — EOD summary (~15:51 ET):**
- **Market context:** S&P 500 +0.12% / Nasdaq -0.27% on Quarterly Index rebalance day; SpaceX -10.7% on bond offering dragged large-cap tech; gold crash (Alamos -14%, Gold Fields -10%) as precious metals retreat sharply; Micron +4% ahead of earnings = positive semi thesis read-through for NVDA. Mixed tape with defensives holding up. Bull's 67.9% cash + 4-sector diversification absorbed tech softness.
- **Today P/L:** +$38.72 = +0.039% (vs SPY −0.37% today) — Bull outperformed by +0.41pp; cash cushion working.
- **Shock check:** $99,078.33 vs last_equity $99,039.61 = **+$38.72 = +0.039%** — no shock ✓
- **Drawdown circuit breaker:** $99,078 vs HWM $101,384.21 = **−2.27%** — NOT triggered ✓ (7.73pp headroom)
- **LLY** $1,105.84 (+1.13% from entry, +0.66% today): Healthy close. Medicare Bridge July 1 in 9 days — explicit hold/trim/exit at pre-market June 30. Buffer $41.38 (3.74%) ✓ (narrowed slightly from midday $44.36). HOLD. Conviction **A**. review_by 2026-07-01.
- **NVDA** $208.155 (−2.47% from entry, −1.20% today): Afternoon session weakness (Nasdaq broad tech selling). Buffer $15.56 (7.48%) ✓. AI thesis intact; Micron +4% = positive semi read-through. No catalyst concern. HOLD. Conviction **B** (starter, filled today). review_by 2026-07-22.
- **V** $326.97 (+1.05% from entry, −0.08% today): Essentially flat on the day. Buffer $23.83 (7.29%) ✓. OpenAI/stablecoin thesis intact. HOLD. Conviction **B** (0/3 C-weeks). review_by 2026-07-28.
- **VST** ⭐⭐ $167.40 (+12.49% from entry, +2.23% today): **HWM AUTO-RATCHETED $170.33 → $170.50** during session (VST hit new position high). Stop updated $153.297 → **$153.45** ✓. Buffer $13.95 (8.34%) ✓. +15% tighten trigger at $171.13 still not reached; $0.73 away — monitor at pre-market. STRONG HOLD. Conviction **A**. review_by 2026-07-07.
- **Exit reconciliation:** No exits today. All 4 positions (LLY, NVDA, V, VST) held. closed-trades.md current ✓.
- **Stop audit: 5/5 PASS ✓** (d4147484 LLY 7sh, 25989fb5 LLY 3sh, dcba7429 NVDA 33sh, 66033918 V 22sh, c4c200a5 VST 40sh HWM $170.50)
- **Trades today:** 1 (NVDA 33sh BUY at open). Week slot 1/3 used.
- **No new lessons required** (no losses; no errors).

**Performance vs SPY (EOD June 22):**
- Bull: $99,078.33 = **−0.922%** since inception (May 21)
- SPY total return: ($744.69 + $1.76 div) / $739.44 = **+0.948%** since inception
- **Bull TRAILS SPY by ~1.87pp** (improved from −2.12pp at market-open as positions recovered intraday, then slight afternoon selling)
- Today: Bull +0.039% vs SPY −0.37% = **+0.41pp outperformance today** ✓ (cash cushion absorbing Nasdaq weakness)

**Race scoreboard (EOD June 22):**
- Bull: **−0.922%** (since May 21, USD 100K start)
- AGGRO: **~−4.957% est** (since June 4; last known midday $95,043.13 after MSFT forced close at −13.22%)
- SPY total return: **+0.948%** (since May 21, $739.44 anchor + $1.76 div)
- **Gap: Bull TRAILS SPY by ~1.87pp**
- Bull leads AGGRO by **~4.04pp est**

**Sector exposure (EOD June 22 — close):**
- Healthcare (LLY): $11,058.40 = 11.16%
- Tech/AI Semi (NVDA): $6,869.12 = 6.93%
- Financials (V): $7,193.34 = 7.26%
- Energy/Utilities (VST): $6,696.00 = 6.76%
- Cash: $67,261.74 = 67.89%
- No sector above 60% cap ✓

**Trailing stop status (EOD June 22 — confirmed via Alpaca open orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $41.38 = 3.74%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- NVDA (dcba7429): 33sh — HWM **$213.99**, stop **$192.591** ✓ (buffer $15.56 = 7.48%)
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $23.83 = 7.29%)
- VST (c4c200a5): 40sh — HWM **$170.50** ⬆️ AUTO-RATCHETED (from $170.33 midday), stop **$153.45** ⬆️ ✓ (buffer $13.95 = 8.34%)

**Upcoming catalysts:**
- **LLY Medicare GLP-1 Bridge effective July 1** (9 days — explicit hold/trim/exit decision REQUIRED at pre-market June 30)
- **VST +15% tighten trigger** ($171.13) — HWM now $170.50; approaching ($0.63 from trigger) — monitor pre-market June 23
- **NVDA review_by July 22** (30 days)
- **VST thesis review_by July 7** (15 days)
- **V Q3 FY26 earnings July 28** (36 days — thesis review_by date)
- **NVDA earnings August 26** (65 days — outside 2-day window ✓)

---

**Midday June 22, 2026 (~12:31 ET — no cuts, no tightenings; VST news scan: thesis intact; stop audit 5/5 PASS):**
- **Shock check:** $99,201.16 vs last_equity $99,039.61 = +$161.55 (+0.163%) — no shock ✓
- **Drawdown circuit breaker:** $99,201 vs HWM $101,384 = −2.15% — NOT triggered ✓
- **LLY** $1,108.815 (+1.40% from entry): +0.93% today. Buffer $44.36 (4.00%) ✓. Medicare Bridge July 1 in 9 days. HOLD. Conviction **A**. review_by 2026-07-01.
- **NVDA** $209.685 (−1.75% from entry): mild pullback; no catalyst concern. Stop HWM auto-ratcheted to $213.99 (from $213.61 at fill). Buffer $17.09 (8.15%) ✓. HOLD. Conviction **B**. review_by 2026-07-22.
- **V** $329.285 (+1.77% from entry): +0.63% today. Buffer $26.15 (7.94%) ✓. OpenAI/stablecoin thesis intact. HOLD. Conviction **B** (0/3 C-weeks). review_by 2026-07-28.
- **VST** ⭐⭐ $167.09 (+12.28% from entry): +2.04% today. **News scan triggered (>10% threshold).** Helix Digital Infrastructure (KKR+NVIDIA+Kuwait) re-rating confirmed intact — analyst fair value ~$225. Thesis-driven move, not noise. Buffer $13.79 (8.24%) ✓. Approaching +15% tighten trigger ($171.13) — close routine should monitor and tighten if triggered. STRONG HOLD. Conviction **A**. review_by 2026-07-07.
- **NVDA trailing stop note:** HWM auto-ratcheted from $213.61 (fill) to $213.99 during early session — stop updated from $192.249 to $192.591. Confirmed active ✓.
- **Stop audit: 5/5 PASS ✓** (d4147484 LLY 7sh, 25989fb5 LLY 3sh, dcba7429 NVDA 33sh HWM $213.99, 66033918 V 22sh, c4c200a5 VST 40sh)
- **No cuts, no tightenings, no new positions** — all within guardrails.

**Sector exposure (midday June 22 — live data):**
- Healthcare (LLY): $11,088.15 = 11.18%
- Tech/AI Semi (NVDA): $6,919.61 = 6.97%
- Financials (V): $7,244.27 = 7.30%
- Energy/Utilities (VST): $6,683.60 = 6.73%
- Cash: $67,261.74 = 67.80%
- No sector above 60% cap ✓

**Race scoreboard (midday June 22):**
- Bull: **−0.799%** (since May 21, USD 100K start)
- AGGRO: **~−2.993% est** (since June 4; last known June 19)
- SPY total return: **+0.91% est** (since May 21; SPY $744.42 midday + $1.76 div / $739.44 anchor)
- **Gap: Bull TRAILS SPY by ~1.71pp** (improved from ~2.12pp at market-open as LLY, V, VST all gained)
- Bull leads AGGRO by ~2.19pp est.

**Upcoming catalysts:**
- **LLY Medicare GLP-1 Bridge effective July 1** (9 days — explicit hold/trim/exit decision REQUIRED at pre-market June 30)
- **NVDA review_by July 22** (30 days)
- **VST thesis review_by July 7** (15 days) — approaching +15% tighten trigger
- **V Q3 FY26 earnings July 28** (36 days — thesis review_by date)
- **NVDA earnings August 26** (65 days — outside 2-day window ✓)

**Trailing stop status (midday June 22 — confirmed via Alpaca open orders ~12:31 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $44.36 = 4.00%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- NVDA (dcba7429): 33sh — HWM **$213.99** ⬆️ AUTO-RATCHETED, stop **$192.591** ⬆️ ✓ (buffer $17.09 = 8.15%)
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $26.15 = 7.94%)
- VST (c4c200a5): 40sh — HWM **$170.33**, stop **$153.297** ✓ (buffer $13.79 = 8.24%)

---

**Market-open June 22, 2026 (~09:41 ET — NVDA 33sh BUY EXECUTED; stop audit 5/5 PASS):**
- **NVDA BUY CONFIRMED:** 33sh filled @ avg $213.42 (order de7decb6, filled 13:41 UTC). Cost basis $7,042.89 (7.10% portfolio). Thesis: AI accelerator monopoly; Helix consortium (KKR+NVIDIA+Kuwait) GPU-demand platform; FY26 data center +92% YoY; BofA PT $350. Starter B conviction.
- **NVDA trailing stop placed:** dcba7429 (33sh, 10% trail, HWM $213.61, stop $192.249) ✓ — verified active.
- **VST ex-dividend:** $0.229/sh × 40sh = USD 9.16 credit confirmed; stop ($153.297) NOT adjusted (trailing stop tracks live HWM, not dividend-adjusted price). Stock opened ~$165.34 (+1.59% today, +11.11% from entry).
- **Shock check:** $99,204.85 vs last_equity $99,039.61 = +$165.24 (+0.167%) — no shock ✓
- **Drawdown circuit breaker:** $99,204.85 vs HWM $101,384.21 = −2.148% — NOT triggered ✓
- **LLY** $1,103.04 (+0.87% from entry): Medicare Bridge July 1 in 9 days. Buffer $38.58 (3.50%) ✓. HOLD. Conviction **A**. review_by 2026-07-01.
- **V** $330.605 (+2.17% from entry): OpenAI agentic payments integration. Buffer $27.47 (8.31%) ✓. HOLD. Conviction **B** (0/3 C-weeks). review_by 2026-07-28.
- **VST** $165.345 (+11.11% from entry): Cogentrix + Helix strongest thesis; ex-div today USD 9.16. Buffer $12.05 (7.29%) ✓. STRONG HOLD. Conviction **A**. review_by 2026-07-07.
- **Stop audit: 5/5 PASS ✓** (d4147484 LLY 7sh, 25989fb5 LLY 3sh, dcba7429 NVDA 33sh, 66033918 V 22sh, c4c200a5 VST 40sh)

**Sector exposure (market-open June 22 — post-NVDA fill):**
- Healthcare (LLY): $11,030.40 = 11.12%
- Tech/AI Semi (NVDA): $7,037.91 = 7.09%
- Financials (V): $7,273.31 = 7.33%
- Energy/Utilities (VST): $6,613.80 = 6.67%
- Cash: $67,261.74 = 67.80%
- No sector above 60% cap ✓

**Monday conviction-weighted review (2026-06-22 — post-fill):**
| Symbol | Rating | C-streak | Notes |
|--------|--------|----------|-------|
| LLY | **A** | N/A | Medicare Bridge 9 days; ARK buying; buffer 3.50% |
| NVDA | **B** | 0/3 | Just filled 33sh @ $213.42; starter conviction; review_by July 22 |
| V | **B** | 0/3 | AI payments integration; July 28 earnings gate |
| VST | **A** | N/A | ex-div today USD 9.16 confirmed; Cogentrix + Helix; PT $212–$230 ⭐⭐ |

**Race scoreboard (market-open June 22):**
- Bull: **−0.795%** (since May 21, USD 100K start)
- AGGRO: **~−2.993% est** (since June 4; last known June 19)
- SPY total return: **+1.323%** (since May 21, $739.44 anchor + $1.76 div)
- **Gap: Bull TRAILS SPY by ~2.12pp** (narrowed 0.14pp from pre-mkt)
- Bull leads AGGRO by ~2.20pp est.

**Week of June 22 — new position slots:**
- **Slot 1:** NVDA — FILLED today ✓
- **Slot 2:** LRCX — pending ATR ≤3% for 3+ sessions (ATR was 6.93% pre-mkt June 22)
- **Slot 3:** PWR — pending ATR normalization + insider selling abates

**Upcoming catalysts:**
- **VST ex-dividend JUNE 22 (TODAY)** — USD 9.16 credit confirmed, payable June 30
- **LLY Medicare GLP-1 Bridge effective July 1** (9 days — explicit hold/trim/exit at pre-market June 30)
- **NVDA review_by July 22** (30 days)
- **VST thesis review_by July 7** (15 days)
- **V Q3 FY26 earnings July 28** (36 days)
- **NVDA earnings August 26** (65 days — outside 2-day window ✓)

---

**Pre-market June 22, 2026 (~08:02 ET — first active session since June 18; VST ex-div day; NVDA 33sh buy planned at open):**
- **Market status:** NYSE opens 09:30 ET (first active session since June 18; Juneteenth June 19 was federal holiday).
- **Macro:** S&P 500 futures flat/−0.1%; 10yr Treasury 4.49% (below 4.75% trigger ✓); Iran/US peace deal constructive; Micron +4% pre-mkt on AI memory demand = positive NVDA read-through.
- **Shock check:** $99,057.63 vs last_equity $99,039.61 = **+$18.02 (+0.018%)** — no shock ✓
- **Drawdown circuit breaker:** $99,058 vs HWM $101,384 = **−2.295%** — NOT triggered ✓
- **LLY** ~$1,100 (+0.59% from entry): Medicare Bridge July 1 in **9 days** — explicit hold/trim/exit at pre-market June 30. Buffer ~3.23% ✓. HOLD. Conviction **A**. review_by 2026-07-01.
- **V** ~$327.50 (+1.22% from entry): OpenAI agentic payments integration catalyst confirmed. Buffer ~7.44% ✓. HOLD. Conviction **B** (0/3 C-weeks). review_by 2026-07-28.
- **VST** ~$163.70 (+10.01% from entry): **⭐ EX-DIVIDEND TODAY — USD 9.16 credit (40sh × $0.229), payable June 30.** Stock may open ~$0.229 lower — normal ex-div; stop ($153.297) not adjusted. Cogentrix + Helix thesis strongest. Buffer ~6.36% ✓. STRONG HOLD. Conviction **A**. review_by 2026-07-07.
- **NVDA** ~$210.10 pre-mkt: All gates cleared. **BUY 33sh at open. 10% trailing stop immediately after fill.** Week slot 1/3.
- **Stop audit: 4/4 PASS ✓** (d4147484 LLY 7sh, 25989fb5 LLY 3sh, 66033918 V 22sh, c4c200a5 VST 40sh — all confirmed active)

**Sector exposure (pre-market June 22 — before NVDA fill):**
- Healthcare (LLY): ~$11,000 = ~11.10%
- Financials (V): ~$7,205 = ~7.27%
- Energy/Utilities (VST): ~$6,548 = ~6.61%
- Cash: $74,304.63 = ~74.97% (→ ~68.0% after NVDA fills)
- Tech / AI Semi (NVDA, pending): ~7.0% after fill
- No sector above 60% cap ✓

**Monday conviction-weighted review (2026-06-22):**
| Symbol | Rating | C-streak | Notes |
|--------|--------|----------|-------|
| LLY | **A** | N/A | Medicare Bridge 9 days; ARK buying; buffer 3.23% |
| V | **B** | 0/3 | AI payments integration; July 28 earnings gate |
| VST | **A** | N/A | ex-div today USD 9.16; Cogentrix + Helix; PT $212–$230 ⭐⭐ |
| NVDA | _pending_ | N/A | 33sh at open; starter B conviction post-fill |

**Race scoreboard (pre-market June 22):**
- Bull: **−0.942%** (since May 21, USD 100K start)
- AGGRO: **~−2.993% est** (since June 4; last known June 19)
- SPY total return: **+1.323%** (since May 21, $739.44 anchor + $1.76 div)
- **Gap: Bull TRAILS SPY by ~2.26pp est** (flat futures pre-mkt June 22)
- Bull leads AGGRO by ~2.05pp est.

**Upcoming catalysts:**
- **VST ex-dividend JUNE 22 (TODAY)** — USD 9.16 credit (40sh × $0.229, payable June 30)
- **LLY Medicare GLP-1 Bridge effective July 1** (9 days — explicit hold/trim/exit decision at pre-market June 30)
- **VST thesis review_by July 7** (15 days)
- **V Q3 FY26 earnings July 28** (36 days — thesis review_by date)
- **NVDA earnings August 26** (65 days — well outside 2-day window ✓)
- **LLY review_by July 1** (9 days — Medicare Bridge effective)

---

**Close June 19, 2026 — EOD summary (~15:50 ET — Juneteenth federal holiday, market CLOSED all day; stop audit 4/4 PASS; next open June 22):**
- **Market closed:** Juneteenth federal holiday — no trading. Last active session: June 18 (SPY +0.977% to $747.47, US-Iran peace deal signed at Versailles). Market confirmed closed via Alpaca clock; next open June 22, 09:30 ET.
- **Today P/L:** $0.00 (0.00%) — market closed; equity unchanged from June 18 official settlement $99,039.61.
- **Shock check:** $0.00 = 0.00% — no shock ✓ (holiday).
- **Drawdown circuit breaker:** $99,040 vs HWM $101,384 = −2.31% — NOT triggered ✓ (7.69pp headroom remaining).
- **Position review (prices = June 18 close — market closed all day):**
  - LLY 10sh @ $1,098.57: +0.46% from entry; −7% threshold $1,017.00 clear by $81.57; buffer $34.11 (3.11%) ✓. Medicare Bridge July 1 in 12 days. HOLD.
  - V 22sh @ $327.24: +1.13% from entry; −7% threshold $300.92 clear by $26.32; buffer $24.10 (7.37%) ✓. OpenAI/stablecoin thesis intact. HOLD.
  - VST 40sh @ $163.75: +10.04% from entry; −7% threshold $138.39 clear by $25.36; buffer $10.45 (6.39%) ✓. Helix+Cogentrix thesis intact. **DIVIDEND EX-DATE MONDAY JUNE 22** — USD 9.16 credit (40sh × $0.229). STRONG HOLD.
- **Stop audit: 4/4 PASS ✓** All stops unchanged (market closed; no ratchets possible).
- **Exit reconciliation:** No exits. closed-trades.md current ✓.
- **No new lessons required** (no losses, no errors today).
- **Friday watchdog:** Today is Friday June 19. Last weekly review: Week ending June 12 (7 days ago — on-schedule; NOT >7 days). Weekly review for week ending June 19 runs at 4:30 PM today. Watchdog NOT triggered ✓.

**Performance vs SPY (EOD June 19):**
- Bull: $99,039.61 = **−0.960%** since inception (May 21)
- SPY total return: ($747.47 + $1.76 div) / $739.44 = **+1.323%** since inception
- **Bull TRAILS SPY by ~2.28pp** (unchanged from June 18 EOD — market closed)

**Race scoreboard (EOD June 19):**
- Bull: **−0.960%** (since May 21, USD 100K start)
- AGGRO: **−2.993%** (since June 4; equity $97,006.60 per June 19 market-open snapshot)
- SPY: **+1.323%** (since May 21, total return incl $1.76 div)
- Bull leads AGGRO by **~2.03pp**

**Sector exposure (EOD June 19 — unchanged from June 18):**
- Healthcare (LLY): $10,985.70 = 11.09%
- Financials (V): $7,199.28 = 7.27%
- Energy/Utilities (VST): $6,550.00 = 6.61%
- Cash: $74,304.63 = 74.97% (NVDA ~7.0% deployed Monday → cash drops to ~68.0% if filled)
- No sector above 60% cap ✓

**Trailing stop status (EOD June 19 — confirmed active, unchanged from June 18):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $34.11 = 3.11%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $24.10 = 7.37%)
- VST (c4c200a5): 40sh — HWM **$170.33**, stop **$153.297** ✓ (buffer $10.45 = 6.39%)

**Monday June 22 priorities:**
- **NVDA BUY: 33sh at market open** (~USD 6,930, 7.0% portfolio) — 10% trailing stop immediately after fill. Confirm 10yr < 4.75% at pre-market first. All other gates already cleared.
- **VST ex-div:** Confirm $0.229/sh × 40sh = USD 9.16 cash credit to account. Normal dividend adjustment; stop levels unchanged.
- **LLY Medicare Bridge July 1:** 12 days — explicit hold/trim/exit decision required at pre-market June 30.
- **New position slots (week of June 22):** Slot 1 = NVDA (planned). Slots 2-3 = LRCX / PWR when ATR gates clear.

---

**Midday June 19, 2026 (~12:31 ET — Juneteenth federal holiday, market CLOSED; stop audit 4/4 PASS; next open June 22):**
- **Market closed:** Juneteenth — no trades. Market clock confirmed `is_open: false`. Next open June 22, 09:30 ET.
- **Shock check:** $99,039.61 vs last_equity $99,039.61 = $0.00 (0.00%) — market closed, no change ✓.
- **Drawdown circuit breaker:** $99,040 vs HWM $101,384 = −2.31% — NOT triggered ✓.
- **Position review (prices = June 18 close, market closed):**
  - LLY 10sh @ $1,098.57: +0.46% from entry; −7% threshold $1,017.00 clear by $81.57; buffer $34.11 (3.11%) ✓. HOLD.
  - V 22sh @ $327.24: +1.14% from entry; −7% threshold $300.92 clear by $26.32; buffer $24.10 (7.37%) ✓. HOLD.
  - VST 40sh @ $163.75: +10.04% from entry; −7% threshold $138.39 clear by $25.36; buffer $10.45 (6.39%) ✓. HOLD. (Not at +15% tighten threshold.)
- **Stop audit: 4/4 PASS ✓** All stops unchanged (market closed; no ratchets possible):
  - LLY: d4147484 (7sh) + 25989fb5 (3sh), HWM $1,182.73, stop $1,064.457 ✓
  - V: 66033918 (22sh), HWM $336.8199, stop $303.138 ✓
  - VST: c4c200a5 (40sh), HWM $170.33, stop $153.297 ✓
- **No exits, no cuts, no tightenings.** All positions within all guardrails. No action possible or required.
- **Monday readiness:** NVDA plan (33sh ~$210, 7.0% portfolio) ready to execute June 22 open. VST ex-div Monday June 22 — confirm USD 9.16 credit at open. LLY Medicare Bridge July 1 = 12 days.

**Market-open June 19, 2026 (~09:36 ET — Juneteenth federal holiday, market CLOSED; stop audit 4/4 PASS; next open June 22):**
- **Market closed:** Juneteenth — no trades. Market clock confirmed `is_open: false`. Next open June 22, 09:30 ET.
- **Plan check:** research-log.md most recent plan has `plan_date: 2026-06-22` (Monday). Plan is NOT for today — no trades to execute. Correct outcome.
- **Shock check:** $99,039.61 vs last_equity $99,039.61 = $0.00 (0.00%) — no change ✓ (holiday, market closed).
- **Drawdown circuit breaker:** $99,040 vs HWM $101,384 = −2.31% — NOT triggered ✓.
- **Stop audit: 4/4 PASS ✓** All positions and stops confirmed via live Alpaca data:
  - LLY 10sh @ $1,098.57: stops d4147484 (7sh) + 25989fb5 (3sh), HWM $1,182.73, stop $1,064.457 ✓
  - V 22sh @ $327.24: stop 66033918, HWM $336.8199, stop $303.138 ✓
  - VST 40sh @ $163.75: stop c4c200a5, HWM $170.33, stop $153.297 ✓
- **No exits since last run.** closed-trades.md current ✓.
- **Monday readiness confirmed:** NVDA plan (33sh ~$210, 7.0% portfolio) ready to execute June 22 open. VST ex-div June 22 — confirm USD 9.16 credit at open. LLY Medicare Bridge July 1 = 12 days.

**Pre-market June 19, 2026 (~12:02 ET — Juneteenth federal holiday, market closed; next open June 22):**
- **Market closed today:** Juneteenth — no trading. All prices = June 18 AH. Routine is planning for Monday June 22.
- **Macro:** 10yr Treasury ~4.44% (below 4.75% gate ✓ — new buys permitted Monday). Iran/US peace deal signed at Versailles; SPY closed $747.47 June 18. No overnight macro shock.
- **Shock check:** $99,039.61 vs last_equity $99,039.61 = $0.00 (0.00%) — no shock ✓ (holiday, no trading).
- **Drawdown circuit breaker:** $99,040 vs HWM $101,384 = −2.31% — NOT triggered ✓.
- **LLY** $1,098.57 (+0.46% from entry, −0.09% from June 18 close of $1,099.55). AH drift minor; no overnight catalyst. Medicare Bridge July 1 in 12 days. Buffer $34.11 (3.10%) ✓. HOLD. Conviction: **A**. review_by: July 1.
- **V** $327.245 (+1.13% from entry, −0.24% from June 18 close of $328.025). AH drift minor; thesis intact. Buffer $24.107 (7.36%) ✓. HOLD. Conviction: **B**. review_by: July 28.
- **VST** $163.75 (+10.04% from entry, −0.15% from June 18 close of $164.00). AH drift minor. ⭐⭐ **DIVIDEND EX-DATE MONDAY JUNE 22** — $0.229/sh × 40sh = USD 9.16 credit (payment June 30). Helix + Cogentrix thesis strongest. Buffer $10.453 (6.39%) ✓. HOLD. Conviction: **A**. review_by: July 7.
- **Stop audit: 4/4 PASS ✓** No changes (market closed).
- **Monday conviction review:** LLY **A**, V **B**, VST **A** — no mandatory trims (no position at C for 3+ weeks). V tracked at B since June 15: 0/3 weeks at C.
- **NVDA — CLEARED FOR MONDAY:** June 18 close $210.38 (above $205 gate ✓), ATR June 17 = 2.80% ✓, ATR June 18 = 2.32% ✓ (2 of 3 required sessions ≤3%). **Planned Monday June 22: BUY 33sh NVDA (~USD 6,930 at ~$210, 7.0% portfolio). Place 10% trailing stop immediately.** thesis: AI accelerator monopoly; Helix consortium embeds GPU demand; FY26 data center +92% YoY; 5/5 entry signals met. invalidation: closes below $200 on volume. review_by: 2026-07-22.
- **LRCX:** ATR 3.54% June 18 — still above ≤3% gate. Deferred. Re-evaluate next week.
- **PWR:** ATR 3.97% June 18 + insider selling $123.2M in 30 days. Deferred. Re-evaluate next week when ATR normalizes.
- **Week of June 22: 3 fresh new-position slots.** Slot 1 = NVDA (planned Monday). Slots 2-3 = reserve for LRCX/PWR when gates clear.
- **VST note for Monday:** Stock goes ex-dividend Monday. May open slightly lower by ~$0.229. This is normal; stop level ($153.297) is NOT affected — trailing stop tracks the HWM ($170.33), not the ex-div gap.

**Sector exposure (pre-market June 19):**
- Healthcare (LLY): $10,985.70 = 11.09%
- Financials (V): $7,199.28 = 7.27%
- Energy/Utilities (VST): $6,550.00 = 6.61%
- Cash: $74,304.63 = 74.97% (incl. NVDA plan: ~USD 6,930 deployed → cash drops to ~68.0% if NVDA fills)
- Tech / AI Semi (NVDA, if filled Mon): ~6.99% = adds new sector
- No sector above 60% cap ✓ (even after NVDA: Tech ~7%, well below 60%)

**Trailing stop status (pre-market June 19 — carried from June 18 close ✓):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $34.11 = 3.10%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $24.107 = 7.36%)
- VST (c4c200a5): 40sh — HWM **$170.33**, stop **$153.297** ✓ (buffer $10.453 = 6.39%)

**Race scoreboard (pre-market June 19):**
- Bull: **−0.960%** (since May 21, USD 100K start)
- AGGRO: **~−2.641% est** (since June 4 inception; read-only)
- SPY total return: **+1.323%** (since May 21, $739.44 anchor + $1.76 div)
- **Gap: Bull TRAILS SPY by ~2.28pp**
- Bull leads AGGRO by ~1.68pp est.

**Week of June 22 — new position slots (fresh 3 slots):**
- **Slot 1:** NVDA — PLANNED buy 33sh Monday at open (~USD 6,930, 7.0% portfolio). 10% trailing stop.
- **Slot 2:** LRCX — pending ATR ≤3% for 3+ sessions
- **Slot 3:** PWR — pending ATR normalization + insider selling abates

**Upcoming catalysts:**
- **VST dividend ex-date MONDAY JUNE 22** (USD 9.16 credit for 40sh — payment June 30)
- **NVDA earnings Aug 26** (68 days — next earnings well outside 2-day window ✓)
- **LLY Medicare GLP-1 Bridge effective July 1** (12 days — explicit hold/trim/exit decision required at pre-market June 30)
- **VST thesis review_by July 7** (18 days)
- **V Q3 FY26 earnings July 28** (39 days — thesis review_by date)
- **PWR next earnings July 30** (41 days — enter before earnings if thesis confirmed)

---

**Close June 18, 2026 — EOD summary (~15:51 ET):**
- **Market context:** US-Iran interim peace agreement formally signed at Versailles (Presidents Trump + Pezeshkian); SPY rebounded +0.977% to $747.47 as the post-FOMC hawkish dot-plot was digested and geopolitical risk faded; financials and pharma led while VST surged on continued Cogentrix/AI-power re-rating.
- **Today P/L:** −$76.38 = −0.077% (75% cash drag on SPY's +0.977% rally)
- **VST** ⭐⭐ $164.00 (+10.21% from entry, +3.26% today). Cogentrix acquisition complete + Helix Digital Infrastructure thesis intact. HWM $170.33 set at midday high; stop $153.297. Buffer $10.70 (6.53%) ✓. **DIVIDEND EX-DATE JUNE 22** (USD 9.16 credit for 40sh — confirm at June 22 open). STRONG HOLD.
- **LLY** $1,099.55 (+0.55% from entry, −1.12% today). Mild pullback on FOMC rate-hike residual fears; no LLY-specific negative catalyst. Medicare Bridge July 1 in 13 days. Buffer $35.09 (3.19%) ✓. HOLD.
- **V** $328.025 (+1.38% from entry, −0.71% today). Mild softness; OpenAI/stablecoin thesis intact. Buffer $24.887 (7.58%) ✓. HOLD.
- **Stop audit: 4/4 PASS ✓** No ratcheting at close (VST closed below midday HWM $170.33).
- **No exits today.** closed-trades.md current ✓.
- **SPY quarterly dividend (Q2 2026):** Ex-date today June 18, $1.76/sh. Total-return anchor: **$741.20** (was $739.44). Cumulative SPY div since inception: **+$1.76/sh** (June 2026 quarter). This credit reduces the Bull vs SPY gap by ~0.238pp vs price-only comparison.
- **Week of June 16:** 0/3 new positions used. All candidates gate-blocked (NVDA price, LRCX ATR, PWR settling). Fresh 3 slots available June 22.
- **Next open:** June 22, 09:30 ET (Juneteenth June 20 — closed)

**Shock check:** $99,074.81 vs last_equity $99,151.19 = −$76.38 = −0.077% ✓
**Drawdown circuit breaker:** $99,074 vs HWM $101,384 = −2.276% ✓ NOT triggered.

**Sector exposure (close June 18):**
- Healthcare (LLY): $10,995.50 = 11.10%
- Financials (V): $7,216.55 = 7.28%
- Energy/Utilities (VST): $6,560.00 = 6.62%
- Cash: $74,304.63 = 74.99%
- No sector above 60% cap ✓

**Week of June 16 — new position slots (0/3 used, 3 remaining for week of June 22):**
- **Slot 1:** NVDA — needs clean close above $205; re-evaluate June 22+
- **Slot 2:** PWR — post-conference settle; TD Cowen PT $775, Citi PT $837; re-evaluate June 22+
- **Slot 3:** LRCX — ATR must reach ≤3% for 3+ sessions; re-evaluate June 22+

**Trailing stop status (close June 18 — confirmed active):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $35.09 = 3.19%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $24.887 = 7.58%)
- VST (c4c200a5): 40sh — HWM **$170.33**, stop **$153.297** ✓ (buffer $10.70 = 6.53%)

**Race scoreboard (EOD June 18):**
- Bull: **−0.925%** (since May 21, USD 100K start)
- AGGRO: **~−2.641% est** (since June 4; midday June 18 $97,358.67; final AGGRO close TBD)
- SPY total return: **+1.323%** (since May 21, $739.44 anchor + $1.76 div)
- **Gap: Bull TRAILS SPY by ~2.25pp** (widened vs yesterday's −1.29pp as SPY rallied +0.98% while 75% cash limited Bull's capture)
- Bull leads AGGRO by ~1.7pp est.

**Upcoming catalysts:**
- **VST dividend ex-date June 22** (USD 9.16 credit for 40sh — 4 days; confirm credit at open)
- **LLY Medicare GLP-1 Bridge effective July 1** (13 days — explicit hold/trim/exit decision required at pre-market June 30)
- **VST thesis review_by July 7** (19 days)
- **V Q3 FY26 earnings July 28** (40 days — thesis review_by date)
- **PWR next earnings July 30** (42 days — enter before earnings if thesis confirmed)

---

**Midday June 18, 2026 (~12:31 ET):**
- **No cuts, no tightenings.** All 3 positions within guardrails. Risk-management-only run.
- **Shock check:** $99,203.28 vs last_equity $99,151.19 = +$52.09 (+0.053%) — no shock ✓.
- **Drawdown circuit breaker:** $99,203 vs HWM $101,384 = −2.15% — NOT triggered ✓.
- **VST** ⭐⭐ $167.77 (+12.741% from entry, +5.629% intraday). **Trailing stop AUTO-RATCHETED to HWM $170.33** (from $164.1075 at market-open), stop $153.297. New session high $170.33 — Cogentrix completion + Helix Digital Infrastructure continuing to drive re-rating. Goldman Sachs maintains Buy (PT $209). Dividend ex-date June 22 (4 days, USD 9.16 for 40sh). Approaching 15% from entry (12.74%) — close routine should monitor tighten threshold. STRONG HOLD.
- **LLY** $1,095.80 (+0.207% from entry, −1.457% intraday). Mild pullback — no LLY-specific negative catalyst. Medicare Bridge July 1 in 13 days. Buffer $31.34 (2.86%) ✓. HOLD.
- **V** $328.90 (+1.647% from entry, −0.448% intraday). Mild softness. OpenAI/stablecoin thesis intact. Buffer $25.76 (7.83%) ✓. HOLD.
- **Stop audit: 4/4 PASS ✓** VST auto-ratcheted to HWM $170.33, stop $153.297. LLY and V unchanged.
- **Week of June 16:** 0/3 new positions used. NVDA, LRCX, PWR all gate-blocked. Re-evaluate June 19+.
- **Next open:** June 22, 09:30 ET (markets closed Friday June 20 — Juneteenth observed).

**Market-open June 18, 2026 (~09:36 ET):**
- **No trades:** Pre-market plan was empty — all candidate gates failed (NVDA below $205, LRCX ATR 6.2%, PWR post-conference). Correct outcome — no trades forced.
- **Shock check:** $99,166.19 vs last_equity $99,151.19 = +$15.00 (+0.015%) — no shock ✓. Portfolio UP slightly at open.
- **Drawdown circuit breaker:** $99,166 vs HWM $101,384 = −2.19% — NOT triggered ✓.

**Sector exposure (midday June 18):**
- Healthcare (LLY): $10,958.00 = 11.05%
- Financials (V): $7,235.80 = 7.30%
- Energy/Utilities (VST): $6,710.80 = 6.77%
- Cash: $74,304.63 = 74.90%
- No sector above 60% cap ✓

**Week of June 16 — new position slots (0/3 used, 3 remaining):**
- **Slot 1:** NVDA — needs close above $205 and hold; failing gate. Re-evaluate June 19+
- **Slot 2:** PWR — conference ended June 17; re-evaluate June 19+ once settled
- **Slot 3:** LRCX — ATR 6.2% disqualified; re-evaluate when ≤3% for 3+ sessions

**Upcoming catalysts:**
- **VST dividend ex-date June 22** (USD 9.16 credit for 40sh — 4 days; markets closed June 20, next open June 22)
- **LLY Medicare GLP-1 Bridge effective July 1** (13 days — explicit hold/trim/exit decision required at pre-market June 30)
- **VST thesis review_by July 7** (19 days)
- **PWR next earnings July 30** (42 days — enter before earnings if thesis confirmed)
- **V Q3 FY26 earnings July 28** (40 days — thesis review_by date)

**Trailing stop status (midday June 18 — confirmed via Alpaca open orders ~12:31 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $31.34 = 2.86%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $25.76 = 7.83%)
- VST (c4c200a5): 40sh — HWM **$170.33** ⬆️ AUTO-RATCHETED (from $164.1075 at open), stop **$153.297** ⬆️ ✓ (buffer $14.47 = 8.62%)

**Race scoreboard (midday June 18):**
- Bull: **−0.797%** (since May 21, USD 100K start)
- AGGRO: **~−5.0% est** (from June 4; hawkish FOMC likely hit MSFT hard)
- SPY total return: **~+0.8% est** (since May 21, $739.44 anchor; incl $1.76 div today)
- **Gap: Bull TRAILS SPY ~1.70pp est** (improving from ~1.76pp at market-open as VST surges)
- Bull leads AGGRO by ~4pp est.

---

**Pre-market June 18, 2026 (~08:03 ET):**
- **Market context:** S&P 500 futures +0.87% — post-FOMC rebound. 10yr Treasury at 4.49% (confirmed BELOW 4.75% trigger ✓ — new buys permitted). SPY ex-dividend today ($1.76/sh); total-return anchor updates from $739.44 to **$741.20**. SPY pre-market $744.55. Import prices May +1.9% (fuel/lubricants +12.5%) — mild inflationary pressure but not alarming.
- **Shock check:** $99,128.29 vs last_equity $99,151.19 = −$22.90 (−0.023%) — no shock ✓.
- **Drawdown circuit breaker:** $99,128 vs HWM $101,384 = −2.22% — NOT triggered ✓.
- **LLY** $1,112.73 (+1.755% from entry). 4E Therapeutics acquisition (neuroscience/non-addictive painkillers) — pipeline diversification. Medicare Bridge July 1 in 13 days. Buffer $48.27 (4.34%) ✓. HOLD.
- **V** $330.00 (+1.987% from entry). No new catalysts. Cross-border slowdown concern (monitoring). OpenAI partnership active. Stop HWM ratcheted to $336.82 yesterday. Buffer $26.86 (8.14%) ✓. HOLD.
- **VST** $160.909 (+8.131% from entry). ⭐⭐ **COGENTRIX COMPLETED** — Vistra closed acquisition of 5,500 MW natural gas capacity ($4.0B). Directly expands AI power infrastructure footprint. Helix thesis + Cogentrix = strongest position in portfolio. Pre-market +1.31% vs SPY +0.48%. Dividend ex-date June 22 in 4 days (USD 9.16). Buffer $14.71 (9.14%) ✓. STRONG HOLD.
- **Stop audit: 4/4 PASS ✓** V HWM ratcheted to $336.82 during June 17 session.
- **No new buys today:** NVDA closed $204.70 (below $205 threshold, pre-market ~$202-205); LRCX ATR 6.2% (>3% gate); PWR conference ended yesterday (volatility settling — re-evaluate June 19+).
- **SPY benchmark update:** Ex-dividend $1.76/sh today → total-return anchor: **$741.20** (was $739.44).

**Sector exposure (pre-market June 18):**
- Healthcare (LLY): $11,127.30 = 11.22%
- Financials (V): $7,260.00 = 7.32%
- Energy/Utilities (VST): $6,436.36 = 6.49%
- Cash: $74,304.63 = 74.96%
- No sector above 60% cap ✓

**Week of June 16 — new position slots (0/3 used, 3 remaining):**
- **Slot 1:** NVDA — needs to reclaim and hold above $205; pre-market fails gate (re-evaluate June 19+)
- **Slot 2:** PWR — conference ended June 17; re-evaluate June 19+ once volatility settles
- **Slot 3:** LRCX — ATR ~6.2% disqualified; re-evaluate when ≤3% for 3+ sessions

**Upcoming catalysts:**
- **VST dividend ex-date June 22** (USD 9.16 credit for 40sh — 4 days)
- **LLY Medicare GLP-1 Bridge effective July 1** (13 days — explicit hold/trim/exit decision required at pre-market June 30 or July 1)
- **VST thesis review_by July 7** (19 days)
- **PWR next earnings July 30** (42 days — enter before earnings if thesis confirmed)
- **V Q3 FY26 earnings July 28** (40 days — thesis review_by date)

**Race scoreboard (pre-mkt June 18):**
- Bull: **−0.872%** (since May 21, USD 100K start)
- AGGRO: **~−5.0% est** (from June 4; hawkish FOMC likely hit MSFT hard)
- SPY total return: **+0.929%** (since May 21, $739.44 anchor; incl $1.76 div today)
- **Gap pre-mkt June 18: Bull TRAILS SPY by ~1.80pp** (vs −1.07pp close June 17 using price-only; total-return gap is wider due to $1.76 dividend credit to SPY today)
- Bull leads AGGRO by ~4pp est.

**Trailing stop status (pre-market June 18):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $48.27 = 4.34%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$336.8199** ⬆️ RATCHETED Jun 17, stop **$303.138** ✓ (buffer $26.86 = 8.14%)
- VST (c4c200a5): 40sh — HWM **$162.44**, stop **$146.196** ✓ (buffer $14.71 = 9.14%)

---

**Close June 17, 2026 — EOD summary (~15:51 ET):**
- **Market context:** Fed held rates (3.50–3.75%) but issued a hawkish dot plot — 9 of 18 members now project a rate hike by year-end. Bond yields surged. Tech bellwethers (MSFT, META, GOOGL, AMZN) led broad losses. SPY fell −1.44% to $740.23. Bull's 75% cash cushion limited the damage to −0.17%, outperforming SPY by +1.27pp. Hawkish surprise is a direct threat to high-multiple tech names; pre-market Thursday must check 10yr vs 4.75% trigger before any new buys.
- **LLY** $1,112.13 (−0.92% intraday, +1.70% from entry). Healthcare sold off modestly on rising rate fears; no LLY-specific negative catalyst. Medicare Bridge July 1 in 14 days. Buffer $47.67 (4.29%) ✓. Thesis STRONGEST. HOLD.
- **V** $330.695 (−0.73% intraday, +2.20% from entry). Financials mixed on rate-hike fear. OpenAI/stablecoin thesis intact. HWM $336.82, buffer $27.56 (8.33%) ✓. HOLD.
- **VST** ⭐⭐ $158.41 (−0.13% intraday, +6.45% from entry). **Stop HWM auto-ratcheted $161.91→$162.44** during afternoon session — VST hit new position high even on a broad market selloff. Resilient to rate-hike fears (nuclear baseload thesis). Dividend ex-date June 22 in 5 days (USD 9.16 credit). Buffer $12.21 (7.71%) ✓. HOLD.
- **Stop audit:** 4/4 confirmed ✓ — VST HWM ratcheted $161.91→$162.44 during afternoon.
- **FOMC gate LIFTED (2 PM ET today)** — but hawkish dot plot changes calculus. Pre-mkt Thursday: (1) check 10yr — if > 4.75%, halt all new buys per macro rule; (2) if < 4.75%, NVDA entry eligible only if basing above $205 with ATR ≤3%; (3) LRCX and PWR same 10yr gate.
- **SPY ex-dividend TOMORROW June 18:** $1.76/sh — after tomorrow, SPY total-return anchor adjusts from $739.44 to **$741.20**. Pre-market June 18 must update the benchmark anchor.
- **Quarterly SPY dividend (June 2026):** Ex-date June 18, $1.76/sh. Cumulative SPY dividends since inception: $0.00 (not yet received — ex-date tomorrow). Post-June 18 cumulative SPY div = +$1.76/sh for total-return benchmarking accuracy.

**Sector exposure (close June 17):**
- Healthcare (LLY): $11,121.30 = 11.23%
- Financials (V): $7,275.29 = 7.35%
- Energy/Utilities (VST): $6,336.40 = 6.40%
- Cash: $74,304.63 = 75.02%
- No sector above 60% cap ✓

**Week of June 16 — new position slots (FOMC gate lifted — 10yr hike risk gate now applies):**
- **Slot 1:** CONDITIONAL — NVDA: pre-mkt Thursday confirm 10yr < 4.75% AND basing above $205 with ATR ≤3%
- **Slot 2:** CONDITIONAL — LRCX: same 10yr gate; ATR must normalize to ≤3%
- **Slot 3:** CONDITIONAL — PWR: same 10yr gate; post-conference volatility settled

**Since inception performance (EOD June 17):**
- Bull: $100,000 → $99,037.62 = **−0.963%**
- SPY: $739.44 → $740.23 = **+0.107%**
- **Gap EOD June 17: Bull TRAILS SPY by ~1.07pp** — massive narrowing from −2.35pp yesterday as SPY fell −1.44% on FOMC hawkish surprise while Bull's cash cushioned the blow
- Today: Bull −0.166% vs SPY −1.435% = **+1.269pp outperformance today** ✓

**Race scoreboard (EOD June 17):**
- Bull: **−0.963%** (since May 21, USD 100K start)
- AGGRO: **~−5.0% est** (since June 4; midday was −4.27%; hawkish FOMC likely hit MSFT/META hard — MSFT was at only 2.29pp buffer from −12% cut at midday)
- SPY vs Bull inception: **+0.107%** (since May 21, $739.44 anchor)
- Bull leads AGGRO by ~4pp (est.). Bull nearly at par with SPY.

**Trailing stop status (EOD June 17 — confirmed via Alpaca open orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $47.67 = 4.29%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$336.8199**, stop **$303.138** ✓ (buffer $27.56 = 8.33%)
- VST (c4c200a5): 40sh — HWM **$162.44** ⬆️ RATCHETED (from $161.91 midday), stop **$146.196** ⬆️ ✓ (buffer $12.21 = 7.71%)

**Upcoming catalysts:**
- **FOMC COMPLETED June 17:** Rate hold 3.50–3.75%; hawkish dot plot (9/18 see rate hike by year end). Pre-mkt Thursday: check 10yr vs 4.75% trigger — critical gate for new buys.
- **SPY dividend ex-date TOMORROW June 18** ($1.76/sh — SPY total-return anchor → $741.20; pre-mkt June 18 must update benchmark)
- **VST dividend ex-date June 22** (USD 9.16 credit for 40sh — 5 days)
- **LLY Medicare GLP-1 Bridge effective July 1** (14 days — explicit hold/trim/exit decision at pre-market June 30 or July 1)
- **VST thesis review_by July 7** (20 days)
- **V Q3 FY26 earnings July 28** (41 days — thesis review_by date)

---

## Account (close June 16, 2026 — live Alpaca data ~15:51 ET)

| Metric | Value |
|--------|-------|
| Equity | $99,209.83 |
| Cash | $74,304.63 (74.90%) |
| Long market value | $24,905.20 |
| Buying power | ~$366,953 |
| Last equity (June 15 close) | $98,862.97 |

## Open positions (close June 16, 2026 — live Alpaca data ~15:51 ET)

| Symbol | Qty | Avg entry | Current price | Mkt value | Unrealized P/L | % of portfolio | Trailing Stop |
|--------|-----|-----------|--------------|-----------|----------------|----------------|---------------|
| LLY | 10 | $1,093.534 | $1,122.2175 | $11,222.175 | +$286.835 (+2.62%) | 11.31% | d4147484 (7sh, HWM **$1,182.73**, stop **$1,064.457**) ✓; 25989fb5 (3sh, same) ✓ — buffer $57.76 (5.14%) ⭐ |
| V | 22 | $323.57 | $332.61 | $7,317.42 | +$198.88 (+2.79%) | 7.38% | 66033918 (22sh, HWM **$333.08** ⬆️ RATCHETED, stop **$299.772** ⬆️) ✓ — buffer $32.84 (9.87%) |
| VST | 40 | $148.81 | $159.14 | $6,365.60 | +$413.20 (+6.94%) | 6.41% | c4c200a5 (40sh, HWM **$161.48** ⬆️ RATCHETED, stop **$145.332** ⬆️) ✓ — buffer $13.81 (8.68%) ⭐⭐ HELIX |
| ~~META~~ | ~~15~~ | ~~$620.637~~ | — | — | **CLOSED -$639.56 (-6.87%) via trailing stop** | — | **FILLED** (4ea07e91) at $578.00 ~11:06 AM ET Jun 10 ✓ |
| ~~NVDA~~ | ~~30~~ | ~~$216.302~~ | — | — | **CLOSED -$217.80 (-3.36%) via trailing stop** | — | **FILLED** (8c6b9680) at $209.042 ~11:20 AM ET Jun 5 ✓ |
| ~~MSFT~~ | ~~20~~ | ~~$422.31~~ | — | — | **CLOSED -$58.94 (-0.70%) via trailing stop** | — | **FILLED** (a55a3db6) at $419.363 ~12:08 PM ET Jun 5 ✓ |
| ~~AVGO~~ | ~~20~~ | ~~$417.366~~ | — | — | **CLOSED -$175.12 (-2.1%) via trailing stop** | — | **FILLED** (a8e344f4) at $408.61 Jun 4 ✓ |
| ~~AMZN~~ | ~~30~~ | ~~$269.13~~ | — | — | **CLOSED -$597.60 (-7.39%) per -7% rule** | — | **CANCELED** (bbcd70fa) ✓ |

## Performance vs S&P 500

| Period | Bull | SPY | Difference |
|--------|------|-----|------------|
| Inception (2026-05-21) | $100,000.00 | $739.44 | — |
| **Close (2026-06-16)** | **$99,209.83** | **$751.01 (close, +1.56% since inception)** | **Bull TRAILS SPY ~2.35pp** |
| **Midday (2026-06-16)** | **$99,260.78** | **$752.76 (~12:32 ET, +1.80% since inception)** | **Bull TRAILS SPY ~2.54pp** |
| **Open (2026-06-16)** | **$99,248.66** | **$755.20 (~09:36 ET, +2.13% since inception)** | **Bull TRAILS SPY ~2.88pp** |
| **Pre-mkt (2026-06-16)** | **$98,901.57** | **~$754.87–$755.05 (latest quote)** | **Bull TRAILS SPY ~3.19pp** |
| **Close (2026-06-15)** | **$98,897.57** | **$754.04 (close, +1.76% from Jun 12 close)** | **Bull TRAILS SPY ~3.07pp** |
| **Midday (2026-06-15)** | **$98,908.11** | **$756.33 (~12:32 ET, +2.01% from Jun 12 close)** | **Bull TRAILS SPY ~3.37pp** |
| **Open (2026-06-15)** | **$98,656.79** | **$753.29 (~09:37 ET, +1.57% from Jun 12 close)** | **Bull TRAILS SPY ~3.21pp** |
| **Pre-mkt (2026-06-15)** | **$98,907.25** | **~$751.37 (pre-mkt, +1.31% from Jun 12)** | **Bull TRAILS SPY ~2.70pp** |
| Close (2026-05-29) | $101,263.22 | $756.65 | — |
| Close (2026-06-01) | $101,368.53 | $758.66 | — |
| Pre-mkt (2026-06-02) | $101,700.20 | $756.75 | — |
| Open (2026-06-02) | $101,399.62 | $757.29 | — |
| Midday (2026-06-02) | $101,428.32 | $759.23 | — |
| Close (2026-06-02) | $101,117.57 | $759.47 | — |
| Pre-mkt (2026-06-03) | $101,380.98 | ~$760.00 | — |
| Open (2026-06-03) | $100,990.59 | $757.72 | — |
| Midday (2026-06-03) | $100,783.39 | $754.33 | — |
| Close (2026-06-03) | $100,950.97 | $754.80 | — |
| Pre-mkt (2026-06-04) | $99,461.64 | ~$757 est | — |
| Open (2026-06-04) | $99,774.35 | $752.69 | — |
| Midday (2026-06-04) | $100,024.52 | $756.31 | **-2.26%** |
| Close (2026-06-04) | $99,820.82 | $757.55 | **-2.63%** |
| Pre-mkt (2026-06-05) | $99,844.00 | ~$757 est | — |
| Open (2026-06-05) | $99,808.65 | ~$757 est | **~-2.64%** |
| Midday (2026-06-05) | $99,370.92 | ~$757 est | ~-3.08% |
| Close (2026-06-05) | $98,916.92 | $737.45 | **-1.30%** |
| Pre-mkt (2026-06-08) | $99,157.77 | $742.81 | -1.30% |
| Open (2026-06-08) | $99,057.34 | ~$742.81 | ~-1.41% |
| Midday (2026-06-08) | $99,115.29 | ~$742 est | ~-1.35% est |
| Close (2026-06-08) | $99,019.89 | $739.30 | **-0.96%** |
| Pre-mkt (2026-06-09) | $99,135.90 | ~$744 est (+0.71% futures) | ~-1.49% est |
| Open (2026-06-09) | $99,222.15 | ~$747 est (+1.04% from Jun 8 close) | ~-1.82% est |
| Midday (2026-06-09) | $98,734.63 | ~$747 est | ~-2.03% est |
| Close (2026-06-09) | $98,817.64 | $733.06 | **-0.32%** |
| Pre-mkt (2026-06-10) | $98,568.84 | ~$729.6 est (futures −0.47%) | ~−0.10% est |
| Open (2026-06-10) | $98,754.29 | ~$734.26 (SPY −0.38% from Jun 9) | ~−0.93% est |
| Midday (2026-06-10) | $98,428.62 | ~$728 est (market weak today) | ~−1.28% est |
| **Close (2026-06-10)** | **$98,315.05** | **$724.73** | **+0.30%** |
| **Pre-mkt (2026-06-11)** | **$98,438.13** | **~$730 est (+0.78% futures)** | **~-0.34% est** |
| **Open (2026-06-11)** | **$98,361.27** | **~$730 est** | **~+0.35% est** |
| **Midday (2026-06-11)** | **$98,706.36** | **~$730 est** | **~+0.70% est** |
| **Close (2026-06-11)** | **$98,825.30** | **$737.62 (est.)** | **-0.93%** |
| **Pre-mkt (2026-06-12)** | **$98,949.03** | **~$740.65 (est. +0.41% futures)** | **~-1.21%** |
| **Open (2026-06-12)** | **$98,996.63** | **$739.08 (live ~09:36 ET)** | **~-0.95%** |
| **Midday (2026-06-12)** | **$98,808.86** | **~$740.44 (live ~12:32 ET)** | **~-1.33%** |
| **Close (2026-06-12)** | **$98,696.00** | **$741.02 (est. close)** | **-1.52%** |
| **Since inception (2026-05-21)** | **-1.10%** | **+1.97% ($754.04 actual Jun 15 close)** | **Bull TRAILS SPY ~3.07pp** |
| **Week 4 (Jun 8–12)** | **-0.22%** | **+0.58%** | **Bull lagged SPY 0.81pp** |

## Notes

**Close June 16, 2026 — EOD summary (15:51 ET):**
- **Market context:** FOMC Day 1 began with markets little changed. SpaceX surged 20% on an AI deal announcement; housing starts fell 15.4% unexpectedly. S&P 500 flat to slightly up on the session; SPY closed $751.01 (−0.50% vs Jun 15 close $754.75) on FOMC caution dampening risk appetite. Bull outperformed: V +2.71% and VST +3.66% (continued Helix momentum) more than offset LLY −0.63% (mild rotation), driving Bull +0.35% vs SPY −0.50% = +0.85pp relative outperformance today.
- **LLY** ⭐ $1,122.2175 (+2.62% from entry, −0.63% today). Mild pullback from session high — FOMC caution weighing on healthcare defensives; no LLY-specific negative catalyst. Medicare Bridge July 1 in 15 days. Buffer $57.76 (5.14%) ✓. HOLD.
- **V** $332.61 (+2.79% from entry, +2.71% today). ⭐ **Stop HWM ratcheted to $333.08** (from $332.00 midday, from $326.905 market-open). Stop $299.772. Best day since entry. Financials outperforming on FOMC rate-hold certainty. OpenAI/stablecoin thesis intact. Buffer $32.84 (9.87%) ✓. HOLD.
- **VST** ⭐⭐ $159.14 (+6.94% from entry, +3.66% today). **Stop HWM ratcheted to $161.48** (from $160.2599 midday, from $158.49 market-open). Stop $145.332. Third consecutive day of strong gains — Helix Digital Infrastructure thesis. Dividend ex-date June 22 in 6 days (USD 9.16 credit for 40sh). Buffer $13.81 (8.68%) ✓. HOLD.
- **FOMC gate:** No new positions before Wednesday June 18, 2 PM ET. Day 1 complete; announcement tomorrow afternoon.
- **Stop audit:** 4/4 confirmed ✓ (V HWM ratcheted $332.00→$333.08; VST HWM ratcheted $160.2599→$161.48 during afternoon session)

**Since inception performance (EOD June 16):**
- Bull: $100,000 → $99,209.83 = **−0.790%**
- SPY: $739.44 → $751.01 = **+1.564%**
- **Gap EOD June 16: Bull TRAILS SPY by ~2.35pp** (best gap reading since June 12; narrowed from 3.07pp at EOD Jun 15 and 2.54pp at midday today)
- Today: Bull +0.351% vs SPY −0.495% = **+0.846pp outperformance today** — V and VST driving vs SPY declining on FOMC caution
- Note: After SPY ex-div June 18 ($1.76/sh), SPY total-return anchor adjusts to $741.20, narrowing reported gap by ~0.238pp.

**Race scoreboard (EOD June 16):**
- Bull: **−0.790%** (since May 21, USD 100K start)
- AGGRO: **~−3.94% est** (midday $96,060.12 vs $100K inception June 4; FOMC-day AI-tech softness — MSFT/AVGO under pressure)
- SPY vs Bull inception: **+1.564%** (since May 21, $739.44 anchor)
- Bull leads AGGRO by ~3.15pp (est.).

**Trailing stop status (EOD June 16 — confirmed via Alpaca open orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $57.76 = 5.14%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$333.08** ⬆️ RATCHETED (from $332.00 midday), stop **$299.772** ⬆️ ✓ (buffer $32.84 = 9.87%)
- VST (c4c200a5): 40sh — HWM **$161.48** ⬆️ RATCHETED (from $160.2599 midday), stop **$145.332** ⬆️ ✓ (buffer $13.81 = 8.68%)

**Sector exposure (EOD June 16):**
- Healthcare (LLY): $11,222.175 = 11.31%
- Financials (V): $7,317.42 = 7.38%
- Energy/Utilities (VST): $6,365.60 = 6.41%
- Cash: $74,304.63 = 74.90%
- No sector above 60% cap ✓

**Week of June 16 — new position slots:**
- **Slot 1:** OPEN — FOMC gate through Wednesday June 18 2 PM ET → then: LRCX if ATR normalizes ≤3%
- **Slot 2:** OPEN — post-FOMC: NVDA if basing above $205
- **Slot 3:** OPEN — post-FOMC: PWR (Quanta Services) after conference volatility settles

**Upcoming catalysts:**
- **FOMC announcement Wednesday June 18 2 PM ET** — dot plot key; FOMC gate active through tomorrow afternoon
- **SPY dividend ex-date June 18** ($1.76/sh — SPY total-return anchor → $741.20 post-June 18)
- **VST dividend ex-date June 22** (USD 9.16 credit for 40sh — 6 days)
- **LLY Medicare GLP-1 Bridge effective July 1** (15 days — thesis review_by date)
- **VST thesis review_by July 7** (21 days)
- **V Q3 FY26 earnings July 28** (42 days — thesis review_by date)

---

**Midday June 16, 2026 (~12:32 ET):**
- **Market context:** SPY $752.76 — slight pullback today (−0.26% from Jun 15 close $754.75) on FOMC Day 1 caution. Bull outperforming: V +2.18% and VST +3.85% intraday offset LLY +0.04%. Bull +0.40% today vs SPY −0.26% = +0.66% relative outperformance. FOMC gate remains active — no new positions before June 18, 2 PM ET.
- **LLY** ⭐ $1,129.785 (+3.31% from entry, +0.04% today). Essentially flat — slight pullback from morning high. Medicare Bridge July 1 in 15 days. Thesis STRONGEST. HOLD.
- **V** $330.89 (+2.26% from entry, +2.18% today). **Stop auto-ratcheted to HWM $332.00** (from $326.905 at market-open), stop $298.80. Financials outperforming on FOMC rate-hold certainty. OpenAI/stablecoin thesis intact. HOLD.
- **VST** ⭐⭐ $159.435 (+7.14% from entry, +3.85% today). **Stop auto-ratcheted to HWM $160.2599** (from $158.49 at market-open), stop $144.234. Dividend ex-date June 22 in 6 days (USD 9.16 credit for 40sh). Helix thesis ongoing. HOLD.
- **No cuts, no tightening** — all positions within guardrails.
- **FOMC gate:** No new positions before Wednesday June 18, 2 PM ET.
- **Stop audit:** 4/4 confirmed ✓ (V and VST stops auto-ratcheted to new HWMs intraday)

**Since inception performance (midday June 16):**
- Bull: $100,000 → $99,260.78 = **−0.74%**
- SPY: $739.44 → $752.76 = **+1.80%**
- **Gap midday June 16: Bull TRAILS SPY by ~2.54pp** (narrowing from 2.88pp at market-open and 3.07pp at EOD Jun 15)
- Today: Bull +0.40% vs SPY −0.26% = **+0.66pp outperformance today**
- Note: After SPY ex-div June 18 ($1.76/sh), SPY total-return anchor adjusts to $741.20, narrowing the reported gap by ~0.24pp.

**Trailing stop status (midday June 16 — confirmed via Alpaca open orders ~12:32 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $65.33 = 5.78%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$332.00** ⬆️ AUTO-RATCHETED (from $326.905 market-open), stop **$298.80** ⬆️ ✓ (buffer $32.09 = 9.70%)
- VST (c4c200a5): 40sh — HWM **$160.2599** ⬆️ AUTO-RATCHETED (from $158.49 market-open), stop **$144.234** ⬆️ ✓ (buffer $15.20 = 9.54%)

**Sector exposure (midday June 16):**
- Healthcare (LLY): $11,297.85 = 11.38%
- Financials (V): $7,279.58 = 7.33%
- Energy/Utilities (VST): $6,377.40 = 6.42%
- Cash: $74,304.63 = 74.87%
- No sector above 60% cap ✓

**Week of June 16 — new position slots:**
- **Slot 1:** OPEN — FOMC gate through Wednesday June 18 2 PM ET → then: LRCX if ATR normalizes ≤3%
- **Slot 2:** OPEN — post-FOMC: NVDA if basing above $205
- **Slot 3:** OPEN — post-FOMC: PWR (Quanta Services) after conference volatility settles

**Upcoming catalysts:**
- **FOMC June 16–17 (TODAY/TOMORROW), announcement June 18 2 PM ET** — dot plot key; no new positions until after
- **SPY dividend ex-date June 18** ($1.76/sh — SPY total-return anchor → $741.20 post-June 18)
- **VST dividend ex-date June 22** (USD 9.16 credit for 40sh — 6 days)
- **LLY Medicare GLP-1 Bridge effective July 1** (15 days — thesis review_by date)
- **VST thesis review_by July 7** (21 days)
- **V Q3 FY26 earnings July 28** (42 days — thesis review_by date)

---

**Market-open June 16, 2026 (~09:36 ET):**
- **Market context:** SPY $755.20 — market opening firm despite FOMC start (June 16–17). All 3 positions up intraday: LLY +1.27%, V +0.73%, VST +3.03%. VST surging on continued Helix Digital Infrastructure momentum. FOMC gate remains active — no new positions before June 18, 2 PM ET.
- **LLY** ⭐ $1,143.695 (+4.59% from entry, +1.27% today). Medicare Bridge July 1 in 15 days. Thesis STRONGEST. HOLD.
- **V** $326.18 (+0.81% from entry, +0.73% today). Stop ratcheted to HWM $326.905. OpenAI/stablecoin thesis intact. HOLD.
- **VST** ⭐⭐ $158.17 (+6.29% from entry, +3.03% today). Stop ratcheted to HWM $158.49, stop $142.641 — significant ratchet from $155.43/$139.887. Dividend ex-date June 22 in 6 days (USD 9.16 credit). Helix thesis ongoing. HOLD.
- **FOMC gate:** No new positions before Wednesday June 18, 2 PM ET.
- **Stop audit:** 4/4 confirmed ✓ (V and VST stops ratcheted to new HWMs)

**Since inception performance (market-open June 16):**
- Bull: $100,000 → $99,248.66 = **−0.75%**
- SPY: $739.44 → $755.20 = **+2.13%**
- **Gap open June 16: Bull TRAILS SPY by ~2.88pp** (gap narrowing from −3.07pp at EOD June 15)
- Note: After SPY ex-div June 18 ($1.76/sh), SPY total-return anchor adjusts to $741.20, narrowing the reported gap by ~0.24pp.

**Trailing stop status (market-open June 16 — confirmed via Alpaca open orders ~09:36 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $79.24 = 6.93%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$326.905** ⬆️ RATCHETED (from $326.435), stop **$294.2145** ⬆️ ✓ (buffer $31.97 = 9.80%)
- VST (c4c200a5): 40sh — HWM **$158.49** ⬆️ RATCHETED (from $155.43), stop **$142.641** ⬆️ ✓ (buffer $15.53 = 9.82%)

**Sector exposure (market-open June 16):**
- Healthcare (LLY): $11,436.95 = 11.52%
- Financials (V): $7,175.96 = 7.23%
- Energy/Utilities (VST): $6,326.80 = 6.38%
- Cash: $74,304.63 = 74.87%
- No sector above 60% cap ✓

**Week of June 16 — new position slots:**
- **Slot 1:** OPEN — FOMC gate through Wednesday June 18 2 PM ET → then: LRCX if ATR normalizes ≤3%
- **Slot 2:** OPEN — post-FOMC: NVDA if basing above $205
- **Slot 3:** OPEN — post-FOMC: PWR (Quanta Services) after conference volatility settles

**Upcoming catalysts:**
- **FOMC June 16–17 (TODAY/TOMORROW), announcement June 18 2 PM ET** — dot plot key; no new positions until after
- **SPY dividend ex-date June 18** ($1.76/sh — SPY total-return anchor → $741.20 post-June 18)
- **VST dividend ex-date June 22** (USD 9.16 credit for 40sh — 6 days)
- **LLY Medicare GLP-1 Bridge effective July 1** (15 days — thesis review_by date)
- **VST thesis review_by July 7** (21 days)
- **V Q3 FY26 earnings July 28** (42 days — thesis review_by date)

---

**Close June 15, 2026 — EOD summary (15:51 ET):**
- **Market context:** US-Iran interim deal to reopen Strait of Hormuz drove S&P 500 +1.7% (Nasdaq +2.8%, Dow +1.1%). WTI oil fell 5% to ~$80/bbl. SpaceX (SPCX) +5% Day 2. Energy sector tumbled broadly, but VST outperformed +4.61% on Helix/nuclear thesis (non-correlated to oil price). Iran deal constructive for equities; slightly bearish for traditional energy but neutral-to-positive for nuclear. All three Bull positions: LLY −0.55% (sector rotation), V +0.55% (financials recovering), VST +4.61% (Helix thesis confirmed). Context is supportive for all three current theses.
- **LLY** ⭐ $1,126.76 (+3.04% from entry). Intraday softness (−0.55%) = broad rotation from defensives to cyclicals on Iran deal; no LLY-specific negative catalyst. Medicare GLP-1 Bridge July 1 in 16 days. Stop buffer $62.30 (5.53%) ✓. HOLD.
- **V** $324.18 (+0.19% from entry). Financials +0.55% intraday. Stop ratcheted to HWM $326.435 — protection improving. OpenAI/stablecoin thesis intact. Stop buffer $30.39 (9.37%) ✓. HOLD.
- **VST** ⭐⭐ $154.84 (+4.05% from entry). Outstanding +4.61% day despite energy sector selloff — nuclear/Helix thesis is non-correlated to oil. Stop ratcheted: HWM $154.74 → $155.43, stop $139.266 → $139.887 ✓. Dividend ex-date June 22 in 7 days (USD 9.16 credit). Stop buffer $14.95 (9.66%) ✓. HOLD.
- **FOMC gate:** No new positions before Wednesday June 18, 2 PM ET.

**Since inception performance (EOD June 15):**
- Bull: $100,000 → $98,897.57 = **−1.10%**
- SPY: $739.44 → $754.04 = **+1.97%** (price only; ex-div $1.76 on June 18 not yet counted)
- **Gap EOD June 15: Bull TRAILS SPY by ~3.07pp** (75% cash limits capture during SPY's +1.76% Iran-deal day)
- Note: After June 18 SPY ex-div, SPY total return anchor adjusts by +0.238pp (SPY = $741.20 effective anchor). This will narrow the reported gap slightly.

**Race scoreboard (EOD June 15):**
- Bull: **−1.10%** (since May 21, USD 100K start)
- AGGRO: **~−3.0% est** (midday $97,008 vs $100K inception June 4; last EOD June 12: −5.95%) — AGGRO recovered significantly on Iran deal risk-on
- SPY vs Bull inception: **+1.97%** (since May 21)
- Bull leads AGGRO by ~1.9pp (est.).

**Trailing stop status (EOD June 15 — confirmed via Alpaca open orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $62.30 = 5.53%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$326.435** ⬆️ RATCHETED (from $326.29 midday), stop **$293.7915** ⬆️ ✓ (buffer $30.39 = 9.37%)
- VST (c4c200a5): 40sh — HWM **$155.43** ⬆️ RATCHETED (from $154.74 midday), stop **$139.887** ⬆️ ✓ (buffer $14.95 = 9.66%)

**Sector exposure (EOD June 15):**
- Healthcare (LLY): $11,267.60 = 11.39%
- Financials (V): $7,131.96 = 7.21%
- Energy/Utilities (VST): $6,193.60 = 6.26%
- Cash: $74,304.63 = 75.14%
- No sector above 60% cap ✓

**Week of June 15 — new position slots:**
- **Slot 1:** OPEN — FOMC gate through Wednesday June 18 2 PM ET → then: LRCX if ATR ≤3%
- **Slot 2:** OPEN — post-FOMC: NVDA if basing above $205
- **Slot 3:** OPEN — post-FOMC: PWR (Quanta Services) research

**Upcoming catalysts:**
- **FOMC June 16–17, announcement June 18 2 PM ET** — hard gate on new positions; dot plot key
- **SPY dividend ex-date June 18** ($1.76/sh — add to benchmark total-return anchor post-June 18: $739.44 + $1.76 = $741.20 adjusted anchor)
- **VST dividend ex-date June 22** (USD 9.16 credit for 40sh — 7 days)
- **LLY Medicare GLP-1 Bridge effective July 1** (16 days — thesis review_by date)
- **VST thesis review_by July 7** (22 days)
- **V Q3 FY26 earnings July 28** (43 days — thesis review_by date)

---

**Midday June 15, 2026 (~12:32 ET):**
- **Market context:** SPY $756.33 mid-session (vs $741.67 Jun 12 close = +1.97% today; +2.28% since inception). Broad risk-on continues ahead of FOMC. FOMC gate remains active: no new positions before Wednesday June 18, 2 PM ET.
- **LLY** ⭐ $1,127.02 (+3.06% from entry, −0.53% intraday from $1,133). Mild softness = broad market rotation; no LLY-specific negative catalyst. Employer GLP-1 coverage concern = 2027 headwind only. HOLD. Stop buffer $62.56 (5.55%) ✓.
- **V** $326.04 (+0.76% from entry, +1.13% intraday). **Stop ratcheted to HWM $326.29.** OpenAI/stablecoin thesis intact. HOLD. Stop buffer $32.38 (9.93%) ✓.
- **VST** ⭐⭐ $154.01 (+3.49% from entry, +4.05% intraday). **Stop ratcheted: HWM $153.21 → $154.74, stop $137.889 → $139.266.** Dividend ex-date June 22 (7 days, USD 9.16 credit). Helix thesis intact. HOLD. Stop buffer $14.74 (9.57%) ✓.
- **Breaking-news gate:** All 3 positions clear — no thesis-breaking events. ✓
- **FOMC gate:** No new positions before Wednesday June 18, 2 PM ET.
- **Sector exposure (midday June 15):**
  - Healthcare (LLY): $11,270.20 = 11.39%
  - Financials (V): $7,172.88 = 7.25%
  - Energy/Utilities (VST): $6,160.40 = 6.23%
  - Cash: $74,304.63 = 75.1%
  - No sector above 60% cap ✓
- **Since inception (2026-05-21):** Bull −1.09% ($100,000 → $98,908.11) vs SPY +2.28% ($756.33) = **Bull TRAILS SPY by ~3.37pp** (SPY continued rally today; 75% cash limits capture; FOMC gate)
- **Race scoreboard (midday June 15):**
  - Bull: **−1.09%** (since May 21)
  - AGGRO: **~−6.04%** (last known EOD June 12)
  - SPY: **+2.28%** (since May 21, midday June 15)
  - Bull leads AGGRO by ~4.95pp.

**Trailing stop status (midday June 15 — confirmed via Alpaca open orders ~12:32 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $62.56 = 5.55%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$326.29** ⬆️ RATCHETED (from $325.93), stop **$293.661** ⬆️ (from $293.337) ✓ (buffer $32.38 = 9.93%)
- VST (c4c200a5): 40sh — HWM **$154.74** ⬆️ RATCHETED (from $153.21), stop **$139.266** ⬆️ (from $137.889) ✓ (buffer $14.74 = 9.57%)

**Week of June 15 — new position slots:**
- **Slot 1:** OPEN — FOMC gate through Wednesday June 18 2 PM ET
- **Slot 2:** OPEN — post-FOMC: NVDA if basing above $205
- **Slot 3:** OPEN — post-FOMC: PWR (Quanta Services) research

**Market-open June 15, 2026 (~09:36 ET):**
- **Market context:** SPY +1.57% today ($741.67 → $753.29) — continued Iran/US peace deal optimism + risk-on tone ahead of FOMC. FOMC gate remains active: no new positions before Wednesday June 18, 2 PM ET.
- **LLY** ⭐ $1,116.47 (+2.10% from entry, −1.46% intraday from $1,133). Session range $1,130.19–$1,169.99 (intraday pullback early; no LLY-specific negative catalyst). Employer GLP-1 coverage concern = 2027 headwind only. HOLD. Stop buffer $52.01 (4.66%) ✓.
- **V** $323.53 (−0.01% from entry, +0.35% intraday). Swipe fee settlement preliminary approval = positive (regulatory overhang removed). OpenAI thesis intact. HOLD. Stop buffer $30.19 (9.33%) ✓.
- **VST** ⭐⭐ $151.92 (+2.09% from entry, +2.64% intraday). **Stop ratcheted at open:** HWM $150.50 → $153.21, stop $135.45 → $137.889. Dividend ex-date June 22 (7 days, USD 9.16 credit). Helix thesis intact. HOLD. Stop buffer $14.03 (9.23%) ✓.
- **Breaking-news gate:** All 3 positions clear — no thesis-breaking events. ✓
- **FOMC gate:** No new positions before Wednesday June 18, 2 PM ET.
- **Sector exposure (market-open June 15):**
  - Healthcare (LLY): $11,164.70 = 11.32%
  - Financials (V): $7,117.66 = 7.21%
  - Energy/Utilities (VST): $6,076.80 = 6.16%
  - Cash: $74,304.63 = 75.3%
  - No sector above 60% cap ✓
- **Since inception (2026-05-21):** Bull −1.34% ($100,000 → $98,656.79) vs SPY +1.87% ($753.29) = **Bull TRAILS SPY by ~3.21pp** (SPY +1.57% intraday; LLY −1.46% intraday; 75% cash limits capture)
- **Race scoreboard (market-open June 15):**
  - Bull: **−1.34%** (since May 21)
  - AGGRO: **~−6.04%** (last known EOD June 12)
  - SPY: **+1.87%** (since May 21, current June 15 open)
  - Bull leads AGGRO by ~4.70pp.

**Trailing stop status (market-open June 15 — confirmed via Alpaca open orders ~09:36 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $52.01 = 4.66%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$325.93**, stop **$293.337** ✓ (buffer $30.19 = 9.33%)
- VST (c4c200a5): 40sh — HWM **$153.21** ⬆️ RATCHETED (from $150.50), stop **$137.889** ⬆️ (from $135.45) ✓ (buffer $14.03 = 9.23%)

**Week of June 15 — new position slots:**
- **Slot 1:** OPEN — FOMC gate through Wednesday June 18 2 PM ET
- **Slot 2:** OPEN — post-FOMC: NVDA if basing above $205
- **Slot 3:** OPEN — post-FOMC: PWR (Quanta Services) research

**Pre-market June 15, 2026 (~08:03 ET):**
- **Market context:** SPY pre-market +1.31% ($741.67 → $751.37) driven by continued Iran/US peace deal optimism and broad risk-on tone. FOMC June 16–17 (Kevin Warsh's first meeting with dot plot); announcement June 18 2 PM ET. Hard gate: no new positions before Wednesday afternoon. Hawkish dot plot risk — 70% probability of at least one year-end rate hike per CME FedWatch.
- **LLY** ⭐ $1,140.47 (+4.29% from entry, +0.66% today). Employer coverage concern (10% of employers dropping in 2027) is a 2027 headwind — does NOT invalidate July 1 Medicare Bridge. HOLD. Conviction: A.
- **V** $323.10 (−0.15% from entry, +0.22% today). Thesis intact; financials sector lagging in tech rallies. HOLD. Conviction: B.
- **VST** ⭐⭐ $152.24 (+2.31% from entry, +2.85% today). Pre-market breakout above prior HWM $150.50. Stop expected to ratchet to ~$137.02 at market open. Dividend ex-date June 22 (7 days, USD 9.16 credit). Helix thesis intact. HOLD. Conviction: A.
- **Monday conviction review:** LLY A, V B, VST A. No C positions. No mandatory trims.
- **FOMC gate:** No new positions before Wednesday June 18, 2 PM ET.
- **Sector exposure (pre-market June 15):**
  - Healthcare (LLY): $11,404.70 = 11.53%
  - Financials (V): $7,108.20 = 7.19%
  - Energy/Utilities (VST): $6,089.72 = 6.16%
  - Cash: $74,304.63 = 75.12%
  - No sector above 60% cap ✓
- **Since inception (2026-05-21):** Bull −1.09% ($100,000 → $98,907.25) vs SPY +1.61% (~$751.37 pre-mkt) = **Bull TRAILS SPY by ~2.70pp** (gap widened due to SPY's strong +1.31% pre-market rally; 75% cash limits upside capture)
- **Race scoreboard (pre-market June 15):**
  - Bull: **−1.09%** (since May 21)
  - AGGRO: **~−6.04%** (last known EOD June 12)
  - SPY: **+1.61%** (since May 21, pre-mkt June 15)
  - Bull leads AGGRO by ~4.95pp.

**Trailing stop status (pre-market June 15 — confirmed active):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $76.01 = 6.67%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$325.93**, stop **$293.337** ✓ (buffer $29.76 = 9.21%)
- VST (c4c200a5): 40sh — HWM **$150.50** (→ ~$152.24 expected ratchet at open), stop **$135.45** (→ ~$137.02 after ratchet) ✓ (buffer ~$15.22 = 10.0% est.)

**Week of June 15 — new position slots:**
- **Slot 1:** OPEN — FOMC gate through Wednesday June 18 2 PM ET
- **Slot 2:** OPEN — post-FOMC: NVDA if basing above $205
- **Slot 3:** OPEN — post-FOMC: PWR (Quanta Services) research

**Close June 12, 2026 — EOD summary (15:51 ET):**
- **Market context:** SpaceX (SPCX) debuted today at $135/sh, surged ~19% to ~$161 — largest IPO in history ($1.77T). Tech capital rotation: S&P 500 +0.34%, Dow +0.40%, Nasdaq 100 −0.5%. Amazon −2.17%, Apple −1.95% (SpaceX liquidity absorption). Iran/US peace deal advancing; oil −2% to ~$85/bbl — direct VST tailwind. Bull's positions: LLY −1.95% intraday (rotation, not thesis-specific), V +0.99% (financials resilient), VST +1.09% (oil decline tailwind). Today's context is neutral-to-supportive for all three current theses.
- **LLY** ⭐ $1,138.355 (+4.10% from entry). Intraday softness (−1.95%) = SpaceX rotation, no LLY-specific catalyst. Medicare GLP-1 Bridge July 1 in 19 days. Stop buffer $73.90 (6.49%) ✓. HOLD.
- **V** $322.21 (−0.42% from entry, +0.99% intraday). Financials resilient. Stop buffer $28.87 (8.96%) ✓. OpenAI/stablecoin thesis intact. HOLD.
- **VST** ⭐⭐ $147.98 (−0.56% from entry, +1.09% intraday). Oil −2% on Iran peace. Helix Digital Infrastructure thesis intact. Dividend ex-date June 22 in 10 days (USD 9.20 for 40sh). Stop buffer $12.53 (8.47%) ✓. HOLD.
- **Quarterly SPY dividend (June quarter):** Q2 2026 SPY ex-date June 18 ($1.76/sh). Cumulative dividends since inception: $0.00. After June 18, SPY total return = price return + 0.238pp. Noted for benchmarking accuracy.

**Since inception performance (EOD June 12):**
- Bull: $100,000 → $98,696.00 = **-1.304%**
- SPY: $739.44 → $741.02 (est.) = **+0.213%**
- **Gap EOD June 12: Bull TRAILS SPY by ~1.52pp** (75% cash limits upside capture; SpaceX IPO rotation today)

**Race scoreboard:**
- Bull: **-1.30%** (since May 21)
- AGGRO: **~-6.04%** (since Jun 4, midday June 12 estimate; last full EOD -5.84% June 11)
- SPY: **+0.21%** (since May 21, Bull's anchor)
- Bull leads AGGRO by ~4.74pp.

**Trailing stop status (EOD June 12 — confirmed via live Alpaca open orders ~15:51 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $73.90 = 6.49%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$325.93**, stop **$293.337** ✓ (buffer $28.87 = 8.96%)
- VST (c4c200a5): 40sh — HWM **$150.50**, stop **$135.45** ✓ (buffer $12.53 = 8.47%)
- ~~META (4ea07e91)~~: FILLED at $578.00 Jun 10 ✓

**Week of June 8 — new position slots (CLOSED — all slots resolved):**
- **Slot 1:** VST — **BOUGHT** 40sh @ $148.81 ✓ (June 9)
- **Slot 2:** V (Visa) — **BOUGHT** 22sh @ $323.57 ✓ (June 10)
- **Slot 3:** **UNUSED (deliberate)** — LRCX ATR ~10% disqualified entry all week; Friday weekend risk. Week of June 16+: 3 fresh slots.

**Sector exposure (EOD June 12):**
- Healthcare (LLY): $11,383.55 = 11.54%
- Financials (V): $7,088.62 = 7.18%
- Energy/Utilities (VST): $5,919.20 = 6.00%
- Cash: $74,304.63 = 75.29%
- No sector above 60% cap ✓

**Upcoming catalysts:**
- **VST Helix Digital Infrastructure** (KKR+NVIDIA+Kuwait) — ongoing thesis upgrade; VST is preferred power provider for USD 10B+ AI infra platform
- **SPY ex-dividend June 18, 2026** — $1.76/sh (benchmark total-return adjustment +0.238pp to SPY)
- **VST dividend ex-date June 22** (USD 9.20 credit for 40 shares — 10 days)
- **LLY Medicare GLP-1 Bridge program effective July 1** (19 days — thesis review_by date)
- **VST thesis review_by July 7** (25 days)
- **V Q3 FY26 earnings July 28** (46 days — thesis review_by date)
- **LLY Q2 FY26 earnings ~August 5** (54 days)
- **VST Q2 FY26 earnings August 6** (55 days)
- **Weekly review tonight 4:30 PM** — week of June 8 review
- **LRCX re-evaluation June 16+** — Slot 1 of 3 next week (ATR must normalize to ≤3%, chart must base)

---

**Midday June 12, 2026 — Friday (12:32 ET):**
- **Market context:** SPY ~$740.44 (+0.37% from June 11 close $737.67) — Iran peace deal optimism continuing. Clean midday — all 3 positions within guardrails. No action taken.
- **LLY** ⭐ $1,143.665 (+4.58% from entry). Mild intraday softness (-1.49% from yesterday close $1,160.95) on broader market. Medicare GLP-1 Bridge July 1 in 19 days. Thesis STRONGEST. Stop buffer $79.21 (6.93%) ✓.
- **V** $324.495 (+0.29% from entry, +1.71% intraday). **STOP RATCHETED:** V hit HWM $325.93 intraday — stop auto-ratcheted from $292.959 to $293.337 ✓. Buffer $31.16 (9.61%) — best of the 3. HOLD.
- **VST** ⭐⭐ $148.125 (-0.46% from entry, +1.19% intraday). Helix Digital Infrastructure (KKR+NVIDIA preferred power partner) thesis. Dividend ex-date June 22 in 10 days (USD 9.20 for 40sh). Stop buffer $12.68 (8.56%) ✓. HOLD.

**Since inception performance (midday June 12 — live Alpaca data ~12:32 ET):**
- Bull: $100,000 → $98,808.86 = **-1.191%**
- SPY: $739.44 → $740.44 (live) = **+0.135%**
- **Gap midday June 12: Bull TRAILS SPY by ~1.33pp** (75% cash limits upside capture)

**Race scoreboard:**
- Bull: **-1.191%** (since May 21)
- AGGRO: **~-7.0%** (since Jun 4, last known estimate)
- SPY: **+0.135%** (since May 21, live Jun 12 mid)
- Bull leads AGGRO by ~5.8pp.

**Trailing stop status (midday June 12 — confirmed via live Alpaca open orders ~12:32 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $79.21 = 6.93%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$325.93** ⬆️, stop **$293.337** ⬆️ ✓ (buffer $31.16 = 9.61%) — RATCHETED
- VST (c4c200a5): 40sh — HWM **$150.50**, stop **$135.45** ✓ (buffer $12.68 = 8.56%)
- ~~META (4ea07e91)~~: FILLED at $578.00 Jun 10 ✓

**Week of June 8 — new position slots (EXPIRED today June 12):**
- **Slot 1:** VST — **BOUGHT** 40sh @ $148.81 ✓ (June 9)
- **Slot 2:** V (Visa) — **BOUGHT** 22sh @ $323.57 ✓ (June 10)
- **Slot 3:** **UNUSED (deliberate)** — LRCX ATR ~10% disqualified entry all week; stock extended +19.5% in 6 sessions; Friday weekend risk. Week of June 16+: 3 fresh slots.

**Sector exposure (midday June 12):**
- Healthcare (LLY): $11,436.65 = 11.57%
- Financials (V): $7,138.89 = 7.22%
- Energy/Utilities (VST): $5,925.00 = 5.99%
- Cash: $74,304.63 = 75.1%
- No sector above 60% cap ✓

**Upcoming catalysts:**
- **VST Helix Digital Infrastructure** (KKR+NVIDIA+Kuwait) — ongoing thesis upgrade; VST is preferred power provider for USD 10B+ AI infra platform
- **VST dividend ex-date June 22** (USD 9.20 credit for 40 shares — 10 days)
- **LLY Medicare GLP-1 Bridge program effective July 1** (19 days — thesis review_by date)
- **VST thesis review_by July 7** (25 days)
- **V Q3 FY26 earnings July 28** (46 days — thesis review_by date)
- **LLY Q2 FY26 earnings ~August 5** (54 days)
- **VST Q2 FY26 earnings August 6** (55 days)
- **Weekly review today 4:30 PM** — week of June 8 review
- **LRCX re-evaluation June 16+** — Slot 1 of 3 next week (ATR must normalize to ≤3%, chart must base)

---

**Close June 10, 2026 — EOD summary (archived):**
- **Market context:** Equities fell broadly — SPY -0.71% to $727.87. Three drivers: May CPI 4.2% YoY (3-year high but matched estimate; core 2.9% benign); US-Iran military strikes escalating with near-closure of Strait of Hormuz; AI sector selloff (NVDA, Micron extended). VIX +12%. 10yr held at ~4.54% (below 4.75% trigger). Bull's 75.5% cash cushioned the day: **Bull -0.45% vs SPY -0.71% = +0.26% outperformance today**.
- **LLY** ⭐ $1,140.49 (+4.29% from avg entry $1,093.534). Both trailing stops: HWM $1,182.73, stop $1,064.457 ✓. Buffer $76.03 (6.67%). Medicare GLP-1 Bridge July 1 in 21 days. Thesis STRONGEST. Mild -0.37% today — constructive.
- **V** $323.08 (-0.15% from entry $323.57). Stop 66033918: HWM $325.51, stop $292.959 ✓. Buffer $30.12 (9.32%). Day 1 essentially at entry — mild market-correlated weakness. Payments compounder thesis intact. Review_by July 28.
- **VST** ⚠️⚠️ $138.91 (-6.65% from entry $148.81). Stop c4c200a5: HWM $150.30, stop $135.270 ✓. Buffer $3.64 (2.62%). **CRITICAL: -7% cut threshold $138.39 — VST closed only $0.52 above it.** Fell -5.00% today; broad-market selloff + Iran/oil correlation. Nuclear PPA thesis intact. Dividend ex-date June 22 (USD 9.16 credit). **Thursday pre-market: HIGHEST PRIORITY CHECK.** If VST opens below $138.39, -7% rule applies at Thursday midday.
- **~~META~~** CLOSED via trailing stop at $578.00 (11:06 AM ET June 10) — loss -$639.56 (-6.87%). Post-mortem in closed-trades.md ✓. Lesson in lessons.md ✓.

**Since inception performance (June 10 close):**
- Bull: $100,000 → $98,374.22 = **-1.63%**
- SPY: $739.44 → $727.87 = **-1.57%**
- Gap: **-0.07%** — NEAR PAR, best reading since inception. High-cash posture repeatedly paying off in down markets.

**Race scoreboard (since respective inceptions):**
- Bull: **-1.63%** (since May 21, USD 100K start)
- AGGRO: **~-6.16%** (since Jun 4, midday estimate — AGGRO close routine pending)
- SPY: **-1.57%** (from May 21)
- Bull leads AGGRO by ~4.5pp; Bull essentially at par with SPY.

**Trailing stop status (close June 10 — confirmed via live Alpaca orders ~15:52 ET):**
- LLY (d4147484): 7sh — HWM **$1,182.73**, stop **$1,064.457** ✓ (buffer $76.03 = 6.67%)
- LLY (25989fb5): 3sh — HWM **$1,182.73**, stop **$1,064.457** ✓
- V (66033918): 22sh — HWM **$325.51**, stop **$292.959** ✓ (buffer $30.12 = 9.32%)
- VST (c4c200a5): 40sh — HWM **$150.30**, stop **$135.270** ✓ (buffer $3.64 = 2.62%) ⚠️ CRITICAL
- ~~META (4ea07e91)~~: **FILLED** at $578.00 ~11:06 AM ET Jun 10 ✓

**Week of June 8 — new position slots (updated June 10 close):**
- **Slot 1:** VST — **BOUGHT** 40sh @ $148.81 ✓ (June 9)
- **Slot 2:** V (Visa) — **BOUGHT** 22sh @ $323.57 ✓ (June 10)
- **Slot 3:** LRCX — DEFER; NVDA hearing June 11 today; re-evaluate Thursday/Friday

**Sector exposure (close June 10):**
- Healthcare (LLY): $11,404.90 = 11.59%
- Financials (V): $7,107.76 = 7.22%
- Energy/Utilities (VST): $5,556.40 = 5.65%
- Cash: $74,304.65 = 75.5%
- No sector above 60% cap ✓

**Upcoming catalysts:**
- **VST ⚠️ PRIORITY THURSDAY:** If VST opens at/below $138.39, -7% rule triggers at Thursday midday. Stop $135.270 is the absolute floor.
- **NVDA Senate Banking hearing June 11 (tomorrow)** — AI semi reaction watch; affects LRCX slot 3 decision
- LLY Medicare GLP-1 Bridge program effective July 1 (21 days)
- VST dividend ex-date June 22 (USD 9.16 credit for 40 shares — if position survives stop)
- V Q3 FY26 earnings July 28 (thesis review_by date)
- VST thesis review_by July 7
