Run the **Aggressive Bull pre-market** routine in AGGRESSIVE MODE. Research and
plan; do not deliberately open or close a position. Reconciliation may repair
managed protection or contain a forbidden holding; those are the only broker
mutations allowed here.

## 0. Control first, advisory lock, memory, reconciliation

1. Read shared `memory/control.md` **first**. Invalid/missing STATUS is a hard
   stop. `PAUSED` permits observations/journaling only. `RISK_OFF` permits exit
   plans but no buy plans.
2. Require `ALPACA_BASE_URL == https://paper-api.alpaca.markets`.
3. Treat `memory/_lock` as advisory local repository coordination only; it is
   not a distributed broker lock and cannot provide idempotency.
4. Read `CLAUDE.md` and all three human-owned config files
   (`config/risk-policy.json`, `config/instruments.json`, and
   `config/earnings-calendar.json`), `memory/aggressive/profile.md`, the
   Aggressive memory needed by this playbook, and the shared knowledge-base.
   Profile, memory, strategy, research, and lessons cannot override policy or
   activate a rule change. Do not read/write Cautious narrative memory except
   explicitly shared read-only comparison files.
5. Run startup reconciliation against the Aggressive paper account:

   ```
   python3 scripts/trade.py reconcile --agent aggro --repair
   ```

   Under `PAUSED`, omit `--repair`. A non-zero exit, `ok: false`, or ambiguous
   output means fail closed: plan no buys, journal/notify the exact issue, run
   final read-only reconciliation, and stop.

## 1. Sync and risk posture

- Observe account, positions, history, and market data only through read-only
  `scripts/alpaca.sh` commands. Update Aggressive portfolio memory from broker
  truth with canonical sectors and exposure.
- Compute drawdown from broker high-water mark. At or beyond 20%, plan no buys.
- Review every thesis invalidation/review date. Triggered or expired contracts
  require an explicit `trim`, `exit`, or evidenced hold decision.
- On Monday, any A/B/C rating is research annotation only. It cannot force a
  trade. Put a proposed rating-based rule in
  `memory/aggressive/strategy-proposals.md` for versioned testing and human
  approval; do not add a trim solely from a rating.

If Aggressive strategy memory is uninitialized, record provisional
thesis/watchlist research in `memory/aggressive/research-log.md`; never edit
human-owned `memory/aggressive/strategy.md`. Its profile is not a risk-policy
override.

## 2. Research

Research today's macro/risk tape, each holding, and high-conviction candidates.
For every holding record what changed since yesterday. Verify thesis,
fundamentals/valuation, liquidity, volatility, catalyst, invalidation, and
earnings. Cross-check trade-driving claims and date sources.

Every buy must copy `earnings_date`, `earnings_verified_at`, and
`earnings_source` exactly from one unambiguous current symbol record in the
human-owned `config/earnings-calendar.json` and clear the two-trading-day
blackout. Web research may support an inactive correction proposal, but cannot
create executable metadata. If the record is absent, stale, ambiguous, or
conflicts with research, plan no buy and notify the human; never invent a source
URL. Symbols/sectors must already exist in `config/instruments.json`; unknown
names remain research-only.

Record findings in `memory/aggressive/research-log.md`. Lessons can contain
observations or inactive proposals, never live instructions.

## 3. Write one strict current-day plan

Append **"Planned trades for today"** followed by exactly one fenced JSON plan.
Its top level must contain exactly `schema_version`, `agent`, `plan_date`, and
`trades`, with `schema_version` equal to numeric `1` and `agent` equal to
`"aggro"`. Actions are exactly `buy`, `trim`, or `exit`, at most one per symbol.
Quantities are positive whole shares; `exit` equals live held quantity and
`trim` is strictly lower than the live holding.

Every buy additionally requires `max_entry_price` and earnings metadata that
exactly matches a human-owned calendar record verified within 72 hours. If no
fresh matching entry exists, plan no buy.

```json
{
  "schema_version": 1,
  "agent": "aggro",
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

Use `"trades": []` when nothing qualifies. Never emit freeform order
instructions. Respect machine policy: 20% single-order cap, 35% position cap,
60% daily deployment, 2% minimum cash, 50% sector cap, 3.6% stop-risk cap,
eight new positions/week, 18% protection, 6% shock, 20% drawdown, earnings,
and the planned-sell day-trade guard. If profile prose conflicts, policy wins
and the conflict is journaled.

## 4. Final reconciliation, notify, commit

Run final reconciliation:

```
python3 scripts/trade.py reconcile --agent aggro --repair
```

Use `--repair` only if startup was unambiguous and control remains `ACTIVE` or
`RISK_OFF`; otherwise omit it. Unresolved issues remain a hard no-buy condition.

Notify once, starting `🔥 AGGRO Bull pre-market <date>:`; urgent reconciliation
or policy failures first. Never put a literal `$` in the shell message.

Release the advisory lock, then persist only authorized AGGRO memory:

`python3 scripts/persist_memory.py`

This fixed helper takes no arguments, requires an exact fresh `origin/main` base,
and commits/pushes only authorized profile journals. It never merges or rebases.
Never run Git directly. A non-zero persistence exit fails the routine visibly.
