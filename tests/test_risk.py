from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from bulltrader.plan import TradeIntent
from bulltrader.policy import load_policy
from bulltrader.risk import RiskRejected, approve_buy, control_status
from tests.fakes import FakeAlpaca


ROOT = Path(__file__).resolve().parents[1]


def intent(now: datetime, qty: str = "10", earnings_days: int = 20) -> TradeIntent:
    today = now.date()
    return TradeIntent(
        plan_date=today,
        action="buy",
        symbol="ETN",
        qty=Decimal(qty),
        sector="Industrials",
        thesis="A precise AI power infrastructure thesis with measurable catalysts.",
        invalidation="Guidance cut or loss of data-center demand.",
        review_by=today + timedelta(days=30),
        max_entry_price=Decimal("110"),
        earnings_date=today + timedelta(days=earnings_days),
        earnings_verified_at=now,
        earnings_source="https://example.com/earnings",
        research_packet_id="bull:2026-07-16:premarket:test",
        research_packet_sha256="a" * 64,
    )


def policy_with_earnings(policy, trade: TradeIntent):
    assert trade.earnings_date and trade.earnings_verified_at and trade.earnings_source
    return replace(
        policy,
        earnings={
            trade.symbol: {
                "earnings_date": trade.earnings_date.isoformat(),
                "verified_at": trade.earnings_verified_at.isoformat(),
                "source": trade.earnings_source,
            }
        },
    )


class RiskTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 7, 16, 14, 0, tzinfo=timezone.utc)
        self.policy = policy_with_earnings(load_policy("bull", ROOT), intent(self.now))
        self.client = FakeAlpaca(self.now)
        self.tmp = tempfile.TemporaryDirectory()
        self.control = Path(self.tmp.name) / "control.md"
        self.control.write_text("STATUS: ACTIVE\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_buy_is_approved_at_bounded_limit(self):
        approval = approve_buy(
            client=self.client,
            policy=self.policy,
            intent=intent(self.now),
            now=self.now,
            control_path=self.control,
        )
        self.assertEqual(approval.limit_price, Decimal("100.30"))

    def test_stale_quote_blocks(self):
        self.client.quote_data = self.client.quote_data.__class__(
            bid=Decimal("99.90"),
            ask=Decimal("100"),
            timestamp=self.now - timedelta(minutes=5),
        )
        with self.assertRaisesRegex(RiskRejected, "quote is stale"):
            approve_buy(
                client=self.client,
                policy=self.policy,
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
            )

    def test_drawdown_breaker_blocks(self):
        self.client.account_data["equity"] = "89000"
        self.client.account_data["last_equity"] = "89000"
        self.client.history_data = {"equity": ["100000", "98000"]}
        with self.assertRaisesRegex(RiskRejected, "drawdown breaker"):
            approve_buy(
                client=self.client,
                policy=self.policy,
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
            )

    def test_position_cap_and_risk_budget_block_oversize_order(self):
        with self.assertRaises(RiskRejected):
            approve_buy(
                client=self.client,
                policy=self.policy,
                intent=intent(self.now, qty="200"),
                now=self.now,
                control_path=self.control,
            )

    def test_earnings_blackout_blocks(self):
        trade = intent(self.now, earnings_days=1)
        policy = policy_with_earnings(self.policy, trade)
        with self.assertRaisesRegex(RiskRejected, "earnings blackout"):
            approve_buy(
                client=self.client,
                policy=policy,
                intent=trade,
                now=self.now,
                control_path=self.control,
            )

    def test_empty_or_mismatched_human_earnings_calendar_blocks(self):
        trade = intent(self.now)
        with self.assertRaisesRegex(RiskRejected, "no human-verified entry"):
            approve_buy(
                client=self.client,
                policy=replace(self.policy, earnings={}),
                intent=trade,
                now=self.now,
                control_path=self.control,
            )
        mismatched = replace(
            self.policy,
            earnings={
                "ETN": {
                    "earnings_date": (trade.earnings_date + timedelta(days=1)).isoformat(),
                    "verified_at": trade.earnings_verified_at.isoformat(),
                    "source": trade.earnings_source,
                }
            },
        )
        with self.assertRaisesRegex(RiskRejected, "does not exactly match"):
            approve_buy(
                client=self.client,
                policy=mismatched,
                intent=trade,
                now=self.now,
                control_path=self.control,
            )

    def test_stale_human_earnings_verification_blocks(self):
        stale_time = self.now - timedelta(hours=73)
        trade = replace(intent(self.now), earnings_verified_at=stale_time)
        policy = policy_with_earnings(self.policy, trade)
        with self.assertRaisesRegex(RiskRejected, "verification is stale"):
            approve_buy(
                client=self.client,
                policy=policy,
                intent=trade,
                now=self.now,
                control_path=self.control,
            )

    def test_risk_off_blocks_new_exposure(self):
        self.control.write_text("STATUS: RISK_OFF\n", encoding="utf-8")
        with self.assertRaisesRegex(RiskRejected, "RISK_OFF"):
            approve_buy(
                client=self.client,
                policy=self.policy,
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
            )

    def test_control_switch_rejects_duplicate_status_lines(self):
        self.control.write_text("STATUS: PAUSED\nSTATUS: ACTIVE\n", encoding="utf-8")
        with self.assertRaisesRegex(RiskRejected, "exactly one STATUS"):
            control_status(self.control)

    def test_wide_spread_blocks_entry(self):
        self.client.quote_data = self.client.quote_data.__class__(
            bid=Decimal("99"),
            ask=Decimal("100"),
            timestamp=self.now,
        )
        with self.assertRaisesRegex(RiskRejected, "spread is too wide"):
            approve_buy(
                client=self.client,
                policy=self.policy,
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
            )

    def test_pending_buy_orders_count_toward_position_risk(self):
        self.client.seed_order(
            symbol="ETN",
            side="buy",
            qty="141",
            filled_qty="0",
            limit_price="100",
            status="new",
        )
        with self.assertRaisesRegex(RiskRejected, "planned stop risk"):
            approve_buy(
                client=self.client,
                policy=self.policy,
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
            )

    def test_pending_orders_count_against_cash_reserve(self):
        self.client.seed_order(
            symbol="CAT",
            side="buy",
            qty="450",
            filled_qty="0",
            limit_price="100",
            status="new",
        )
        with self.assertRaisesRegex(RiskRejected, "cash after order"):
            approve_buy(
                client=self.client,
                policy=self.policy,
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
            )

    def test_exact_drawdown_threshold_blocks(self):
        self.client.account_data["equity"] = "90000"
        self.client.account_data["last_equity"] = "90000"
        self.client.history_data = {"equity": ["100000", "90000"]}
        with self.assertRaisesRegex(RiskRejected, "drawdown breaker"):
            approve_buy(
                client=self.client,
                policy=self.policy,
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
            )

    def test_stale_plan_blocks_direct_library_call(self):
        stale = intent(self.now - timedelta(days=1))
        with self.assertRaisesRegex(RiskRejected, "plan_date .* is stale"):
            approve_buy(
                client=self.client,
                policy=self.policy,
                intent=stale,
                now=self.now,
                control_path=self.control,
            )


if __name__ == "__main__":
    unittest.main()
