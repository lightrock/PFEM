import unittest
from pathlib import Path

from pfem.policy import (
    load_sharing_policy,
    validate_policy_repository,
    validate_record_sharing_scopes,
)


ROOT = Path(__file__).resolve().parents[2]


class PolicyTests(unittest.TestCase):
    def test_policy_repository_validates(self):
        report = validate_policy_repository(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_profiles, 0)
        self.assertGreater(report.checked_sharing_records, 0)

    def test_unknown_sharing_scope_fails_from_repo_root(self):
        policy = load_sharing_policy(ROOT / "policy" / "sharing-policy.json")
        fixture_path = ROOT / "tests" / "fixtures" / "policy-bad"
        fixture_path.mkdir(parents=True, exist_ok=True)
        message_path = fixture_path / "federation_message.json"
        message_path.write_text(
            '{"message_id":"bad-1","sharing_scope":"unknown-scope"}\n',
            encoding="utf-8",
        )

        try:
            checked, failures = validate_record_sharing_scopes(ROOT, policy)
            self.assertGreaterEqual(checked, 1)
            self.assertTrue(any("unknown-scope" in failure for failure in failures))
        finally:
            message_path.unlink(missing_ok=True)
            try:
                fixture_path.rmdir()
            except OSError:
                pass

    def test_unknown_sharing_scope_fails_from_fixture_root(self):
        policy = load_sharing_policy(ROOT / "policy" / "sharing-policy.json")
        fixture_path = ROOT / "tests" / "fixtures" / "policy-bad-direct"
        fixture_path.mkdir(parents=True, exist_ok=True)
        message_path = fixture_path / "federation_message.json"
        message_path.write_text(
            '{"message_id":"bad-2","sharing_scope":"unknown-scope"}\n',
            encoding="utf-8",
        )

        try:
            checked, failures = validate_record_sharing_scopes(ROOT / "tests" / "fixtures", policy)
            self.assertGreaterEqual(checked, 1)
            self.assertTrue(any("unknown-scope" in failure for failure in failures))
        finally:
            message_path.unlink(missing_ok=True)
            try:
                fixture_path.rmdir()
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()
