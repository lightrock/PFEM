import unittest
from pathlib import Path

from pfem.dispatch_decision import (
    collect_dispatch_decision_ids,
    load_dispatch_decisions,
    validate_dispatch_decisions,
)


ROOT = Path(__file__).resolve().parents[2]


class DispatchDecisionTests(unittest.TestCase):
    def test_dispatch_decisions_load(self):
        decisions = load_dispatch_decisions(ROOT / "dispatch" / "dispatch-decisions.json")

        self.assertGreaterEqual(len(decisions), 1)
        self.assertEqual(decisions[0].dispatch_decision_id, "dispatch-decision-basic-manual-export-001")
        self.assertEqual(decisions[0].decision, "allowed")

    def test_dispatch_decision_ids_collect(self):
        decision_ids = collect_dispatch_decision_ids(ROOT)

        self.assertIn("dispatch-decision-basic-manual-export-001", decision_ids)

    def test_dispatch_decisions_validate(self):
        report = validate_dispatch_decisions(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_decisions, 0)


if __name__ == "__main__":
    unittest.main()
