import unittest
from pathlib import Path

from pfem.state_transition import (
    collect_state_transition_ids,
    load_state_transitions,
    validate_state_transitions,
)


ROOT = Path(__file__).resolve().parents[2]


class StateTransitionTests(unittest.TestCase):
    def test_state_transitions_load(self):
        transitions = load_state_transitions(ROOT / "state" / "state-transitions.json")

        self.assertGreaterEqual(len(transitions), 1)
        self.assertEqual(transitions[0].state_transition_id, "state-transition-basic-after-apply-001")
        self.assertEqual(transitions[0].transition_state, "completed")
        self.assertEqual(transitions[0].to_state_checkpoint_id, "state-checkpoint-basic-after-apply-001")

    def test_state_transition_ids_collect(self):
        transition_ids = collect_state_transition_ids(ROOT)

        self.assertIn("state-transition-basic-after-apply-001", transition_ids)

    def test_state_transitions_validate(self):
        report = validate_state_transitions(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_transitions, 0)


if __name__ == "__main__":
    unittest.main()
