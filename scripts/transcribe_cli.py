#!/usr/bin/env python3
"""
LabelFit India: Interactive Founder Transcription CLI.
Assists Swastik Tripathi and Saumya Tripathi in recording independent physical packaging
transcriptions for the 50 target baby food products directly into
docs/founder-independent-transcriptions.csv without manual spreadsheet editing.
"""

import os
import sys
import csv
import datetime
from pathlib import Path

_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.adjudication import AdjudicationEngine, FIELD_NAMES, normalize_text

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "founder-independent-transcriptions.csv"


def prompt_reviewer() -> str:
    print("\nSelect Active Reviewer:")
    print("  [1] Swastik Tripathi")
    print("  [2] Saumya Tripathi")
    choice = input("Enter 1 or 2 (default 1): ").strip()
    return "saumya" if choice == "2" else "swastik"


def main():
    print("==================================================================")
    print("  LABELFIT INDIA - INDEPENDENT FOUNDER TRANSCRIPTION ASSISTANT   ")
    print("==================================================================")

    if not CSV_PATH.exists():
        print(f"Error: Worksheet not found: {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    reviewer = prompt_reviewer()
    today_str = datetime.date.today().isoformat()
    rev_name = "Saumya Tripathi" if reviewer == "saumya" else "Swastik Tripathi"
    print(f"\n--> Active reviewer: {rev_name} (Date: {today_str})")

    engine = AdjudicationEngine(str(CSV_PATH))
    records = engine.load()

    # Find records pending for this reviewer
    pending_indices = []
    for idx, r in enumerate(records):
        val = r.saumya_transcription if reviewer == "saumya" else r.swastik_transcription
        dt = r.saumya_date if reviewer == "saumya" else r.swastik_date
        if not dt:
            pending_indices.append(idx)

    print(f"--> Total fields: {len(records)} | Pending for {rev_name}: {len(pending_indices)}")

    if not pending_indices:
        print(f"All {len(records)} records have been transcribed by {rev_name}!")
        return

    print("\nEntering transcription loop. Press Ctrl+C at any time to save and exit.\n")
    updated_count = 0

    try:
        for idx in pending_indices:
            r = records[idx]
            print("-" * 65)
            print(f"SKU:   {r.sku_id} | {r.brand} - {r.product_name}")
            print(f"Field: {r.field}")
            print("Instruction: Inspect physical package and type exact printed text.")
            print("             (Press Enter with empty input if field is not visible on package)")
            print("             (Type ':skip' to skip, ':quit' to exit and save)")

            user_text = input(f"[{r.field}] > ").strip()
            if user_text == ":quit":
                break
            if user_text == ":skip":
                continue

            if reviewer == "saumya":
                r.saumya_transcription = user_text
                r.saumya_date = today_str
            else:
                r.swastik_transcription = user_text
                r.swastik_date = today_str

            updated_count += 1
            print(f"  ✓ Saved {r.field} for {r.sku_id}")

    except KeyboardInterrupt:
        print("\n\nSession interrupted by user. Saving current progress...")

    if updated_count > 0:
        # Save back to CSV
        headers = [
            "sku_id", "brand", "product_name", "field",
            "swastik_transcription", "swastik_date",
            "saumya_transcription", "saumya_date",
            "adjudicated_ground_truth", "adjudication_notes",
        ]
        with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for r in records:
                writer.writerow({
                    "sku_id": r.sku_id,
                    "brand": r.brand,
                    "product_name": r.product_name,
                    "field": r.field,
                    "swastik_transcription": r.swastik_transcription,
                    "swastik_date": r.swastik_date,
                    "saumya_transcription": r.saumya_transcription,
                    "saumya_date": r.saumya_date,
                    "adjudicated_ground_truth": r.adjudicated_ground_truth,
                    "adjudication_notes": r.adjudication_notes,
                })

        print(f"\n--> Successfully saved {updated_count} updated fields to: {CSV_PATH}")

        # Check adjudication status
        engine = AdjudicationEngine(str(CSV_PATH))
        engine.load()
        results = engine.evaluate()
        print(f"--> Progress: {results['completed_count']}/{results['total_records']} completed ({results['pending_count']} pending)")
        if results['completed_count'] > 0:
            print(f"--> Inter-rater agreement on completed: {results['concurrence_rate']}% ({results['concurrence_count']} exact matches, {results['discrepancy_count']} discrepancies)")
    else:
        print("No changes to save.")


if __name__ == "__main__":
    main()
