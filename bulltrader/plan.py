from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from .policy import Policy, PolicyError, instrument


class PlanError(RuntimeError):
    pass


@dataclass(frozen=True)
class TradeIntent:
    plan_date: date
    action: str
    symbol: str
    qty: Decimal
    sector: str
    thesis: str
    invalidation: str
    review_by: date
    max_entry_price: Decimal | None
    earnings_date: date | None
    earnings_verified_at: datetime | None
    earnings_source: str | None

    def canonical(self) -> dict[str, str | None]:
        return {
            "plan_date": self.plan_date.isoformat(),
            "action": self.action,
            "symbol": self.symbol,
            "qty": str(self.qty),
            "sector": self.sector,
            "thesis": self.thesis,
            "invalidation": self.invalidation,
            "review_by": self.review_by.isoformat(),
            "max_entry_price": str(self.max_entry_price) if self.max_entry_price else None,
            "earnings_date": self.earnings_date.isoformat() if self.earnings_date else None,
            "earnings_verified_at": (
                self.earnings_verified_at.isoformat() if self.earnings_verified_at else None
            ),
            "earnings_source": self.earnings_source,
        }


def _date(value: Any, field: str) -> date:
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise PlanError(f"{field} must be YYYY-MM-DD") from exc


def _datetime(value: Any, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise PlanError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise PlanError(f"{field} must include a timezone")
    return parsed


def _decimal(value: Any, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise PlanError(f"{field} must be numeric") from exc
    if not result.is_finite() or result <= 0:
        raise PlanError(f"{field} must be greater than zero")
    return result


def parse_trade(plan_date: date, raw: dict[str, Any], policy: Policy) -> TradeIntent:
    action = str(raw.get("action", "")).lower().strip()
    if action not in {"buy", "trim", "exit"}:
        raise PlanError("trade action must be buy, trim, or exit")
    common_fields = {"action", "symbol", "qty", "sector", "thesis", "invalidation", "review_by"}
    buy_fields = common_fields | {
        "max_entry_price",
        "earnings_date",
        "earnings_verified_at",
        "earnings_source",
    }
    allowed_fields = buy_fields if action == "buy" else common_fields
    if unknown := sorted(set(raw) - allowed_fields):
        raise PlanError(f"unknown fields in {action} intent: {', '.join(unknown)}")
    if missing := sorted(common_fields - set(raw)):
        raise PlanError(f"required trade fields missing: {', '.join(missing)}")
    symbol = str(raw.get("symbol", "")).upper().strip()
    if not re.fullmatch(r"[A-Z][A-Z0-9.\-]{0,9}", symbol):
        raise PlanError(f"invalid symbol: {symbol!r}")
    try:
        canonical_instrument = instrument(policy, symbol)
    except PolicyError as exc:
        raise PlanError(str(exc)) from exc
    sector = str(raw.get("sector", "")).strip()
    if sector != canonical_instrument["sector"]:
        raise PlanError(
            f"{symbol} sector must equal canonical value {canonical_instrument['sector']!r}"
        )
    qty = _decimal(raw.get("qty"), "qty")
    if qty != qty.to_integral_value():
        raise PlanError("qty must be a whole-share quantity")
    thesis = str(raw.get("thesis", "")).strip()
    invalidation = str(raw.get("invalidation", "")).strip()
    if len(thesis) < 20 or len(invalidation) < 10:
        raise PlanError("thesis and invalidation must be specific, non-placeholder text")
    review_by = _date(raw.get("review_by"), "review_by")
    if review_by < plan_date:
        raise PlanError("review_by cannot be before plan_date")

    max_entry_price = None
    earnings_date = None
    earnings_verified_at = None
    earnings_source = None
    if action == "buy":
        max_entry_price = _decimal(raw.get("max_entry_price"), "max_entry_price")
        earnings_date = _date(raw.get("earnings_date"), "earnings_date")
        earnings_verified_at = _datetime(raw.get("earnings_verified_at"), "earnings_verified_at")
        earnings_source = str(raw.get("earnings_source", "")).strip()
        if not earnings_source.startswith("https://"):
            raise PlanError("earnings_source must be an https URL")
    return TradeIntent(
        plan_date=plan_date,
        action=action,
        symbol=symbol,
        qty=qty,
        sector=sector,
        thesis=thesis,
        invalidation=invalidation,
        review_by=review_by,
        max_entry_price=max_entry_price,
        earnings_date=earnings_date,
        earnings_verified_at=earnings_verified_at,
        earnings_source=earnings_source,
    )


def latest_plan(path: Path, policy: Policy) -> tuple[date, list[TradeIntent]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PlanError(f"cannot read plan file {path}: {exc}") from exc
    blocks = re.findall(r"```json\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if not blocks:
        raise PlanError(f"no fenced planned-trades JSON block in {path}")
    candidates: list[tuple[date, dict[str, Any]]] = []
    for index, block in enumerate(blocks, start=1):
        try:
            parsed = json.loads(block)
        except json.JSONDecodeError as exc:
            raise PlanError(f"fenced JSON block {index} is malformed: {exc.msg}") from exc
        if not isinstance(parsed, dict) or "plan_date" not in parsed or "trades" not in parsed:
            raise PlanError(f"fenced JSON block {index} is not a trade-plan object")
        candidates.append((_date(parsed.get("plan_date"), "plan_date"), parsed))
    newest_date = max(item[0] for item in candidates)
    newest = [item[1] for item in candidates if item[0] == newest_date]
    typed_newest = [item for item in newest if item.get("schema_version") == 1]
    if len(typed_newest) == 1:
        raw = typed_newest[0]
    elif len(newest) == 1:
        raw = newest[0]
    else:
        raise PlanError(f"ambiguous trade plans: {len(newest)} blocks use latest date {newest_date}")
    if set(raw) != {"schema_version", "agent", "plan_date", "trades"}:
        raise PlanError(
            "plan object must contain exactly schema_version, agent, plan_date, and trades"
        )
    if raw.get("schema_version") != 1:
        raise PlanError("unsupported trade-plan schema_version")
    if raw.get("agent") != policy.agent_name:
        raise PlanError(
            f"trade plan agent {raw.get('agent')!r} does not match {policy.agent_name!r}"
        )
    plan_date = newest_date
    trades = raw.get("trades")
    if not isinstance(trades, list):
        raise PlanError("trades must be a JSON array")
    if len(trades) > 12:
        raise PlanError("a plan may contain at most 12 trades")
    intents: list[TradeIntent] = []
    seen: set[str] = set()
    for item in trades:
        if not isinstance(item, dict):
            raise PlanError("every trade must be a JSON object")
        intent = parse_trade(plan_date, item, policy)
        if intent.symbol in seen:
            raise PlanError(f"a plan may contain only one action for {intent.symbol}")
        seen.add(intent.symbol)
        intents.append(intent)
    return plan_date, intents


def find_intent(path: Path, policy: Policy, symbol: str, action: str, today: date) -> TradeIntent:
    plan_date, intents = latest_plan(path, policy)
    if policy.system.get("require_current_day_plan") and plan_date != today:
        raise PlanError(f"plan_date {plan_date} is stale; expected {today}")
    matches = [
        item
        for item in intents
        if item.symbol == symbol.upper() and item.action == action.lower()
    ]
    if len(matches) != 1:
        raise PlanError(f"today's plan must contain exactly one {action} for {symbol.upper()}")
    return matches[0]
