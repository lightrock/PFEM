import unittest
from pathlib import Path

from pfem.custody_closeout_record import (
    collect_custody_closeout_record_ids,
    load_custody_closeout_records,
    validate_custody_closeout_records,
)


ROOT = Path(__file__).resolve().parents[2]


class CustodyCloseoutRecordTests(unittest.TestCase):
    def test_custody_closeout_records_load(self):
        records = load_custody_closeout_records(ROOT / "custody" / "custody-closeout-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].custody_closeout_record_id, "custody-closeout-basic-restore-001")
        self.assertEqual(records[0].closeout_state, "closed")

    def test_custody_closeout_record_ids_collect(self):
        record_ids = collect_custody_closeout_record_ids(ROOT)

        self.assertIn("custody-closeout-basic-restore-001", record_ids)

    def test_custody_closeout_records_validate(self):
        report = validate_custody_closeout_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
