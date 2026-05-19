import unittest
from pathlib import Path

from pfem.archive_verification_receipt import (
    collect_archive_verification_receipt_ids,
    load_archive_verification_receipts,
    validate_archive_verification_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class ArchiveVerificationReceiptTests(unittest.TestCase):
    def test_records_load(self):
        records = load_archive_verification_receipts(ROOT / "archive/archive-verification-receipts.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["archive_verification_receipt_id"], "archive-verification-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_archive_verification_receipt_ids(ROOT)

        self.assertIn("archive-verification-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_archive_verification_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
