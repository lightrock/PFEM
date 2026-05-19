import unittest
from pathlib import Path

from pfem.conflict_record import collect_conflict_record_ids, load_conflict_records, validate_conflict_records


ROOT = Path(__file__).resolve().parents[2]


class ConflictRecordTests(unittest.TestCase):
    def test_conflict_records_load(self):
        records = load_conflict_records(ROOT / "conflicts" / "conflict-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].conflict_record_id, "conflict-record-basic-import-001")
        self.assertEqual(records[0].conflict_state, "none_detected")

    def test_conflict_record_ids_collect(self):
        record_ids = collect_conflict_record_ids(ROOT)

        self.assertIn("conflict-record-basic-import-001", record_ids)

    def test_conflict_records_validate(self):
        report = validate_conflict_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
