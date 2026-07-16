from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from decimal import Decimal, ROUND_DOWN
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from .alpaca import AlpacaClient, BrokerError, Quote
from .plan import TradeIntent
from .policy import Policy, PolicyError, instrument


class RiskRejected(RuntimeError):
    pass


@dataclass(frozen=True)
class BuyApproval:
    limit_price: Decimal
    notional: Decimal
    equity: Decimal
    cash_after: Decimal
    position_pct_after: Decimal
    sector_pct_after: Decimal
    daily_buy_pct_after: Decimal
    drawdown_pct: Decimal


def D(value: Any, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except Exception as exc:
        raise RiskRejected(f"missing or invalid broker field: {field}") from exc
    if not result.is_finite():
        raise RiskRejected(f"non-finite broker field: {field}")
    return result


def control_status(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RiskRejected(f"cannot read control switch: {exc}") from exc
    status_lines = [line for line in text.splitlines() if line.startswith("STATUS:")]
    if len(status_lines) != 1:
        raise RiskRejected(
            f"control switch must contain exactly one STATUS line; found {len(status_lines)}"
        )
    status = status_lines[0].partition(":")[2].strip().upper()
    if status not in {"ACTIVE", "RISK_OFF", "PAUSED"}:
        raise RiskRejected(f"invalid control status: {status}")
    return status


def assert_mutation_allowed(path: Path, *, opening: bool) -> str:
    status = control_status(path)
    if status == "PAUSED":
        raise RiskRejected("control status PAUSED blocks all orders")
    if opening and status == "RISK_OFF":
        raise RiskRejected("control status RISK_OFF blocks new buys")
    return status


def _position_value(position: dict[str, Any]) -> Decimal:
    value = D(position.get("market_value"), "position.market_value")
    if value < 0:
        raise RiskRejected("a long position has negative market value")
    return value


def _order_value(order: dict[str, Any]) -> Decimal:
    if str(order.get("side", "")).lower() != "buy":
        return Decimal("0")
    filled_qty = D(order.get("filled_qty", 0), "order.filled_qty")
    filled_price = D(order.get("filled_avg_price") or 0, "order.filled_avg_price")
    if filled_qty > 0 and filled_price <= 0:
        raise RiskRejected("a filled buy order has no valid average price")
    terminal_without_more_fills = {
        "canceled",
        "expired",
        "rejected",
        "replaced",
    }
    remaining = max(D(order.get("qty") or 0, "order.qty") - filled_qty, Decimal("0"))
    if str(order.get("status", "")).lower() in terminal_without_more_fills:
        remaining = Decimal("0")
    pending_price = D(
        order.get("limit_price") or order.get("stop_price") or order.get("filled_avg_price") or 0,
        "order.price",
    )
    if remaining > 0 and pending_price <= 0:
        raise RiskRejected("an active buy order has no bounded price")
    return (filled_qty * filled_price) + (remaining * pending_price)


def _pending_buy_value(order: dict[str, Any]) -> Decimal:
    if str(order.get("side", "")).lower() != "buy":
        return Decimal("0")
    remaining = max(
        D(order.get("qty", 0), "order.qty")
        - D(order.get("filled_qty", 0), "order.filled_qty"),
        Decimal("0"),
    )
    if remaining == 0:
        return Decimal("0")
    price = D(order.get("limit_price") or order.get("stop_price") or 0, "order.price")
    if price <= 0:
        raise RiskRejected("an open buy order has no bounded price")
    return remaining * price


def _history_high_water(history: dict[str, Any]) -> Decimal:
    values = [D(value, "portfolio_history.equity") for value in history.get("equity", [])]
    values = [value for value in values if value > 0]
    if not values:
        raise RiskRejected("portfolio history has no usable equity values")
    return max(values)


def _trading_days_to_earnings(
    client: AlpacaClient, today: date, earnings_date: date
) -> int:
    if earnings_date < today:
        raise RiskRejected("earnings_date is in the past")
    calendar = client.calendar(today.isoformat(), earnings_date.isoformat())
    try:
        sessions = [
            item
            for item in calendar
            if today <= date.fromisoformat(str(item["date"])) <= earnings_date
        ]
    except (KeyError, TypeError, ValueError) as exc:
        raise RiskRejected("broker calendar returned an invalid session") from exc
    if not sessions:
        raise RiskRejected("broker calendar returned no sessions through earnings_date")
    return max(len(sessions) - 1, 0)


def _session_boundaries(now: datetime, timezone_name: str) -> tuple[datetime, datetime]:
    local = now.astimezone(ZoneInfo(timezone_name))
    start_day = datetime.combine(local.date(), time.min, tzinfo=local.tzinfo)
    monday = local.date().fromordinal(local.date().toordinal() - local.weekday())
    start_week = datetime.combine(monday, time.min, tzinfo=local.tzinfo)
    return start_day, start_week


def approve_buy(
    *,
    client: AlpacaClient,
    policy: Policy,
    intent: TradeIntent,
    now: datetime,
    control_path: Path,
) -> BuyApproval:
    if now.tzinfo is None:
        raise RiskRejected("risk evaluation time must include a timezone")
    assert_mutation_allowed(control_path, opening=True)
    if intent.action != "buy":
        raise RiskRejected("approve_buy received a non-buy intent")
    local_today = now.astimezone(ZoneInfo(str(policy.system["timezone"]))).date()
    if policy.system.get("require_current_day_plan") and intent.plan_date != local_today:
        raise RiskRejected(f"plan_date {intent.plan_date} is stale; expected {local_today}")

    account = client.account()
    if account.get("trading_blocked") or account.get("account_blocked"):
        raise RiskRejected("broker account is blocked")
    if str(account.get("status", "")).upper() != "ACTIVE":
        raise RiskRejected(f"broker account status is {account.get('status')!r}")
    clock = client.clock()
    if clock.get("is_open") is not True:
        raise RiskRejected("market is closed")

    asset = client.asset(intent.symbol)
    if not asset.get("tradable") or str(asset.get("status", "")).lower() != "active":
        raise RiskRejected(f"{intent.symbol} is not active and tradable")
    if str(asset.get("class", "")) != str(policy.system["allowed_asset_class"]):
        raise RiskRejected(f"{intent.symbol} is not an allowed US equity")

    quote: Quote = client.quote(intent.symbol)
    quote_age = (now.astimezone(timezone.utc) - quote.timestamp).total_seconds()
    if quote_age < -5 or quote_age > float(policy.system["maximum_quote_age_seconds"]):
        raise RiskRejected(f"{intent.symbol} quote is stale or future-dated ({quote_age:.1f}s)")
    if quote.ask < D(policy.system["minimum_stock_price"], "minimum_stock_price"):
        raise RiskRejected(f"{intent.symbol} is below the minimum stock price")
    midpoint = (quote.bid + quote.ask) / 2
    spread_bps = (quote.ask - quote.bid) / midpoint * 10000
    if spread_bps > D(policy.agent["max_spread_bps"], "max_spread_bps"):
        raise RiskRejected(f"{intent.symbol} spread is too wide at {spread_bps:.2f} bps")
    assert intent.max_entry_price is not None
    if quote.ask > intent.max_entry_price:
        raise RiskRejected(
            f"{intent.symbol} ask {quote.ask} exceeds planned max entry {intent.max_entry_price}"
        )
    markup = Decimal("1") + D(policy.system["maximum_limit_markup_pct"], "markup") / 100
    limit_price = min(quote.ask * markup, intent.max_entry_price).quantize(
        Decimal("0.01"), rounding=ROUND_DOWN
    )
    notional = intent.qty * limit_price

    equity = D(account.get("equity"), "account.equity")
    cash = D(account.get("cash"), "account.cash")
    last_equity = D(account.get("last_equity"), "account.last_equity")
    if min(equity, cash, last_equity) < 0 or equity <= 0 or last_equity <= 0:
        raise RiskRejected("account equity/cash values are invalid")
    shock = max((last_equity - equity) / last_equity * 100, Decimal("0"))
    if shock >= D(policy.agent["intraday_shock_pct"], "intraday_shock_pct"):
        raise RiskRejected(f"intraday shock breaker active at {shock:.3f}%")

    hwm = _history_high_water(client.portfolio_history())
    drawdown = max((hwm - equity) / hwm * 100, Decimal("0"))
    if drawdown >= D(policy.agent["max_drawdown_pct"], "max_drawdown_pct"):
        raise RiskRejected(f"drawdown breaker active at {drawdown:.3f}%")

    positions = client.positions()
    open_orders = client.orders(status="open")
    pending_total = sum((_pending_buy_value(order) for order in open_orders), Decimal("0"))
    by_symbol = {str(item.get("symbol", "")).upper(): item for item in positions}
    existing = _position_value(by_symbol[intent.symbol]) if intent.symbol in by_symbol else Decimal("0")
    pending_symbol = sum(
        (
            _pending_buy_value(order)
            for order in open_orders
            if str(order.get("symbol", "")).upper() == intent.symbol
        ),
        Decimal("0"),
    )
    position_pct = (existing + pending_symbol + notional) / equity * 100
    if position_pct > D(policy.agent["max_position_pct"], "max_position_pct"):
        raise RiskRejected(f"position would reach {position_pct:.3f}% of equity")
    order_pct = notional / equity * 100
    if order_pct > D(policy.agent["max_single_order_pct"], "max_single_order_pct"):
        raise RiskRejected(f"order would use {order_pct:.3f}% of equity")
    risk_at_stop = (
        position_pct * D(policy.agent["trailing_stop_pct"], "trailing_stop_pct") / 100
    )
    if risk_at_stop > D(policy.agent["max_risk_at_stop_pct"], "max_risk_at_stop_pct"):
        raise RiskRejected(f"planned stop risk would be {risk_at_stop:.3f}% of equity")

    cash_after = cash - pending_total - notional
    min_cash = equity * D(policy.agent["min_cash_pct"], "min_cash_pct") / 100
    if cash_after < min_cash:
        raise RiskRejected(
            f"cash after order {cash_after:.2f} would breach minimum {min_cash:.2f}"
        )

    canonical = instrument(policy, intent.symbol)
    sector = canonical["sector"]
    sector_value = Decimal("0")
    for position in positions:
        sym = str(position.get("symbol", "")).upper()
        try:
            item = instrument(policy, sym)
        except PolicyError as exc:
            raise RiskRejected(str(exc)) from exc
        if item["sector"] == sector:
            sector_value += _position_value(position)
    for order in open_orders:
        if str(order.get("side", "")).lower() != "buy":
            continue
        pending_symbol_name = str(order.get("symbol", "")).upper()
        try:
            pending_instrument = instrument(policy, pending_symbol_name)
        except PolicyError as exc:
            raise RiskRejected(str(exc)) from exc
        if pending_instrument["sector"] == sector:
            sector_value += _pending_buy_value(order)
    sector_pct = (sector_value + notional) / equity * 100
    if sector_pct > D(policy.agent["max_sector_pct"], "max_sector_pct"):
        raise RiskRejected(f"{sector} exposure would reach {sector_pct:.3f}%")

    start_day, start_week = _session_boundaries(now, str(policy.system["timezone"]))
    today_orders = client.orders(after=start_day)
    if any(
        str(order.get("symbol", "")).upper() == intent.symbol
        and str(order.get("side", "")).lower() == "sell"
        and D(order.get("filled_qty", 0), "filled_qty") > 0
        for order in today_orders
    ):
        raise RiskRejected(f"day-trade guard: {intent.symbol} was sold today")
    daily_buys = sum((_order_value(order) for order in today_orders), Decimal("0"))
    daily_pct = (daily_buys + notional) / equity * 100
    if daily_pct > D(policy.agent["max_daily_new_buy_pct"], "max_daily_new_buy_pct"):
        raise RiskRejected(f"daily new-buy deployment would reach {daily_pct:.3f}%")

    week_orders = client.orders(after=start_week)
    weekly_symbols = {
        str(order.get("symbol", "")).upper()
        for order in week_orders
        if str(order.get("side", "")).lower() == "buy"
        and D(order.get("filled_qty", 0), "filled_qty") > 0
    }
    if intent.symbol not in by_symbol and intent.symbol not in weekly_symbols:
        if len(weekly_symbols) >= int(policy.agent["max_new_positions_per_week"]):
            raise RiskRejected("weekly new-position limit is exhausted")

    if policy.system.get("require_verified_earnings_date"):
        if not intent.earnings_date or not intent.earnings_verified_at or not intent.earnings_source:
            raise RiskRejected("verified earnings metadata is required")
        calendar_entry = policy.earnings.get(intent.symbol)
        if not calendar_entry:
            raise RiskRejected(
                f"{intent.symbol} has no human-verified entry in config/earnings-calendar.json"
            )
        try:
            canonical_date = date.fromisoformat(calendar_entry["earnings_date"])
            canonical_verified_at = datetime.fromisoformat(
                calendar_entry["verified_at"].replace("Z", "+00:00")
            )
        except (KeyError, ValueError) as exc:
            raise RiskRejected(f"invalid canonical earnings entry for {intent.symbol}") from exc
        if (
            intent.earnings_date != canonical_date
            or intent.earnings_verified_at.astimezone(timezone.utc)
            != canonical_verified_at.astimezone(timezone.utc)
            or intent.earnings_source != calendar_entry["source"]
        ):
            raise RiskRejected(
                f"{intent.symbol} earnings metadata does not exactly match the human-owned calendar"
            )
        age_hours = (
            now.astimezone(timezone.utc) - canonical_verified_at.astimezone(timezone.utc)
        ).total_seconds() / 3600
        if age_hours < 0:
            raise RiskRejected("earnings verification timestamp is in the future")
        if age_hours > float(policy.system["maximum_earnings_verification_age_hours"]):
            raise RiskRejected(
                f"{intent.symbol} earnings verification is stale ({age_hours:.1f} hours old)"
            )
        trading_days = _trading_days_to_earnings(client, intent.plan_date, intent.earnings_date)
        if trading_days <= int(policy.system["earnings_blackout_trading_days"]):
            raise RiskRejected(f"earnings blackout: {trading_days} trading day(s) to earnings")

    return BuyApproval(
        limit_price=limit_price,
        notional=notional,
        equity=equity,
        cash_after=cash_after,
        position_pct_after=position_pct,
        sector_pct_after=sector_pct,
        daily_buy_pct_after=daily_pct,
        drawdown_pct=drawdown,
    )
