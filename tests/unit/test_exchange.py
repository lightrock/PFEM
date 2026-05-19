import unittest
from pathlib import Path

from pfem.exchange import load_exchange_receipts, validate_exchange_repository


ROOT = Path(__file__).resolve().parents[2]


class ExchangeTests(unittest.TestCase):
    def test_exchange_receipts_load(self):
        receipts = load_exchange_receipts(ROOT / "exchange" / "exchange-receipts.json")

        self.assertGreaterEqual(len(receipts), 1)
        self.assertEqual(receipts[0].bundle_id, "bundle-basic-rollup-exchange-001")

    def test_exchange_repository_validates(self):
        report = validate_exchange_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
