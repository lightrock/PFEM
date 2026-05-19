import unittest
from pathlib import Path

from pfem.restore_approval import (
    collect_restore_approval_ids,
    load_restore_approvals,
    validate_restore_approvals,
)


ROOT = Path(__file__).resolve().parents[2]


class RestoreApprovalTests(unittest.TestCase):
    def test_restore_approvals_load(self):
        approvals = load_restore_approvals(ROOT / "restore" / "restore-approvals.json")

        self.assertGreaterEqual(len(approvals), 1)
        self.assertEqual(approvals[0].restore_approval_id, "restore-approval-basic-state-001")
        self.assertEqual(approvals[0].approval_state, "approved")

    def test_restore_approval_ids_collect(self):
        approval_ids = collect_restore_approval_ids(ROOT)

        self.assertIn("restore-approval-basic-state-001", approval_ids)

    def test_restore_approvals_validate(self):
        report = validate_restore_approvals(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_approvals, 0)


if __name__ == "__main__":
    unittest.main()
