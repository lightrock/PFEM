import unittest
from pathlib import Path

from pfem.custody_lifecycle_verification_receipt import (
    collect_custody_lifecycle_verification_receipt_ids,
    load_custody_lifecycle_verification_receipts,
    validate_custody_lifecycle_verification_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class CustodyLifecycleVerificationReceiptTests(unittest.TestCase):
    def test_records_load(self):
        records = load_custody_lifecycle_verification_receipts(ROOT / "custody/custody-lifecycle-verification-receipts.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["custody_lifecycle_verification_receipt_id"], "custody-lifecycle-verification-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_custody_lifecycle_verification_receipt_ids(ROOT)

        self.assertIn("custody-lifecycle-verification-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_custody_lifecycle_verification_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
