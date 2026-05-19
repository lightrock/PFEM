import unittest
from pathlib import Path

from pfem.snapshot_verification_receipt import (
    collect_snapshot_verification_receipt_ids,
    load_snapshot_verification_receipts,
    validate_snapshot_verification_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class SnapshotVerificationReceiptTests(unittest.TestCase):
    def test_snapshot_verification_receipts_load(self):
        receipts = load_snapshot_verification_receipts(ROOT / "snapshots" / "snapshot-verification-receipts.json")

        self.assertGreaterEqual(len(receipts), 1)
        self.assertEqual(receipts[0].snapshot_verification_receipt_id, "snapshot-verification-basic-state-001")
        self.assertEqual(receipts[0].verification_state, "passed")

    def test_snapshot_verification_receipt_ids_collect(self):
        receipt_ids = collect_snapshot_verification_receipt_ids(ROOT)

        self.assertIn("snapshot-verification-basic-state-001", receipt_ids)

    def test_snapshot_verification_receipts_validate(self):
        report = validate_snapshot_verification_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
