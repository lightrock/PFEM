import unittest
from pathlib import Path

from pfem.action import load_action_policy, load_action_records, validate_action_repository


ROOT = Path(__file__).resolve().parents[2]


class ActionTests(unittest.TestCase):
    def test_action_policy_loads(self):
        policy = load_action_policy(ROOT / "action" / "action-policy.json")

        self.assertEqual(policy.policy_id, "pfem-action-policy")
        self.assertGreaterEqual(len(policy.action_kinds), 1)
        self.assertIn("proposed", policy.action_states)

    def test_action_records_load(self):
        records = load_action_records(ROOT / "action" / "action-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].action_kind, "monitor")

    def test_action_repository_validates(self):
        report = validate_action_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
