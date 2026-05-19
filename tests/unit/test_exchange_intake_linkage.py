import unittest
from pathlib import Path

from pfem.exchange import load_exchange_receipts, validate_exchange_repository


ROOT = Path(__file__).resolve().parents[2]


class ExchangeIntakeLinkageTests(unittest.TestCase):
    def test_accepted_exchange_receipt_links_to_intake_path(self):
        receipts = load_exchange_receipts(ROOT / "exchange" / "exchange-receipts.json")
        accepted = next(
            receipt
            for receipt in receipts
            if receipt.exchange_receipt_id == "exchange-receipt-basic-accept-001"
        )

        self.assertEqual(accepted.inbox_item_id, "inbox-item-basic-manual-export-001")
        self.assertEqual(accepted.intake_decision_id, "intake-decision-basic-manual-export-001")
        self.assertEqual(accepted.transport_receipt_id, "transport-receipt-basic-manual-export-001")

    def test_exchange_repository_validates(self):
        report = validate_exchange_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreaterEqual(report.checked_receipts, 2)


if __name__ == "__main__":
    unittest.main()
