from __future__ import annotations

import hashlib
import json
import os
import re
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo

from .alpaca import AlpacaClient, BrokerError
from .plan import TradeIntent
from .policy import Policy, PolicyError, instrument
from .risk import D, RiskRejected, approve_buy, assert_mutation_allowed


ROOT = Path(__file__).resolve().parents[1]
OPEN_ORDER_STATUSES = {
    "new",
    "accepted",
    "pending_new",
    "accepted_for_bidding",
    "partially_filled",
    "held",
    "suspended",
    "stopped",
    "done_for_day",
    "calculated",
    "pending_cancel",
    "pending_replace",
}
TERMINAL_ORDER_STATUSES = {"filled", "canceled", "expired", "rejected"}


@dataclass
class ReconciliationReport:
    ok: bool
    equity: str
    cash: str
    positions: int
    issues: list[str]
    repaired: list[str]


def _client_id(prefix: str, payload: dict[str, Any]) -> str:
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:20]
    cleaned = "".join(ch.lower() for ch in prefix if ch.isalnum() or ch == "-")
    return f"bt-{cleaned[:24]}-{digest}"


def _assert_order_role(
    order: dict[str, Any],
    *,
    client_order_id: str,
    symbol: str,
    side: str,
    order_type: str,
) -> None:
    expected = {
        "client_order_id": client_order_id,
        "symbol": symbol.upper(),
        "side": side.lower(),
        "type": order_type.lower(),
    }
    actual = {
        "client_order_id": str(order.get("client_order_id", "")),
        "symbol": str(order.get("symbol", "")).upper(),
        "side": str(order.get("side", "")).lower(),
        "type": str(order.get("type", "")).lower(),
    }
    if actual != expected:
        raise BrokerError(
            f"client_order_id collision or broker mismatch for {client_order_id}: {actual}"
        )


def _assert_order_qty(order: dict[str, Any], expected: Any) -> None:
    if D(order.get("qty"), "order.qty") != D(expected, "expected.qty"):
        raise BrokerError(f"broker order quantity mismatch for {order.get('client_order_id')}")


def _assert_contiguous_attempt_history(
    orders: list[dict[str, Any] | None], operation: str
) -> None:
    gap_seen = False
    for attempt, order in enumerate(orders, start=1):
        if order is None:
            gap_seen = True
        elif gap_seen:
            raise BrokerError(
                f"non-contiguous broker history for {operation}: "
                f"attempt {attempt} exists after a missing earlier attempt"
            )


def _append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _agent_memory(root: Path, agent: str) -> Path:
    if agent == "bull":
        return root / "memory"
    if agent == "aggro":
        return root / "memory" / "aggressive"
    raise RiskRejected(f"unknown execution agent: {agent}")


def event(root: Path, kind: str, **details: Any) -> bool:
    """Persist audit telemetry without interrupting protection of a broker position."""
    agent = str(details.get("agent", ""))
    try:
        _append_jsonl(
            _agent_memory(root, agent) / "execution-events.jsonl",
            {
                "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "event": kind,
                **details,
            },
        )
    except OSError:
        return False
    return True


