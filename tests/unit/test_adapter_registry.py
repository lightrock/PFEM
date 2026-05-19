import unittest
from pathlib import Path

from pfem.adapter_runtime import load_adapter_registry, validate_adapter_registry


ROOT = Path(__file__).resolve().parents[2]


class AdapterRegistryTests(unittest.TestCase):
    def test_adapter_registry_loads(self):
        registry = load_adapter_registry(ROOT / "adapters" / "adapter-registry.json")
        self.assertEqual(registry.registry_id, "pfem-adapter-registry")
        self.assertGreaterEqual(len(registry.adapters), 1)

    def test_adapter_registry_validates(self):
        failures = validate_adapter_registry(ROOT)
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
