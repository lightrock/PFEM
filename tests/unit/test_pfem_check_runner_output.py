from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class PfemCheckRunnerOutputTests(unittest.TestCase):
    def test_runner_help_exposes_quiet_output_controls(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pfem_check.py"), "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("--verbose", result.stdout)
        self.assertIn("--log-dir", result.stdout)

    def test_runner_writes_list_nothing_to_log_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "pfem_check.py"),
                    "--quick",
                    "--list",
                    "--log-dir",
                    tmp,
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual([], list(Path(tmp).glob("*")))


if __name__ == "__main__":
    unittest.main()
