#!/usr/bin/env python3
"""
Score a benchmark worksheet with confidence intervals and honest strata.

  python scripts/score_benchmark.py --csv docs/benchmark-50sku-results.csv \
      --out docs/BENCHMARK_50_SKU_INTERVALS.md

Reports how often a field marked "Readable" is wrong, number mismatches, per-field exact
match with Wilson intervals, a SKU-clustered bootstrap, and suppresses tiny strata.
Pending rows are excluded. Never overwrites a file unless --out is given.
"""

import argparse
import json
import sys
from pathlib import Path

_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.benchmark_stats import evaluate_csv, format_markdown  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a LabelFit benchmark worksheet with uncertainty.")
    parser.add_argument("--csv", default="docs/benchmark-50sku-results.csv")
    parser.add_argument("--out", help="Write the Markdown report to this file")
    parser.add_argument("--json", action="store_true", help="Print raw metrics as JSON instead")
    parser.add_argument("--min-rows", type=int, default=10, help="Minimum rows for a stratum to be reported")
    parser.add_argument("--min-skus", type=int, default=5, help="Minimum SKUs for a stratum to be reported")
    parser.add_argument("--iterations", type=int, default=2000, help="Bootstrap resamples")
    parser.add_argument("--seed", type=int, default=1, help="Bootstrap seed (fixed for repeatable reports)")
    args = parser.parse_args()
    try:
        summary = evaluate_csv(args.csv, min_rows=args.min_rows, min_skus=args.min_skus,
                               bootstrap_iterations=args.iterations, seed=args.seed)
    except (FileNotFoundError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(summary, indent=2))
        return 0
    report = format_markdown(summary)
    print(report)
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Report saved to: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
