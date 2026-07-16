from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DataIsolationTests(unittest.TestCase):
    def test_performance_ledgers_are_profile_scoped_and_unique_by_date(self):
        for relative, expected_agent in (
            ("memory/performance.csv", "bull"),
            ("memory/aggressive/performance.csv", "aggro"),
        ):
            with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertTrue(rows, relative)
            self.assertEqual({row["agent"] for row in rows}, {expected_agent})
            dates = [row["date"] for row in rows]
            self.assertEqual(len(dates), len(set(dates)), relative)

    def test_trade_ledgers_are_profile_scoped_jsonl(self):
        for relative, expected_agent in (
            ("memory/trades.jsonl", "bull"),
            ("memory/aggressive/trades.jsonl", "aggro"),
        ):
            rows = [
                json.loads(line)
                for line in (ROOT / relative).read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertTrue(rows, relative)
            self.assertEqual(
                {str(row.get("agent", "")).lower() for row in rows},
                {expected_agent},
            )


if __name__ == "__main__":
    unittest.main()
