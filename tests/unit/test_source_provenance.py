import unittest
from pathlib import Path

from pfem.source_runtime import (
    collect_source_ids,
    load_source_registry,
    validate_source_provenance_repository,
    validate_source_registry,
)


ROOT = Path(__file__).resolve().parents[2]


class SourceProvenanceTests(unittest.TestCase):
    def test_source_registry_loads(self):
        registry = load_source_registry(ROOT / "sources" / "source-registry.json")

        self.assertEqual(registry.registry_id, "pfem-source-registry")
        self.assertGreaterEqual(len(registry.sources), 1)

    def test_source_ids_collect(self):
        source_ids = collect_source_ids(ROOT)

        self.assertIn("manual-entry", source_ids)

    def test_source_registry_validates(self):
        failures = validate_source_registry(ROOT)

        self.assertEqual(failures, [])

    def test_source_provenance_validates_repository(self):
        report = validate_source_provenance_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_sources, 0)
        self.assertGreater(report.checked_evidence_records, 0)


if __name__ == "__main__":
    unittest.main()
