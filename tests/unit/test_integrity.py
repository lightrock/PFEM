import unittest
from pathlib import Path

from pfem.integrity import (
    build_integrity_manifest,
    compute_digest,
    validate_integrity_manifest,
    write_integrity_manifest,
)


ROOT = Path(__file__).resolve().parents[2]


class IntegrityTests(unittest.TestCase):
    def test_digest_is_canonical_json(self):
        digest1 = compute_digest(ROOT / "policy" / "sharing-policy.json")
        digest2 = compute_digest(ROOT / "policy" / "sharing-policy.json")

        self.assertEqual(digest1, digest2)
        self.assertEqual(len(digest1), 64)

    def test_manifest_builds(self):
        manifest = build_integrity_manifest(ROOT)

        self.assertEqual(manifest["receipt_set_id"], "pfem-integrity-receipts")
        self.assertGreater(len(manifest["receipts"]), 0)

    def test_manifest_validates_after_update(self):
        path = write_integrity_manifest(ROOT)
        report = validate_integrity_manifest(ROOT)

        self.assertTrue(path.exists())
        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_receipts, 0)


if __name__ == "__main__":
    unittest.main()
