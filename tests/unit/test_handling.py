import unittest
from pathlib import Path

from pfem.handling import load_handling_policy, validate_handling_policy


ROOT = Path(__file__).resolve().parents[2]


class HandlingTests(unittest.TestCase):
    def test_handling_policy_loads(self):
        policy = load_handling_policy(ROOT / "handling" / "handling-policy.json")

        self.assertEqual(policy.policy_id, "pfem-handling-policy")
        self.assertGreaterEqual(len(policy.handling_labels), 1)

    def test_handling_policy_validates_repository(self):
        report = validate_handling_policy(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_labels, 0)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
