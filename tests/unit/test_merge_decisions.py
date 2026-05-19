import unittest
from pathlib import Path

from pfem.merge_decision import collect_merge_decision_ids, load_merge_decisions, validate_merge_decisions


ROOT = Path(__file__).resolve().parents[2]


class MergeDecisionTests(unittest.TestCase):
    def test_merge_decisions_load(self):
        decisions = load_merge_decisions(ROOT / "merge" / "merge-decisions.json")

        self.assertGreaterEqual(len(decisions), 1)
        self.assertEqual(decisions[0].merge_decision_id, "merge-decision-basic-import-001")
        self.assertEqual(decisions[0].decision, "accept_incoming")

    def test_merge_decision_ids_collect(self):
        decision_ids = collect_merge_decision_ids(ROOT)

        self.assertIn("merge-decision-basic-import-001", decision_ids)

    def test_merge_decisions_validate(self):
        report = validate_merge_decisions(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_decisions, 0)


if __name__ == "__main__":
    unittest.main()
