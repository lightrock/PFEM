import unittest
from pathlib import Path

from pfem.quality import (
    load_quality_assessments,
    load_quality_policy,
    validate_quality_repository,
)


ROOT = Path(__file__).resolve().parents[2]


class QualityTests(unittest.TestCase):
    def test_quality_policy_loads(self):
        policy = load_quality_policy(ROOT / "quality" / "quality-policy.json")

        self.assertEqual(policy.policy_id, "pfem-quality-policy")
        self.assertGreaterEqual(len(policy.confidence_levels), 1)
        self.assertGreaterEqual(len(policy.quality_flags), 1)

    def test_quality_assessments_load(self):
        assessments = load_quality_assessments(ROOT / "quality" / "quality-assessments.json")

        self.assertGreaterEqual(len(assessments), 1)
        self.assertEqual(assessments[0].confidence_level, "medium")

    def test_quality_repository_validates(self):
        report = validate_quality_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_assessments, 0)


if __name__ == "__main__":
    unittest.main()
