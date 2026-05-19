import unittest
from pathlib import Path

from pfem.custody_chain_verification_receipt import (
    collect_custody_chain_verification_receipt_ids,
    compute_chain_ref_digest,
    load_custody_chain_verification_receipts,
    validate_custody_chain_verification_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class CustodyChainVerificationReceiptTests(unittest.TestCase):
    def test_custody_chain_verification_receipts_load(self):
        receipts = load_custody_chain_verification_receipts(ROOT / "custody" / "custody-chain-verification-receipts.json")

        self.assertGreaterEqual(len(receipts), 1)
        self.assertEqual(receipts[0].custody_chain_verification_receipt_id, "custody-chain-verification-basic-restore-001")
        self.assertEqual(receipts[0].verification_state, "passed")

    def test_custody_chain_verification_receipt_ids_collect(self):
        receipt_ids = collect_custody_chain_verification_receipt_ids(ROOT)

        self.assertIn("custody-chain-verification-basic-restore-001", receipt_ids)

    def test_custody_chain_verification_digest_matches(self):
        receipt = load_custody_chain_verification_receipts(ROOT / "custody" / "custody-chain-verification-receipts.json")[0]

        self.assertEqual(receipt.actual_chain_ref_digest, compute_chain_ref_digest(receipt.checked_chain_refs))

    def test_custody_chain_verification_receipts_validate(self):
        report = validate_custody_chain_verification_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
