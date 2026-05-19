import unittest
from pathlib import Path

from pfem.snapshot_manifest import (
    collect_snapshot_manifest_ids,
    compute_snapshot_digest,
    load_snapshot_manifests,
    validate_snapshot_manifests,
)


ROOT = Path(__file__).resolve().parents[2]


class SnapshotManifestTests(unittest.TestCase):
    def test_snapshot_manifests_load(self):
        manifests = load_snapshot_manifests(ROOT / "snapshots" / "snapshot-manifests.json")

        self.assertGreaterEqual(len(manifests), 1)
        self.assertEqual(manifests[0].snapshot_manifest_id, "snapshot-manifest-basic-state-001")
        self.assertEqual(manifests[0].snapshot_state, "current")

    def test_snapshot_manifest_ids_collect(self):
        manifest_ids = collect_snapshot_manifest_ids(ROOT)

        self.assertIn("snapshot-manifest-basic-state-001", manifest_ids)

    def test_snapshot_digest_matches_items(self):
        manifest = load_snapshot_manifests(ROOT / "snapshots" / "snapshot-manifests.json")[0]

        self.assertEqual(manifest.snapshot_digest, compute_snapshot_digest(manifest.items))

    def test_snapshot_manifests_validate(self):
        report = validate_snapshot_manifests(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_manifests, 0)


if __name__ == "__main__":
    unittest.main()
