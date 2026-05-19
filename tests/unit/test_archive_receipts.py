import unittest
from pathlib import Path

from pfem.archive_receipt import (
    collect_archive_receipt_ids,
    load_archive_receipts,
    validate_archive_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class ArchiveReceiptTests(unittest.TestCase):
    def test_records_load(self):
        records = load_archive_receipts(ROOT / "archive/archive-receipts.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["archive_receipt_id"], "archive-receipt-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_archive_receipt_ids(ROOT)

        self.assertIn("archive-receipt-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_archive_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
