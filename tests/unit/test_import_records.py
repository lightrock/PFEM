import unittest
from pathlib import Path

from pfem.import_record import collect_import_record_ids, load_import_records, validate_import_records


ROOT = Path(__file__).resolve().parents[2]


class ImportRecordTests(unittest.TestCase):
    def test_import_records_load(self):
        records = load_import_records(ROOT / "imports" / "import-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].import_record_id, "import-record-basic-exchange-001")
        self.assertEqual(records[0].exchange_receipt_id, "exchange-receipt-basic-accept-001")
        self.assertEqual(records[0].import_state, "imported")

    def test_import_record_ids_collect(self):
        record_ids = collect_import_record_ids(ROOT)

        self.assertIn("import-record-basic-exchange-001", record_ids)

    def test_import_records_validate(self):
        report = validate_import_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
