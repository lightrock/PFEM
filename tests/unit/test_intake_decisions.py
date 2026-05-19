import unittest
from pathlib import Path

from pfem.intake_decision import (
    collect_intake_decision_ids,
    load_intake_decisions,
    validate_intake_decisions,
)


ROOT = Path(__file__).resolve().parents[2]


class IntakeDecisionTests(unittest.TestCase):
    def test_intake_decisions_load(self):
        decisions = load_intake_decisions(ROOT / "intake" / "intake-decisions.json")

        self.assertGreaterEqual(len(decisions), 1)
        self.assertEqual(decisions[0].intake_decision_id, "intake-decision-basic-manual-export-001")
        self.assertEqual(decisions[0].decision, "allowed_for_exchange")

    def test_intake_decision_ids_collect(self):
        decision_ids = collect_intake_decision_ids(ROOT)

        self.assertIn("intake-decision-basic-manual-export-001", decision_ids)

    def test_intake_decisions_validate(self):
        report = validate_intake_decisions(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_decisions, 0)


if __name__ == "__main__":
    unittest.main()
