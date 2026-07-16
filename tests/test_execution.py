from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from bulltrader.execution import (
    OPEN_ORDER_STATUSES,
    _cancel_and_confirm,
    _client_id,
    execute_buy,
    execute_sell,
    reconcile,
)
from bulltrader.plan import TradeIntent
from bulltrader.risk import RiskRejected
from bulltrader.policy import load_policy
from tests.fakes import FakeAlpaca
from tests.test_risk import intent, policy_with_earnings


ROOT = Path(__file__).resolve().parents[1]


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 7, 16, 14, 0, tzinfo=timezone.utc)
        self.policy = policy_with_earnings(load_policy("bull", ROOT), intent(self.now))
        self.client = FakeAlpaca(self.now)
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "memory").mkdir()
        self.control = self.root / "memory" / "control.md"
        self.control.write_text("STATUS: ACTIVE\n", encoding="utf-8")
        self.research_evidence = {
            "packet_id": "bull:2026-07-16:premarket:test",
            "packet_sha256": "a" * 64,
        }
        self.research_guard = lambda: self.research_evidence.copy()

    def tearDown(self):
        self.tmp.cleanup()

    def test_buy_places_one_entry_and_exact_stop_then_records_broker_ids(self):
        result = execute_buy(
            client=self.client,
            policy=self.policy,
            agent="bull",
            intent=intent(self.now),
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=self.research_guard,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(result["status"], "filled")
        self.assertEqual(result["research_packet_id"], self.research_evidence["packet_id"])
        self.assertEqual(
            result["research_packet_sha256"], self.research_evidence["packet_sha256"]
        )
        self.assertEqual([item["type"] for item in self.client.submissions], ["limit", "trailing_stop"])
        self.assertEqual(self.client.submissions[1]["qty"], "10")
        row = json.loads((self.root / "memory" / "trades.jsonl").read_text())
        self.assertEqual(row["broker_order_id"], "order-1")
        self.assertEqual(row["protective_order_id"], "order-2")
        self.assertEqual(row["research_packet_id"], self.research_evidence["packet_id"])
        self.assertEqual(
            row["research_packet_sha256"], self.research_evidence["packet_sha256"]
        )

    def test_fresh_buy_fails_closed_when_research_gate_rejects(self):
        def blocked():
            raise RiskRejected("no current candidate research")

        with self.assertRaisesRegex(RiskRejected, "no current candidate research"):
            execute_buy(
                client=self.client,
                policy=self.policy,
                agent="bull",
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
                fresh_buy_guard=blocked,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertEqual(self.client.submissions, [])

    def test_fresh_buy_rejects_mismatched_or_legacy_research_identity(self):
        def mismatched():
            return {
                "packet_id": "bull:2026-07-16:premarket:different",
                "packet_sha256": "b" * 64,
            }
        with self.assertRaisesRegex(RiskRejected, "does not match the planned buy"):
            execute_buy(
                client=self.client,
                policy=self.policy,
                agent="bull",
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
                fresh_buy_guard=mismatched,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertEqual(self.client.submissions, [])

        legacy = replace(
            intent(self.now),
            research_packet_id=None,
            research_packet_sha256=None,
        )
        with self.assertRaisesRegex(RiskRejected, "does not match the planned buy"):
            execute_buy(
                client=self.client,
                policy=self.policy,
                agent="bull",
                intent=legacy,
                now=self.now,
                control_path=self.control,
                fresh_buy_guard=self.research_guard,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertEqual(self.client.submissions, [])

    def test_broker_guaranteed_or_next_session_statuses_are_not_terminal(self):
        self.assertIn("stopped", OPEN_ORDER_STATUSES)
        self.assertIn("done_for_day", OPEN_ORDER_STATUSES)
        self.assertIn("suspended", OPEN_ORDER_STATUSES)
        self.assertIn("calculated", OPEN_ORDER_STATUSES)

    def test_stopped_entry_cannot_mint_a_second_attempt_while_cancel_is_unresolved(self):
        trade = intent(self.now)
        payload = {
            "agent": "bull",
            "plan_date": trade.plan_date.isoformat(),
            "action": "buy",
            "symbol": trade.symbol,
        }
        client_order_id = _client_id(
            f"bull-{trade.plan_date.isoformat()}-{trade.symbol}-a1", payload
        )
        self.client.seed_order(
            symbol="ETN",
            qty="10",
            side="buy",
            type="limit",
            status="stopped",
            client_order_id=client_order_id,
        )
        self.client.fail_cancel_statuses.add("stopped")
        zero_timeout = replace(
            self.policy,
            system={**self.policy.system, "fill_timeout_seconds": 0},
        )
        with self.assertRaisesRegex(Exception, "cancellation failure"):
            execute_buy(
                client=self.client,
                policy=zero_timeout,
                agent="bull",
                intent=trade,
                now=self.now,
                control_path=self.control,
                fresh_buy_guard=self.research_guard,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertEqual(self.client.submissions, [])

    def test_rerun_finds_same_broker_order_and_submits_no_duplicate_entry(self):
        first = execute_buy(
            client=self.client,
            policy=self.policy,
            agent="bull",
            intent=intent(self.now),
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=self.research_guard,
            root=self.root,
            sleep=lambda _: None,
        )
        count = len(self.client.submissions)
        guard_calls = []

        def stale_research():
            guard_calls.append(True)
            raise RiskRejected("research became unavailable")

        second = execute_buy(
            client=self.client,
            policy=self.policy,
            agent="bull",
            intent=intent(self.now),
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=stale_research,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(first["entry_order_id"], second["entry_order_id"])
        self.assertEqual(len(self.client.submissions), count)
        self.assertEqual(guard_calls, [])

    def test_started_zero_fill_operation_cannot_mint_retry_after_restart(self):
        trade = intent(self.now)
        payload = {
            "agent": "bull",
            "plan_date": trade.plan_date.isoformat(),
            "action": "buy",
            "symbol": trade.symbol,
        }
        first_client_id = _client_id(
            f"bull-{trade.plan_date.isoformat()}-{trade.symbol}-a1", payload
        )
        self.client.seed_order(
            symbol="ETN",
            qty="10",
            filled_qty="0",
            side="buy",
            type="limit",
            status="canceled",
            client_order_id=first_client_id,
        )

        changed_legacy_plan = replace(
            trade,
            thesis="A changed thesis must not inherit an earlier broker authorization.",
            research_packet_id=None,
            research_packet_sha256=None,
        )
        guard_calls = []

        def stale_research():
            guard_calls.append(True)
            raise RiskRejected("research became unavailable")

        with self.assertRaisesRegex(RiskRejected, "cannot authorize a new attempt"):
            execute_buy(
                client=self.client,
                policy=self.policy,
                agent="bull",
                intent=changed_legacy_plan,
                now=self.now,
                control_path=self.control,
                fresh_buy_guard=stale_research,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertEqual(guard_calls, [])
        self.assertEqual(self.client.submissions, [])

    def test_rerun_cancels_partially_filled_live_entry_before_completion(self):
        trade = intent(self.now)
        payload = {
            "agent": "bull",
            "plan_date": trade.plan_date.isoformat(),
            "action": "buy",
            "symbol": trade.symbol,
        }
        client_order_id = _client_id(
            f"bull-{trade.plan_date.isoformat()}-{trade.symbol}-a1", payload
        )
        entry = self.client.seed_order(
            symbol="ETN",
            qty="10",
            filled_qty="4",
            filled_avg_price="100",
            side="buy",
            type="limit",
            status="partially_filled",
            client_order_id=client_order_id,
        )
        self.client.position_data = [
            {"symbol": "ETN", "qty": "4", "market_value": "400", "unrealized_plpc": "0"}
        ]
        zero_timeout = replace(
            self.policy,
            system={**self.policy.system, "fill_timeout_seconds": 0},
        )
        result = execute_buy(
            client=self.client,
            policy=zero_timeout,
            agent="bull",
            intent=trade,
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=self.research_guard,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(result["status"], "already_executed_open")
        self.assertIn(entry["id"], self.client.cancellations)
        self.assertFalse(any(item["type"] == "limit" for item in self.client.submissions))
        live_stops = [
            item
            for item in self.client.order_data
            if item.get("type") == "trailing_stop" and item.get("status") == "new"
        ]
        self.assertEqual(sum(Decimal(item["qty"]) for item in live_stops), Decimal("4"))

    def test_cancel_follows_replacement_and_targets_live_successor(self):
        old = self.client.seed_order(status="replaced")
        successor = self.client.seed_order(status="new")
        self.client.by_order_id[old["id"]]["replaced_by"] = successor["id"]
        result = _cancel_and_confirm(
            self.client,
            old,
            0,
            sleep=lambda _: None,
        )
        self.assertEqual(result["id"], successor["id"])
        self.assertEqual(self.client.cancellations, [successor["id"]])

    def test_stop_failure_submits_emergency_liquidation(self):
        self.client.fail_stop = True
        with self.assertRaisesRegex(Exception, "emergency liquidation"):
            execute_buy(
                client=self.client,
                policy=self.policy,
                agent="bull",
                intent=intent(self.now),
                now=self.now,
                control_path=self.control,
                fresh_buy_guard=self.research_guard,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertTrue(any(item["side"] == "sell" and item["type"] == "market" for item in self.client.submissions))

    def test_reconciliation_repairs_only_missing_stop_quantity(self):
        self.client.position_data = [
            {"symbol": "ETN", "qty": "10", "market_value": "1000", "unrealized_plpc": "0"}
        ]
        self.client.order_data = [
            {
                "id": "old-stop",
                "symbol": "ETN",
                "qty": "7",
                "filled_qty": "0",
                "side": "sell",
                "type": "trailing_stop",
                "status": "new",
                "trail_percent": "10",
                "time_in_force": "gtc",
            }
        ]
        report = reconcile(
            client=self.client,
            policy=self.policy,
            agent="bull",
            repair=True,
            control_path=self.control,
            root=self.root,
        )
        self.assertTrue(report.ok)
        self.assertEqual(self.client.submissions[-1]["qty"], "3")

    def test_completed_entry_never_rebuys_after_stop_has_closed_position(self):
        first = execute_buy(
            client=self.client,
            policy=self.policy,
            agent="bull",
            intent=intent(self.now),
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=self.research_guard,
            root=self.root,
            sleep=lambda _: None,
        )
        self.client.by_order_id[first["protective_order_id"]]["status"] = "filled"
        self.client.position_data.clear()
        count = len(self.client.submissions)
        second = execute_buy(
            client=self.client,
            policy=self.policy,
            agent="bull",
            intent=intent(self.now),
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=self.research_guard,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(second["status"], "already_executed_closed")
        self.assertEqual(len(self.client.submissions), count)

    def test_completed_entry_repairs_missing_stop_without_rebuying(self):
        first = execute_buy(
            client=self.client,
            policy=self.policy,
            agent="bull",
            intent=intent(self.now),
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=self.research_guard,
            root=self.root,
            sleep=lambda _: None,
        )
        self.client.by_order_id[first["protective_order_id"]]["status"] = "canceled"
        count = len(self.client.submissions)
        second = execute_buy(
            client=self.client,
            policy=self.policy,
            agent="bull",
            intent=intent(self.now),
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=self.research_guard,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(second["status"], "already_executed_open")
        self.assertEqual(len(self.client.submissions), count + 1)
        self.assertEqual(self.client.submissions[-1]["type"], "trailing_stop")
        self.assertEqual(sum(item["type"] == "limit" for item in self.client.submissions), 1)

    def test_editing_plan_narrative_cannot_create_a_second_same_day_entry(self):
        first_intent = intent(self.now)
        execute_buy(
            client=self.client,
            policy=self.policy,
            agent="bull",
            intent=first_intent,
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=self.research_guard,
            root=self.root,
            sleep=lambda _: None,
        )
        count = len(self.client.submissions)
        revised = replace(
            first_intent,
            thesis="A materially revised narrative that must not change execution identity.",
        )
        result = execute_buy(
            client=self.client,
            policy=self.policy,
            agent="bull",
            intent=revised,
            now=self.now,
            control_path=self.control,
            fresh_buy_guard=self.research_guard,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(result["status"], "already_executed_open")
        self.assertEqual(len(self.client.submissions), count)

    def test_editing_entry_quantity_cannot_resize_started_operation(self):
        trade = intent(self.now)
        payload = {
            "agent": "bull",
            "plan_date": trade.plan_date.isoformat(),
            "action": "buy",
            "symbol": trade.symbol,
        }
        client_order_id = _client_id(
            f"bull-{trade.plan_date.isoformat()}-{trade.symbol}-a1", payload
        )
        self.client.seed_order(
            symbol="ETN",
            qty="10",
            filled_qty="0",
            side="buy",
            type="limit",
            status="canceled",
            client_order_id=client_order_id,
        )
        revised = replace(trade, qty=Decimal("11"))
        with self.assertRaisesRegex(Exception, "quantity mismatch"):
            execute_buy(
                client=self.client,
                policy=self.policy,
                agent="bull",
                intent=revised,
                now=self.now,
                control_path=self.control,
                fresh_buy_guard=self.research_guard,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertEqual(self.client.submissions, [])

    def test_noncontiguous_entry_attempt_history_blocks_recreation(self):
        trade = intent(self.now)
        payload = {
            "agent": "bull",
            "plan_date": trade.plan_date.isoformat(),
            "action": "buy",
            "symbol": trade.symbol,
        }
        second_client_id = _client_id(
            f"bull-{trade.plan_date.isoformat()}-{trade.symbol}-a2", payload
        )
        self.client.seed_order(
            symbol="ETN",
            qty="10",
            filled_qty="0",
            side="buy",
            type="limit",
            status="canceled",
            client_order_id=second_client_id,
        )
        with self.assertRaisesRegex(Exception, "non-contiguous broker history"):
            execute_buy(
                client=self.client,
                policy=self.policy,
                agent="bull",
                intent=trade,
                now=self.now,
                control_path=self.control,
                fresh_buy_guard=self.research_guard,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertEqual(self.client.submissions, [])

    def test_reconcile_leaves_unmanaged_and_orphan_orders_untouched(self):
        unmanaged = self.client.seed_order(symbol="ETN", side="buy", type="limit")
        orphan = self.client.seed_order(
            symbol="CAT",
            side="sell",
            type="trailing_stop",
            trail_percent="10",
            time_in_force="gtc",
        )
        report = reconcile(
            client=self.client,
            policy=self.policy,
            agent="bull",
            repair=True,
            control_path=self.control,
            root=self.root,
        )
        self.assertFalse(report.ok)
        self.assertEqual(self.client.cancellations, [])
        self.assertTrue(any(unmanaged["id"] in issue for issue in report.issues))
        self.assertTrue(any(orphan["id"] in issue for issue in report.issues))

    def test_reconcile_resets_overcovered_stop(self):
        self.client.position_data = [
            {"symbol": "ETN", "qty": "10", "market_value": "1000", "unrealized_plpc": "0"}
        ]
        old = self.client.seed_order(
            symbol="ETN",
            qty="12",
            side="sell",
            type="trailing_stop",
            trail_percent="10",
            time_in_force="gtc",
        )
        report = reconcile(
            client=self.client,
            policy=self.policy,
            agent="bull",
            repair=True,
            control_path=self.control,
            root=self.root,
        )
        self.assertTrue(report.ok)
        self.assertNotIn(old["id"], self.client.cancellations)
        self.assertEqual(self.client.replacements[-1]["qty"], "10")
        self.assertEqual(self.client.by_order_id[old["id"]]["status"], "replaced")

    def test_failed_stop_replacement_preserves_existing_protection(self):
        self.client.position_data = [
            {"symbol": "ETN", "qty": "10", "market_value": "1000", "unrealized_plpc": "0"}
        ]
        old = self.client.seed_order(
            symbol="ETN",
            qty="10",
            side="sell",
            type="trailing_stop",
            trail_percent="9",
            time_in_force="gtc",
        )
        self.client.fail_replace = True
        report = reconcile(
            client=self.client,
            policy=self.policy,
            agent="bull",
            repair=True,
            control_path=self.control,
            root=self.root,
        )
        self.assertFalse(report.ok)
        self.assertEqual(self.client.by_order_id[old["id"]]["status"], "new")
        self.assertNotIn(old["id"], self.client.cancellations)

    def test_unknown_long_is_protected_but_remains_a_policy_issue(self):
        self.client.position_data = [
            {"symbol": "AAPL", "qty": "5", "market_value": "1000", "unrealized_plpc": "0"}
        ]
        report = reconcile(
            client=self.client,
            policy=self.policy,
            agent="bull",
            repair=True,
            control_path=self.control,
            root=self.root,
        )
        self.assertFalse(report.ok)
        self.assertTrue(any("absent from config/instruments.json" in item for item in report.issues))
        self.assertEqual(self.client.submissions[-1]["symbol"], "AAPL")
        self.assertEqual(self.client.submissions[-1]["type"], "trailing_stop")

    def test_forbidden_short_is_flattened_instead_of_ignored(self):
        self.client.position_data = [
            {"symbol": "ETN", "qty": "-5", "market_value": "-500", "unrealized_plpc": "0"}
        ]
        report = reconcile(
            client=self.client,
            policy=self.policy,
            agent="bull",
            repair=True,
            control_path=self.control,
            root=self.root,
        )
        self.assertTrue(report.ok)
        self.assertEqual(self.client.position_data, [])
        self.assertTrue(
            any(item["side"] == "buy" and item["type"] == "market" for item in self.client.submissions)
        )

    def test_paused_control_blocks_reconciliation_mutations(self):
        self.control.write_text("STATUS: PAUSED\n", encoding="utf-8")
        with self.assertRaisesRegex(RiskRejected, "PAUSED"):
            reconcile(
                client=self.client,
                policy=self.policy,
                agent="bull",
                repair=True,
                control_path=self.control,
                root=self.root,
            )

    def _seed_position_and_stop(self, pnl: str = "0"):
        self.client.position_data = [
            {"symbol": "ETN", "qty": "10", "market_value": "1000", "unrealized_plpc": pnl}
        ]
        return self.client.seed_order(
            symbol="ETN",
            qty="10",
            side="sell",
            type="trailing_stop",
            trail_percent="10",
            time_in_force="gtc",
        )

    def _sell_intent(self, action: str, qty: str) -> TradeIntent:
        return replace(
            intent(self.now, qty=qty),
            action=action,
            max_entry_price=None,
            earnings_date=None,
            earnings_verified_at=None,
            earnings_source=None,
            research_packet_id=None,
            research_packet_sha256=None,
        )

    def test_planned_trim_confirms_stop_cancel_and_reprotects_remainder(self):
        old_stop = self._seed_position_and_stop()
        result = execute_sell(
            client=self.client,
            policy=self.policy,
            agent="bull",
            symbol="ETN",
            qty=Decimal("4"),
            trigger="planned",
            reason="Reduce concentration after thesis review.",
            intent=self._sell_intent("trim", "4"),
            now=self.now,
            control_path=self.control,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(result["status"], "filled")
        self.assertIn(old_stop["id"], self.client.cancellations)
        self.assertEqual(self.client.position_data[0]["qty"], "6")
        self.assertEqual(self.client.submissions[-1]["type"], "trailing_stop")
        self.assertEqual(self.client.submissions[-1]["qty"], "6")
        rows = [json.loads(line) for line in (self.root / "memory" / "trades.jsonl").read_text().splitlines()]
        self.assertEqual(rows[-1]["action"], "sell")
        self.assertTrue(rows[-1]["broker_order_id"])

    def test_planned_sell_blocks_same_day_round_trip(self):
        self._seed_position_and_stop()
        self.client.seed_order(
            symbol="ETN",
            side="buy",
            type="limit",
            status="filled",
            filled_qty="10",
            filled_avg_price="100",
        )
        with self.assertRaisesRegex(RiskRejected, "day-trade guard"):
            execute_sell(
                client=self.client,
                policy=self.policy,
                agent="bull",
                symbol="ETN",
                qty=Decimal("4"),
                trigger="planned",
                reason="Reduce concentration after thesis review.",
                intent=self._sell_intent("trim", "4"),
                now=self.now,
                control_path=self.control,
                root=self.root,
                sleep=lambda _: None,
            )

    def test_midday_loss_cut_overrides_day_trade_guard_at_exact_threshold(self):
        self._seed_position_and_stop(pnl="-0.07")
        self.client.seed_order(
            symbol="ETN",
            side="buy",
            type="limit",
            status="filled",
            filled_qty="10",
            filled_avg_price="100",
        )
        result = execute_sell(
            client=self.client,
            policy=self.policy,
            agent="bull",
            symbol="ETN",
            qty=Decimal("10"),
            trigger="midday_loss",
            reason="Hard loss threshold reached; capital protection exit.",
            intent=None,
            now=self.now,
            control_path=self.control,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(result["status"], "filled")
        self.assertEqual(self.client.position_data, [])

    def test_midday_loss_recovery_uses_immutable_original_target(self):
        self.client.position_data = [
            {"symbol": "ETN", "qty": "5", "market_value": "500", "unrealized_plpc": "-0.08"}
        ]
        self.client.seed_order(
            symbol="ETN",
            qty="5",
            side="sell",
            type="trailing_stop",
            status="new",
            trail_percent="10",
            time_in_force="gtc",
        )
        local = self.now.astimezone(__import__("zoneinfo").ZoneInfo(self.policy.system["timezone"]))
        payload = {
            "agent": "bull",
            "date": local.date().isoformat(),
            "symbol": "ETN",
            "operation": "midday_loss_exit",
        }
        first_client_id = _client_id("bull-sell-ETN-a1", payload)
        self.client.seed_order(
            symbol="ETN",
            qty="10",
            filled_qty="5",
            filled_avg_price="99",
            side="sell",
            type="market",
            status="canceled",
            client_order_id=first_client_id,
        )
        result = execute_sell(
            client=self.client,
            policy=self.policy,
            agent="bull",
            symbol="ETN",
            qty=Decimal("10"),
            trigger="midday_loss",
            reason="Resume the verified hard-loss liquidation after a partial fill.",
            intent=None,
            now=self.now,
            control_path=self.control,
            root=self.root,
            sleep=lambda _: None,
        )
        market_sells = [
            item for item in self.client.submissions if item["side"] == "sell" and item["type"] == "market"
        ]
        self.assertEqual(result["status"], "filled")
        self.assertEqual(result["filled_qty"], "10")
        self.assertEqual([item["qty"] for item in market_sells], ["5"])
        self.assertEqual(self.client.position_data, [])

    def test_noncontiguous_exit_attempt_history_blocks_recreation(self):
        self._seed_position_and_stop(pnl="-0.08")
        local = self.now.astimezone(__import__("zoneinfo").ZoneInfo(self.policy.system["timezone"]))
        payload = {
            "agent": "bull",
            "date": local.date().isoformat(),
            "symbol": "ETN",
            "operation": "midday_loss_exit",
        }
        second_client_id = _client_id("bull-sell-ETN-a2", payload)
        self.client.seed_order(
            symbol="ETN",
            qty="10",
            filled_qty="0",
            side="sell",
            type="market",
            status="canceled",
            client_order_id=second_client_id,
        )
        with self.assertRaisesRegex(Exception, "non-contiguous broker history"):
            execute_sell(
                client=self.client,
                policy=self.policy,
                agent="bull",
                symbol="ETN",
                qty=Decimal("10"),
                trigger="midday_loss",
                reason="Hard loss threshold reached; capital protection exit.",
                intent=None,
                now=self.now,
                control_path=self.control,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertFalse(
            any(item["side"] == "sell" and item["type"] == "market" for item in self.client.submissions)
        )

    def test_partial_sell_is_not_repeated_and_remainder_is_protected(self):
        self._seed_position_and_stop()
        self.client.market_fill_fraction = Decimal("0.5")
        sell_intent = self._sell_intent("trim", "4")
        first = execute_sell(
            client=self.client,
            policy=self.policy,
            agent="bull",
            symbol="ETN",
            qty=Decimal("4"),
            trigger="planned",
            reason="Reduce concentration after thesis review.",
            intent=sell_intent,
            now=self.now,
            control_path=self.control,
            root=self.root,
            sleep=lambda _: None,
        )
        sell_count = sum(item["side"] == "sell" and item["type"] == "market" for item in self.client.submissions)
        second = execute_sell(
            client=self.client,
            policy=self.policy,
            agent="bull",
            symbol="ETN",
            qty=Decimal("4"),
            trigger="planned",
            reason="Reduce concentration after thesis review.",
            intent=sell_intent,
            now=self.now,
            control_path=self.control,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(first["status"], "partially_filled")
        self.assertEqual(second["status"], "partially_filled")
        self.assertEqual(
            sum(item["side"] == "sell" and item["type"] == "market" for item in self.client.submissions),
            sell_count,
        )
        self.assertEqual(first["filled_qty"], "3.00")
        self.assertEqual(second["filled_qty"], "3.00")
        self.assertEqual(self.client.position_data[0]["qty"], "7.00")

    def test_partial_exit_retries_only_the_cumulative_remainder(self):
        self._seed_position_and_stop()
        self.client.market_fill_fractions = [Decimal("0.5"), Decimal("1")]
        result = execute_sell(
            client=self.client,
            policy=self.policy,
            agent="bull",
            symbol="ETN",
            qty=Decimal("4"),
            trigger="planned",
            reason="Reduce concentration after thesis review.",
            intent=self._sell_intent("trim", "4"),
            now=self.now,
            control_path=self.control,
            root=self.root,
            sleep=lambda _: None,
        )
        market_sells = [
            item for item in self.client.submissions if item["side"] == "sell" and item["type"] == "market"
        ]
        self.assertEqual(result["status"], "filled")
        self.assertEqual(result["filled_qty"], "4.0")
        self.assertEqual([item["qty"] for item in market_sells], ["4", "2.0"])
        self.assertEqual(self.client.position_data[0]["qty"], "6.0")

    def test_editing_sell_narrative_cannot_create_a_second_trim(self):
        self._seed_position_and_stop()
        first_intent = self._sell_intent("trim", "4")
        execute_sell(
            client=self.client,
            policy=self.policy,
            agent="bull",
            symbol="ETN",
            qty=Decimal("4"),
            trigger="planned",
            reason="Reduce concentration after thesis review.",
            intent=first_intent,
            now=self.now,
            control_path=self.control,
            root=self.root,
            sleep=lambda _: None,
        )
        count = len(
            [item for item in self.client.submissions if item["side"] == "sell" and item["type"] == "market"]
        )
        revised = replace(
            first_intent,
            thesis="A revised narrative that must not create another liquidation operation.",
        )
        result = execute_sell(
            client=self.client,
            policy=self.policy,
            agent="bull",
            symbol="ETN",
            qty=Decimal("4"),
            trigger="planned",
            reason="Reduce concentration after thesis review.",
            intent=revised,
            now=self.now,
            control_path=self.control,
            root=self.root,
            sleep=lambda _: None,
        )
        self.assertEqual(result["status"], "already_executed")
        self.assertEqual(
            len([item for item in self.client.submissions if item["side"] == "sell" and item["type"] == "market"]),
            count,
        )
        self.assertEqual(self.client.position_data[0]["qty"], "6")

    def test_trim_equal_to_full_holding_is_rejected(self):
        self._seed_position_and_stop()
        with self.assertRaisesRegex(RiskRejected, "strictly smaller"):
            execute_sell(
                client=self.client,
                policy=self.policy,
                agent="bull",
                symbol="ETN",
                qty=Decimal("10"),
                trigger="planned",
                reason="Reduce concentration after thesis review.",
                intent=self._sell_intent("trim", "10"),
                now=self.now,
                control_path=self.control,
                root=self.root,
                sleep=lambda _: None,
            )
        self.assertFalse(
            any(item["side"] == "sell" and item["type"] == "market" for item in self.client.submissions)
        )

    def test_sell_rejects_nonfinite_quantity_and_oversized_reason(self):
        self._seed_position_and_stop()
        with self.assertRaisesRegex(RiskRejected, "non-finite"):
            execute_sell(
                client=self.client,
                policy=self.policy,
                agent="bull",
                symbol="ETN",
                qty=Decimal("NaN"),
                trigger="planned",
                reason="Reduce concentration after thesis review.",
                intent=self._sell_intent("trim", "4"),
                now=self.now,
                control_path=self.control,
                root=self.root,
                sleep=lambda _: None,
            )
        with self.assertRaisesRegex(RiskRejected, "no longer than 1000"):
            execute_sell(
                client=self.client,
                policy=self.policy,
                agent="bull",
                symbol="ETN",
                qty=Decimal("4"),
                trigger="planned",
                reason="x" * 1001,
                intent=self._sell_intent("trim", "4"),
                now=self.now,
                control_path=self.control,
                root=self.root,
                sleep=lambda _: None,
            )


if __name__ == "__main__":
    unittest.main()
