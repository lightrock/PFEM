import unittest
from pathlib import Path

from pfem.transport import (
    collect_transport_adapter_ids,
    load_transport_adapter_registry,
    validate_transport_adapter_registry,
)


ROOT = Path(__file__).resolve().parents[2]


class TransportTests(unittest.TestCase):
    def test_transport_registry_loads(self):
        registry = load_transport_adapter_registry(ROOT / "transport" / "transport-adapter-registry.json")

        self.assertEqual(registry.registry_id, "pfem-transport-adapter-registry")
        self.assertGreaterEqual(len(registry.adapters), 1)
        self.assertEqual(registry.adapters[0].transport_adapter_id, "transport-manual-export")

    def test_transport_adapter_ids_collect(self):
        adapter_ids = collect_transport_adapter_ids(ROOT)

        self.assertIn("transport-manual-export", adapter_ids)

    def test_transport_registry_validates(self):
        report = validate_transport_adapter_registry(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_adapters, 0)


if __name__ == "__main__":
    unittest.main()
