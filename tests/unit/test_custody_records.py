import unittest
from pathlib import Path

from pfem.custody_record import (
    collect_custody_record_ids,
    load_custody_records,
    validate_custody_records,
)


ROOT = Path(__file__).resolve().parents[2]


class CustodyRecordTests(unittest.TestCase):
    def test_custody_records_load(self):
        records = load_custody_records(ROOT / "custody" / "custody-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].custody_record_id, "custody-record-basic-restore-001")
        self.assertEqual(records[0].custody_state, "active")

    def test_custody_record_ids_collect(self):
        record_ids = collect_custody_record_ids(ROOT)

        self.assertIn("custody-record-basic-restore-001", record_ids)

    def test_custody_records_validate(self):
        report = validate_custody_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
