import unittest
from pathlib import Path

from pfem.retention import load_retention_policy, validate_retention_policy


ROOT = Path(__file__).resolve().parents[2]


class RetentionTests(unittest.TestCase):
    def test_retention_policy_loads(self):
        policy = load_retention_policy(ROOT / "retention" / "retention-policy.json")

        self.assertEqual(policy.policy_id, "pfem-retention-policy")
        self.assertGreaterEqual(len(policy.retention_classes), 1)

    def test_retention_policy_validates_repository(self):
        report = validate_retention_policy(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_classes, 0)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
