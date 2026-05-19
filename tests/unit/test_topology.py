import unittest
from pathlib import Path

from pfem.topology import load_federation_topology, validate_topology_repository


ROOT = Path(__file__).resolve().parents[2]


class TopologyTests(unittest.TestCase):
    def test_topology_loads(self):
        topology = load_federation_topology(ROOT / "topology" / "federation-topology.json")

        self.assertEqual(topology.topology_id, "pfem-example-federation-topology")
        self.assertGreaterEqual(len(topology.links), 1)

    def test_topology_validates_repository(self):
        report = validate_topology_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_links, 0)
        self.assertGreater(report.checked_messages, 0)


if __name__ == "__main__":
    unittest.main()
