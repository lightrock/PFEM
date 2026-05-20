import unittest
from pathlib import Path

from pfem.retention_permanent_archive_terminal_closure_final_index_record import collect_retention_permanent_archive_terminal_closure_final_index_record_ids, load_retention_permanent_archive_terminal_closure_final_index_records, validate_retention_permanent_archive_terminal_closure_final_index_records

ROOT = Path(__file__).resolve().parents[2]

class RetentionPermanentArchiveTerminalClosureFinalIndexRecordTests(unittest.TestCase):
    def test_records_load(self):
        records = load_retention_permanent_archive_terminal_closure_final_index_records(ROOT / "retention/retention-permanent-archive-terminal-closure-final-index-records.json")
        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["retention_permanent_archive_terminal_closure_final_index_record_id"], "retention-permanent-archive-terminal-closure-final-index-basic-restore-001")

    def test_record_ids_collect(self):
        self.assertIn("retention-permanent-archive-terminal-closure-final-index-basic-restore-001", collect_retention_permanent_archive_terminal_closure_final_index_record_ids(ROOT))

    def test_records_validate(self):
        report = validate_retention_permanent_archive_terminal_closure_final_index_records(ROOT)
        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)

if __name__ == "__main__":
    unittest.main()
