import unittest
from pathlib import Path

from tools.run_pfem_example import run_example


ROOT = Path(__file__).resolve().parents[2]


class ExampleTests(unittest.TestCase):
    def test_field_radio_example_runs(self):
        result = run_example(ROOT / "examples" / "field-radio-node")
        self.assertTrue(result["matches_expected"])
        self.assertEqual(result["profile_id"], "field-radio-node")
        self.assertEqual(result["adapter_id"], "manual-observer-report")
        self.assertEqual(result["observation"]["observation_kind"], "manual_observer_report")


if __name__ == "__main__":
    unittest.main()
