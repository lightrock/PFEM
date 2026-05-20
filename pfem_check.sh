#!/usr/bin/env sh
# PFEM_CHECK_LAUNCHER_VERSION=1
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$ROOT"

PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}" python3 tools/pfem_check.py "$@"
