import unittest
from pathlib import Path

from pfem.lineage import validate_lifecycle_dir, validate_lifecycle_records


ROOT = Path(__file__).resolve().parents[2]


class LineageTests(unittest.TestCase):
    def test_basic_lifecycle_fixture_validates(self):
        report = validate_lifecycle_dir(ROOT / "tests" / "fixtures" / "lifecycle" / "basic")

        self.assertTrue(report.ok, report.failures)
        self.assertEqual(report.checked_records, 5)

    def test_missing_evidence_reference_fails(self):
        report = validate_lifecycle_records(
            evidence_records=[],
            observation_records=[
                {
                    "observation_id": "obs-bad",
                    "source_evidence_ids": ["missing-evidence"],
                }
            ],
            finding_records=[],
            alert_records=[],
            source="unit-test",
        )

        self.assertFalse(report.ok)
        self.assertIn("missing evidence", report.failures[0])


if __name__ == "__main__":
    unittest.main()
