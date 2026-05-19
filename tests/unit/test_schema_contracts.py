import unittest
from pathlib import Path

from pfem.schema_contracts import validate_schema_contracts, validate_records_against_schema


ROOT = Path(__file__).resolve().parents[2]


class SchemaContractTests(unittest.TestCase):
    def test_schema_contracts_validate_fixtures(self):
        report = validate_schema_contracts(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)

    def test_missing_required_field_fails(self):
        temp_dir = ROOT / "tests" / "fixtures" / "schema-bad"
        temp_dir.mkdir(parents=True, exist_ok=True)
        bad_record = temp_dir / "finding.json"
        bad_record.write_text('{"finding_id":"bad"}\n', encoding="utf-8")

        try:
            checked, failures = validate_records_against_schema(
                ROOT / "schemas" / "finding.schema.json",
                [bad_record],
                ROOT,
            )
            self.assertEqual(checked, 1)
            self.assertTrue(any("finding_kind" in failure for failure in failures))
        finally:
            bad_record.unlink(missing_ok=True)
            try:
                temp_dir.rmdir()
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()
