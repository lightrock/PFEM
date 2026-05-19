import unittest
from pathlib import Path

from pfem.transport_receipt import collect_transport_receipt_ids, load_transport_receipts, validate_transport_receipts


ROOT = Path(__file__).resolve().parents[2]


class TransportReceiptTests(unittest.TestCase):
    def test_transport_receipts_load(self):
        receipts = load_transport_receipts(ROOT / "transport" / "transport-receipts.json")

        self.assertGreaterEqual(len(receipts), 1)
        self.assertEqual(receipts[0].transport_receipt_id, "transport-receipt-basic-manual-export-001")
        self.assertEqual(receipts[0].delivery_job_id, "delivery-job-basic-manual-export-001")
        self.assertEqual(receipts[0].outbox_item_id, "outbox-item-basic-manual-export-001")
        self.assertEqual(receipts[0].transport_state, "succeeded")

    def test_transport_receipt_ids_collect(self):
        receipt_ids = collect_transport_receipt_ids(ROOT)

        self.assertIn("transport-receipt-basic-manual-export-001", receipt_ids)

    def test_transport_receipts_validate(self):
        report = validate_transport_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
