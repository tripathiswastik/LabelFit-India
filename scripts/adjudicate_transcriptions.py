#!/usr/bin/env python3
"""
CLI entry point for founder independent transcription adjudication.
Delegates to labelfit.adjudication.
"""

import sys
import argparse
from pathlib import Path

_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.adjudication import AdjudicationEngine


def main():
    repo_root = Path(__file__).resolve().parent.parent
    default_csv = repo_root / "docs" / "founder-independent-transcriptions.csv"

    parser = argparse.ArgumentParser(
        description="Audit founder independent transcriptions and check physical package adjudication."
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=str(default_csv),
        help=f"Path to dual-transcription CSV (default: {default_csv})",
    )
    parser.add_argument(
        "--export-markdown",
        type=str,
        default=None,
        help="Optional file path to write Markdown summary report",
    )
    args = parser.parse_args()

    engine = AdjudicationEngine(args.csv)
    records = engine.load()
    results = engine.evaluate()

    report = engine.format_markdown_report(results)
    print(report)

    if args.export_markdown:
        with open(args.export_markdown, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nReport exported to: {args.export_markdown}")

    if not results.get("all_adjudicated") and results.get("total_records", 0) > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
