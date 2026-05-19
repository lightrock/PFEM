# Retention Rollup Records

PFEM retention rollup records add the next retention/status boundary.

The boundary is:

```text
retention status snapshot verification receipt = evidence that retention status snapshot was checked
retention rollup record                        = published rollup of verified retention status
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention status snapshot verification receipt:
evidence that retention status snapshot was checked

retention rollup record:
published rollup of verified retention status
```
