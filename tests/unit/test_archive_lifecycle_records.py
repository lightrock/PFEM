import unittest
from pathlib import Path

from pfem.archive_lifecycle_record import (
    collect_archive_lifecycle_record_ids,
    load_archive_lifecycle_records,
    validate_archive_lifecycle_records,
)


ROOT = Path(__file__).resolve().parents[2]


class ArchiveLifecycleRecordTests(unittest.TestCase):
    def test_records_load(self):
        records = load_archive_lifecycle_records(ROOT / "archive/archive-lifecycle-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["archive_lifecycle_record_id"], "archive-lifecycle-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_archive_lifecycle_record_ids(ROOT)

        self.assertIn("archive-lifecycle-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_archive_lifecycle_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
