"""Small JSON file helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    """Load a JSON file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump_json(path: str | Path, value: Any) -> None:
    """Write a JSON file with stable formatting."""
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
