import unittest
from pathlib import Path

from pfem.dispatch import collect_dispatch_rule_ids, load_dispatch_policy, validate_dispatch_policy


ROOT = Path(__file__).resolve().parents[2]


class DispatchTests(unittest.TestCase):
    def test_dispatch_policy_loads(self):
        policy = load_dispatch_policy(ROOT / "dispatch" / "dispatch-policy.json")

        self.assertEqual(policy.policy_id, "pfem-dispatch-policy")
        self.assertGreaterEqual(len(policy.rules), 1)
        self.assertEqual(policy.rules[0].dispatch_rule_id, "dispatch-manual-export-routine-bundle")

    def test_dispatch_rule_ids_collect(self):
        rule_ids = collect_dispatch_rule_ids(ROOT)

        self.assertIn("dispatch-manual-export-routine-bundle", rule_ids)

    def test_dispatch_policy_validates(self):
        report = validate_dispatch_policy(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_rules, 0)


if __name__ == "__main__":
    unittest.main()
