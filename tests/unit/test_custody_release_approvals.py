import unittest
from pathlib import Path

from pfem.custody_release_approval import (
    collect_custody_release_approval_ids,
    load_custody_release_approvals,
    validate_custody_release_approvals,
)


ROOT = Path(__file__).resolve().parents[2]


class CustodyReleaseApprovalTests(unittest.TestCase):
    def test_records_load(self):
        records = load_custody_release_approvals(ROOT / "custody/custody-release-approvals.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["custody_release_approval_id"], "custody-release-approval-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_custody_release_approval_ids(ROOT)

        self.assertIn("custody-release-approval-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_custody_release_approvals(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
