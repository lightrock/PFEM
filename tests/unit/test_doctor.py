import unittest
from pathlib import Path

from pfem.doctor import format_report, run_doctor


ROOT = Path(__file__).resolve().parents[2]


class DoctorTests(unittest.TestCase):
    def test_doctor_passes_current_repo(self):
        report = run_doctor(ROOT)
        self.assertTrue(report.ok, format_report(report))
        self.assertGreater(report.checked_json_files, 0)
        self.assertGreater(report.checked_adapter_manifests, 0)
        self.assertGreater(report.checked_capability_manifests, 0)


if __name__ == "__main__":
    unittest.main()
