import unittest
from pathlib import Path

from pfem.custody_transfer_verification_receipt import (
    collect_custody_transfer_verification_receipt_ids,
    compute_ref_digest,
    load_custody_transfer_verification_receipts,
    validate_custody_transfer_verification_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class CustodyTransferVerificationReceiptTests(unittest.TestCase):
    def test_custody_transfer_verification_receipts_load(self):
        receipts = load_custody_transfer_verification_receipts(ROOT / "custody" / "custody-transfer-verification-receipts.json")

        self.assertGreaterEqual(len(receipts), 1)
        self.assertEqual(receipts[0].custody_transfer_verification_receipt_id, "custody-transfer-verification-basic-restore-001")
        self.assertEqual(receipts[0].verification_state, "passed")

    def test_custody_transfer_verification_receipt_ids_collect(self):
        receipt_ids = collect_custody_transfer_verification_receipt_ids(ROOT)

        self.assertIn("custody-transfer-verification-basic-restore-001", receipt_ids)

    def test_custody_transfer_verification_digest_matches(self):
        receipt = load_custody_transfer_verification_receipts(ROOT / "custody" / "custody-transfer-verification-receipts.json")[0]

        self.assertEqual(receipt.actual_checked_ref_digest, compute_ref_digest(receipt.checked_refs))

    def test_custody_transfer_verification_receipts_validate(self):
        report = validate_custody_transfer_verification_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
