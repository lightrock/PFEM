import unittest
from pathlib import Path

from pfem.inbox import collect_inbox_item_ids, load_inbox_items, validate_inbox_items


ROOT = Path(__file__).resolve().parents[2]


class InboxTests(unittest.TestCase):
    def test_inbox_items_load(self):
        items = load_inbox_items(ROOT / "inbox" / "inbox-items.json")

        self.assertGreaterEqual(len(items), 1)
        self.assertEqual(items[0].inbox_item_id, "inbox-item-basic-manual-export-001")
        self.assertEqual(items[0].inbox_state, "ready_for_exchange")

    def test_inbox_item_ids_collect(self):
        item_ids = collect_inbox_item_ids(ROOT)

        self.assertIn("inbox-item-basic-manual-export-001", item_ids)

    def test_inbox_items_validate(self):
        report = validate_inbox_items(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_items, 0)


if __name__ == "__main__":
    unittest.main()
