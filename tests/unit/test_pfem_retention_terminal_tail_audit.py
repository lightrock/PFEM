import unittest
from pathlib import Path

from pfem.retention_terminal_tail_audit import audit_retention_terminal_tail


ROOT = Path(__file__).resolve().parents[2]


class RetentionTerminalTailAuditTests(unittest.TestCase):
    def test_terminal_tail_audit_passes(self):
        report = audit_retention_terminal_tail(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertTrue(report.final_endcap_closeout_found)
        self.assertGreaterEqual(report.verification_schemas_checked, 1)
        self.assertGreaterEqual(report.verification_receipts_checked, 1)


if __name__ == "__main__":
    unittest.main()
