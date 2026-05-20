from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]


class PfemDoctorModeTests(unittest.TestCase):
    def test_doctor_tool_exposes_deep_mode(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pfem_doctor.py"), "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("--deep", result.stdout)

    def test_doctor_defaults_to_shallow_mode(self):
        text = (ROOT / "src" / "pfem" / "doctor.py").read_text(encoding="utf-8")

        self.assertIn("deep_validators: bool = False", text)
        self.assertIn("if deep_validators:", text)


if __name__ == "__main__":
    unittest.main()
