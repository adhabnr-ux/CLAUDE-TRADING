from __future__ import annotations

import json
import io
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from scripts import notify


class NotifyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "memory" / "aggressive").mkdir(parents=True)
        self.root_patch = patch.object(notify, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.real_verify_integration = notify._verify_integration
        self.verify_patch = patch.object(notify, "_verify_integration", return_value=None)
        self.verify = self.verify_patch.start()
        self.addCleanup(self.verify_patch.stop)
        self.digest_patch = patch.object(
            notify, "_methodology_digest", return_value="a" * 64
        )
        self.digest_patch.start()
        self.addCleanup(self.digest_patch.stop)
        self.env = {
            "TELEGRAM_BOT_TOKEN": "test-token",
            "TELEGRAM_CHAT_ID": "12345",
            "TRADING_AGENT": "bull",
            "CLAUDE_CODE_REMOTE": "true",
        }
        self.sent: list[str] = []

    def _sender(self, token: str, chat_id: str, message: str) -> int:
        self.assertEqual(token, "test-token")
        self.assertEqual(chat_id, "12345")
        self.sent.append(message)
        return 77

    def _arm(self, agent: str) -> Path:
        path = self.root / notify.PROOF_MARKERS[agent]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(notify.PROOF_BYTES)
        return path

    def _deliver_proof(self, message: str, **kwargs):
        return notify.deliver(
            message,
            env=kwargs.pop("env", self.env),
            sender=kwargs.pop("sender", self._sender),
            proof_receipt="a" * 64,
            **kwargs,
        )

    def test_bull_proof_is_appended_once_and_profile_isolated(self):
        bull = self._arm("bull")
        aggro = self._arm("aggro")
        result = self._deliver_proof("Bull pre-market: complete")
        self.assertTrue(result["proof_appended"])
        self.assertTrue(result["remote_environment"])
        self.assertEqual(
            self.sent,
            [
                "Bull pre-market: complete\n"
                "New instructions recieve from QuantMind and ATLAS"
            ],
        )
        self.assertFalse(bull.exists())
        self.assertTrue(aggro.exists())

        self._deliver_proof("Bull second message")
        self.assertEqual(self.sent[-1], "Bull second message")

    def test_aggro_uses_its_own_marker(self):
        bull = self._arm("bull")
        aggro = self._arm("aggro")
        env = {**self.env, "TRADING_AGENT": "aggro"}
        self._deliver_proof("AGGRO done", env=env)
        self.assertEqual(
            self.sent[-1],
            "AGGRO done\nNew instructions recieve from QuantMind and ATLAS",
        )
        self.assertTrue(bull.exists())
        self.assertFalse(aggro.exists())

    def test_local_notification_does_not_consume_remote_proof(self):
        marker = self._arm("bull")
        env = {**self.env, "CLAUDE_CODE_REMOTE": "false"}
        result = notify.deliver("Local check", env=env, sender=self._sender)
        self.assertFalse(result["proof_appended"])
        self.assertFalse(result["remote_environment"])
        self.assertEqual(self.sent[-1], "Local check")
        self.assertTrue(marker.exists())

    def test_existing_exact_suffix_is_not_duplicated(self):
        marker = self._arm("bull")
        message = f"Bull done\n{notify.PROOF_TEXT}"
        self._deliver_proof(message)
        self.assertEqual(self.sent[-1], message)
        self.assertFalse(marker.exists())

    def test_delivery_failure_retains_marker(self):
        marker = self._arm("bull")

        def fail(_token: str, _chat: str, _message: str) -> int:
            raise notify.NotifyError("Telegram unavailable")

        with self.assertRaisesRegex(notify.NotifyError, "unavailable"):
            self._deliver_proof("Bull failed", sender=fail)
        self.assertTrue(marker.exists())

    def test_integration_failure_retains_marker_and_sends_base_alert(self):
        marker = self._arm("bull")
        self.verify.side_effect = notify.NotifyError("snapshot mismatch")
        with self.assertRaisesRegex(notify.NotifyError, "snapshot mismatch"):
            self._deliver_proof("Bull failed")
        self.assertTrue(marker.exists())
        self.assertEqual(self.sent, ["Bull failed"])

    def test_unexpected_proof_failure_still_sends_base_alert(self):
        marker = self._arm("bull")
        self.verify.side_effect = RuntimeError("unexpected validator bug")
        with self.assertRaisesRegex(notify.NotifyError, "RuntimeError"):
            self._deliver_proof("Bull safety alert")
        self.assertEqual(self.sent, ["Bull safety alert"])
        self.assertTrue(marker.exists())

    def test_missing_receipt_sends_base_alert_and_retains_marker(self):
        marker = self._arm("bull")
        result = notify.deliver(
            "Urgent safety alert",
            env=self.env,
            sender=self._sender,
        )
        self.assertEqual(self.sent, ["Urgent safety alert"])
        self.assertFalse(result["proof_appended"])
        self.assertTrue(result["proof_pending"])
        self.assertTrue(marker.exists())

    def test_invalid_receipt_sends_base_alert_then_fails_visible(self):
        marker = self._arm("bull")
        with self.assertRaisesRegex(notify.NotifyError, "receipt is invalid"):
            notify.deliver(
                "Urgent safety alert",
                env=self.env,
                sender=self._sender,
                proof_receipt="b" * 64,
            )
        self.assertEqual(self.sent, ["Urgent safety alert"])
        self.assertTrue(marker.exists())

    def test_malformed_or_symlink_marker_fails_closed(self):
        marker = self._arm("bull")
        marker.write_text("wrong\n", encoding="utf-8")
        with self.assertRaisesRegex(notify.NotifyError, "content is invalid"):
            self._deliver_proof("Bull")
        self.assertEqual(self.sent[-1], "Bull")
        marker.unlink()
        target = self.root / "target"
        target.write_bytes(notify.PROOF_BYTES)
        marker.symlink_to(target)
        with self.assertRaisesRegex(notify.NotifyError, "regular file"):
            self._deliver_proof("Bull")
        self.assertEqual(self.sent[-1], "Bull")

    def test_environment_and_message_limits_are_strict(self):
        with self.assertRaisesRegex(notify.NotifyError, "TRADING_AGENT"):
            notify.deliver(
                "Bull",
                env={**self.env, "TRADING_AGENT": ""},
                sender=self._sender,
            )
        with self.assertRaisesRegex(notify.NotifyError, "4000"):
            notify.deliver("x" * 4001, env=self.env, sender=self._sender)
        with self.assertRaisesRegex(notify.NotifyError, "positive message id"):
            notify.deliver(
                "Bull",
                env=self.env,
                sender=lambda *_args: True,
            )

    def test_telegram_success_response_requires_positive_message_id(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            @staticmethod
            def read(_limit: int) -> bytes:
                return json.dumps({"ok": True, "result": {"message_id": 42}}).encode()

        captured = {}

        def opener(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return Response()

        message_id = notify._send_telegram("secret", "123", "hello", opener=opener)
        self.assertEqual(message_id, 42)
        self.assertEqual(captured["timeout"], 30)
        self.assertIn(b"text=hello", captured["request"].data)

    def test_telegram_rejects_false_zero_and_boolean_acknowledgements(self):
        class Response:
            def __init__(self, payload):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit: int) -> bytes:
                return json.dumps(self.payload).encode()

        for payload in (
            {"ok": False, "result": {"message_id": 42}},
            {"ok": True, "result": {"message_id": 0}},
            {"ok": True, "result": {"message_id": True}},
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(notify.NotifyError):
                    notify._send_telegram(
                        "secret",
                        "123",
                        "hello",
                        opener=lambda *_args, **_kwargs: Response(payload),
                    )

    def test_telegram_rejects_malformed_and_oversized_responses(self):
        class Response:
            def __init__(self, payload: bytes):
                self.payload = payload

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit: int) -> bytes:
                return self.payload

        for payload in (b"not-json", b"x" * (notify.MAX_RESPONSE_BYTES + 1)):
            with self.subTest(size=len(payload)):
                with self.assertRaises(notify.NotifyError):
                    notify._send_telegram(
                        "secret",
                        "123",
                        "hello",
                        opener=lambda *_args, **_kwargs: Response(payload),
                    )

    def test_http_and_timeout_errors_are_fail_visible(self):
        failures = (
            urllib.error.HTTPError(
                "https://api.telegram.org", 500, "bad", None, io.BytesIO(b"")
            ),
            TimeoutError(),
        )
        for failure in failures:
            with self.subTest(failure=type(failure).__name__):
                def opener(*_args, **_kwargs):
                    raise failure

                with self.assertRaises(notify.NotifyError):
                    notify._send_telegram("secret", "123", "hello", opener=opener)

    def test_real_integration_verifier_accepts_checked_in_snapshots(self):
        repository = Path(__file__).resolve().parents[1]
        with patch.object(notify, "ROOT", repository):
            self.real_verify_integration()

    def test_network_error_does_not_expose_bot_token(self):
        def opener(_request, timeout):
            self.assertEqual(timeout, 30)
            raise urllib.error.URLError("secret-token leaked by transport")

        with self.assertRaises(notify.NotifyError) as caught:
            notify._send_telegram(
                "secret-token",
                "123",
                "hello",
                opener=opener,
            )
        self.assertNotIn("secret-token", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
