import unittest
from pathlib import Path

from pfem.routing import load_routing_policy, validate_routing_policy


ROOT = Path(__file__).resolve().parents[2]


class RoutingTests(unittest.TestCase):
    def test_routing_policy_loads(self):
        policy = load_routing_policy(ROOT / "routing" / "routing-policy.json")

        self.assertEqual(policy.policy_id, "pfem-routing-policy")
        self.assertGreaterEqual(len(policy.routes), 1)
        self.assertEqual(policy.routes[0].route_kind, "action")

    def test_routing_policy_validates(self):
        report = validate_routing_policy(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_routes, 0)


if __name__ == "__main__":
    unittest.main()
