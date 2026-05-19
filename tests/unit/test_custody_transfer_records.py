import unittest
from pathlib import Path

from pfem.custody_transfer_record import (
    collect_custody_transfer_record_ids,
    load_custody_transfer_records,
    validate_custody_transfer_records,
)


ROOT = Path(__file__).resolve().parents[2]


class CustodyTransferRecordTests(unittest.TestCase):
    def test_custody_transfer_records_load(self):
        records = load_custody_transfer_records(ROOT / "custody" / "custody-transfer-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].custody_transfer_record_id, "custody-transfer-basic-restore-001")
        self.assertEqual(records[0].transfer_state, "completed")

    def test_custody_transfer_record_ids_collect(self):
        record_ids = collect_custody_transfer_record_ids(ROOT)

        self.assertIn("custody-transfer-basic-restore-001", record_ids)

    def test_custody_transfer_records_validate(self):
        report = validate_custody_transfer_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
