from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from .policy import Policy


class BrokerError(RuntimeError):
    pass


@dataclass(frozen=True)
class Quote:
    bid: Decimal
    ask: Decimal
    timestamp: datetime


class AlpacaClient:
    def __init__(
        self,
        key: str,
        secret: str,
        base_url: str,
        policy: Policy,
        expected_account_id: str,
    ):
        expected = str(policy.system["paper_base_url"]).rstrip("/")
        actual = base_url.rstrip("/")
        if actual != expected:
            raise BrokerError(f"refusing non-canonical endpoint {actual!r}; expected {expected!r}")
        if not key or not secret:
            raise BrokerError("missing Alpaca credentials")
        if not expected_account_id.strip():
            raise BrokerError("missing ALPACA_EXPECTED_ACCOUNT_ID")
        self.key = key
        self.secret = secret
        self.expected_account_id = expected_account_id.strip().lower()
        self._account_verified = False
        self.base_url = actual
        self.data_url = str(policy.system["market_data_base_url"]).rstrip("/")
        self.feed = str(policy.system["market_data_feed"])

    @classmethod
    def from_env(cls, policy: Policy) -> "AlpacaClient":
        return cls(
            key=os.environ.get("ALPACA_API_KEY_ID", ""),
            secret=os.environ.get("ALPACA_API_SECRET_KEY", ""),
            base_url=os.environ.get("ALPACA_BASE_URL", ""),
            policy=policy,
            expected_account_id=os.environ.get("ALPACA_EXPECTED_ACCOUNT_ID", ""),
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        data_api: bool = False,
        allow_404: bool = False,
    ) -> Any:
        base = self.data_url if data_api else self.base_url
        query = urllib.parse.urlencode(
            {k: str(v) for k, v in (params or {}).items() if v is not None}
        )
        url = f"{base}{path}" + (f"?{query}" if query else "")
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "APCA-API-KEY-ID": self.key,
                "APCA-API-SECRET-KEY": self.secret,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "bull-risk-gateway/1",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                payload = response.read()
        except urllib.error.HTTPError as exc:
            payload = exc.read().decode("utf-8", errors="replace")
            if allow_404 and exc.code == 404:
                return None
            raise BrokerError(f"Alpaca {method} {path} failed ({exc.code}): {payload[:500]}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise BrokerError(f"Alpaca {method} {path} failed: {exc}") from exc
        if not payload:
            return None
        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:
            raise BrokerError(f"Alpaca {method} {path} returned invalid JSON") from exc

    @staticmethod
    def _dict(value: Any, context: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise BrokerError(f"Alpaca {context} returned an unexpected payload shape")
        return value

    @staticmethod
    def _rows(value: Any, context: str) -> list[dict[str, Any]]:
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            raise BrokerError(f"Alpaca {context} returned an unexpected payload shape")
        return value

    def account(self) -> dict[str, Any]:
        account = self._dict(self._request("GET", "/v2/account"), "account")
        actual = str(account.get("id", "")).strip().lower()
        if not actual:
            raise BrokerError("Alpaca account response has no account ID")
        if actual != self.expected_account_id:
            raise BrokerError("Alpaca account ID does not match the configured agent account")
        self._account_verified = True
        return account

    def _require_verified_account(self) -> None:
        if not self._account_verified:
            self.account()

    def positions(self) -> list[dict[str, Any]]:
        self._require_verified_account()
        return self._rows(self._request("GET", "/v2/positions"), "positions")

    def clock(self) -> dict[str, Any]:
        self._require_verified_account()
        return self._dict(self._request("GET", "/v2/clock"), "clock")

    def asset(self, symbol: str) -> dict[str, Any]:
        self._require_verified_account()
        return self._dict(
            self._request("GET", f"/v2/assets/{urllib.parse.quote(symbol)}"),
            f"asset {symbol}",
        )

    def quote(self, symbol: str) -> Quote:
        self._require_verified_account()
        result = self._request(
            "GET",
            f"/v2/stocks/{urllib.parse.quote(symbol)}/quotes/latest",
            params={"feed": self.feed},
            data_api=True,
        )
        result = self._dict(result, f"latest quote {symbol}")
        raw = self._dict(result.get("quote"), f"latest quote {symbol}")
        try:
            bid = Decimal(str(raw["bp"]))
            ask = Decimal(str(raw["ap"]))
            timestamp = datetime.fromisoformat(str(raw["t"]).replace("Z", "+00:00"))
        except (KeyError, ValueError, InvalidOperation) as exc:
            raise BrokerError(f"latest quote for {symbol} is incomplete") from exc
        if (
            not bid.is_finite()
            or not ask.is_finite()
            or bid <= 0
            or ask <= 0
            or ask < bid
            or timestamp.tzinfo is None
        ):
            raise BrokerError(f"latest quote for {symbol} is invalid")
        return Quote(bid=bid, ask=ask, timestamp=timestamp.astimezone(timezone.utc))

    def orders(
        self,
        *,
        status: str = "all",
        after: datetime | None = None,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        self._require_verified_account()
        params: dict[str, Any] = {"status": status, "limit": limit, "direction": "asc"}
        if after:
            params["after"] = after.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        return self._rows(self._request("GET", "/v2/orders", params=params), "orders")

    def order(self, order_id: str) -> dict[str, Any]:
        self._require_verified_account()
        return self._dict(
            self._request("GET", f"/v2/orders/{urllib.parse.quote(order_id)}"),
            f"order {order_id}",
        )

    def order_by_client_id(self, client_order_id: str) -> dict[str, Any] | None:
        self._require_verified_account()
        result = self._request(
            "GET",
            "/v2/orders:by_client_order_id",
            params={"client_order_id": client_order_id},
            allow_404=True,
        )
        return None if result is None else self._dict(result, f"client order {client_order_id}")

    def submit_order(self, body: dict[str, Any]) -> dict[str, Any]:
        self._require_verified_account()
        return self._dict(self._request("POST", "/v2/orders", body=body), "order submission")

    def cancel_order(self, order_id: str) -> None:
        self._require_verified_account()
        self._request("DELETE", f"/v2/orders/{urllib.parse.quote(order_id)}")

    def replace_order(self, order_id: str, body: dict[str, Any]) -> dict[str, Any]:
        self._require_verified_account()
        return self._dict(
            self._request(
                "PATCH",
                f"/v2/orders/{urllib.parse.quote(order_id)}",
                body=body,
            ),
            f"order replacement {order_id}",
        )

    def portfolio_history(self) -> dict[str, Any]:
        self._require_verified_account()
        return self._dict(
            self._request(
                "GET",
                "/v2/account/portfolio/history",
                params={"period": "1A", "timeframe": "1D", "intraday_reporting": "market_hours"},
            ),
            "portfolio history",
        )

    def calendar(self, start: str, end: str) -> list[dict[str, Any]]:
        self._require_verified_account()
        return self._rows(
            self._request("GET", "/v2/calendar", params={"start": start, "end": end}),
            "calendar",
        )
