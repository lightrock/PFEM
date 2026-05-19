"""Update PFEM integrity receipts from the current source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.integrity import write_integrity_manifest  # noqa: E402


def main() -> int:
    path = write_integrity_manifest(ROOT)
    print(f"Updated PFEM integrity receipts: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
