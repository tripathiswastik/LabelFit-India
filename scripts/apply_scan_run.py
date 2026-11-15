#!/usr/bin/env python3
"""
Copy a finished scan run into the benchmark worksheet.

  python scripts/apply_scan_run.py --run benchmark-runs/bf-run-1 \
      --worksheet docs/benchmark-50sku-results.csv --dry-run

Only rows marked pending_model_scan are filled. Ground truth is never touched.
After applying, a reviewer must fill evidence_located, unsupported_text,
error_category and (optionally) review_seconds before support metrics are reported.
"""

import argparse
import json
import sys
from pathlib import Path

_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.scan_runs import apply_run  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply a scan run to a benchmark worksheet.")
    parser.add_argument("--run", required=True, help="Run folder created by scripts/scan_benchmark.js")
    parser.add_argument("--worksheet", required=True, help="Benchmark CSV to update")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change without writing")
    args = parser.parse_args()
    try:
        summary = apply_run(args.worksheet, args.run, dry_run=args.dry_run)
    except (FileNotFoundError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(summary, indent=2))
    if args.dry_run:
        print("\nDry run only: nothing was written.")
    elif summary["filled_rows"]:
        print(f"\nFilled {summary['filled_rows']} rows. Next: have a reviewer complete the reviewer columns.")
    else:
        print("\nNo rows needed filling.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
