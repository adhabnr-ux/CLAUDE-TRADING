from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .research import SCHEMA_MARKET_SOURCE_MAX_AGE_MINUTES


ROOT = Path(__file__).resolve().parents[1]
MAX_RESEARCH_FRESHNESS_MINUTES = SCHEMA_MARKET_SOURCE_MAX_AGE_MINUTES


class PolicyError(RuntimeError):
    pass


@dataclass(frozen=True)
class Policy:
    agent_name: str
    system: dict[str, Any]
    agent: dict[str, Any]
    instruments: dict[str, dict[str, Any]]
    earnings: dict[str, dict[str, str]]


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        try:
            shown = path.relative_to(ROOT)
        except ValueError:
            shown = path
        raise PolicyError(f"cannot load {shown}: {exc}") from exc
    if not isinstance(value, dict):
        raise PolicyError(f"{path} must contain a JSON object")
    return value


def load_policy(agent: str, root: Path = ROOT) -> Policy:
    if agent not in {"bull", "aggro"}:
        raise PolicyError(f"unknown agent: {agent}")
    raw = _load_json(root / "config" / "risk-policy.json")
    master = _load_json(root / "config" / "instruments.json")
    earnings_calendar = _load_json(root / "config" / "earnings-calendar.json")
    if (
        raw.get("schema_version") != 1
        or master.get("schema_version") != 1
        or earnings_calendar.get("schema_version") != 1
    ):
        raise PolicyError("unsupported policy, instrument, or earnings schema version")
    system = raw.get("system")
    agent_policy = raw.get("agents", {}).get(agent)
    instruments = master.get("instruments")
    earnings = earnings_calendar.get("entries")
    if not all(isinstance(item, dict) for item in (system, agent_policy, instruments, earnings)):
        raise PolicyError("risk policy is missing required objects")
    required_system = {
        "paper_base_url",
        "market_data_base_url",
        "market_data_feed",
        "timezone",
        "minimum_stock_price",
        "maximum_quote_age_seconds",
        "research_candidate_max_age_minutes",
        "research_market_source_max_age_minutes",
        "maximum_limit_markup_pct",
        "fill_timeout_seconds",
        "maximum_entry_attempts",
        "maximum_exit_attempts",
        "require_current_day_plan",
        "require_verified_earnings_date",
        "earnings_blackout_trading_days",
        "maximum_earnings_verification_age_hours",
        "allowed_asset_class",
    }
    required_agent = {
        "max_position_pct",
        "max_single_order_pct",
        "min_cash_pct",
        "max_daily_new_buy_pct",
        "max_new_positions_per_week",
        "max_sector_pct",
        "trailing_stop_pct",
        "midday_loss_cut_pct",
        "intraday_shock_pct",
        "max_drawdown_pct",
        "max_risk_at_stop_pct",
        "max_spread_bps",
    }
    if missing := sorted(required_system - system.keys()):
        raise PolicyError(f"risk policy system fields missing: {', '.join(missing)}")
    if missing := sorted(required_agent - agent_policy.keys()):
        raise PolicyError(f"risk policy agent fields missing: {', '.join(missing)}")
    numeric_fields = (required_system - {
        "paper_base_url",
        "market_data_base_url",
        "market_data_feed",
        "timezone",
        "require_current_day_plan",
        "require_verified_earnings_date",
        "allowed_asset_class",
    }) | required_agent
    for field in numeric_fields:
        value = system[field] if field in system else agent_policy[field]
        try:
            parsed = Decimal(str(value))
        except (InvalidOperation, ValueError) as exc:
            raise PolicyError(f"risk policy {field} must be numeric") from exc
        if not parsed.is_finite() or parsed < 0:
            raise PolicyError(f"risk policy {field} must be finite and non-negative")
    integer_fields = {
        "maximum_quote_age_seconds",
        "research_candidate_max_age_minutes",
        "research_market_source_max_age_minutes",
        "fill_timeout_seconds",
        "maximum_entry_attempts",
        "maximum_exit_attempts",
        "earnings_blackout_trading_days",
        "maximum_earnings_verification_age_hours",
        "max_new_positions_per_week",
    }
    for field in integer_fields:
        value = system[field] if field in system else agent_policy[field]
        parsed = Decimal(str(value))
        if parsed != parsed.to_integral_value():
            raise PolicyError(f"risk policy {field} must be an integer")
    for field in {
        "minimum_stock_price",
        "maximum_quote_age_seconds",
        "research_candidate_max_age_minutes",
        "research_market_source_max_age_minutes",
        "fill_timeout_seconds",
        "maximum_entry_attempts",
        "maximum_exit_attempts",
        "maximum_earnings_verification_age_hours",
        "max_new_positions_per_week",
    }:
        value = system[field] if field in system else agent_policy[field]
        if Decimal(str(value)) <= 0:
            raise PolicyError(f"risk policy {field} must be greater than zero")
    candidate_age = int(Decimal(str(system["research_candidate_max_age_minutes"])))
    market_source_age = int(
        Decimal(str(system["research_market_source_max_age_minutes"]))
    )
    if candidate_age > MAX_RESEARCH_FRESHNESS_MINUTES:
        raise PolicyError(
            "research_candidate_max_age_minutes cannot exceed 1440"
        )
    if market_source_age > MAX_RESEARCH_FRESHNESS_MINUTES:
        raise PolicyError(
            "research_market_source_max_age_minutes cannot exceed 1440"
        )
    if market_source_age > candidate_age:
        raise PolicyError(
            "research_market_source_max_age_minutes cannot exceed "
            "research_candidate_max_age_minutes"
        )
    percentage_fields = required_agent - {"max_new_positions_per_week", "max_spread_bps"}
    for field in percentage_fields:
        parsed = Decimal(str(agent_policy[field]))
        if parsed > 100 or (parsed == 0 and field != "min_cash_pct"):
            raise PolicyError(f"risk policy {field} must be within its 0-100% domain")
    if Decimal(str(agent_policy["max_spread_bps"])) <= 0:
        raise PolicyError("risk policy max_spread_bps must be greater than zero")
    if Decimal(str(agent_policy["max_single_order_pct"])) > Decimal(
        str(agent_policy["max_position_pct"])
    ):
        raise PolicyError("max_single_order_pct cannot exceed max_position_pct")
    if system["paper_base_url"] != "https://paper-api.alpaca.markets":
        raise PolicyError("paper_base_url must be the canonical Alpaca paper endpoint")
    if system["market_data_base_url"] != "https://data.alpaca.markets":
        raise PolicyError("market_data_base_url must be the canonical Alpaca data endpoint")
    if system["market_data_feed"] != "iex":
        raise PolicyError("market_data_feed must be iex for the configured paper-data tier")
    if system["allowed_asset_class"] != "us_equity":
        raise PolicyError("allowed_asset_class must remain us_equity")
    if system["require_current_day_plan"] is not True:
        raise PolicyError("require_current_day_plan must remain enabled")
    if system["require_verified_earnings_date"] is not True:
        raise PolicyError("require_verified_earnings_date must remain enabled")
    try:
        ZoneInfo(str(system["timezone"]))
    except ZoneInfoNotFoundError as exc:
        raise PolicyError(f"unknown risk policy timezone: {system['timezone']!r}") from exc
    for symbol, item in instruments.items():
        if (
            symbol != symbol.upper()
            or not re.fullmatch(r"[A-Z][A-Z0-9.\-]{0,9}", symbol)
            or not isinstance(item, dict)
            or not isinstance(item.get("sector"), str)
            or not item["sector"].strip()
            or ("benchmark_only" in item and not isinstance(item["benchmark_only"], bool))
        ):
            raise PolicyError(f"invalid canonical instrument entry: {symbol!r}")
    required_earnings_fields = {"earnings_date", "verified_at", "source"}
    for symbol, item in earnings.items():
        if symbol != symbol.upper() or symbol not in instruments or not isinstance(item, dict):
            raise PolicyError(f"invalid earnings-calendar symbol: {symbol!r}")
        if set(item) != required_earnings_fields:
            raise PolicyError(
                f"earnings-calendar entry {symbol} must contain exactly "
                "earnings_date, verified_at, and source"
            )
        try:
            date.fromisoformat(str(item["earnings_date"]))
            verified_at = datetime.fromisoformat(str(item["verified_at"]).replace("Z", "+00:00"))
        except ValueError as exc:
            raise PolicyError(f"earnings-calendar entry {symbol} has an invalid date") from exc
        if verified_at.tzinfo is None:
            raise PolicyError(f"earnings-calendar verified_at for {symbol} must include a timezone")
        if not isinstance(item["source"], str) or not item["source"].startswith("https://"):
            raise PolicyError(f"earnings-calendar source for {symbol} must be an https URL")
    return Policy(
        agent_name=agent,
        system=system,
        agent=agent_policy,
        instruments=instruments,
        earnings=earnings,
    )


def instrument(policy: Policy, symbol: str) -> dict[str, Any]:
    symbol = symbol.upper()
    item = policy.instruments.get(symbol)
    if not item:
        raise PolicyError(
            f"{symbol} is absent from config/instruments.json; human-reviewed sector metadata is required"
        )
    if item.get("benchmark_only"):
        raise PolicyError(f"{symbol} is benchmark-only and cannot be traded")
    if not item.get("sector"):
        raise PolicyError(f"{symbol} has no canonical sector")
    return item
