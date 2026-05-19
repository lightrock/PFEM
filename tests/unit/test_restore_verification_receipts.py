import unittest
from pathlib import Path

from pfem.restore_verification_receipt import (
    collect_restore_verification_receipt_ids,
    compute_ref_digest,
    load_restore_verification_receipts,
    validate_restore_verification_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class RestoreVerificationReceiptTests(unittest.TestCase):
    def test_restore_verification_receipts_load(self):
        receipts = load_restore_verification_receipts(ROOT / "restore" / "restore-verification-receipts.json")

        self.assertGreaterEqual(len(receipts), 1)
        self.assertEqual(receipts[0].restore_verification_receipt_id, "restore-verification-basic-state-001")
        self.assertEqual(receipts[0].verification_state, "passed")

    def test_restore_verification_receipt_ids_collect(self):
        receipt_ids = collect_restore_verification_receipt_ids(ROOT)

        self.assertIn("restore-verification-basic-state-001", receipt_ids)

    def test_restore_verification_digest_matches(self):
        receipt = load_restore_verification_receipts(ROOT / "restore" / "restore-verification-receipts.json")[0]

        self.assertEqual(receipt.actual_restored_ref_digest, compute_ref_digest(receipt.checked_refs))

    def test_restore_verification_receipts_validate(self):
        report = validate_restore_verification_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
