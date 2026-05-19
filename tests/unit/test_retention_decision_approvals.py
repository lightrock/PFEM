import unittest
from pathlib import Path

from pfem.retention_decision_approval import (
    collect_retention_decision_approval_ids,
    load_retention_decision_approvals,
    validate_retention_decision_approvals,
)


ROOT = Path(__file__).resolve().parents[2]


class RetentionDecisionApprovalTests(unittest.TestCase):
    def test_records_load(self):
        records = load_retention_decision_approvals(ROOT / "retention/retention-decision-approvals.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["retention_decision_approval_id"], "retention-decision-approval-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_retention_decision_approval_ids(ROOT)

        self.assertIn("retention-decision-approval-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_retention_decision_approvals(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
