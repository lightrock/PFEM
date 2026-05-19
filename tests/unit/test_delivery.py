import unittest
from pathlib import Path

from pfem.delivery import (
    collect_delivery_channel_ids,
    load_delivery_channel_registry,
    validate_delivery_channel_registry,
)


ROOT = Path(__file__).resolve().parents[2]


class DeliveryTests(unittest.TestCase):
    def test_delivery_registry_loads(self):
        registry = load_delivery_channel_registry(ROOT / "delivery" / "delivery-channel-registry.json")

        self.assertEqual(registry.registry_id, "pfem-delivery-channel-registry")
        self.assertGreaterEqual(len(registry.channels), 1)
        self.assertEqual(registry.channels[0].channel_id, "manual-export")

    def test_delivery_channel_ids_collect(self):
        channel_ids = collect_delivery_channel_ids(ROOT)

        self.assertIn("manual-export", channel_ids)

    def test_delivery_registry_validates(self):
        report = validate_delivery_channel_registry(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_channels, 0)


if __name__ == "__main__":
    unittest.main()
