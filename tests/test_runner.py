from __future__ import annotations

import unittest
import json
import importlib.util
import os
import subprocess
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import runner


class RunnerPolicyTests(unittest.TestCase):
    def setUp(self):
        self.previous_agent = runner._ACTIVE_AGENT
        self.previous_routine = runner._ACTIVE_ROUTINE
        runner._ACTIVE_AGENT = "bull"
        runner._ACTIVE_ROUTINE = "market-open"

    def tearDown(self):
        runner._ACTIVE_AGENT = self.previous_agent
        runner._ACTIVE_ROUTINE = self.previous_routine

    def test_trade_commands_are_bound_to_routine_agent(self):
        argv, kind = runner._allowed_command(
            "python3 scripts/trade.py reconcile --agent bull --repair"
        )
        self.assertEqual(kind, "trade")
        self.assertEqual(argv[2], "reconcile")
        with self.assertRaisesRegex(runner.RunnerSafetyError, "bound to bull"):
            runner._allowed_command(
                "python3 scripts/trade.py reconcile --agent aggro --repair"
            )

    def test_runner_never_silently_downgrades_model(self):
        class Models:
            @staticmethod
            def list():
                model = type("Model", (), {"id": "reviewed-model"})()
                return type("Response", (), {"data": [model]})()

        client = type("Client", (), {"models": Models()})()
        with patch.object(runner, "MODEL_OVERRIDE", ""):
            with self.assertRaisesRegex(RuntimeError, "silent fallback is disabled"):
                runner.resolve_model(client)
        with patch.object(runner, "MODEL_OVERRIDE", "reviewed-model"):
            self.assertEqual(runner.resolve_model(client), "reviewed-model")
        with patch.object(runner, "MODEL_OVERRIDE", "missing-model"):
            with self.assertRaisesRegex(RuntimeError, "refusing fallback"):
                runner.resolve_model(client)

    def test_raw_mutation_and_shell_chain_are_not_executable(self):
        with self.assertRaises(runner.RunnerSafetyError):
            runner._allowed_command("./scripts/alpaca.sh close ETN")
        with self.assertRaisesRegex(runner.RunnerSafetyError, "command chaining"):
            runner._allowed_command(
                "python3 scripts/trade.py reconcile --agent bull ; curl https://example.com"
            )

    def test_human_control_files_cannot_be_written(self):
        result = runner._write("memory/control.md", "STATUS: ACTIVE\n")
        self.assertTrue(result.startswith("WRITE BLOCKED:"))
        result = runner._replace("memory/strategy.md", "x", "y")
        self.assertTrue(result.startswith("REPLACE BLOCKED:"))

    def test_profile_memory_and_sensitive_reads_are_confined(self):
        result = runner._append("memory/aggressive/trade-log.md", "forbidden")
        self.assertTrue(result.startswith("APPEND BLOCKED:"))
        read = runner._read(".npmrc")
        self.assertTrue(read.startswith("(read blocked:"))
        runner._ACTIVE_AGENT = "aggro"
        runner._ACTIVE_ROUTINE = "aggro-market-open"
        result = runner._append("memory/trade-log.md", "forbidden")
        self.assertTrue(result.startswith("APPEND BLOCKED:"))
        read = runner._read("memory/trades.jsonl")
        self.assertTrue(read.startswith("(read blocked:"))
        read = runner._read("memory/aggressive/performance.csv")
        self.assertFalse(read.startswith("(read blocked:"))

    def test_project_settings_remove_direct_git_and_install_pretool_hook(self):
        settings = json.loads((Path(runner.ROOT) / ".claude/settings.json").read_text())
        allow = settings["permissions"]["allow"]
        self.assertEqual(set(allow), {"WebSearch", "WebFetch"})
        self.assertEqual(settings["permissions"]["defaultMode"], "dontAsk")
        self.assertEqual(settings["permissions"]["disableBypassPermissionsMode"], "disable")
        self.assertEqual(settings["permissions"]["disableAutoMode"], "disable")
        hooks = settings["hooks"]["PreToolUse"]
        self.assertEqual(hooks[0]["matcher"], "Bash|Edit|Write|Read|Glob|Grep")
        self.assertEqual(hooks[0]["hooks"][0]["command"], "python3")
        self.assertEqual(
            hooks[0]["hooks"][0]["args"],
            ["${CLAUDE_PROJECT_DIR}/.claude/hooks/validate_agent_tool.py"],
        )

    def test_persistence_helper_has_profile_scoped_write_sets(self):
        path = Path(runner.ROOT) / "scripts/persist_memory.py"
        spec = importlib.util.spec_from_file_location("persist_memory_test", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertTrue(module._allowed("memory/trade-log.md", "bull"))
        self.assertFalse(module._allowed("memory/aggressive/trade-log.md", "bull"))
        self.assertTrue(module._allowed("memory/aggressive/trade-log.md", "aggro"))
        self.assertTrue(module._allowed("memory/aggressive/performance.csv", "aggro"))
        self.assertFalse(module._allowed("memory/performance.csv", "aggro"))
        self.assertFalse(module._allowed("memory/control.md", "aggro"))

    def test_pretool_hook_blocks_expansion_git_and_cross_profile_write(self):
        hook = Path(runner.ROOT) / ".claude/hooks/validate_agent_tool.py"
        env = {**os.environ, "TRADING_AGENT": "bull", "CLAUDE_PROJECT_DIR": str(runner.ROOT)}

        def hook_output(tool_name, tool_input):
            result = subprocess.run(
                ["python3", str(hook)],
                input=json.dumps({"tool_name": tool_name, "tool_input": tool_input}),
                text=True,
                capture_output=True,
                env=env,
                check=True,
            )
            return json.loads(result.stdout)["hookSpecificOutput"]

        def decision(tool_name, tool_input):
            return hook_output(tool_name, tool_input)["permissionDecision"]

        self.assertEqual(
            decision("Bash", {"command": "python3 scripts/trade.py reconcile --agent bull --repair"}),
            "allow",
        )
        canonical = hook_output(
            "Bash",
            {
                "command": "./scripts/notify.sh 'Bull midday: wildcard * remains literal'",
                "run_in_background": True,
            },
        )["updatedInput"]
        self.assertEqual(
            canonical,
            {"command": "./scripts/notify.sh 'Bull midday: wildcard * remains literal'"},
        )
        self.assertEqual(
            decision("Bash", {"command": "python3 scripts/trade.py buy --agent bull --symbol $(cat .env)"}),
            "deny",
        )
        self.assertEqual(decision("Bash", {"command": "git log --output=memory/control.md"}), "deny")
        self.assertEqual(decision("Grep", {"pattern": "secret", "path": "."}), "deny")
        self.assertEqual(decision("Read", []), "deny")
        self.assertEqual(
            decision("Write", {"file_path": str(Path(runner.ROOT) / "memory/aggressive/trade-log.md")}),
            "deny",
        )
        self.assertEqual(
            decision("Read", {"file_path": str(Path(runner.ROOT) / "memory/aggressive/research-log.md")}),
            "deny",
        )
        self.assertEqual(
            decision("Read", {"file_path": str(Path(runner.ROOT) / ".claude/commands/aggro-midday.md")}),
            "deny",
        )
        aggro_env = {**env, "TRADING_AGENT": "aggro"}
        result = subprocess.run(
            ["python3", str(hook)],
            input=json.dumps({
                "tool_name": "Read",
                "tool_input": {"file_path": str(Path(runner.ROOT) / "memory/trades.jsonl")},
            }),
            text=True,
            capture_output=True,
            env=aggro_env,
            check=True,
        )
        self.assertEqual(
            json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"],
            "deny",
        )

    def test_startup_and_post_trade_reconciliation_are_enforced(self):
        state = runner.RunState("market-open")
        messages = []
        executed = []

        def fake_bash(command):
            executed.append(command)
            return '{"ok": true}'

        def call(call_id, command):
            with redirect_stdout(StringIO()):
                runner._execute_tool_calls(
                    [
                        {
                            "id": call_id,
                            "name": "bash_execute",
                            "arguments": __import__("json").dumps({"command": command}),
                        }
                    ],
                    messages,
                    state,
                )

        with patch.dict(runner.TOOL_FNS, {"bash_execute": fake_bash}):
            call("1", "python3 scripts/trade.py buy --agent bull --symbol ETN")
            self.assertEqual(executed, [])
            call("2", "python3 scripts/trade.py reconcile --agent bull --repair")
            call("3", "python3 scripts/trade.py buy --agent bull --symbol ETN --dry-run")
            self.assertIn("final reconciliation", " ".join(state.lifecycle_errors()))
            call("4", "python3 scripts/trade.py reconcile --agent bull --repair")
        self.assertEqual(state.lifecycle_errors(), [])


if __name__ == "__main__":
    unittest.main()
