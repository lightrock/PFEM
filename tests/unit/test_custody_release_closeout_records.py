import unittest
from pathlib import Path

from pfem.custody_release_closeout_record import (
    collect_custody_release_closeout_record_ids,
    load_custody_release_closeout_records,
    validate_custody_release_closeout_records,
)


ROOT = Path(__file__).resolve().parents[2]


class CustodyReleaseCloseoutRecordTests(unittest.TestCase):
    def test_records_load(self):
        records = load_custody_release_closeout_records(ROOT / "custody/custody-release-closeout-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["custody_release_closeout_record_id"], "custody-release-closeout-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_custody_release_closeout_record_ids(ROOT)

        self.assertIn("custody-release-closeout-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_custody_release_closeout_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
