import unittest
from pathlib import Path

from pfem.profile_runtime import load_node_profile


ROOT = Path(__file__).resolve().parents[2]


class NodeProfileTests(unittest.TestCase):
    def test_field_radio_profile_loads_if_present(self):
        path = ROOT / "profiles" / "field-radio" / "field-radio.profile.yaml"
        if not path.exists():
            self.skipTest("field-radio profile has not been added yet")

        profile = load_node_profile(path)

        self.assertEqual(profile.profile_id, "field-radio-node")
        self.assertEqual(profile.profile_kind, "field")
        self.assertIn("manual-report-intake", profile.enabled_capabilities)


if __name__ == "__main__":
    unittest.main()
