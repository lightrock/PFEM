import unittest
from pathlib import Path

from pfem.bundle import load_exchange_bundle, validate_bundle_repository


ROOT = Path(__file__).resolve().parents[2]


class BundleTests(unittest.TestCase):
    def test_exchange_bundle_loads(self):
        bundle = load_exchange_bundle(ROOT / "bundles" / "examples" / "basic-rollup-exchange.bundle.json")

        self.assertEqual(bundle.bundle_id, "bundle-basic-rollup-exchange-001")
        self.assertEqual(bundle.producer_node_id, "field-radio-node-example")
        self.assertIn("federation-basic-001", bundle.included_record_refs)

    def test_bundle_repository_validates(self):
        report = validate_bundle_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_bundles, 0)


if __name__ == "__main__":
    unittest.main()
