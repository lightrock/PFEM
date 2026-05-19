import unittest
from pathlib import Path

from pfem.node_runtime import load_node_manifest, load_node_registry, validate_node_registry


ROOT = Path(__file__).resolve().parents[2]


class NodeRegistryTests(unittest.TestCase):
    def test_node_manifest_loads(self):
        manifest = load_node_manifest(ROOT / "nodes" / "examples" / "field-radio-node-example.node.yaml")

        self.assertEqual(manifest.node_id, "field-radio-node-example")
        self.assertEqual(manifest.profile_id, "field-radio-node")
        self.assertIn("manual-observer-report", manifest.configured_adapters)

    def test_node_registry_loads(self):
        registry = load_node_registry(ROOT / "nodes" / "node-registry.json")

        self.assertEqual(registry.registry_id, "pfem-node-registry")
        self.assertGreaterEqual(len(registry.nodes), 1)

    def test_node_registry_validates(self):
        failures = validate_node_registry(ROOT)

        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
