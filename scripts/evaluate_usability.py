#!/usr/bin/env python3
"""
CLI entry point for caregiver usability study evaluation.
Delegates to the core labelfit.usability engine.
"""

import sys
from pathlib import Path

# Ensure src is on sys.path for direct CLI script execution
_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.usability import (
    is_truthy,
    parse_float,
    UsabilityEvaluator,
    main,
)

if __name__ == "__main__":
    main()
