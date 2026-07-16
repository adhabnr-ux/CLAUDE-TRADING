from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from datetime import date
from pathlib import Path

from bulltrader.alpaca import AlpacaClient, BrokerError
from bulltrader.plan import PlanError, latest_plan
from bulltrader.policy import load_policy
from bulltrader.risk import RiskRejected
from scripts.trade import _require_agent_binding


ROOT = Path(__file__).resolve().parents[1]


class PolicyPlanTests(unittest.TestCase):
    def _valid_plan(self):
        return {
            "schema_version": 2,
            "agent": "bull",
            "plan_date": "2026-07-16",
            "trades": [
                {
                    "action": "buy",
                    "symbol": "ETN",
                    "qty": 10,
                    "sector": "Industrials",
                    "thesis": "A specific durable thesis that is long enough.",
                    "invalidation": "A concrete invalidation event.",
                    "review_by": "2026-08-01",
                    "max_entry_price": "425.00",
                    "earnings_date": "2026-07-31",
                    "earnings_verified_at": "2026-07-16T11:30:00-04:00",
                    "earnings_source": "https://example.com/earnings",
                    "research_packet_id": "bull:2026-07-16:premarket:test",
                    "research_packet_sha256": "a" * 64,
                }
            ],
        }

    def _parse(self, plan):
        policy = load_policy("bull", ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "research.md"
            path.write_text(f"```json\n{json.dumps(plan)}\n```\n", encoding="utf-8")
            return latest_plan(path, policy)

    def test_only_exact_paper_endpoint_is_accepted(self):
        policy = load_policy("bull", ROOT)
        AlpacaClient(
            "key",
            "secret",
            "https://paper-api.alpaca.markets",
            policy,
            "paper-account-id",
        )
        with self.assertRaises(BrokerError):
            AlpacaClient(
                "key",
                "secret",
                "https://paper-api.alpaca.markets.evil.example",
                policy,
                "paper-account-id",
            )

    def test_account_fingerprint_is_required_and_verified(self):
        policy = load_policy("bull", ROOT)
        with self.assertRaisesRegex(BrokerError, "EXPECTED_ACCOUNT_ID"):
            AlpacaClient(
                "key",
                "secret",
                "https://paper-api.alpaca.markets",
                policy,
                "",
            )
        client = AlpacaClient(
            "key",
            "secret",
            "https://paper-api.alpaca.markets",
            policy,
            "expected-paper-account",
        )
        client._request = lambda *args, **kwargs: {"id": "different-paper-account"}
        with self.assertRaisesRegex(BrokerError, "does not match"):
            client.account()
        client._request = lambda *args, **kwargs: {"id": "EXPECTED-PAPER-ACCOUNT"}
        self.assertEqual(client.account()["id"], "EXPECTED-PAPER-ACCOUNT")

    def test_cli_agent_must_match_environment_binding(self):
        from unittest.mock import patch

        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(RiskRejected, "TRADING_AGENT"):
                _require_agent_binding("bull")
        with patch.dict("os.environ", {"TRADING_AGENT": "aggro"}, clear=True):
            with self.assertRaisesRegex(RiskRejected, "refusing bull"):
                _require_agent_binding("bull")
        with patch.dict("os.environ", {"TRADING_AGENT": "bull"}, clear=True):
            _require_agent_binding("bull")

    def test_plan_requires_typed_buy_metadata(self):
        plan_date, intents = self._parse(self._valid_plan())
        self.assertEqual(plan_date, date(2026, 7, 16))
        self.assertEqual(intents[0].symbol, "ETN")
        self.assertEqual(
            intents[0].research_packet_id,
            "bull:2026-07-16:premarket:test",
        )
        self.assertEqual(intents[0].research_packet_sha256, "a" * 64)

        missing_identity = self._valid_plan()
        missing_identity["trades"][0].pop("research_packet_sha256")
        with self.assertRaisesRegex(PlanError, "required buy fields missing"):
            self._parse(missing_identity)

    def test_plan_rejects_wrong_sector_and_missing_earnings(self):
        policy = load_policy("bull", ROOT)
        plan = {
            "schema_version": 1,
            "agent": "bull",
            "plan_date": "2026-07-16",
            "trades": [
                {
                    "action": "buy",
                    "symbol": "ETN",
                    "qty": 10,
                    "sector": "Technology",
                    "thesis": "A specific durable thesis that is long enough.",
                    "invalidation": "A concrete invalidation event.",
                    "review_by": "2026-08-01"
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "research.md"
            path.write_text(f"```json\n{json.dumps(plan)}\n```\n", encoding="utf-8")
            with self.assertRaises(PlanError):
                latest_plan(path, policy)

    def test_plan_agent_must_match_loaded_policy(self):
        plan = self._valid_plan()
        plan["agent"] = "aggro"
        with self.assertRaisesRegex(PlanError, "does not match"):
            self._parse(plan)

    def test_plan_rejects_extra_top_level_and_trade_fields(self):
        top_level = self._valid_plan()
        top_level["override_risk"] = True
        with self.assertRaisesRegex(PlanError, "must contain exactly"):
            self._parse(top_level)
        trade_level = self._valid_plan()
        trade_level["trades"][0]["confidence"] = 1.0
        with self.assertRaisesRegex(PlanError, "unknown fields"):
            self._parse(trade_level)

    def test_plan_rejects_multiple_actions_for_same_symbol(self):
        plan = self._valid_plan()
        duplicate = deepcopy(plan["trades"][0])
        duplicate.update(
            {
                "action": "trim",
                "qty": 1,
            }
        )
        for key in (
            "max_entry_price",
            "earnings_date",
            "earnings_verified_at",
            "earnings_source",
            "research_packet_id",
            "research_packet_sha256",
        ):
            duplicate.pop(key)
        plan["trades"].append(duplicate)
        with self.assertRaisesRegex(PlanError, "only one action"):
            self._parse(plan)

    def test_newest_plan_is_selected_by_date_not_file_position(self):
        current = self._valid_plan()
        older = deepcopy(current)
        older["plan_date"] = "2026-07-15"
        older["trades"] = []
        policy = load_policy("bull", ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "research.md"
            path.write_text(
                f"```json\n{json.dumps(current)}\n```\n"
                f"```json\n{json.dumps(older)}\n```\n",
                encoding="utf-8",
            )
            plan_date, intents = latest_plan(path, policy)
        self.assertEqual(plan_date, date(2026, 7, 16))
        self.assertEqual(intents[0].symbol, "ETN")

    def test_malformed_or_duplicate_latest_plan_fails_closed(self):
        valid = self._valid_plan()
        policy = load_policy("bull", ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "research.md"
            path.write_text(
                f"```json\n{json.dumps(valid)}\n```\n```json\n{{broken\n```\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(PlanError, "malformed"):
                latest_plan(path, policy)
            path.write_text(
                f"```json\n{json.dumps(valid)}\n```\n"
                f"```json\n{json.dumps(valid)}\n```\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(PlanError, "ambiguous trade plans"):
                latest_plan(path, policy)

    def test_checked_in_latest_plans_are_valid_and_non_replayable(self):
        for agent, relative in (
            ("bull", "memory/research-log.md"),
            ("aggro", "memory/aggressive/research-log.md"),
        ):
            plan_date, intents = latest_plan(ROOT / relative, load_policy(agent, ROOT))
            self.assertEqual(plan_date, date(2026, 7, 15))
            self.assertEqual(intents, [])

    def test_invalid_policy_semantics_fail_before_trading(self):
        base_policy = json.loads((ROOT / "config" / "risk-policy.json").read_text())
        instruments = (ROOT / "config" / "instruments.json").read_text()
        earnings = (ROOT / "config" / "earnings-calendar.json").read_text()

        def rejected(updates, message):
            policy = deepcopy(base_policy)
            policy["system"].update(updates)
            with tempfile.TemporaryDirectory() as tmp:
                config = Path(tmp) / "config"
                config.mkdir()
                (config / "risk-policy.json").write_text(
                    json.dumps(policy), encoding="utf-8"
                )
                (config / "instruments.json").write_text(
                    instruments, encoding="utf-8"
                )
                (config / "earnings-calendar.json").write_text(
                    earnings, encoding="utf-8"
                )
                with self.assertRaisesRegex(Exception, message):
                    load_policy("bull", Path(tmp))

        rejected({"maximum_entry_attempts": 0}, "greater than zero")
        rejected(
            {"research_candidate_max_age_minutes": 1441},
            "cannot exceed 1440",
        )
        rejected(
            {
                "research_candidate_max_age_minutes": 60,
                "research_market_source_max_age_minutes": 61,
            },
            "cannot exceed research_candidate_max_age_minutes",
        )


if __name__ == "__main__":
    unittest.main()
