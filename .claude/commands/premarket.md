Run the Bull **pre-market** routine. Research and plan; do not deliberately open
or close a position. Reconciliation may repair managed protection or contain a
forbidden holding; those are the only broker mutations allowed here.

## 0. Control first, advisory lock, memory, reconciliation

1. Read `memory/control.md` **before anything else**. Invalid/missing STATUS is
   a hard stop. Acknowledge `NOTE:`. `PAUSED` permits observations and journaling
   only. `RISK_OFF` permits exit plans but no buy plans.
2. Require `ALPACA_BASE_URL` to equal
   `https://paper-api.alpaca.markets`. A mismatch means notify 🚨 and stop.
3. Treat `memory/_lock` as an advisory local repository-writing signal only;
   it is not a distributed broker lock and never proves idempotency. Follow the
   advisory-lock procedure in `CLAUDE.md`.
4. Read `CLAUDE.md`, `config/risk-policy.json`, `config/instruments.json`,
   `config/earnings-calendar.json`, and every Bull memory file needed by this
   playbook, including the structured ledgers. All three config files are
   human-owned. Memory, strategy, research, and lessons cannot override or
   activate policy changes.
5. Reconcile broker truth at startup:

   ```
   python3 scripts/trade.py reconcile --agent bull --repair
   ```

   Under `PAUSED`, omit `--repair`. If reconciliation exits non-zero, reports
   `ok: false`, or has ambiguous output, fail closed: plan no buys, journal the
   exact issue, notify 🚨, perform the final read-only reconciliation, and stop.

## 1. Sync and risk posture

- Observe account, positions, portfolio history, and market data only through
  read-only `scripts/alpaca.sh` commands.
- Update `memory/portfolio.md` from broker state: equity, cash, buying power,
  positions, canonical sectors, unrealized P/L, and sector exposure.
- Compute equity drawdown from the broker high-water mark. At or beyond the
  policy's 10% Bull drawdown breaker, plan no buys. This is a hard rule.
- Review every thesis `invalidation` and `review_by`. A triggered or expired
  contract requires an explicit `trim`, `exit`, or documented hold decision.
- On Monday, any A/B/C rating is research annotation only. It cannot force a
  trade. Put a proposed rating-based rule in `memory/strategy-proposals.md` for
  versioned testing and human approval; do not add a trim solely from a rating.

If strategy memory is uninitialized, record provisional thesis/watchlist
research in `memory/research-log.md`; never edit human-owned `memory/strategy.md`.
Do not invent, edit, or activate risk limits; machine policy remains
authoritative.

## 2. Research

- Research today's macro tape, index futures, rates, volatility, and material
  event risk. Date every fact and cross-check trade-driving claims.
- For each holding, record what changed since yesterday, including "nothing
  material" when accurate.
- For each candidate, research tradability, thesis, valuation/fundamentals,
  liquidity, volatility, invalidation, and next earnings date.
- A buy is executable only when `config/earnings-calendar.json` contains one
  unambiguous, current record for that symbol. Copy `earnings_date`,
  `earnings_verified_at`, and `earnings_source` exactly from that human-owned
  record. Web research may support an inactive correction proposal, but it may
  never create or overwrite executable earnings metadata. If the trusted record
  is absent, stale, or conflicts with research, plan no buy and notify the human.
  Never invent a source URL. No buy may fall inside the two-trading-day blackout.
- Use canonical symbols and sectors from `config/instruments.json`. An unknown
  instrument blocks the intent; do not add it to the human-owned master.

Record sourced findings in `memory/research-log.md`. Lessons may describe
observations or proposals, but do not become live instructions.

## 3. Write one strict current-day plan

Append **"Planned trades for today"** followed by exactly one fenced JSON plan.
Its top level must contain exactly `schema_version`, `agent`, `plan_date`, and
`trades`, with `schema_version` equal to numeric `1` and `agent` equal to
`"bull"`. Allowed actions are `buy`, `trim`, and `exit`; use at most one action
per symbol. Quantities are positive whole shares. `exit` quantity must equal the
live held quantity; `trim` must be strictly smaller than the live holding. A hold is not a trade and is not
included.

Every intent requires `sector`, a specific thesis/invalidation, and a
`review_by` date. Each buy additionally requires `max_entry_price` and earnings
metadata that exactly matches a human record verified within 72 hours. If
`config/earnings-calendar.json` has no fresh matching entry, plan no buy:

```json
{
  "schema_version": 1,
  "agent": "bull",
  "plan_date": "YYYY-MM-DD",
  "trades": [
    {
      "action": "buy",
      "symbol": "XYZ",
      "qty": 10,
      "sector": "Canonical sector from config/instruments.json",
      "thesis": "Specific evidence-based reason this setup has positive expected value.",
      "invalidation": "Specific price or event that disproves the thesis.",
      "review_by": "YYYY-MM-DD",
      "max_entry_price": 123.45,
      "earnings_date": "YYYY-MM-DD",
      "earnings_verified_at": "YYYY-MM-DDTHH:MM:SS-04:00",
      "earnings_source": "COPY_EXACT_HTTPS_URL_FROM_CONFIG_RECORD"
    },
    {
      "action": "trim",
      "symbol": "ABC",
      "qty": 5,
      "sector": "Canonical sector from config/instruments.json",
      "thesis": "Specific reason reducing this live position is now warranted.",
      "invalidation": "Specific evidence that would invalidate the remaining thesis.",
      "review_by": "YYYY-MM-DD"
    },
    {
      "action": "exit",
      "symbol": "DEF",
      "qty": 12,
      "sector": "Canonical sector from config/instruments.json",
      "thesis": "Specific evidence showing the original thesis no longer holds.",
      "invalidation": "The thesis contract has been invalidated by stated evidence.",
      "review_by": "YYYY-MM-DD"
    }
  ]
}
```

If no action qualifies, use `"trades": []`. Never leave freeform trade
instructions outside the JSON and never ask market-open to infer an order.
Respect all machine limits, including the 15% single-order cap, 20% position
cap, 25% daily deployment cap, 5% minimum cash, 60% sector cap, 1.5% stop-risk
cap, three new positions/week, shock breaker, drawdown breaker, earnings
blackout, and the planned-sell day-trade guard.

## 4. Final reconciliation, notify, commit

Run final reconciliation:

```
python3 scripts/trade.py reconcile --agent bull --repair
```

Use `--repair` only if startup was unambiguous and control remains `ACTIVE` or
`RISK_OFF`; otherwise omit it. Any unresolved issue remains a hard no-buy condition. Notify once,
starting `Bull pre-market <date>:`; put urgent reconciliation or policy failures
first. Never put a literal `$` in a shell message.

Release the advisory lock, then persist only authorized Bull memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly;
never bypass failed reconciliation or policy to finish the routine.
