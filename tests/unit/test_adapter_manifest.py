import unittest
from pathlib import Path

from pfem.adapter_runtime import load_adapter_manifest


ROOT = Path(__file__).resolve().parents[2]


class AdapterManifestTests(unittest.TestCase):
    def test_template_adapter_manifest_loads(self):
        manifest = load_adapter_manifest(ROOT / "adapters" / "vendors" / "template" / "adapter.yaml")

        self.assertTrue(manifest.adapter_id)
        self.assertTrue(manifest.display_name)
        self.assertIsInstance(manifest.capabilities, list)
        self.assertIsInstance(manifest.outputs, list)


if __name__ == "__main__":
    unittest.main()
