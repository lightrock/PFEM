import unittest
from pathlib import Path

from pfem.contributor_command_protocol_audit import audit_contributor_command_protocol

ROOT = Path(__file__).resolve().parents[2]

class ContributorCommandProtocolAuditTests(unittest.TestCase):
    def test_contributor_command_protocol_audit_passes(self):
        report = audit_contributor_command_protocol(ROOT)
        self.assertTrue(report.ok, report.failures)
        self.assertGreaterEqual(report.required_files_checked, 1)
        self.assertGreaterEqual(report.optional_first_read_files_found, 1)

if __name__ == "__main__":
    unittest.main()
