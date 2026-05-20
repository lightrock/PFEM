import unittest
from pathlib import Path

from pfem.retention_permanent_archive_terminal_final_retrieval_endpoint_verification_receipt import collect_retention_permanent_archive_terminal_final_retrieval_endpoint_verification_receipt_ids, load_retention_permanent_archive_terminal_final_retrieval_endpoint_verification_receipts, validate_retention_permanent_archive_terminal_final_retrieval_endpoint_verification_receipts

ROOT = Path(__file__).resolve().parents[2]

class RetentionPermanentArchiveTerminalFinalRetrievalEndpointVerificationReceiptTests(unittest.TestCase):
    def test_records_load(self):
        records = load_retention_permanent_archive_terminal_final_retrieval_endpoint_verification_receipts(ROOT / "retention/retention-permanent-archive-terminal-final-retrieval-endpoint-verification-receipts.json")
        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["retention_permanent_archive_terminal_final_retrieval_endpoint_verification_receipt_id"], "retention-permanent-archive-terminal-final-retrieval-endpoint-verification-basic-restore-001")

    def test_record_ids_collect(self):
        self.assertIn("retention-permanent-archive-terminal-final-retrieval-endpoint-verification-basic-restore-001", collect_retention_permanent_archive_terminal_final_retrieval_endpoint_verification_receipt_ids(ROOT))

    def test_records_validate(self):
        report = validate_retention_permanent_archive_terminal_final_retrieval_endpoint_verification_receipts(ROOT)
        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)

if __name__ == "__main__":
    unittest.main()
