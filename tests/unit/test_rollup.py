import unittest
from pathlib import Path

from pfem.rollup import validate_rollup_dir, validate_rollup_records


ROOT = Path(__file__).resolve().parents[2]


class RollupTests(unittest.TestCase):
    def test_basic_rollup_fixture_validates(self):
        report = validate_rollup_dir(ROOT / "tests" / "fixtures" / "rollup" / "basic")

        self.assertTrue(report.ok, report.failures)
        self.assertEqual(report.checked_records, 7)

    def test_missing_rollup_lineage_ref_fails(self):
        report = validate_rollup_records(
            evidence_records=[],
            observation_records=[],
            finding_records=[],
            alert_records=[],
            package_records=[],
            rollup_records=[
                {
                    "rollup_id": "rollup-bad",
                    "producer_node_id": "node-1",
                    "summary_kind": "bad",
                    "source_lineage_refs": ["missing-record"],
                }
            ],
            federation_records=[],
            source="unit-test",
        )

        self.assertFalse(report.ok)
        self.assertIn("missing lifecycle record", report.failures[0])


if __name__ == "__main__":
    unittest.main()
