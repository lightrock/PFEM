import unittest
from pathlib import Path

from pfem.preservation_verification_receipt import (
    collect_preservation_verification_receipt_ids,
    load_preservation_verification_receipts,
    validate_preservation_verification_receipts,
)


ROOT = Path(__file__).resolve().parents[2]


class PreservationVerificationReceiptTests(unittest.TestCase):
    def test_records_load(self):
        records = load_preservation_verification_receipts(ROOT / "preservation/preservation-verification-receipts.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["preservation_verification_receipt_id"], "preservation-verification-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_preservation_verification_receipt_ids(ROOT)

        self.assertIn("preservation-verification-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_preservation_verification_receipts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
