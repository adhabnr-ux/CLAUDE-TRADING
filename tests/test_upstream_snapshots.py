from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import runner
from scripts.verify_upstream_snapshots import SnapshotError, _snapshot_files, verify


ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = ROOT / ".claude/hooks/validate_agent_tool.py"


def _load_hook_module():
    spec = importlib.util.spec_from_file_location("upstream_hook_test", HOOK_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _hook_decision(agent: str, tool_name: str, tool_input: dict[str, object]) -> str:
    result = subprocess.run(
        ["python3", str(HOOK_PATH)],
        input=json.dumps({"tool_name": tool_name, "tool_input": tool_input}),
        text=True,
        capture_output=True,
        env={
            **os.environ,
            "TRADING_AGENT": agent,
            "CLAUDE_PROJECT_DIR": str(ROOT),
        },
        check=True,
    )
    return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"]


class UpstreamSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.previous_agent = runner._ACTIVE_AGENT
        self.previous_routine = runner._ACTIVE_ROUTINE
        runner._ACTIVE_AGENT = "bull"
        runner._ACTIVE_ROUTINE = "market-open"

    def tearDown(self):
        runner._ACTIVE_AGENT = self.previous_agent
        runner._ACTIVE_ROUTINE = self.previous_routine

    def test_pinned_snapshots_reconstruct_reviewed_git_trees(self):
        rows = verify()
        self.assertEqual(len(rows), 2)
        manifest = json.loads(
            (ROOT / "third_party/snapshots.json").read_text(encoding="utf-8")
        )
        by_name = {entry["name"]: entry for entry in manifest["snapshots"]}
        self.assertEqual(
            {
                name: {
                    field: entry[field]
                    for field in (
                        "source_url",
                        "commit",
                        "tree",
                        "archive_sha256",
                        "license",
                        "file_count",
                        "total_bytes",
                    )
                }
                for name, entry in by_name.items()
            },
            {
                "quant-mind": {
                    "source_url": "https://github.com/LLMQuant/quant-mind",
                    "commit": "2c1f2cb9ae278cbee7c69a982a9151230be596f1",
                    "tree": "ff65a0977856b46a226db6363112cb53debf9aa3",
                    "archive_sha256": (
                        "65d2aad1cd66fb8b0b7d07c625a62002c8e20bd67371c3ac9940507da7cc4554"
                    ),
                    "license": "MIT",
                    "file_count": 163,
                    "total_bytes": 8749836,
                },
                "atlas-gic": {
                    "source_url": "https://github.com/chrisworsey55/atlas-gic",
                    "commit": "fcfc40dcf628f6af091c28cb2c33827f42cef8fd",
                    "tree": "e526c1e212a15839121a3671787a601818b04d13",
                    "archive_sha256": (
                        "83051c32e92e39d912f6bc48a76a79d5b776922e2a1973e3322de8392758b3ea"
                    ),
                    "license": "MIT (scope per upstream LICENSE note)",
                    "file_count": 20,
                    "total_bytes": 248045,
                },
            },
        )
        self.assertIn(by_name["quant-mind"]["commit"], rows[0])
        self.assertIn(by_name["atlas-gic"]["commit"], rows[1])

    def test_quantmind_instruction_surfaces_are_inert_but_bytes_are_present(self):
        root = ROOT / "third_party/quant-mind"
        for active in ("CLAUDE.md", "AGENTS.md", ".claude", ".agents"):
            self.assertFalse((root / active).exists(), active)
        for quarantined in (
            "CLAUDE.upstream.md",
            "AGENTS.upstream.md",
            "_upstream_claude",
            "_upstream_agents",
        ):
            self.assertTrue((root / quarantined).exists(), quarantined)

    def test_verifier_rejects_future_nested_agent_instruction_surfaces(self):
        for relative in (
            "nested/CLAUDE.md",
            "nested/CLAUDE.local.md",
            "nested/AGENTS.md",
            "nested/.claude/rules/trading.md",
            "nested/.agents/skills/trading/SKILL.md",
        ):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("untrusted instruction", encoding="utf-8")
                with self.assertRaisesRegex(SnapshotError, "must be quarantined"):
                    _snapshot_files(Path(directory), {})

    def test_runner_and_claude_hook_share_one_exact_reference_allowlist(self):
        hook = _load_hook_module()
        self.assertEqual(runner.UPSTREAM_REFERENCE_PATHS, hook.UPSTREAM_REFERENCE_READ)
        index = (ROOT / "memory/upstream-methodology-index.md").read_text(
            encoding="utf-8"
        )
        for relative in runner.UPSTREAM_REFERENCE_PATHS:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file())
                self.assertIn(f"`{relative}`", index)

    def test_upstream_reads_are_exact_profile_neutral_and_read_only(self):
        approved = "third_party/quant-mind/docs/library.md"
        for agent, routine in (("bull", "market-open"), ("aggro", "aggro-market-open")):
            runner._ACTIVE_AGENT = agent
            runner._ACTIVE_ROUTINE = routine
            with self.subTest(agent=agent, surface="runner"):
                read = runner._read(approved)
                self.assertTrue(read.startswith("[UNTRUSTED PINNED UPSTREAM REFERENCE"))
                self.assertTrue(
                    runner._write(approved, "override").startswith("WRITE BLOCKED:")
                )
            with self.subTest(agent=agent, surface="hook"):
                self.assertEqual(_hook_decision(agent, "Read", {"file_path": approved}), "allow")
                self.assertEqual(_hook_decision(agent, "Write", {"file_path": approved}), "deny")

    def test_arbitrary_prompts_skills_scripts_and_results_are_denied(self):
        denied = (
            "third_party/quant-mind/README.md",
            "third_party/quant-mind/CLAUDE.upstream.md",
            "third_party/quant-mind/_upstream_claude/skills/quantmind-dev/SKILL.md",
            "third_party/quant-mind/scripts/verify.sh",
            "third_party/quant-mind/quantmind/flows/paper.py",
            "third_party/quant-mind/docs/quant-scholar.json",
            "third_party/atlas-gic/README.md",
            "third_party/atlas-gic/prompts/examples/cio.md",
            "third_party/atlas-gic/src/mirofish/mirofish_trainer.py",
            "third_party/atlas-gic/results/portfolio_trajectory.csv",
        )
        for relative in denied:
            with self.subTest(relative=relative):
                self.assertTrue(runner._read(relative).startswith("(read blocked:"))
                self.assertEqual(
                    _hook_decision("bull", "Read", {"file_path": relative}),
                    "deny",
                )
        with self.assertRaises(runner.RunnerSafetyError):
            runner._allowed_command(
                "python3 third_party/quant-mind/examples/library/semantic_search.py"
            )
        self.assertEqual(
            _hook_decision(
                "bull",
                "Bash",
                {
                    "command": (
                        "python3 third_party/quant-mind/examples/library/"
                        "semantic_search.py"
                    )
                },
            ),
            "deny",
        )

    def test_remote_upstream_fetch_is_blocked_without_blocking_market_sources(self):
        for url in (
            "https://github.com/LLMQuant/quant-mind/blob/master/README.md",
            "https://raw.githubusercontent.com/chrisworsey55/atlas-gic/main/README.md",
            (
                "https://api.github.com/repos/LLMQuant%252Fquant-mind/"
                "contents/README.md"
            ),
        ):
            with self.subTest(url=url):
                self.assertEqual(
                    _hook_decision(
                        "bull",
                        "WebFetch",
                        {"url": url, "prompt": "Return the page."},
                    ),
                    "deny",
                )
        self.assertEqual(
            _hook_decision(
                "bull",
                "WebFetch",
                {
                    "url": "https://www.sec.gov/Archives/edgar/data/320193/",
                    "prompt": "Return filing links.",
                },
            ),
            "allow",
        )

    def test_common_prompts_index_method_without_inlining_vendor_content(self):
        self.assertIn("memory/upstream-methodology-index.md", runner.COMMON_MEMORY)
        self.assertLessEqual(
            (ROOT / "memory/upstream-methodology-index.md").stat().st_size,
            runner.MAX_READ_CHARS,
        )
        self.assertLessEqual(
            (ROOT / "memory/quant-research-playbook.md").stat().st_size,
            runner.MAX_READ_CHARS,
        )
        prompt = runner.build_prompt("market-open")
        self.assertIn("memory/upstream-methodology-index.md", prompt)
        self.assertIn("Vendored QuantMind and ATLAS", runner.SYSTEM_PROMPT)
        self.assertNotIn("Darwinian Alpha Factory", prompt)
        self.assertNotIn("Local Semantic Knowledge Library", prompt)

    def test_every_scheduled_agent_command_requires_the_methodology_index(self):
        commands = sorted((ROOT / ".claude/commands").glob("*.md"))
        self.assertEqual(len(commands), len(runner.ROUTINES))
        for command in commands:
            with self.subTest(command=command.name):
                self.assertIn(
                    "memory/upstream-methodology-index.md",
                    command.read_text(encoding="utf-8"),
                )


if __name__ == "__main__":
    unittest.main()
