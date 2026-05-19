import unittest
from pathlib import Path

from pfem.restore_plan import (
    collect_restore_plan_ids,
    load_restore_plans,
    validate_restore_plans,
)


ROOT = Path(__file__).resolve().parents[2]


class RestorePlanTests(unittest.TestCase):
    def test_restore_plans_load(self):
        plans = load_restore_plans(ROOT / "restore" / "restore-plans.json")

        self.assertGreaterEqual(len(plans), 1)
        self.assertEqual(plans[0].restore_plan_id, "restore-plan-basic-state-001")
        self.assertEqual(plans[0].plan_state, "ready")

    def test_restore_plan_ids_collect(self):
        plan_ids = collect_restore_plan_ids(ROOT)

        self.assertIn("restore-plan-basic-state-001", plan_ids)

    def test_restore_plans_validate(self):
        report = validate_restore_plans(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_plans, 0)


if __name__ == "__main__":
    unittest.main()
