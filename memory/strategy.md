# Trading Strategy

**STATUS: ACTIVE**
**Initialized:** 2026-05-21

---

## Thesis

2026 is a sector-rotation year. After years of tech/AI dominance, the market has
pivoted sharply toward "real economy" sectors: Energy (Middle East oil premium
from the Iran conflict), Industrials (infrastructure, data-center power-gen
build-out), and Consumer Staples (defensive, inflation-resistant). Meanwhile
the Fed is in mild easing mode at 3.5–3.75% with a new chair (Kevin Warsh)
taking over in June, which supports equities broadly — but S&P forward PE at
~21x means valuations are stretched, so selectivity matters.

**Our edge:** own high-quality names in the sectors that are structurally
leading SPY in 2026, sized deliberately, while cutting losers quickly. We are
not trying to beat SPY by owning more of it — we are trying to own better.

---

## Universe

Eligible: US large/mid-cap stocks with market cap > $10B, price ≥ $5, highly
liquid (avg volume > 500K/day), listed on NYSE/NASDAQ. Broad sector ETFs
(XLE, XLI, XLP, XLV) may be used for diversified sector exposure.

Ineligible (per CLAUDE.md guardrails): options, penny stocks, crypto, shorts,
leveraged/margin trades, day trades.

---

## Sector Priorities (as of initialization)

| Rank | Sector | Rationale |
|------|--------|-----------|
| 1 | Energy | Best-performing sector in 2026 (+22% YTD); oil in $90s sustained by Iran/Middle East risk premium; integrated majors (CVX, XOM) have strong FCF and growing dividends |
| 2 | Industrials | +16% YTD; infrastructure spending, US re-shoring, and explosion of AI data-center power demand (CAT, HON) |
| 3 | Consumer Staples | +13% YTD; defensive against inflation and macro slowdown; WMT and COST gaining market share |
| 4 | Healthcare | Secular growth + defensive; LLY (GLP-1), MRK (Keytruda oncology), UNH (managed care, strong Q1 beat) |
| 5 | Technology | Lagging in relative 2026 rotation but quality megacap tech (MSFT) acceptable at right price |

---

## Entry Signals

Open a position when ≥ 3 of the following conditions are met:
1. **Sector tailwind** — in a top-3 sector or has a clear idiosyncratic catalyst.
2. **Earnings momentum** — beat most recent estimates OR raised guidance.
3. **Valuation not stretched** — forward PE below sector average OR justified by
   above-average growth rate (PEG < 2).
4. **Technical support** — not more than 5% below a meaningful moving average;
   not gapping down on heavy volume.
5. **Written thesis** — a clear sentence on why this name beats SPY from here.

Never open a position just because the market is going up.

---

## Sizing

- **Starter position:** 7–10% of portfolio (deliberate, conviction must grow).
- **Full position:** up to 15% after confirming thesis.
- **Hard cap:** 20% of portfolio per name (per CLAUDE.md).
- Prefer whole-share quantities to allow trailing-stop orders.
- Do not add to a losing position — add only to winners with improving thesis.

---

## Exit Signals

In priority order:
1. **Hard stop:** −10% trailing stop (set immediately after every entry).
2. **Midday rule:** close any position trading > 7% below entry price.
3. **Thesis break:** sell within the session if the reason for owning evaporates
   (e.g., guidance cut, merger collapse, sector catalyst reversal).
4. **Valuation stretched:** trim if a position grows beyond 18% of portfolio.
5. **Sector rotation:** if a sector falls out of top-3 for 3+ weeks, reduce
   exposure there and redeploy.

---

## Cash Policy

- Minimum cash: **5%** of portfolio at all times.
- Target cash in first 4 weeks: **≥ 50%** — build the portfolio gradually,
  no more than 3 new positions/week and 25%/day in new buys.
- Raise cash to ≥ 20% if: VIX spikes above 30, Fed makes a surprise hike,
  or 3+ positions trigger stops in the same week.

---

## Watchlist (initial, 2026-05-21)

| Ticker | Sector | Thesis | Price at init |
|--------|--------|--------|--------------|
| CVX | Energy | Integrated major, 39 yrs dividend growth, FCF machine at $90+ oil | $191.36 |
| XOM | Energy | Largest US integrated, Permian growth, strong FCF | $156.30 |
| CAT | Industrials | Power generation/data-center demand driving backlog, 57% YTD, still momentum | $872.78 |
| HON | Industrials | Diversified conglomerate, energy + aerospace exposure, cheaper than CAT | $217.27 |
| WMT | Consumer Staples | Market share gains, strong logistics, defensive; reasonable PE | $130.93 |
| COST | Consumer Staples | Loyal membership model, dividend raised 13%, UBS PT $1,275 | $1,073.97 |
| LLY | Healthcare | GLP-1 obesity/diabetes franchise, 37% EPS CAGR forecast, PT $1,255 consensus | $1,018.42 |
| MRK | Healthcare | Keytruda oncology, reasonable valuation vs LLY, strong pipeline | $112.97 |
| UNH | Healthcare | Managed care, Q1 beat + guidance raise, PT raised to $420–$440 | ~$404 |
| MSFT | Technology | Cloud + AI, quality anchor if tech recovers, fortress balance sheet | TBD |
| XLE | Energy ETF | Sector ETF for diversified energy exposure, liquid | TBD |

---

## Benchmark

**SPY** (SPDR S&P 500 ETF Trust). Inception price: **$741.31** (close 2026-05-20).
All performance comparisons are total-return, SPY as baseline.

---

## Rules Summary (from CLAUDE.md)

- Max 20% per position · Min 5% cash · ≤ 3 new positions/week · ≤ 25% new buys/day
- Every long entry → immediate 10% trailing stop
- Midday: close any position > 7% below entry
- No options, no shorts, no margin, no crypto, no penny stocks, no day trades
- Confirm market open before every order; verify every fill
