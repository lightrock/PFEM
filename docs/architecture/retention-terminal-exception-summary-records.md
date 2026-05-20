# Retention Terminal Exception Summary Records

PFEM retention terminal exception summary records add the next retention publication closeout boundary.

The boundary is:

```text
retention terminal consumer summary closeout record = formal closure of retention terminal consumer summary workflow
retention terminal exception summary record = terminal-exception-summary layer terminal exception summary record
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal consumer summary closeout record:
formal closure of retention terminal consumer summary workflow

retention terminal exception summary record:
terminal-exception-summary layer terminal exception summary record
```
