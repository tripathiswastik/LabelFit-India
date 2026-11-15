#!/usr/bin/env python3
"""
LabelFit India: Benchmark Builder.
Delegates to build_10sku_benchmark.py to generate the empirical 10-SKU benchmark.
A full 50-SKU benchmark remains future work pending additional packaging panels.
"""

import sys
from pathlib import Path

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from build_10sku_benchmark import main as build_10sku_main


if __name__ == "__main__":
    print("50-SKU benchmark remains future work. Generating verified 10-SKU empirical benchmark...")
    build_10sku_main()
