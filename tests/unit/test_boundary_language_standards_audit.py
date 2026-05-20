import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.boundary_language_standards_audit import audit_boundary_language_standards


class BoundaryLanguageStandardsAuditTests(unittest.TestCase):
    def test_boundary_language_standards_audit_passes(self):
        report = audit_boundary_language_standards(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.manifest_steps_checked, 0)
        self.assertGreater(report.verification_schemas_checked, 0)
        self.assertGreater(report.verification_receipts_checked, 0)


if __name__ == "__main__":
    unittest.main()
