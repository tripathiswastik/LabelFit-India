#!/usr/bin/env python3
"""
LabelFit India: Benchmark Builder.
Delegates to build_10sku_benchmark.py to generate the empirical 10-SKU benchmark.
A full 50-SKU benchmark remains future work pending additional packaging panels.
"""

import runpy
from pathlib import Path


def main() -> None:
    print("50-SKU benchmark remains future work. Generating verified 10-SKU empirical benchmark...")
    target_script = Path(__file__).resolve().parent / "build_10sku_benchmark.py"
    runpy.run_path(str(target_script), run_name="__main__")


if __name__ == "__main__":
    main()

