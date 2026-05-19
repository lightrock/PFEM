import unittest
from pathlib import Path

from pfem.state_checkpoint import (
    collect_state_checkpoint_ids,
    compute_ref_digest,
    load_state_checkpoints,
    validate_state_checkpoints,
)


ROOT = Path(__file__).resolve().parents[2]


class StateCheckpointTests(unittest.TestCase):
    def test_state_checkpoints_load(self):
        checkpoints = load_state_checkpoints(ROOT / "state" / "state-checkpoints.json")

        self.assertGreaterEqual(len(checkpoints), 1)
        self.assertEqual(checkpoints[0].state_checkpoint_id, "state-checkpoint-basic-after-apply-001")
        self.assertEqual(checkpoints[0].checkpoint_state, "current")

    def test_state_checkpoint_ids_collect(self):
        checkpoint_ids = collect_state_checkpoint_ids(ROOT)

        self.assertIn("state-checkpoint-basic-after-apply-001", checkpoint_ids)

    def test_state_digest_matches_included_refs(self):
        checkpoint = load_state_checkpoints(ROOT / "state" / "state-checkpoints.json")[0]

        self.assertEqual(checkpoint.state_digest, compute_ref_digest(checkpoint.included_refs))

    def test_state_checkpoints_validate(self):
        report = validate_state_checkpoints(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_checkpoints, 0)


if __name__ == "__main__":
    unittest.main()
