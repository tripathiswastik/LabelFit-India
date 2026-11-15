#!/usr/bin/env python3
"""
CLI entry point for benchmark evaluation.
Delegates to the core labelfit.benchmark engine.
"""

import sys
from pathlib import Path

# Ensure src is on sys.path for direct CLI script execution
_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

# Names below are re-exported for callers that import from this script.
from labelfit.benchmark import (
    normalize_text,
    levenshtein_distance,
    compute_cer,
    BenchmarkEvaluator,
    main
)

__all__ = ['normalize_text', 'levenshtein_distance', 'compute_cer', 'BenchmarkEvaluator', 'main']

if __name__ == "__main__":
    main()
