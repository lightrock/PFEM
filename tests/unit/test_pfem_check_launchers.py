from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]


class PfemCheckLauncherTests(unittest.TestCase):
    def test_windows_and_shell_launchers_share_version(self):
        bat = (ROOT / "pfem_check.bat").read_text(encoding="utf-8")
        sh = (ROOT / "pfem_check.sh").read_text(encoding="utf-8")

        bat_version = re.search(r"PFEM_CHECK_LAUNCHER_VERSION=([0-9]+)", bat)
        sh_version = re.search(r"PFEM_CHECK_LAUNCHER_VERSION=([0-9]+)", sh)

        self.assertIsNotNone(bat_version)
        self.assertIsNotNone(sh_version)
        self.assertEqual(bat_version.group(1), sh_version.group(1))

    def test_launchers_call_same_python_runner(self):
        bat = (ROOT / "pfem_check.bat").read_text(encoding="utf-8").replace("\\", "/")
        sh = (ROOT / "pfem_check.sh").read_text(encoding="utf-8")

        self.assertIn("tools/pfem_check.py", bat)
        self.assertIn("tools/pfem_check.py", sh)

    def test_run_tests_bat_delegates_to_pfem_check(self):
        text = (ROOT / "run_tests.bat").read_text(encoding="utf-8")

        self.assertIn("pfem_check.bat", text)
        self.assertNotIn("python tools\\pfem_", text)

    def test_root_has_no_generated_pfem_bat_wrappers(self):
        leftovers = sorted(
            path.name for path in ROOT.glob("pfem_*.bat")
            if path.name != "pfem_check.bat"
        )

        self.assertEqual([], leftovers)


if __name__ == "__main__":
    unittest.main()
