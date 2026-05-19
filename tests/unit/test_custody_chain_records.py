import unittest
from pathlib import Path

from pfem.custody_chain_record import (
    collect_custody_chain_record_ids,
    compute_chain_ref_digest,
    load_custody_chain_records,
    validate_custody_chain_records,
)


ROOT = Path(__file__).resolve().parents[2]


class CustodyChainRecordTests(unittest.TestCase):
    def test_custody_chain_records_load(self):
        records = load_custody_chain_records(ROOT / "custody" / "custody-chain-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0].custody_chain_record_id, "custody-chain-basic-restore-001")
        self.assertEqual(records[0].chain_state, "closed")

    def test_custody_chain_record_ids_collect(self):
        record_ids = collect_custody_chain_record_ids(ROOT)

        self.assertIn("custody-chain-basic-restore-001", record_ids)

    def test_custody_chain_digest_matches(self):
        record = load_custody_chain_records(ROOT / "custody" / "custody-chain-records.json")[0]

        self.assertEqual(record.chain_ref_digest, compute_chain_ref_digest(record.chain_refs))

    def test_custody_chain_records_validate(self):
        report = validate_custody_chain_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
