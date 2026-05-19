"""Run PFEM rollup/federation validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.rollup import format_rollup_report, validate_rollup_dir  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    target = Path(args[0]) if args else ROOT / "tests" / "fixtures" / "rollup" / "basic"

    if not target.is_absolute():
        target = ROOT / target

    report = validate_rollup_dir(target)
    print(format_rollup_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