def _poll_order(
    client: AlpacaClient,
    order: dict[str, Any],
    timeout_seconds: int,
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    current = _follow_replacement(client, order)
    while str(current.get("status", "")).lower() in OPEN_ORDER_STATUSES:
        if time.monotonic() >= deadline:
            break
        sleep(2)
        current = _follow_replacement(client, client.order(str(current["id"])))
    _assert_known_status(current)
    return current


def _assert_known_status(order: dict[str, Any]) -> str:
    status = str(order.get("status", "")).lower()
    if status not in OPEN_ORDER_STATUSES | TERMINAL_ORDER_STATUSES | {"replaced"}:
        raise BrokerError(f"unknown Alpaca order status {status!r} for {order.get('id')}")
    return status


def _follow_replacement(client: AlpacaClient, order: dict[str, Any]) -> dict[str, Any]:
    current = order
    seen: set[str] = set()
    while str(current.get("status", "")).lower() == "replaced":
        replacement_id = str(current.get("replaced_by", ""))
        if not replacement_id or replacement_id in seen:
            raise BrokerError(f"replaced order {current.get('id')} has no valid successor")
        seen.add(replacement_id)
        current = client.order(replacement_id)
    _assert_known_status(current)
    return current


def _cancel_and_confirm(
    client: AlpacaClient,
    order: dict[str, Any],
    timeout_seconds: int,
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    current = _follow_replacement(client, client.order(str(order["id"])))
    if str(current.get("status", "")).lower() not in OPEN_ORDER_STATUSES:
        return current
    current_id = str(current["id"])
    try:
        client.cancel_order(current_id)
    except BrokerError:
        current = _follow_replacement(client, client.order(current_id))
        if str(current.get("status", "")).lower() in OPEN_ORDER_STATUSES:
            raise
        return current
    current = _follow_replacement(client, client.order(current_id))
    current = _poll_order(client, current, timeout_seconds, sleep=sleep)
    if str(current.get("status", "")).lower() in OPEN_ORDER_STATUSES:
        raise BrokerError(f"order cancellation was not confirmed: {current_id}")
    return current


def _open_stop_orders(client: AlpacaClient, symbol: str) -> list[dict[str, Any]]:
    return [
        order
        for order in client.orders(status="open")
        if str(order.get("symbol", "")).upper() == symbol.upper()
        and str(order.get("side", "")).lower() == "sell"
        and str(order.get("type", "")).lower() == "trailing_stop"
        and str(order.get("status", "")).lower() in OPEN_ORDER_STATUSES
    ]


def _remaining_order_qty(order: dict[str, Any]) -> Decimal:
    qty = D(order.get("qty", 0), "order.qty")
    filled = D(order.get("filled_qty", 0), "order.filled_qty")
    if qty <= 0 or filled < 0 or filled > qty:
        raise RiskRejected(f"invalid broker order quantities: qty={qty}, filled={filled}")
    return qty - filled


def _position(client: AlpacaClient, symbol: str) -> dict[str, Any] | None:
    for position in client.positions():
        if str(position.get("symbol", "")).upper() == symbol.upper():
            return position
    return None


def place_trailing_stop(
    *,
    client: AlpacaClient,
    policy: Policy,
    agent: str,
    symbol: str,
    qty: Decimal,
    seed: str,
    root: Path = ROOT,
) -> dict[str, Any]:
    if qty <= 0:
        raise RiskRejected("trailing-stop quantity must be positive")
    existing = None
    client_order_id = ""
    for generation in range(8):
        client_order_id = _client_id(
            f"{agent}-stop-{symbol}",
            {
                "seed": seed,
                "symbol": symbol,
                "qty": str(qty),
                "generation": generation,
            },
        )
        existing = client.order_by_client_id(client_order_id)
        if existing is None:
            break
        _assert_order_role(
            existing,
            client_order_id=client_order_id,
            symbol=symbol,
            side="sell",
            order_type="trailing_stop",
        )
        _assert_order_qty(existing, qty)
        if str(existing.get("status", "")).lower() in OPEN_ORDER_STATUSES:
            return existing
    else:
        raise BrokerError(f"protective stop idempotency generations exhausted for {symbol}")
    body = {
        "symbol": symbol,
        "qty": str(qty),
        "side": "sell",
        "type": "trailing_stop",
        "trail_percent": str(policy.agent["trailing_stop_pct"]),
        "time_in_force": "gtc",
        "client_order_id": client_order_id,
    }
    try:
        order = client.submit_order(body)
    except BrokerError as exc:
        try:
            recovered = client.order_by_client_id(client_order_id)
        except BrokerError as lookup_exc:
            raise BrokerError(
                f"protective stop outcome is unknown for {symbol}; broker lookup also failed"
            ) from lookup_exc
        if recovered and str(recovered.get("status", "")).lower() in OPEN_ORDER_STATUSES:
            order = recovered
        else:
            raise exc
    if str(order.get("status", "")).lower() not in OPEN_ORDER_STATUSES:
        raise BrokerError(f"protective stop was not accepted: {order.get('status')}")
    _assert_order_role(
        order,
        client_order_id=client_order_id,
        symbol=symbol,
        side="sell",
        order_type="trailing_stop",
    )
    _assert_order_qty(order, qty)
    event(
        root,
        "protective_stop_accepted",
        agent=agent,
        symbol=symbol,
        qty=str(qty),
        order_id=order.get("id"),
        client_order_id=client_order_id,
    )
    return order


def _replace_trailing_stop(
    *,
    client: AlpacaClient,
    policy: Policy,
    agent: str,
    symbol: str,
    stop: dict[str, Any],
    target_qty: Decimal,
    root: Path,
) -> dict[str, Any]:
    """Replace protection in-place; a failed PATCH leaves the old stop working."""
    if target_qty <= 0:
        raise RiskRejected("replacement protective-stop quantity must be positive")
    if D(stop.get("filled_qty", 0), "stop.filled_qty") != 0:
        raise BrokerError(
            f"cannot safely replace partially filled protective stop {stop.get('id')}"
        )
    expected_trail = D(policy.agent["trailing_stop_pct"], "trailing_stop_pct")
    client_order_id = _client_id(
        f"{agent}-stop-replace-{symbol}",
        {
            "old_order_id": str(stop.get("id")),
            "qty": str(target_qty),
            "trail_percent": str(expected_trail),
            "time_in_force": "gtc",
        },
    )
    replacement = client.order_by_client_id(client_order_id)
    if replacement is None:
        body = {
            "qty": str(target_qty),
            "time_in_force": "gtc",
            "trail": str(expected_trail),
            "client_order_id": client_order_id,
        }
        try:
            replacement = client.replace_order(str(stop["id"]), body)
        except BrokerError as exc:
            try:
                replacement = client.order_by_client_id(client_order_id)
            except BrokerError as lookup_exc:
                raise BrokerError(
                    f"protective-stop replacement outcome is unknown for {symbol}"
                ) from lookup_exc
            if replacement is None:
                # Do not cancel the old stop. A failed replace must preserve the
                # best protection the account already had.
                raise exc
    replacement = _follow_replacement(client, replacement)
    _assert_order_role(
        replacement,
        client_order_id=client_order_id,
        symbol=symbol,
        side="sell",
        order_type="trailing_stop",
    )
    _assert_order_qty(replacement, target_qty)
    if str(replacement.get("status", "")).lower() not in OPEN_ORDER_STATUSES:
        raise BrokerError(
            f"protective-stop replacement was not accepted: {replacement.get('status')}"
        )
    actual_trail = D(replacement.get("trail_percent"), "replacement.trail_percent")
    if actual_trail != expected_trail or str(replacement.get("time_in_force", "")).lower() != "gtc":
        raise BrokerError("broker did not apply the requested protective-stop replacement")
    event(
        root,
        "protective_stop_replaced",
        agent=agent,
        symbol=symbol,
        old_order_id=stop.get("id"),
        replacement_order_id=replacement.get("id"),
        qty=str(target_qty),
    )
    return replacement


def _stop_is_canonical(stop: dict[str, Any], expected_trail: Decimal) -> bool:
    try:
        actual_trail = D(stop.get("trail_percent"), "stop.trail_percent")
    except RiskRejected:
        return False
    return actual_trail == expected_trail and str(stop.get("time_in_force", "")).lower() == "gtc"


def ensure_symbol_protected(
    *,
    client: AlpacaClient,
    policy: Policy,
    agent: str,
    symbol: str,
    repair: bool,
    root: Path = ROOT,
) -> tuple[Decimal, Decimal]:
    position = _position(client, symbol)
    if not position:
        return Decimal("0"), Decimal("0")
    qty = D(position.get("qty"), "position.qty")
    if qty <= 0:
        raise RiskRejected(f"short or zero position detected in {symbol}")
    stops = _open_stop_orders(client, symbol)
    expected_trail = D(policy.agent["trailing_stop_pct"], "trailing_stop_pct")
    invalid_stops = [stop for stop in stops if not _stop_is_canonical(stop, expected_trail)]
    if invalid_stops:
        ids = ", ".join(str(item.get("id")) for item in invalid_stops)
        if not repair:
            raise RiskRejected(f"{symbol} has invalid protective stop configuration: {ids}")
        for stop in invalid_stops:
            _replace_trailing_stop(
                client=client,
                policy=policy,
                agent=agent,
                symbol=symbol,
                stop=stop,
                target_qty=_remaining_order_qty(stop),
                root=root,
            )
        stops = _open_stop_orders(client, symbol)
    covered = sum((_remaining_order_qty(order) for order in stops), Decimal("0"))
    if covered > qty:
        if not repair:
            raise RiskRejected(f"{symbol} stop over-coverage: {covered} for {qty} shares")
        excess = covered - qty
        # Reduce only the excess. Replacements preserve the old stop until the
        # broker confirms its successor. A fully redundant stop is canceled only
        # after the remaining live stops already cover the entire position.
        for stop in reversed(stops):
            if excess <= 0:
                break
            remaining = _remaining_order_qty(stop)
            reduction = min(remaining, excess)
            target = remaining - reduction
            if target > 0:
                _replace_trailing_stop(
                    client=client,
                    policy=policy,
                    agent=agent,
                    symbol=symbol,
                    stop=stop,
                    target_qty=target,
                    root=root,
                )
            else:
                other_coverage = covered - remaining
                if other_coverage < qty:
                    raise BrokerError(
                        f"cannot remove redundant {symbol} stop without reducing protection"
                    )
                _cancel_and_confirm(
                    client,
                    stop,
                    int(policy.system["fill_timeout_seconds"]),
                )
            covered -= reduction
            excess -= reduction
        stops = _open_stop_orders(client, symbol)
        covered = sum((_remaining_order_qty(order) for order in stops), Decimal("0"))
    missing = qty - covered
    if missing > 0 and repair:
        seed = _client_id(
            f"repair-{agent}-{symbol}",
            {"live_stop_ids": sorted(str(item.get("id")) for item in stops), "missing": str(missing)},
        )
        place_trailing_stop(
            client=client,
            policy=policy,
            agent=agent,
            symbol=symbol,
            qty=missing,
            seed=seed,
            root=root,
        )
    # Never report an algebraic repair as successful. Re-read broker truth after
    # every mutation because an accepted stop can still race a position fill.
    final_position = _position(client, symbol)
    if not final_position:
        return Decimal("0"), Decimal("0")
    final_qty = D(final_position.get("qty"), "position.qty")
    if final_qty <= 0:
        raise RiskRejected(f"short or zero position detected in {symbol}")
    final_stops = _open_stop_orders(client, symbol)
    final_covered = sum((_remaining_order_qty(order) for order in final_stops), Decimal("0"))
    if any(not _stop_is_canonical(stop, expected_trail) for stop in final_stops):
        raise BrokerError(f"{symbol} still has non-canonical protective stops after repair")
    return final_qty, final_covered


def reconcile(
    *,
    client: AlpacaClient,
    policy: Policy,
    agent: str,
    repair: bool,
    control_path: Path,
    root: Path = ROOT,
    owned_order_client_ids: set[str] | None = None,
) -> ReconciliationReport:
    status = assert_mutation_allowed(control_path, opening=False) if repair else None
    account = client.account()
    positions = client.positions()
    open_orders = client.orders(status="open")
    issues: list[str] = []
    repaired: list[str] = []
    owned_order_client_ids = owned_order_client_ids or set()
    owned_exit_symbols: set[str] = set()
    if account.get("trading_blocked") or account.get("account_blocked"):
        issues.append("broker account is blocked")
    if account.get("trade_suspended_by_user"):
        issues.append("broker trading is suspended by user")
    if str(account.get("status", "")).upper() != "ACTIVE":
        issues.append(f"broker account status is {account.get('status')!r}")
    try:
        equity_value = D(account.get("equity"), "account.equity")
        cash_value = D(account.get("cash"), "account.cash")
        if equity_value <= 0 or cash_value < 0:
            issues.append("broker account equity/cash is invalid")
    except RiskRejected as exc:
        issues.append(str(exc))
    for order in open_orders:
        symbol = str(order.get("symbol", "")).upper()
        is_protective = (
            str(order.get("side", "")).lower() == "sell"
            and str(order.get("type", "")).lower() == "trailing_stop"
        )
        if is_protective:
            continue
        client_order_id = str(order.get("client_order_id", ""))
        if client_order_id in owned_order_client_ids:
            if str(order.get("side", "")).lower() == "sell":
                owned_exit_symbols.add(symbol)
            continue
        classification = "gateway-managed" if client_order_id.startswith("bt-") else "unmanaged"
        issues.append(
            f"{symbol or '?'} {classification} open order {order.get('id')} left untouched"
        )
    positions = client.positions()
    position_symbols = {str(item.get("symbol", "")).upper() for item in positions}
    for order in client.orders(status="open"):
        symbol = str(order.get("symbol", "")).upper()
        is_protective = (
            str(order.get("side", "")).lower() == "sell"
            and str(order.get("type", "")).lower() == "trailing_stop"
        )
        if not is_protective or symbol in position_symbols:
            continue
        issues.append(f"{symbol or '?'} orphan protective stop {order.get('id')} left untouched")
    for position in positions:
        symbol = str(position.get("symbol", "")).upper()
        qty = D(position.get("qty"), "position.qty")
        known_instrument = True
        try:
            instrument(policy, symbol)
        except PolicyError as exc:
            issues.append(str(exc))
            known_instrument = False
        if qty == 0:
            issues.append(f"forbidden zero position row: {symbol}")
            continue
        if qty < 0:
            if repair:
                try:
                    result = _emergency_flatten(
                        client=client,
                        policy=policy,
                        agent=agent,
                        symbol=symbol,
                        seed=f"reconcile-forbidden-short-{symbol}",
                        root=root,
                        sleep=time.sleep,
                    )
                    if result["status"] == "flat":
                        repaired.append(f"{symbol}: flattened forbidden short position")
                    else:
                        issues.append(f"{symbol}: forbidden short containment incomplete")
                except (RiskRejected, BrokerError) as exc:
                    issues.append(f"{symbol}: forbidden short containment failed: {exc}")
            else:
                issues.append(f"forbidden short position: {symbol} qty={qty}")
            continue
        if not known_instrument:
            try:
                asset = client.asset(symbol)
                is_equity = (
                    str(asset.get("class", "")) == str(policy.system["allowed_asset_class"])
                    and asset.get("tradable") is True
                )
            except BrokerError as exc:
                issues.append(f"{symbol}: cannot classify unknown held asset: {exc}")
                continue
            if not is_equity:
                if repair:
                    try:
                        result = _emergency_flatten(
                            client=client,
                            policy=policy,
                            agent=agent,
                            symbol=symbol,
                            seed=f"reconcile-forbidden-asset-{symbol}",
                            root=root,
                            sleep=time.sleep,
                        )
                        if result["status"] == "flat":
                            repaired.append(f"{symbol}: flattened forbidden held asset")
                        else:
                            issues.append(f"{symbol}: forbidden asset containment incomplete")
                    except (RiskRejected, BrokerError) as exc:
                        issues.append(f"{symbol}: forbidden asset containment failed: {exc}")
                continue
        if symbol in owned_exit_symbols:
            # The caller owns a live liquidation for this symbol. A competing
            # protective sell would conflict with that order's reserved shares.
            continue
        try:
            held, covered_before = ensure_symbol_protected(
                client=client,
                policy=policy,
                agent=agent,
                symbol=symbol,
                repair=False,
                root=root,
            )
            if held != covered_before:
                if repair:
                    _, covered_after = ensure_symbol_protected(
                        client=client,
                        policy=policy,
                        agent=agent,
                        symbol=symbol,
                        repair=True,
                        root=root,
                    )
                    if covered_after == held:
                        repaired.append(f"{symbol}: restored {held - covered_before} shares of stop coverage")
                    else:
                        issues.append(f"{symbol}: protection remains incomplete")
                else:
                    issues.append(f"{symbol}: stop coverage {covered_before}/{held}")
        except (RiskRejected, BrokerError) as exc:
            if repair:
                try:
                    held, covered_after = ensure_symbol_protected(
                        client=client,
                        policy=policy,
                        agent=agent,
                        symbol=symbol,
                        repair=True,
                        root=root,
                    )
                    if held == covered_after:
                        repaired.append(f"{symbol}: normalized protective-stop configuration")
                    else:
                        issues.append(f"{symbol}: protection remains incomplete")
                except (RiskRejected, BrokerError) as repair_exc:
                    issues.append(f"{exc}; repair failed: {repair_exc}")
            else:
                issues.append(str(exc))
    report = ReconciliationReport(
        ok=not issues,
        equity=str(account.get("equity", "")),
        cash=str(account.get("cash", "")),
        positions=len(positions),
        issues=issues,
        repaired=repaired,
    )
    event(root, "reconciliation", agent=agent, repair=repair, control_status=status, **asdict(report))
    return report


def _record_fill(
    root: Path,
    *,
    agent: str,
    intent: TradeIntent,
    order: dict[str, Any],
    stops: list[dict[str, Any]],
) -> None:
    trade_path = _agent_memory(root, agent) / "trades.jsonl"
    order_id = str(order.get("id", ""))
    if trade_path.exists() and f'"broker_order_id":"{order_id}"' in trade_path.read_text(
        encoding="utf-8"
    ).replace(" ", ""):
        return
    _append_jsonl(
        trade_path,
        {
            "ts": order.get("filled_at") or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "agent": agent,
            "action": "buy",
            "symbol": intent.symbol,
            "qty": float(D(order.get("filled_qty"), "filled_qty")),
            "fill_price": float(D(order.get("filled_avg_price"), "filled_avg_price")),
            "thesis": intent.thesis,
            "invalidation": intent.invalidation,
            "review_by": intent.review_by.isoformat(),
            "sector": intent.sector,
            "broker_order_id": order_id,
            "client_order_id": order.get("client_order_id"),
            "protective_order_id": stops[0].get("id") if stops else None,
            "protective_order_ids": [item.get("id") for item in stops],
        },
    )


def _record_sell_fill(
    root: Path,
    *,
    agent: str,
    symbol: str,
    trigger: str,
    reason: str,
    order: dict[str, Any],
) -> None:
    trade_path = _agent_memory(root, agent) / "trades.jsonl"
    order_id = str(order.get("id", ""))
    if trade_path.exists() and f'"broker_order_id":"{order_id}"' in trade_path.read_text(
        encoding="utf-8"
    ).replace(" ", ""):
        return
    _append_jsonl(
        trade_path,
        {
            "ts": order.get("filled_at")
            or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "agent": agent,
            "action": "sell",
            "symbol": symbol,
            "qty": float(D(order.get("filled_qty"), "filled_qty")),
            "fill_price": float(D(order.get("filled_avg_price"), "filled_avg_price")),
            "trigger": trigger,
            "reason": reason,
            "broker_order_id": order_id,
            "client_order_id": order.get("client_order_id"),
        },
    )


def _submit_idempotent(client: AlpacaClient, body: dict[str, Any]) -> dict[str, Any]:
    client_order_id = str(body["client_order_id"])
    existing = client.order_by_client_id(client_order_id)
    if existing is not None:
        _assert_order_role(
            existing,
            client_order_id=client_order_id,
            symbol=str(body["symbol"]),
            side=str(body["side"]),
            order_type=str(body["type"]),
        )
        _assert_order_qty(existing, body.get("qty"))
        return existing
    try:
        submitted = client.submit_order(body)
        _assert_order_role(
            submitted,
            client_order_id=client_order_id,
            symbol=str(body["symbol"]),
            side=str(body["side"]),
            order_type=str(body["type"]),
        )
        _assert_order_qty(submitted, body.get("qty"))
        return submitted
    except BrokerError as exc:
        try:
            recovered = client.order_by_client_id(client_order_id)
        except BrokerError as lookup_exc:
            raise BrokerError(
                f"broker outcome unknown for client_order_id {client_order_id}"
            ) from lookup_exc
        if recovered is not None:
            _assert_order_role(
                recovered,
                client_order_id=client_order_id,
                symbol=str(body["symbol"]),
                side=str(body["side"]),
                order_type=str(body["type"]),
            )
            _assert_order_qty(recovered, body.get("qty"))
            return recovered
        raise exc


def _safe_record_buy(
    root: Path,
    *,
    agent: str,
    intent: TradeIntent,
    order: dict[str, Any],
    stops: list[dict[str, Any]],
) -> str | None:
    try:
        _record_fill(root, agent=agent, intent=intent, order=order, stops=stops)
    except (OSError, RiskRejected) as exc:
        return f"trade ledger write failed: {exc}"
    return None


def _safe_record_sell(
    root: Path,
    *,
    agent: str,
    symbol: str,
    trigger: str,
    reason: str,
    order: dict[str, Any],
) -> str | None:
    try:
        _record_sell_fill(
            root,
            agent=agent,
            symbol=symbol,
            trigger=trigger,
            reason=reason,
            order=order,
        )
    except (OSError, RiskRejected) as exc:
        return f"trade ledger write failed: {exc}"
    return None


def _emergency_flatten(
    *,
    client: AlpacaClient,
    policy: Policy,
    agent: str,
    symbol: str,
    seed: str,
    root: Path,
    sleep: Callable[[float], None],
) -> dict[str, Any]:
    def contain_residual() -> tuple[Decimal, Decimal]:
        residual = _position(client, symbol)
        if not residual:
            return Decimal("0"), Decimal("0")
        residual_qty = D(residual.get("qty"), "position.qty")
        if residual_qty < 0:
            raise BrokerError(f"forbidden residual short remains in {symbol}: {residual_qty}")
        held, covered = ensure_symbol_protected(
            client=client,
            policy=policy,
            agent=agent,
            symbol=symbol,
            repair=True,
            root=root,
        )
        if held != covered:
            raise BrokerError(f"emergency liquidation left {held} unprotected {symbol} shares")
        return held, covered

    timeout = int(policy.system["fill_timeout_seconds"])
    attempts = int(policy.system["maximum_exit_attempts"])
    last_order: dict[str, Any] | None = None
    try:
        for stop in _open_stop_orders(client, symbol):
            _cancel_and_confirm(client, stop, timeout, sleep=sleep)
        for attempt in range(1, attempts + 1):
            position = _position(client, symbol)
            if not position:
                return {"status": "flat", "order": last_order}
            signed_qty = D(position.get("qty"), "position.qty")
            if signed_qty == 0:
                raise BrokerError(f"broker returned a zero-quantity position for {symbol}")
            side = "sell" if signed_qty > 0 else "buy"
            order_qty = abs(signed_qty)
            emergency_id = _client_id(
                f"{agent}-emergency-{symbol}-a{attempt}",
                {"seed": seed, "symbol": symbol, "side": side, "qty": str(order_qty)},
            )
            order = _submit_idempotent(
                client,
                {
                    "symbol": symbol,
                    "qty": str(order_qty),
                    "side": side,
                    "type": "market",
                    "time_in_force": "day",
                    "client_order_id": emergency_id,
                },
            )
            order = _poll_order(client, order, timeout, sleep=sleep)
            if str(order.get("status", "")).lower() in OPEN_ORDER_STATUSES:
                order = _cancel_and_confirm(client, order, timeout, sleep=sleep)
            last_order = order
            event(
                root,
                "emergency_liquidation_attempt",
                agent=agent,
                symbol=symbol,
                attempt=attempt,
                side=side,
                order_id=order.get("id"),
                filled_qty=str(order.get("filled_qty", "0")),
                status=order.get("status"),
            )
        held, _ = contain_residual()
        if held > 0:
            return {
                "status": "residual_protected",
                "remaining_qty": str(held),
                "order": last_order,
            }
        return {"status": "flat", "order": last_order}
    except Exception as exc:
        try:
            contain_residual()
        except Exception as containment_exc:
            raise BrokerError(
                f"emergency liquidation failed and residual {symbol} could not be contained"
            ) from containment_exc
        raise exc


def _completed_buy_result(
    *,
    client: AlpacaClient,
    policy: Policy,
    agent: str,
    intent: TradeIntent,
    order: dict[str, Any],
    root: Path,
    repair: bool,
) -> dict[str, Any]:
    position = _position(client, intent.symbol)
    stops: list[dict[str, Any]] = []
    if position:
        held, covered = ensure_symbol_protected(
            client=client,
            policy=policy,
            agent=agent,
            symbol=intent.symbol,
            repair=repair,
            root=root,
        )
        if held != covered:
            raise RiskRejected(f"{intent.symbol} is not fully protected: {covered}/{held}")
        stops = _open_stop_orders(client, intent.symbol)
        status = "already_executed_open"
    else:
        status = "already_executed_closed"
    warning = _safe_record_buy(
        root,
        agent=agent,
        intent=intent,
        order=order,
        stops=stops,
    )
    result = {
        "status": status,
        "symbol": intent.symbol,
        "filled_qty": str(order.get("filled_qty", "0")),
        "fill_price": str(order.get("filled_avg_price")),
        "entry_order_id": order.get("id"),
        "client_order_id": order.get("client_order_id"),
        "protective_order_ids": [item.get("id") for item in stops],
    }
    if warning:
        result["audit_warning"] = warning
    return result


def execute_buy(
    *,
    client: AlpacaClient,
    policy: Policy,
    agent: str,
    intent: TradeIntent,
    now: datetime,
    control_path: Path,
    root: Path = ROOT,
    dry_run: bool = False,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    if agent != policy.agent_name:
        raise RiskRejected("execution agent does not match loaded policy")
    # One entry identity per agent/date/symbol. Narrative or quantity edits after a
    # fill must never manufacture a fresh broker identity and buy the symbol again.
    base_payload = {
        "agent": agent,
        "plan_date": intent.plan_date.isoformat(),
        "action": "buy",
        "symbol": intent.symbol,
    }
    attempts = int(policy.system["maximum_entry_attempts"])
    client_ids = [
        _client_id(
            f"{agent}-{intent.plan_date.isoformat()}-{intent.symbol}-a{attempt}",
            base_payload,
        )
        for attempt in range(1, attempts + 1)
    ]
    preflight = reconcile(
        client=client,
        policy=policy,
        agent=agent,
        repair=not dry_run,
        control_path=control_path,
        root=root,
        owned_order_client_ids=set(client_ids),
    )
    if not preflight.ok:
        raise RiskRejected(f"broker reconciliation failed: {'; '.join(preflight.issues)}")
    timeout = int(policy.system["fill_timeout_seconds"])
    existing_attempts: list[dict[str, Any] | None] = []
    for client_order_id in client_ids:
        existing = client.order_by_client_id(client_order_id)
        if existing:
            _assert_order_role(
                existing,
                client_order_id=client_order_id,
                symbol=intent.symbol,
                side="buy",
                order_type="limit",
            )
            _assert_order_qty(existing, intent.qty)
        existing_attempts.append(existing)
    _assert_contiguous_attempt_history(
        existing_attempts,
        f"{agent} {intent.plan_date.isoformat()} buy {intent.symbol}",
    )
    for attempt, (client_order_id, existing) in enumerate(
        zip(client_ids, existing_attempts), start=1
    ):
        if existing and D(existing.get("filled_qty", 0), "filled_qty") > 0:
            if str(existing.get("status", "")).lower() in OPEN_ORDER_STATUSES:
                if dry_run:
                    raise RiskRejected(
                        f"{intent.symbol} has a partially filled live entry; "
                        "dry-run cannot recover it safely"
                    )
                existing = _poll_order(client, existing, timeout, sleep=sleep)
                if str(existing.get("status", "")).lower() in OPEN_ORDER_STATUSES:
                    existing = _cancel_and_confirm(client, existing, timeout, sleep=sleep)
            return _completed_buy_result(
                client=client,
                policy=policy,
                agent=agent,
                intent=intent,
                order=existing,
                root=root,
                repair=not dry_run,
            )
        if existing is None:
            approval = approve_buy(
                client=client,
                policy=policy,
                intent=intent,
                now=now,
                control_path=control_path,
            )
            if dry_run:
                return {
                    "status": "approved",
                    "client_order_id": client_order_id,
                    "limit_price": str(approval.limit_price),
                    "notional": str(approval.notional),
                    "position_pct_after": str(approval.position_pct_after),
                    "sector_pct_after": str(approval.sector_pct_after),
                    "daily_buy_pct_after": str(approval.daily_buy_pct_after),
                    "drawdown_pct": str(approval.drawdown_pct),
                }
            event(
                root,
                "buy_preflight_approved",
                agent=agent,
                symbol=intent.symbol,
                attempt=attempt,
                client_order_id=client_order_id,
                limit_price=str(approval.limit_price),
                notional=str(approval.notional),
            )
            existing = _submit_idempotent(
                client,
                {
                    "symbol": intent.symbol,
                    "qty": str(intent.qty),
                    "side": "buy",
                    "type": "limit",
                    "limit_price": str(approval.limit_price),
                    "time_in_force": "day",
                    "client_order_id": client_order_id,
                },
            )
            event(
                root,
                "entry_order_accepted",
                agent=agent,
                symbol=intent.symbol,
                attempt=attempt,
                order_id=existing.get("id"),
                client_order_id=client_order_id,
            )

        order = _poll_order(client, existing, timeout, sleep=sleep)
        if str(order.get("status", "")).lower() in OPEN_ORDER_STATUSES:
            order = _cancel_and_confirm(client, order, timeout, sleep=sleep)
        status = str(order.get("status", "")).lower()
        filled_qty = D(order.get("filled_qty", 0), "filled_qty")
        if filled_qty <= 0:
            event(
                root,
                "entry_attempt_unfilled",
                agent=agent,
                symbol=intent.symbol,
                attempt=attempt,
                status=status,
            )
            continue

        try:
            stop = place_trailing_stop(
                client=client,
                policy=policy,
                agent=agent,
                symbol=intent.symbol,
                qty=filled_qty,
                seed=f"{client_order_id}-stop",
                root=root,
            )
        except Exception as exc:
            event(
                root,
                "protective_stop_failed",
                agent=agent,
                symbol=intent.symbol,
                entry_order_id=order.get("id"),
                error=str(exc),
            )
            emergency = _emergency_flatten(
                client=client,
                policy=policy,
                agent=agent,
                symbol=intent.symbol,
                seed=f"entry-{order.get('id')}-stop-failure",
                root=root,
                sleep=sleep,
            )
            raise BrokerError(
                f"protective stop failed; emergency liquidation result: {emergency['status']}"
            ) from exc

        warning = _safe_record_buy(
            root,
            agent=agent,
            intent=intent,
            order=order,
            stops=[stop],
        )
        event(
            root,
            "buy_complete",
            agent=agent,
            symbol=intent.symbol,
            qty=str(filled_qty),
            fill_price=str(order.get("filled_avg_price")),
            entry_order_id=order.get("id"),
            protective_order_id=stop.get("id"),
        )
        result = {
            "status": "filled" if filled_qty == intent.qty else "partially_filled",
            "symbol": intent.symbol,
            "filled_qty": str(filled_qty),
            "fill_price": str(order.get("filled_avg_price")),
            "entry_order_id": order.get("id"),
            "client_order_id": client_order_id,
            "protective_order_id": stop.get("id"),
        }
        if warning:
            result["audit_warning"] = warning
        return result
    raise BrokerError(f"{intent.symbol} did not fill after {attempts} bounded attempts")


def execute_sell(
    *,
    client: AlpacaClient,
    policy: Policy,
    agent: str,
    symbol: str,
    qty: Decimal,
    trigger: str,
    reason: str,
    intent: TradeIntent | None,
    now: datetime,
    control_path: Path,
    root: Path = ROOT,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    if agent != policy.agent_name:
        raise RiskRejected("execution agent does not match loaded policy")
    assert_mutation_allowed(control_path, opening=False)
    symbol = symbol.upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9.\-]{0,9}", symbol):
        raise RiskRejected(f"invalid liquidation symbol: {symbol!r}")
    if trigger not in {"planned", "midday_loss"}:
        raise RiskRejected("sell trigger must be planned or midday_loss")
    if len(reason.strip()) < 15 or len(reason) > 1000:
        raise RiskRejected("sell reason must be specific and no longer than 1000 characters")
    qty = D(qty, "sell.qty")
    if qty <= 0 or qty != qty.to_integral_value():
        raise RiskRejected("sell quantity must be positive whole shares")
    if trigger == "planned":
        instrument(policy, symbol)
        if intent is None or intent.action not in {"trim", "exit"}:
            raise RiskRejected("planned sell requires today's trim/exit intent")
        if intent.symbol != symbol or intent.qty != qty:
            raise RiskRejected("sell request does not exactly match today's plan")
    if client.clock().get("is_open") is not True:
        raise RiskRejected("market is closed")

    local = now.astimezone(ZoneInfo(str(policy.system["timezone"])))
    # One immutable operation per trigger/symbol/session. Narrative, review date,
    # action wording, and requested remainder must not mint a second liquidation.
    payload = {
        "agent": agent,
        "date": local.date().isoformat(),
        "symbol": symbol,
        "operation": "planned_sell" if trigger == "planned" else "midday_loss_exit",
    }
    attempts = int(policy.system["maximum_exit_attempts"])
    client_ids = [
        _client_id(f"{agent}-sell-{symbol}-a{attempt}", payload)
        for attempt in range(1, attempts + 1)
    ]
    preflight = reconcile(
        client=client,
        policy=policy,
        agent=agent,
        repair=True,
        control_path=control_path,
        root=root,
        owned_order_client_ids=set(client_ids),
    )
    if not preflight.ok:
        raise RiskRejected(f"broker reconciliation failed: {'; '.join(preflight.issues)}")

    position = _position(client, symbol)
    existing_orders: list[dict[str, Any] | None] = []
    for client_order_id in client_ids:
        existing = client.order_by_client_id(client_order_id)
        if existing:
            existing = _follow_replacement(client, existing)
            _assert_order_role(
                existing,
                client_order_id=client_order_id,
                symbol=symbol,
                side="sell",
                order_type="market",
            )
        existing_orders.append(existing)
    _assert_contiguous_attempt_history(
        existing_orders,
        f"{agent} {local.date().isoformat()} {trigger} sell {symbol}",
    )
    first_order = existing_orders[0]
    target_qty = D(first_order.get("qty"), "initial sell target") if first_order else qty
    if trigger == "planned" and target_qty != qty:
        raise RiskRejected(
            f"planned sell target changed after execution began: {qty} vs {target_qty}"
        )
    initial_filled = sum(
        (D(order.get("filled_qty", 0), "filled_qty") for order in existing_orders if order),
        Decimal("0"),
    )
    if initial_filled > target_qty:
        raise BrokerError(f"sell operation overfilled its immutable target: {initial_filled}/{target_qty}")
    if not position:
        if initial_filled > 0:
            return {
                "status": "already_executed",
                "symbol": symbol,
                "filled_qty": str(initial_filled),
                "target_qty": str(target_qty),
                "order_ids": [order.get("id") for order in existing_orders if order],
            }
        raise RiskRejected(f"no open position in {symbol}")
    held_qty = D(position.get("qty"), "position.qty")
    if held_qty <= 0:
        raise RiskRejected(f"cannot submit a sell against non-long {symbol} qty={held_qty}")
    if trigger == "planned" and intent:
        if intent.action == "trim" and qty >= held_qty and first_order is None:
            raise RiskRejected("planned trim must be strictly smaller than the current holding")
        if intent.action == "exit" and first_order is None and qty != held_qty:
            raise RiskRejected("planned exit must close the full position")
    if trigger == "midday_loss":
        if first_order is None:
            if qty != held_qty:
                raise RiskRejected("midday loss cut must close the full current position")
            pnl_pct = D(position.get("unrealized_plpc"), "position.unrealized_plpc") * 100
            threshold = -D(policy.agent["midday_loss_cut_pct"], "midday_loss_cut_pct")
            if pnl_pct > threshold:
                raise RiskRejected(f"midday cut not triggered: P/L is {pnl_pct:.3f}%")
        elif qty != target_qty:
            raise RiskRejected(
                f"midday loss target changed after execution began: {qty} vs {target_qty}"
            )

    start_day = datetime.combine(local.date(), datetime.min.time(), tzinfo=local.tzinfo)
    if trigger == "planned" and any(
        str(order.get("symbol", "")).upper() == symbol
        and str(order.get("side", "")).lower() == "buy"
        and D(order.get("filled_qty", 0), "filled_qty") > 0
        for order in client.orders(after=start_day)
    ):
        raise RiskRejected(f"day-trade guard: {symbol} was bought today")

    timeout = int(policy.system["fill_timeout_seconds"])
    cumulative_filled = Decimal("0")
    completed_orders: list[dict[str, Any]] = []
    warnings: list[str] = []
    submitted_this_call = False

    def contain_remaining(active_order: dict[str, Any] | None, client_order_id: str) -> None:
        if active_order is not None:
            try:
                live = _follow_replacement(client, client.order(str(active_order["id"])))
                if str(live.get("status", "")).lower() in OPEN_ORDER_STATUSES:
                    # A live market liquidation owns these shares. Do not create a
                    # competing stop or second sell while its outcome is unresolved.
                    return
            except BrokerError:
                raise
        try:
            remaining = _position(client, symbol)
            if not remaining:
                return
            held, covered = ensure_symbol_protected(
                client=client,
                policy=policy,
                agent=agent,
                symbol=symbol,
                repair=True,
                root=root,
            )
            if held != covered:
                raise BrokerError(f"stop coverage remains incomplete: {covered}/{held}")
        except Exception as protection_exc:
            emergency = _emergency_flatten(
                client=client,
                policy=policy,
                agent=agent,
                symbol=symbol,
                seed=f"sell-{client_order_id}-protection-failure",
                root=root,
                sleep=sleep,
            )
            raise BrokerError(
                f"remaining-position protection failed; emergency result: {emergency['status']}"
            ) from protection_exc

    for attempt, client_order_id in enumerate(client_ids, start=1):
        remaining_target = target_qty - cumulative_filled
        if remaining_target <= 0:
            break
        order = client.order_by_client_id(client_order_id)
        if order:
            order = _follow_replacement(client, order)
            _assert_order_role(
                order,
                client_order_id=client_order_id,
                symbol=symbol,
                side="sell",
                order_type="market",
            )
            _assert_order_qty(order, remaining_target)
        if order is None:
            refreshed = _position(client, symbol)
            if not refreshed:
                break
            refreshed_qty = D(refreshed.get("qty"), "position.qty")
            if refreshed_qty <= 0:
                raise RiskRejected(f"position changed to non-long qty {refreshed_qty}")
            if refreshed_qty > remaining_target:
                if trigger == "planned" and intent and intent.action == "trim":
                    order_qty = remaining_target
                else:
                    raise RiskRejected(
                        f"position increased during liquidation: held {refreshed_qty}, "
                        f"remaining target {remaining_target}"
                    )
            else:
                order_qty = refreshed_qty
            if trigger == "planned" and intent and intent.action == "trim" and order_qty >= refreshed_qty:
                raise RiskRejected("planned trim must leave a positive residual holding")
        else:
            order_qty = D(order.get("qty"), "order.qty")

        active_order: dict[str, Any] | None = order
        try:
            if order is None or str(order.get("status", "")).lower() in OPEN_ORDER_STATUSES:
                for stop in _open_stop_orders(client, symbol):
                    _cancel_and_confirm(client, stop, timeout, sleep=sleep)
            if order is None:
                refreshed = _position(client, symbol)
                if not refreshed:
                    break
                refreshed_qty = D(refreshed.get("qty"), "position.qty")
                if order_qty > refreshed_qty:
                    raise RiskRejected(
                        f"position changed during stop cancellation: requested {order_qty}, "
                        f"held {refreshed_qty}"
                    )
                if trigger == "planned" and intent and intent.action == "trim" and order_qty >= refreshed_qty:
                    raise RiskRejected("planned trim must leave a positive residual holding")
                order = _submit_idempotent(
                    client,
                    {
                        "symbol": symbol,
                        "qty": str(order_qty),
                        "side": "sell",
                        "type": "market",
                        "time_in_force": "day",
                        "client_order_id": client_order_id,
                    },
                )
                active_order = order
                submitted_this_call = True
            order = _poll_order(client, order, timeout, sleep=sleep)
            active_order = order
            if str(order.get("status", "")).lower() in OPEN_ORDER_STATUSES:
                order = _cancel_and_confirm(client, order, timeout, sleep=sleep)
                active_order = order
        finally:
            contain_remaining(active_order, client_order_id)

        filled_qty = D(order.get("filled_qty", 0), "filled_qty")
        if filled_qty > order_qty:
            raise BrokerError(f"sell attempt overfilled: {filled_qty}/{order_qty}")
        cumulative_filled += filled_qty
        completed_orders.append(order)
        if filled_qty > 0:
            warning = _safe_record_sell(
                root,
                agent=agent,
                symbol=symbol,
                trigger=trigger,
                reason=reason,
                order=order,
            )
            if warning:
                warnings.append(warning)
        event(
            root,
            "sell_attempt_complete",
            agent=agent,
            symbol=symbol,
            attempt=attempt,
            filled_qty=str(filled_qty),
            cumulative_filled_qty=str(cumulative_filled),
            target_qty=str(target_qty),
            trigger=trigger,
            reason=reason,
            order_id=order.get("id"),
            client_order_id=client_order_id,
        )

    remaining_position = _position(client, symbol)
    complete = cumulative_filled >= target_qty or not remaining_position
    result: dict[str, Any] = {
        "status": (
            "filled"
            if complete and submitted_this_call
            else "already_executed"
            if complete
            else "partially_filled"
        ),
        "symbol": symbol,
        "filled_qty": str(cumulative_filled),
        "target_qty": str(target_qty),
        "remaining_target_qty": str(max(target_qty - cumulative_filled, Decimal("0"))),
        "order_id": completed_orders[-1].get("id") if completed_orders else None,
        "order_ids": [order.get("id") for order in completed_orders],
        "client_order_ids": [order.get("client_order_id") for order in completed_orders],
    }
    if not remaining_position and cumulative_filled < target_qty:
        result["status"] = "closed_by_protective_stop"
    if warnings:
        result["audit_warning"] = "; ".join(sorted(set(warnings)))
    return result
