import unittest
from pathlib import Path

from pfem.delivery_job import collect_delivery_job_ids, load_delivery_jobs, validate_delivery_jobs


ROOT = Path(__file__).resolve().parents[2]


class DeliveryJobTests(unittest.TestCase):
    def test_delivery_jobs_load(self):
        jobs = load_delivery_jobs(ROOT / "delivery" / "delivery-jobs.json")

        self.assertGreaterEqual(len(jobs), 1)
        self.assertEqual(jobs[0].delivery_job_id, "delivery-job-basic-manual-export-001")
        self.assertEqual(jobs[0].job_state, "completed")

    def test_delivery_job_ids_collect(self):
        job_ids = collect_delivery_job_ids(ROOT)

        self.assertIn("delivery-job-basic-manual-export-001", job_ids)

    def test_delivery_jobs_validate(self):
        report = validate_delivery_jobs(ROOT)

        self.assertTrue(report.ok, report.failures)
        self.assertGreater(report.checked_jobs, 0)


if __name__ == "__main__":
    unittest.main()
