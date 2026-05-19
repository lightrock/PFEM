"""Run a PFEM example directory.

This runner is intentionally small and dependency-free. It currently supports
examples that point at a Python adapter folder with `decoder.py` and
`normalizer.py`.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_example(example_dir: str | Path) -> dict[str, Any]:
    example_path = Path(example_dir)
    if not example_path.is_absolute():
        example_path = ROOT / example_path

    manifest_path = example_path / "example.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing example manifest: {manifest_path}")

    manifest = load_json(manifest_path)

    adapter_path = ROOT / manifest["adapter_path"]
    input_path = example_path / manifest["input_path"]
    expected_path = example_path / manifest["expected_observation_path"]

    decoder = load_module(f"{manifest['example_id']}_decoder", adapter_path / "decoder.py")
    normalizer = load_module(f"{manifest['example_id']}_normalizer", adapter_path / "normalizer.py")

    raw_payload = load_json(input_path)
    evidence = decoder.decode_raw(raw_payload)
    observation = normalizer.normalize(evidence)
    expected = load_json(expected_path)

    result = {
        "example_id": manifest["example_id"],
        "profile_id": manifest["profile_id"],
        "adapter_id": manifest["adapter_id"],
        "evidence": evidence,
        "observation": observation,
        "expected_observation": expected,
        "matches_expected": observation == expected,
    }

    return result


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: python tools/run_pfem_example.py examples/field-radio-node")
        return 2

    result = run_example(args[0])

    print(json.dumps({
        "example_id": result["example_id"],
        "profile_id": result["profile_id"],
        "adapter_id": result["adapter_id"],
        "matches_expected": result["matches_expected"],
        "observation": result["observation"],
    }, indent=2))

    return 0 if result["matches_expected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
