import unittest
from pathlib import Path

from pfem.retention_terminal_public_release_summary_closeout_record import (
    collect_retention_terminal_public_release_summary_closeout_record_ids,
    load_retention_terminal_public_release_summary_closeout_records,
    validate_retention_terminal_public_release_summary_closeout_records,
)


ROOT = Path(__file__).resolve().parents[2]


class RetentionTerminalPublicReleaseSummaryCloseoutRecordTests(unittest.TestCase):
    def test_records_load(self):
        records = load_retention_terminal_public_release_summary_closeout_records(ROOT / "retention/retention-terminal-public-release-summary-closeout-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["retention_terminal_public_release_summary_closeout_record_id"], "retention-terminal-public-release-summary-closeout-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_retention_terminal_public_release_summary_closeout_record_ids(ROOT)

        self.assertIn("retention-terminal-public-release-summary-closeout-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_retention_terminal_public_release_summary_closeout_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
