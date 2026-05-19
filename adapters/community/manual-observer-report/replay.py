"""Manual observer report replay helper."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_reports(path: str | Path) -> list[dict[str, Any]]:
    """Load newline-delimited JSON manual reports."""
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError("manual report replay records must be JSON objects")
                records.append(value)
    return records
