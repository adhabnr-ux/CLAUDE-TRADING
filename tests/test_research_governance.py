from __future__ import annotations

import json
import unittest
from pathlib import Path

import runner


ROOT = Path(__file__).resolve().parents[1]


class ResearchGovernanceTests(unittest.TestCase):
    def test_runtime_playbook_is_compact_pinned_and_non_executable(self):
        path = ROOT / "memory/quant-research-playbook.md"
        text = path.read_text(encoding="utf-8")
        self.assertLessEqual(len(text), runner.MAX_READ_CHARS)
        self.assertIn("168720dc5f4eed3d8b2e55f23026fe77ecb95b67", text)
        self.assertIn("fcfc40dcf628f6af091c28cb2c33827f42cef8fd", text)
        self.assertGreaterEqual(text.count("MIT"), 2)
        self.assertIn("There is no autonomous path to `ACTIVE`", text)
        self.assertIn("cannot authorize execution", text)

    def test_both_profiles_and_review_routines_use_the_protocol(self):
        commands = [
            ".claude/commands/premarket.md",
            ".claude/commands/aggro-premarket.md",
            ".claude/commands/weekly-review.md",
            ".claude/commands/aggro-weekly-review.md",
            ".claude/commands/monthly-review.md",
        ]
        routines = [
            "routines/premarket.md",
            "routines/aggro-premarket.md",
            "routines/weekly-review.md",
            "routines/aggro-weekly-review.md",
            "routines/monthly-review.md",
        ]
        for relative in commands:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("quant-research-playbook.md", text, relative)
            self.assertIn("scripts/research.py validate", text, relative)
        for relative in routines:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("quant-research-playbook.md", text, relative)
            self.assertIn("command owns", text, relative)
            self.assertNotIn("scripts/research.py", text, relative)

    def test_premarket_commands_use_fixed_append_workflow(self):
        expectations = {
            ".claude/commands/premarket.md": (
                "memory/research-packet.pending.json",
                "python3 scripts/research.py append --agent bull",
            ),
            ".claude/commands/aggro-premarket.md": (
                "memory/aggressive/research-packet.pending.json",
                "python3 scripts/research.py append --agent aggro",
            ),
        }
        for relative, required in expectations.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            for phrase in required:
                self.assertIn(phrase, text, relative)
            self.assertIn("Never use Edit, Write", text, relative)

    def test_experiment_schema_cannot_activate_or_approve(self):
        schema = json.loads(
            (ROOT / "schemas/strategy-experiment.schema.json").read_text(
                encoding="utf-8"
            )
        )
        statuses = schema["properties"]["status"]["enum"]
        self.assertEqual(statuses, ["DRAFT", "REJECTED"])
        self.assertNotIn("allOf", schema)
        decisions = schema["properties"]["human_review"]["properties"]["decision"]["enum"]
        self.assertEqual(decisions, ["PENDING", "REJECTED"])


if __name__ == "__main__":
    unittest.main()
