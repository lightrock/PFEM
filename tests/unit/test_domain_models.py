import unittest

from pfem.domain import Alert, Finding, NormalizedObservation, RawEvidence


class DomainModelTests(unittest.TestCase):
    def test_evidence_observation_finding_alert_boundaries(self):
        evidence = RawEvidence(
            evidence_id="evidence-1",
            evidence_kind="example",
            source_id="source-1",
            received_time="2026-01-01T00:00:00Z",
        )

        observation = NormalizedObservation(
            observation_id="observation-1",
            observation_kind="example-observation",
            source_evidence_ids=[evidence.evidence_id],
            observed_time="2026-01-01T00:00:00Z",
        )

        finding = Finding(
            finding_id="finding-1",
            finding_kind="example-finding",
            created_time="2026-01-01T00:00:01Z",
            source_observation_ids=[observation.observation_id],
        )

        alert = Alert(
            alert_id="alert-1",
            alert_kind="example-alert",
            finding_id=finding.finding_id,
            created_time="2026-01-01T00:00:02Z",
            status="new",
        )

        self.assertEqual(observation.source_evidence_ids, ["evidence-1"])
        self.assertEqual(finding.source_observation_ids, ["observation-1"])
        self.assertEqual(alert.finding_id, "finding-1")


if __name__ == "__main__":
    unittest.main()
