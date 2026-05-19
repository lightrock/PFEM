import unittest
from pathlib import Path

from pfem.reconciliation import load_reconciliation_records, validate_reconciliation_repository


ROOT = Path(__file__).resolve().parents[2]


class ReconciliationTests(unittest.TestCase):
    def test_reconciliation_records_load(self):
        records = load_reconciliation_records(ROOT / "reconciliation" / "reconciliation-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].reconciliation_kind, "supersession")

    def test_reconciliation_repository_validates(self):
        report = validate_reconciliation_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
