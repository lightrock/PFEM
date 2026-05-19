import unittest
from pathlib import Path

from pfem.restore_closeout_record import (
    collect_restore_closeout_record_ids,
    load_restore_closeout_records,
    validate_restore_closeout_records,
)


ROOT = Path(__file__).resolve().parents[2]


class RestoreCloseoutRecordTests(unittest.TestCase):
    def test_restore_closeout_records_load(self):
        records = load_restore_closeout_records(ROOT / "restore" / "restore-closeout-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].restore_closeout_record_id, "restore-closeout-basic-state-001")
        self.assertEqual(records[0].closeout_state, "closed")

    def test_restore_closeout_record_ids_collect(self):
        record_ids = collect_restore_closeout_record_ids(ROOT)

        self.assertIn("restore-closeout-basic-state-001", record_ids)

    def test_restore_closeout_records_validate(self):
        report = validate_restore_closeout_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
