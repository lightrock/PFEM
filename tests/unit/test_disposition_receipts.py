import unittest
from pathlib import Path

from pfem.disposition_receipt import (
    collect_disposition_receipt_ids,
    load_disposition_receipts,
    validate_disposition_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class DispositionReceiptTests(unittest.TestCase):
    def test_disposition_receipts_load(self):
        receipts = load_disposition_receipts(ROOT / "disposition" / "disposition-receipts.json")

        self.assertGreaterEqual(len(receipts), 1)
        self.assertEqual(receipts[0].disposition_receipt_id, "disposition-receipt-basic-restore-001")
        self.assertEqual(receipts[0].receipt_state, "completed")

    def test_disposition_receipt_ids_collect(self):
        receipt_ids = collect_disposition_receipt_ids(ROOT)

        self.assertIn("disposition-receipt-basic-restore-001", receipt_ids)

    def test_disposition_receipts_validate(self):
        report = validate_disposition_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
