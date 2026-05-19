import unittest
from pathlib import Path

from pfem.review import load_review_records, validate_review_repository


ROOT = Path(__file__).resolve().parents[2]


class ReviewTests(unittest.TestCase):
    def test_review_records_load(self):
        records = load_review_records(ROOT / "review" / "review-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].review_gate, "review-before-rollup")

    def test_review_repository_validates(self):
        report = validate_review_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_reviews, 0)
        self.assertGreater(report.checked_gate_requirements, 0)


if __name__ == "__main__":
    unittest.main()
