import unittest
from pathlib import Path

from pfem.retention_distribution_manifest_record import (
    collect_retention_distribution_manifest_record_ids,
    load_retention_distribution_manifest_records,
    validate_retention_distribution_manifest_records,
)


ROOT = Path(__file__).resolve().parents[2]


class RetentionDistributionManifestRecordTests(unittest.TestCase):
    def test_records_load(self):
        records = load_retention_distribution_manifest_records(ROOT / "retention/retention-distribution-manifest-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["retention_distribution_manifest_record_id"], "retention-distribution-manifest-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_retention_distribution_manifest_record_ids(ROOT)

        self.assertIn("retention-distribution-manifest-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_retention_distribution_manifest_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
