import unittest
from pathlib import Path

from pfem.audit import load_audit_events, validate_audit_repository


ROOT = Path(__file__).resolve().parents[2]


class AuditTests(unittest.TestCase):
    def test_audit_events_load(self):
        events = load_audit_events(ROOT / "audit" / "audit-journal.json")

        self.assertGreaterEqual(len(events), 1)
        self.assertEqual(events[0].event_kind, "review_approved")

    def test_audit_repository_validates(self):
        report = validate_audit_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_events, 0)


if __name__ == "__main__":
    unittest.main()
