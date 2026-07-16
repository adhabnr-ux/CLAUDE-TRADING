from __future__ import annotations

import copy
import json
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import bulltrader.research as research_module
from bulltrader.research import (
    ResearchError,
    append_pending_packet,
    canonical_url,
    pending_path,
    require_current_candidate,
    validate_ledger,
    validate_packet,
)


ROOT = Path(__file__).resolve().parents[1]


class ResearchPacketTests(unittest.TestCase):
    def setUp(self):
        self.example = json.loads(
            (ROOT / "schemas/examples/research-packet.json").read_text(encoding="utf-8")
        )
        self.packet = copy.deepcopy(self.example)
        self.packet["decision_support"][0]["assessment"] = "candidate"
        self.packet["packet_limitations"] = []
        self.packet["sources"][3]["limitations"] = []
        self.packet["claims"][3]["limitations"] = []

    def _candidate_kwargs(self):
        decision = self.packet["decision_support"][0]
        return {
            "thesis": decision["thesis"],
            "invalidation": decision["invalidation"],
            "review_by": date.fromisoformat(decision["review_by"]),
        }

    def test_example_and_checked_in_profile_ledgers_validate(self):
        validate_packet(copy.deepcopy(self.example), "bull")
        validate_packet(copy.deepcopy(self.packet), "bull")
        self.assertEqual(
            len(validate_ledger(ROOT / "memory/research-evidence.jsonl", "bull")),
            1,
        )
        self.assertEqual(
            len(
                validate_ledger(
                    ROOT / "memory/aggressive/research-evidence.jsonl", "aggro"
                )
            ),
            1,
        )

    def test_unknown_fields_and_execution_instructions_fail_closed(self):
        unknown = copy.deepcopy(self.packet)
        unknown["order"] = {"action": "buy", "qty": 10}
        with self.assertRaisesRegex(ResearchError, "unknown fields: order"):
            validate_packet(unknown, "bull")

        injection = copy.deepcopy(self.packet)
        injection["untrusted_instructions_detected"] = True
        injection["packet_limitations"] = []
        with self.assertRaisesRegex(ResearchError, "must explain how detected"):
            validate_packet(injection, "bull")

        oversized = copy.deepcopy(self.packet)
        oversized["packet_limitations"] = ["x" * 31_000]
        with self.assertRaisesRegex(ResearchError, "serialized size"):
            validate_packet(oversized, "bull")

    def test_profile_binding_and_timestamps_fail_closed(self):
        with self.assertRaisesRegex(ResearchError, "expected aggro"):
            validate_packet(copy.deepcopy(self.packet), "aggro")
        future = copy.deepcopy(self.packet)
        future["sources"][0]["as_of"] = "2026-07-17T00:00:00Z"
        with self.assertRaisesRegex(ResearchError, "cannot be after decision_time"):
            validate_packet(future, "bull")
        naive = copy.deepcopy(self.packet)
        naive["decision_time"] = "2026-07-16T12:00:00"
        with self.assertRaisesRegex(ResearchError, "canonical RFC-3339"):
            validate_packet(naive, "bull")
        loose = copy.deepcopy(self.packet)
        loose["decision_time"] = "2026-07-16 12:00:00+00:00"
        with self.assertRaisesRegex(ResearchError, "canonical RFC-3339"):
            validate_packet(loose, "bull")
        unknown_offset = copy.deepcopy(self.packet)
        unknown_offset["decision_time"] = "2026-07-16T12:00:00-00:00"
        with self.assertRaisesRegex(ResearchError, "known UTC offset"):
            validate_packet(unknown_offset, "bull")
        boolean_version = copy.deepcopy(self.packet)
        boolean_version["schema_version"] = True
        with self.assertRaisesRegex(ResearchError, "must equal 1"):
            validate_packet(boolean_version, "bull")
        padded_agent = copy.deepcopy(self.packet)
        padded_agent["agent"] = " bull "
        with self.assertRaisesRegex(ResearchError, "surrounding whitespace"):
            validate_packet(padded_agent, "bull")
        padded_reference = copy.deepcopy(self.packet)
        padded_reference["claims"][0]["source_ids"] = [" src-company-release "]
        with self.assertRaisesRegex(ResearchError, "surrounding whitespace"):
            validate_packet(padded_reference, "bull")
        uppercase = copy.deepcopy(self.packet)
        uppercase["packet_id"] = "Bull:2026-07-16:premarket:example"
        with self.assertRaisesRegex(ResearchError, "must use lowercase"):
            validate_packet(uppercase, "bull")
        wrong_prefix = copy.deepcopy(self.packet)
        wrong_prefix["packet_id"] = "aggro:2026-07-16:premarket:example"
        with self.assertRaisesRegex(ResearchError, "must begin with bull:"):
            validate_packet(wrong_prefix, "bull")

    def test_references_hashes_and_canonical_duplicates_are_checked(self):
        undefined = copy.deepcopy(self.packet)
        undefined["claims"][0]["source_ids"] = ["src-missing"]
        with self.assertRaisesRegex(ResearchError, "undefined source IDs"):
            validate_packet(undefined, "bull")

        bad_hash = copy.deepcopy(self.packet)
        bad_hash["sources"][0]["hash_status"] = "captured"
        bad_hash["sources"][0]["content_sha256"] = "abc"
        with self.assertRaisesRegex(ResearchError, "lowercase sha256"):
            validate_packet(bad_hash, "bull")

        duplicate_hash = copy.deepcopy(self.packet)
        for source in duplicate_hash["sources"][:2]:
            source["hash_status"] = "captured"
            source["content_sha256"] = "a" * 64
        with self.assertRaisesRegex(ResearchError, "duplicates captured content"):
            validate_packet(duplicate_hash, "bull")

        duplicate = copy.deepcopy(self.packet)
        duplicate["sources"][1]["url"] = (
            duplicate["sources"][0]["url"] + "/?utm_source=copy#fragment"
        )
        with self.assertRaisesRegex(ResearchError, "duplicates a canonical URL"):
            validate_packet(duplicate, "bull")

    def test_candidate_requires_complete_diverse_adversarial_evidence(self):
        incomplete = copy.deepcopy(self.packet)
        incomplete["window"]["complete"] = False
        incomplete["window"]["limitations"] = ["One requested source was unavailable."]
        with self.assertRaisesRegex(ResearchError, "complete requested research window"):
            validate_packet(incomplete, "bull")

        critical = copy.deepcopy(self.packet)
        critical["decision_support"][0]["critical_unknowns"] = [
            "The primary demand driver could not be verified."
        ]
        with self.assertRaisesRegex(ResearchError, "cannot retain critical unknowns"):
            validate_packet(critical, "bull")

        no_primary = copy.deepcopy(self.packet)
        for source in no_primary["sources"]:
            if source["source_id"] != "src-independent-risk":
                source["source_type"] = "reputable_secondary"
                source["tier"] = 2
        with self.assertRaisesRegex(ResearchError, "tier-1 primary market source"):
            validate_packet(no_primary, "bull")

        not_opposing = copy.deepcopy(self.packet)
        not_opposing["claims"][2]["stance"] = "context"
        with self.assertRaisesRegex(ResearchError, "stance=opposes"):
            validate_packet(not_opposing, "bull")

        wrong_symbol = copy.deepcopy(self.packet)
        wrong_symbol["decision_support"][0]["symbol"] = "AAPL"
        with self.assertRaisesRegex(ResearchError, "scoped to AAPL"):
            validate_packet(wrong_symbol, "bull")

        no_support = copy.deepcopy(self.packet)
        no_support["claims"][0]["stance"] = "context"
        no_support["claims"][1]["stance"] = "context"
        no_support["claims"][3]["stance"] = "context"
        with self.assertRaisesRegex(ResearchError, "stance=supports"):
            validate_packet(no_support, "bull")

        detected_instructions = copy.deepcopy(self.packet)
        detected_instructions["untrusted_instructions_detected"] = True
        detected_instructions["packet_limitations"] = [
            "A source contained instructions; it was treated only as untrusted data."
        ]
        with self.assertRaisesRegex(ResearchError, "detected instructions"):
            validate_packet(detected_instructions, "bull")

        packet_limitation = copy.deepcopy(self.packet)
        packet_limitation["packet_limitations"] = [
            "This packet is illustrative rather than decision-grade research."
        ]
        with self.assertRaisesRegex(ResearchError, "packet-level limitations"):
            validate_packet(packet_limitation, "bull")

        stale_market_source = copy.deepcopy(self.packet)
        stale_market_source["sources"][3]["as_of"] = "2026-07-15T00:00:00Z"
        stale_market_source["claims"][3]["as_of"] = "2026-07-15T00:00:00Z"
        with self.assertRaisesRegex(ResearchError, "current unqualified traced exchange"):
            validate_packet(stale_market_source, "bull")

    def test_window_and_cutoff_claims_are_machine_checked(self):
        outside_window = copy.deepcopy(self.packet)
        outside_window["sources"][0]["fetched_at"] = "2026-07-15T11:59:59Z"
        with self.assertRaisesRegex(ResearchError, "declared half-open research window"):
            validate_packet(outside_window, "bull")

        at_exclusive_end = copy.deepcopy(self.packet)
        at_exclusive_end["sources"][0]["fetched_at"] = at_exclusive_end["window"]["end"]
        with self.assertRaisesRegex(ResearchError, "half-open research window"):
            validate_packet(at_exclusive_end, "bull")

        synthetic_freshness = copy.deepcopy(self.packet)
        synthetic_freshness["sources"][3]["fetched_at"] = "2026-07-16T11:30:00Z"
        with self.assertRaisesRegex(ResearchError, "as_of: cannot be after fetched_at"):
            validate_packet(synthetic_freshness, "bull")

        false_complete = copy.deepcopy(self.packet)
        false_complete["window"]["failures"] = [
            {
                "stage": "fetch",
                "source": "primary filings",
                "error": "All requested primary filings were unavailable.",
            }
        ]
        with self.assertRaisesRegex(ResearchError, "complete window cannot contain"):
            validate_packet(false_complete, "bull")

        after_cutoff = copy.deepcopy(self.packet)
        after_cutoff["sources"][0]["as_of"] = "2026-07-16T11:56:00Z"
        with self.assertRaisesRegex(ResearchError, "market_data_cutoff"):
            validate_packet(after_cutoff, "bull")

    def test_duplicate_packet_ids_fail_append_only_ledger(self):
        line = json.dumps(self.packet, separators=(",", ":"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "research-evidence.jsonl"
            path.write_text(f"{line}\n{line}\n", encoding="utf-8")
            with self.assertRaisesRegex(ResearchError, "duplicate packet_id"):
                validate_ledger(path, "bull")

    def test_ledger_requires_strict_chronological_append_order(self):
        later = copy.deepcopy(self.packet)
        later["packet_id"] = "bull:2026-07-16:premarket:later"
        later["decision_time"] = "2026-07-16T12:01:00Z"
        earlier_line = json.dumps(later, separators=(",", ":"))
        current_line = json.dumps(self.packet, separators=(",", ":"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "research-evidence.jsonl"
            path.write_text(f"{earlier_line}\n{current_line}\n", encoding="utf-8")
            with self.assertRaisesRegex(ResearchError, "strictly later"):
                validate_ledger(path, "bull")

    def test_historical_validation_is_independent_of_tighter_current_policy(self):
        historical = copy.deepcopy(self.packet)
        historical["sources"][3]["as_of"] = "2026-07-16T10:30:00Z"
        historical["claims"][3]["as_of"] = "2026-07-16T10:30:00Z"
        validate_packet(
            copy.deepcopy(historical),
            "bull",
            market_source_max_age_minutes=120,
        )
        with self.assertRaisesRegex(ResearchError, "current unqualified traced exchange"):
            validate_packet(
                copy.deepcopy(historical),
                "bull",
                market_source_max_age_minutes=60,
            )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "research-evidence.jsonl"
            path.write_text(json.dumps(historical) + "\n", encoding="utf-8")
            self.assertEqual(len(validate_ledger(path, "bull")), 1)

    def test_exact_replay_remains_idempotent_after_policy_tightens(self):
        historical = copy.deepcopy(self.packet)
        historical["sources"][3]["as_of"] = "2026-07-16T10:30:00Z"
        historical["claims"][3]["as_of"] = "2026-07-16T10:30:00Z"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "memory").mkdir()
            ledger = root / "memory" / "research-evidence.jsonl"
            original = json.dumps(historical, separators=(",", ":")) + "\n"
            ledger.write_text(original, encoding="utf-8")
            pending = pending_path(root, "bull")
            pending.write_text(json.dumps(historical), encoding="utf-8")
            append_pending_packet(
                root,
                "bull",
                now=datetime(2026, 7, 16, 12, 1, tzinfo=timezone.utc),
                market_source_max_age_minutes=60,
            )
            self.assertFalse(pending.exists())
            self.assertEqual(len(validate_ledger(ledger, "bull")), 1)

    def test_pending_append_is_validated_atomic_monotonic_and_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "memory").mkdir()
            ledger = root / "memory" / "research-evidence.jsonl"
            ledger.write_text("", encoding="utf-8")
            pending = pending_path(root, "bull")
            pending.write_text(json.dumps(self.packet), encoding="utf-8")
            now = datetime(2026, 7, 16, 12, 1, tzinfo=timezone.utc)
            appended = append_pending_packet(root, "bull", now=now)
            self.assertEqual(appended["packet_id"], self.packet["packet_id"])
            self.assertFalse(pending.exists())
            original = ledger.read_text(encoding="utf-8")
            self.assertEqual(len(validate_ledger(ledger, "bull")), 1)

            pending.write_text(json.dumps(self.packet), encoding="utf-8")
            append_pending_packet(root, "bull", now=now)
            self.assertEqual(ledger.read_text(encoding="utf-8"), original)
            self.assertFalse(pending.exists())

            stale = copy.deepcopy(self.packet)
            stale["packet_id"] = "bull:2026-07-16:premarket:stale"
            stale["decision_time"] = "2026-07-16T11:59:00Z"
            pending.write_text(json.dumps(stale), encoding="utf-8")
            with self.assertRaisesRegex(ResearchError, "strictly later"):
                append_pending_packet(root, "bull", now=now)
            self.assertEqual(ledger.read_text(encoding="utf-8"), original)
            self.assertTrue(pending.exists())

            future = copy.deepcopy(self.packet)
            future["packet_id"] = "bull:2099-01-01:premarket:future"
            future["decision_time"] = "2099-01-01T12:00:00Z"
            future["market_data_cutoff"] = "2026-07-16T11:55:00Z"
            pending.write_text(json.dumps(future), encoding="utf-8")
            with self.assertRaisesRegex(ResearchError, "too far in the future"):
                append_pending_packet(root, "bull", now=now)
            self.assertTrue(pending.exists())

    def test_discovery_only_append_rejects_candidates_and_restores_pending(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "memory").mkdir()
            ledger = root / "memory" / "research-evidence.jsonl"
            ledger.write_text("", encoding="utf-8")
            pending = pending_path(root, "bull")
            pending.write_text(json.dumps(self.packet), encoding="utf-8")
            with self.assertRaisesRegex(ResearchError, "discovery-only runner"):
                append_pending_packet(
                    root,
                    "bull",
                    now=datetime(2026, 7, 16, 12, 1, tzinfo=timezone.utc),
                    allow_candidates=False,
                )
            self.assertTrue(pending.exists())
            self.assertEqual(ledger.read_text(encoding="utf-8"), "")
            claims = list(
                (root / "memory").glob(".research-packet.claimed-*.json")
            )
            self.assertEqual(len(claims), 1)
            self.assertTrue(pending.samefile(claims[0]))

            append_pending_packet(
                root,
                "bull",
                now=datetime(2026, 7, 16, 12, 1, tzinfo=timezone.utc),
            )
            self.assertFalse(pending.exists())
            self.assertEqual(
                list((root / "memory").glob(".research-packet.claimed-*.json")),
                [],
            )
            self.assertEqual(len(validate_ledger(ledger, "bull")), 1)

            with self.assertRaisesRegex(ResearchError, "schema-v1 ceiling"):
                append_pending_packet(
                    root,
                    "bull",
                    market_source_max_age_minutes=1441,
                )

    def test_pending_claim_never_overwrites_a_concurrent_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "memory").mkdir()
            (root / "memory" / "research-evidence.jsonl").write_text(
                "", encoding="utf-8"
            )
            pending = pending_path(root, "bull")
            original = json.dumps(self.packet)
            replacement = '{"newer":"packet"}'
            pending.write_text(original, encoding="utf-8")

            def fail_after_replacement(*args, **kwargs):
                pending.write_text(replacement, encoding="utf-8")
                raise ResearchError("simulated append failure")

            with patch.object(
                research_module,
                "_append_claimed_packet",
                side_effect=fail_after_replacement,
            ):
                with self.assertRaisesRegex(ResearchError, "newer pending packet exists"):
                    append_pending_packet(root, "bull")
            self.assertEqual(pending.read_text(encoding="utf-8"), replacement)
            claims = list(
                (root / "memory").glob(".research-packet.claimed-*.json")
            )
            self.assertEqual(len(claims), 1)
            self.assertEqual(claims[0].read_text(encoding="utf-8"), original)

    def test_fresh_buy_candidate_lookup_binds_profile_session_symbol_and_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "memory").mkdir()
            path = root / "memory" / "research-evidence.jsonl"
            path.write_text(
                json.dumps(self.packet, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            now = datetime(2026, 7, 16, 13, 30, tzinfo=timezone.utc)
            identity = require_current_candidate(
                root,
                "bull",
                "ETN",
                now,
                "America/New_York",
                **self._candidate_kwargs(),
            )
            self.assertEqual(identity["packet_id"], self.packet["packet_id"])
            self.assertRegex(identity["packet_sha256"], r"^[0-9a-f]{64}$")
            with self.assertRaisesRegex(ResearchError, "stale at execution time"):
                require_current_candidate(
                    root,
                    "bull",
                    "ETN",
                    datetime(2026, 7, 16, 14, 0, tzinfo=timezone.utc),
                    "America/New_York",
                    **self._candidate_kwargs(),
                )
            with self.assertRaisesRegex(ResearchError, "candidate for AAPL"):
                require_current_candidate(
                    root,
                    "bull",
                    "AAPL",
                    now,
                    "America/New_York",
                    **self._candidate_kwargs(),
                )

            with self.assertRaisesRegex(ResearchError, "does not match the planned buy"):
                require_current_candidate(
                    root,
                    "bull",
                    "ETN",
                    now,
                    "America/New_York",
                    thesis="A different plan thesis that is unrelated to the packet.",
                    invalidation=self._candidate_kwargs()["invalidation"],
                    review_by=self._candidate_kwargs()["review_by"],
                )
            superseding = copy.deepcopy(self.packet)
            superseding["packet_id"] = "bull:2026-07-16:premarket:superseding-hold"
            superseding["decision_time"] = "2026-07-16T12:05:00Z"
            superseding["decision_support"][0]["assessment"] = "hold"
            path.write_text(
                json.dumps(self.packet, separators=(",", ":"))
                + "\n"
                + json.dumps(superseding, separators=(",", ":"))
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ResearchError, "candidate for ETN"):
                require_current_candidate(
                    root,
                    "bull",
                    "ETN",
                    now,
                    "America/New_York",
                    **self._candidate_kwargs(),
                )

            stale_cutoff = copy.deepcopy(self.packet)
            stale_cutoff["market_data_cutoff"] = "2026-07-16T10:00:00Z"
            stale_cutoff["sources"][3]["as_of"] = "2026-07-16T10:00:00Z"
            stale_cutoff["claims"][3]["as_of"] = "2026-07-16T10:00:00Z"
            path.write_text(
                json.dumps(stale_cutoff, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ResearchError, "market_data_cutoff is stale"):
                require_current_candidate(
                    root,
                    "bull",
                    "ETN",
                    datetime(2026, 7, 16, 14, 1, tzinfo=timezone.utc),
                    "America/New_York",
                    **self._candidate_kwargs(),
                )

            future_hold = copy.deepcopy(self.packet)
            future_hold["packet_id"] = "bull:2026-07-16:premarket:future-hold"
            future_hold["decision_time"] = "2026-07-16T12:03:00Z"
            future_hold["decision_support"][0]["assessment"] = "hold"
            path.write_text(
                json.dumps(self.packet, separators=(",", ":"))
                + "\n"
                + json.dumps(future_hold, separators=(",", ":"))
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ResearchError, "future-dated"):
                require_current_candidate(
                    root,
                    "bull",
                    "ETN",
                    datetime(2026, 7, 16, 12, 1, tzinfo=timezone.utc),
                    "America/New_York",
                    **self._candidate_kwargs(),
                )

            path.write_text(
                json.dumps(self.packet, separators=(",", ":"))
                + "\n"
                + json.dumps(superseding, separators=(",", ":"))
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ResearchError, "no validated same-session"):
                require_current_candidate(
                    root,
                    "bull",
                    "ETN",
                    now + timedelta(days=1),
                    "America/New_York",
                    **self._candidate_kwargs(),
                )

    def test_url_canonicalization_removes_tracking_and_fragments(self):
        self.assertEqual(
            canonical_url(
                "https://Example.COM/path/?b=2&utm_source=x&a=1#instructions"
            ),
            "https://example.com/path?a=1&b=2",
        )
        with self.assertRaisesRegex(ResearchError, "valid hostname"):
            canonical_url("https://:443/path")

        packet = copy.deepcopy(self.packet)
        packet["sources"][0]["url"] += "?utm_source=test#fragment"
        validated = validate_packet(packet, "bull")
        self.assertEqual(
            validated["sources"][0]["url"],
            "https://issuer.example.invalid/investors/update",
        )


if __name__ == "__main__":
    unittest.main()
