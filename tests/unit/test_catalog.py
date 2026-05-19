import unittest
from pathlib import Path

from pfem.catalog import build_catalog, format_catalog


ROOT = Path(__file__).resolve().parents[2]


class CatalogTests(unittest.TestCase):
    def test_catalog_builds(self):
        catalog = build_catalog(ROOT)

        self.assertGreater(catalog["counts"]["capabilities"], 0)
        self.assertGreater(catalog["counts"]["adapters"], 0)
        self.assertGreater(catalog["counts"]["profiles"], 0)
        self.assertGreater(catalog["counts"]["examples"], 0)

    def test_catalog_formats(self):
        catalog = build_catalog(ROOT)
        text = format_catalog(catalog)

        self.assertIn("Capabilities", text)
        self.assertIn("Adapters", text)
        self.assertIn("Profiles", text)
        self.assertIn("Examples", text)


if __name__ == "__main__":
    unittest.main()
