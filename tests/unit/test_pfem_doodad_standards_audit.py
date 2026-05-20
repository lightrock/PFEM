import unittest
from pathlib import Path

from pfem.boundary_language_standards_audit import audit_boundary_language_standards


ROOT = Path(__file__).resolve().parents[2]


class Generated BoundaryStandardsAuditTests(unittest.TestCase):
    def test_boundary_language_standards_audit_passes(self):
        report = audit_boundary_language_standards(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.manifest_steps_checked, 0)
        self.assertGreater(report.verification_schemas_checked, 0)
        self.assertGreater(report.verification_receipts_checked, 0)


if __name__ == "__main__":
    unittest.main()
