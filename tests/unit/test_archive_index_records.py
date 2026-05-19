import unittest
from pathlib import Path

from pfem.archive_index_record import (
    collect_archive_index_record_ids,
    load_archive_index_records,
    validate_archive_index_records,
)


ROOT = Path(__file__).resolve().parents[2]


class ArchiveIndexRecordTests(unittest.TestCase):
    def test_records_load(self):
        records = load_archive_index_records(ROOT / "archive/archive-index-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["archive_index_record_id"], "archive-index-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_archive_index_record_ids(ROOT)

        self.assertIn("archive-index-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_archive_index_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
