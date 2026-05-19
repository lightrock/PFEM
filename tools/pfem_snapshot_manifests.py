"""Run PFEM snapshot manifest validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.snapshot_manifest import format_snapshot_manifest_report, validate_snapshot_manifests  # noqa: E402


def main() -> int:
    report = validate_snapshot_manifests(ROOT)
    print(format_snapshot_manifest_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
