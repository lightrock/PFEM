import unittest
from pathlib import Path

from pfem.outbox import collect_outbox_item_ids, load_outbox_items, validate_outbox_items


ROOT = Path(__file__).resolve().parents[2]


class OutboxTests(unittest.TestCase):
    def test_outbox_items_load(self):
        items = load_outbox_items(ROOT / "outbox" / "outbox-items.json")

        self.assertGreaterEqual(len(items), 1)
        self.assertEqual(items[0].outbox_item_id, "outbox-item-basic-manual-export-001")
        self.assertEqual(items[0].outbox_state, "picked_up")

    def test_outbox_item_ids_collect(self):
        item_ids = collect_outbox_item_ids(ROOT)

        self.assertIn("outbox-item-basic-manual-export-001", item_ids)

    def test_outbox_items_validate(self):
        report = validate_outbox_items(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_items, 0)


if __name__ == "__main__":
    unittest.main()
