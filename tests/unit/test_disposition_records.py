import unittest
from pathlib import Path

from pfem.disposition_record import (
    collect_disposition_record_ids,
    load_disposition_records,
    validate_disposition_records,
)


ROOT = Path(__file__).resolve().parents[2]


class DispositionRecordTests(unittest.TestCase):
    def test_disposition_records_load(self):
        records = load_disposition_records(ROOT / "disposition" / "disposition-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].disposition_record_id, "disposition-record-basic-restore-001")
        self.assertEqual(records[0].disposition_state, "retained")

    def test_disposition_record_ids_collect(self):
        record_ids = collect_disposition_record_ids(ROOT)

        self.assertIn("disposition-record-basic-restore-001", record_ids)

    def test_disposition_records_validate(self):
        report = validate_disposition_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
