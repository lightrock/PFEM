import unittest
from pathlib import Path

from pfem.preservation_chain_record import (
    collect_preservation_chain_record_ids,
    load_preservation_chain_records,
    validate_preservation_chain_records,
)


ROOT = Path(__file__).resolve().parents[2]


class PreservationChainRecordTests(unittest.TestCase):
    def test_records_load(self):
        records = load_preservation_chain_records(ROOT / "preservation/preservation-chain-records.json")

        self.assertGreaterEqual(len(records), 1)
        self.assertEqual(records[0]["preservation_chain_record_id"], "preservation-chain-basic-restore-001")

    def test_record_ids_collect(self):
        record_ids = collect_preservation_chain_record_ids(ROOT)

        self.assertIn("preservation-chain-basic-restore-001", record_ids)

    def test_records_validate(self):
        report = validate_preservation_chain_records(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_records, 0)


if __name__ == "__main__":
    unittest.main()
