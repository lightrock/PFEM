"""Template PFEM adapter replay hook."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_replay_records(path: str | Path) -> list[Any]:
    """Load newline-delimited JSON replay records."""
    records: list[Any] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records
