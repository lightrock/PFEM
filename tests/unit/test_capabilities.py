import unittest
from pathlib import Path

from pfem.capability_runtime import load_capability_manifest


ROOT = Path(__file__).resolve().parents[2]


class CapabilityManifestTests(unittest.TestCase):
    def test_capability_manifests_load(self):
        paths = sorted((ROOT / "capabilities").rglob("*.capability.yaml"))
        self.assertGreater(len(paths), 0)

        ids = set()
        for path in paths:
            manifest = load_capability_manifest(path)
            self.assertTrue(manifest.capability_id, path)
            self.assertTrue(manifest.display_name, path)
            self.assertTrue(manifest.capability_kind, path)
            self.assertNotIn(manifest.capability_id, ids)
            ids.add(manifest.capability_id)


if __name__ == "__main__":
    unittest.main()
