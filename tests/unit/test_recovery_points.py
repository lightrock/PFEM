import unittest
from pathlib import Path

from pfem.recovery_point import (
    collect_recovery_point_ids,
    load_recovery_points,
    validate_recovery_points,
)


ROOT = Path(__file__).resolve().parents[2]


class RecoveryPointTests(unittest.TestCase):
    def test_recovery_points_load(self):
        points = load_recovery_points(ROOT / "recovery" / "recovery-points.json")

        self.assertGreaterEqual(len(points), 1)
        self.assertEqual(points[0].recovery_point_id, "recovery-point-basic-state-001")
        self.assertEqual(points[0].recovery_state, "available")

    def test_recovery_point_ids_collect(self):
        point_ids = collect_recovery_point_ids(ROOT)

        self.assertIn("recovery-point-basic-state-001", point_ids)

    def test_recovery_points_validate(self):
        report = validate_recovery_points(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_points, 0)


if __name__ == "__main__":
    unittest.main()
