# Trade Log

_Every order placed, with its reasoning. Append-only — newest entries at the top.
The weekly new-position count is derived from this log._

<!-- Template for each entry:

## YYYY-MM-DD HH:MM ET — BUY/SELL SYMBOL
- **Action:** BUY $X notional / SELL N shares
- **Fill:** N shares @ $price (order id: ...)
- **Why:** one or two sentences of rationale
- **Stop:** 10% trailing stop placed (order id: ...) — buys only
- **Verified:** confirmed via positions/orders re-fetch

-->

_No trades yet._

## 2026-05-20 12:30 ET — MIDDAY CHECK (no action)
- **Status:** Credentials missing — `ALPACA_API_KEY_ID` and `ALPACA_API_SECRET_KEY` not set in environment.
- **Action:** None. Halted per guardrail: never trade without valid credentials.
- **Note:** Pre-market routine has also not run (strategy.md uninitialized, no positions on record). Both issues need resolution before the agent can operate.
