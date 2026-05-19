import unittest
from pathlib import Path

from pfem.example_runtime import load_example_registry, validate_example_registry


ROOT = Path(__file__).resolve().parents[2]


class ExampleRegistryTests(unittest.TestCase):
    def test_example_registry_loads(self):
        registry = load_example_registry(ROOT / "examples" / "example-registry.json")
        self.assertEqual(registry.registry_id, "pfem-example-registry")
        self.assertGreaterEqual(len(registry.examples), 1)

    def test_example_registry_validates(self):
        failures = validate_example_registry(ROOT)
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
