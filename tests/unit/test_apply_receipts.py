import unittest
from pathlib import Path

from pfem.apply_receipt import collect_apply_receipt_ids, load_apply_receipts, validate_apply_receipts


ROOT = Path(__file__).resolve().parents[2]


class ApplyReceiptTests(unittest.TestCase):
    def test_apply_receipts_load(self):
        receipts = load_apply_receipts(ROOT / "apply" / "apply-receipts.json")

        self.assertGreaterEqual(len(receipts), 1)
        self.assertEqual(receipts[0].apply_receipt_id, "apply-receipt-basic-merge-001")
        self.assertEqual(receipts[0].apply_state, "applied")

    def test_apply_receipt_ids_collect(self):
        receipt_ids = collect_apply_receipt_ids(ROOT)

        self.assertIn("apply-receipt-basic-merge-001", receipt_ids)

    def test_apply_receipts_validate(self):
        report = validate_apply_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
