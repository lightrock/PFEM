import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADAPTER_DIR = ROOT / "adapters" / "community" / "manual-observer-report"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ManualObserverAdapterTests(unittest.TestCase):
    def test_decode_and_normalize_example(self):
        decoder = load_module("manual_observer_decoder", ADAPTER_DIR / "decoder.py")
        normalizer = load_module("manual_observer_normalizer", ADAPTER_DIR / "normalizer.py")

        raw_payload = json.loads((ADAPTER_DIR / "samples" / "raw" / "example.json").read_text(encoding="utf-8"))

        evidence = decoder.decode_raw(raw_payload)
        observation = normalizer.normalize(evidence)

        self.assertEqual(evidence["evidence_id"], "manual-report-example-001")
        self.assertEqual(evidence["evidence_kind"], "manual_observer_report")
        self.assertEqual(observation["observation_kind"], "manual_observer_report")
        self.assertEqual(observation["source_evidence_ids"], [evidence["evidence_id"]])
        self.assertIn("description", observation["normalized_fields"])
        self.assertEqual(observation["uncertainty_notes"], "Location is approximate.")

    def test_decode_rejects_missing_required_fields(self):
        decoder = load_module("manual_observer_decoder", ADAPTER_DIR / "decoder.py")

        with self.assertRaises(ValueError):
            decoder.decode_raw({"report_id": "bad"})


if __name__ == "__main__":
    unittest.main()
