from __future__ import annotations

import unittest

from bulltrader.lock import account_lock
from bulltrader.risk import RiskRejected


class AccountLockTests(unittest.TestCase):
    def test_same_host_account_lock_fails_closed_on_overlap(self):
        with account_lock("unit-test-paper-account"):
            with self.assertRaisesRegex(RiskRejected, "another trading gateway"):
                with account_lock("unit-test-paper-account"):
                    self.fail("overlapping lock unexpectedly succeeded")

    def test_account_lock_requires_expected_identity(self):
        with self.assertRaisesRegex(RiskRejected, "EXPECTED_ACCOUNT_ID"):
            with account_lock(""):
                self.fail("empty identity unexpectedly acquired a lock")


if __name__ == "__main__":
    unittest.main()
