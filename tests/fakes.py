from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

from bulltrader.alpaca import BrokerError, Quote


class FakeAlpaca:
    def __init__(self, now: datetime):
        self.now = now
        self.account_data: dict[str, Any] = {
            "id": "paper-bull-account",
            "status": "ACTIVE",
            "trading_blocked": False,
            "account_blocked": False,
            "equity": "100000",
            "cash": "50000",
            "last_equity": "100000",
        }
        self.position_data: list[dict[str, Any]] = []
        self.order_data: list[dict[str, Any]] = []
        self.by_client_id: dict[str, dict[str, Any]] = {}
        self.by_order_id: dict[str, dict[str, Any]] = {}
        self.submissions: list[dict[str, Any]] = []
        self.cancellations: list[str] = []
        self.replacements: list[dict[str, Any]] = []
        self.quote_data = Quote(
            bid=Decimal("99.90"),
            ask=Decimal("100"),
            timestamp=now.astimezone(timezone.utc),
        )
        self.history_data = {"equity": ["100000", "100000"]}
        self.fail_stop = False
        self.fail_replace = False
        self.fail_cancel_statuses: set[str] = set()
        self.market_fill_fraction = Decimal("1")
        self.market_fill_fractions: list[Decimal] = []

    def seed_order(self, **values):
        number = len(self.order_data) + 1
        item = {
            "id": f"seed-{number}",
            "symbol": "ETN",
            "qty": "1",
            "filled_qty": "0",
            "filled_avg_price": None,
            "side": "buy",
            "type": "limit",
            "limit_price": "100",
            "time_in_force": "day",
            "status": "new",
            "client_order_id": f"seed-client-{number}",
            **values,
        }
        self.order_data.append(item)
        self.by_order_id[item["id"]] = item
        self.by_client_id[item["client_order_id"]] = item
        return item

    def account(self):
        return dict(self.account_data)

    def positions(self):
        return [dict(item) for item in self.position_data]

    def clock(self):
        return {"is_open": True}

    def asset(self, symbol):
        return {"symbol": symbol, "status": "active", "tradable": True, "class": "us_equity"}

    def quote(self, symbol):
        return self.quote_data

    def portfolio_history(self):
        return self.history_data

    def calendar(self, start: str, end: str):
        first = date.fromisoformat(start)
        last = date.fromisoformat(end)
        rows = []
        cursor = first
        while cursor <= last:
            if cursor.weekday() < 5:
                rows.append({"date": cursor.isoformat()})
            cursor += timedelta(days=1)
        return rows

    def orders(self, *, status="all", after=None, limit=500):
        if status == "open":
            return [
                dict(item)
                for item in self.order_data
                if item.get("status")
                in {
                    "new",
                    "accepted",
                    "partially_filled",
                    "pending_cancel",
                    "suspended",
                    "stopped",
                    "done_for_day",
                    "calculated",
                }
            ]
        return [dict(item) for item in self.order_data]

    def order_by_client_id(self, client_order_id):
        item = self.by_client_id.get(client_order_id)
        return dict(item) if item else None

    def order(self, order_id):
        return dict(self.by_order_id[order_id])

    def submit_order(self, body):
        if body["type"] == "trailing_stop" and self.fail_stop:
            raise BrokerError("simulated stop failure")
        number = len(self.order_data) + 1
        is_stop = body["type"] == "trailing_stop"
        filled_qty = Decimal("0") if is_stop else Decimal(str(body["qty"]))
        if body["side"] == "sell" and body["type"] == "market":
            fraction = (
                self.market_fill_fractions.pop(0)
                if self.market_fill_fractions
                else self.market_fill_fraction
            )
            filled_qty *= fraction
        status = "new" if is_stop else "filled"
        if not is_stop and filled_qty < Decimal(str(body["qty"])):
            status = "canceled"
        item = {
            **body,
            "id": f"order-{number}",
            "status": status,
            "filled_qty": str(filled_qty),
            "filled_avg_price": None if is_stop else body.get("limit_price", "99"),
            "filled_at": self.now.isoformat(),
        }
        self.submissions.append(dict(body))
        self.by_client_id[body["client_order_id"]] = item
        self.by_order_id[item["id"]] = item
        self.order_data.append(item)
        if body["side"] == "buy" and body["type"] == "limit":
            current = next(
                (item for item in self.position_data if item["symbol"] == body["symbol"]),
                None,
            )
            if current:
                current["qty"] = str(Decimal(current["qty"]) + Decimal(body["qty"]))
                current["market_value"] = str(
                    Decimal(current["market_value"])
                    + Decimal(body["qty"]) * Decimal(body["limit_price"])
                )
            else:
                self.position_data.append(
                    {
                        "symbol": body["symbol"],
                        "qty": body["qty"],
                        "market_value": str(Decimal(body["qty"]) * Decimal(body["limit_price"])),
                        "unrealized_plpc": "0",
                    }
                )
        if body["side"] == "sell" and body["type"] == "market" and filled_qty > 0:
            current = next(
                (item for item in self.position_data if item["symbol"] == body["symbol"]),
                None,
            )
            if current:
                old_qty = Decimal(current["qty"])
                new_qty = old_qty - filled_qty
                if new_qty <= 0:
                    self.position_data.remove(current)
                else:
                    current["qty"] = str(new_qty)
                    current["market_value"] = str(
                        Decimal(current["market_value"]) * new_qty / old_qty
                    )
        if body["side"] == "buy" and body["type"] == "market" and filled_qty > 0:
            current = next(
                (item for item in self.position_data if item["symbol"] == body["symbol"]),
                None,
            )
            if current and Decimal(current["qty"]) < 0:
                old_qty = Decimal(current["qty"])
                new_qty = old_qty + filled_qty
                if new_qty >= 0:
                    self.position_data.remove(current)
                else:
                    current["qty"] = str(new_qty)
                    current["market_value"] = str(abs(new_qty) * Decimal("99"))
        return dict(item)

    def cancel_order(self, order_id):
        if self.by_order_id[order_id].get("status") in self.fail_cancel_statuses:
            raise BrokerError("simulated cancellation failure")
        self.cancellations.append(order_id)
        self.by_order_id[order_id]["status"] = "canceled"

    def replace_order(self, order_id, body):
        if self.fail_replace:
            raise BrokerError("simulated replacement failure")
        old = self.by_order_id[order_id]
        number = len(self.order_data) + 1
        replacement = {
            **old,
            "id": f"order-{number}",
            "qty": body.get("qty", old["qty"]),
            "time_in_force": body.get("time_in_force", old.get("time_in_force")),
            "client_order_id": body["client_order_id"],
            "filled_qty": "0",
            "filled_avg_price": None,
            "status": "new",
            "replaces": order_id,
        }
        if "trail" in body:
            replacement["trail_percent"] = body["trail"]
        old["status"] = "replaced"
        old["replaced_by"] = replacement["id"]
        self.order_data.append(replacement)
        self.by_order_id[replacement["id"]] = replacement
        self.by_client_id[replacement["client_order_id"]] = replacement
        self.replacements.append(dict(body))
        return dict(replacement)
