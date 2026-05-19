import unittest
from pathlib import Path

from pfem.playbook import load_playbook, validate_playbook_repository


ROOT = Path(__file__).resolve().parents[2]


class PlaybookTests(unittest.TestCase):
    def test_playbook_loads(self):
        playbook = load_playbook(ROOT / "playbooks" / "examples" / "monitor-accepted-rollup.playbook.json")

        self.assertEqual(playbook.playbook_id, "playbook-monitor-accepted-rollup")
        self.assertIn("monitor", playbook.applies_to_action_kinds)
        self.assertGreaterEqual(len(playbook.steps), 1)

    def test_playbook_repository_validates(self):
        report = validate_playbook_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_playbooks, 0)
        self.assertGreater(report.checked_steps, 0)


if __name__ == "__main__":
    unittest.main()
