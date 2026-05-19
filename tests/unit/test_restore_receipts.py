import unittest
from pathlib import Path

from pfem.restore_receipt import (
    collect_restore_receipt_ids,
    load_restore_receipts,
    validate_restore_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class RestoreReceiptTests(unittest.TestCase):
    def test_restore_receipts_load(self):
        receipts = load_restore_receipts(ROOT / "restore" / "restore-receipts.json")

        self.assertGreaterEqual(len(receipts), 1)
        self.assertEqual(receipts[0].restore_receipt_id, "restore-receipt-basic-state-001")
        self.assertEqual(receipts[0].restore_state, "completed")

    def test_restore_receipt_ids_collect(self):
        receipt_ids = collect_restore_receipt_ids(ROOT)

        self.assertIn("restore-receipt-basic-state-001", receipt_ids)

    def test_restore_receipts_validate(self):
        report = validate_restore_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
