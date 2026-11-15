#!/usr/bin/env python3
"""
LabelFit India: Founder Transcription CLI & Batch Ingestion Tool.
Assists Swastik Tripathi and Saumya Tripathi in recording independent physical packaging
transcriptions for the 50 target baby food products directly into
docs/founder-independent-transcriptions.csv via interactive mode, CLI flags, or JSON import.
"""

import os
import sys
import csv
import json
import argparse
import datetime
from pathlib import Path
from typing import List, Optional

_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.adjudication import AdjudicationEngine, DualTranscriptionRecord, FIELD_NAMES, normalize_text

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "docs" / "founder-independent-transcriptions.csv"

CSV_HEADERS = [
    "sku_id", "brand", "product_name", "field",
    "swastik_transcription", "swastik_date",
    "saumya_transcription", "saumya_date",
    "adjudicated_ground_truth", "adjudication_notes",
]


def save_records(records: List[DualTranscriptionRecord], path: Path = CSV_PATH) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
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


def list_pending(records: List[DualTranscriptionRecord], reviewer: Optional[str] = None) -> None:
    print("\n== PENDING TRANSCRIPTIONS ==")
    pending_by_sku = {}
    for r in records:
        sw_done = bool(r.swastik_date)
        sa_done = bool(r.saumya_date)
        if reviewer == "swastik" and sw_done:
            continue
        if reviewer == "saumya" and sa_done:
            continue
        if not reviewer and sw_done and sa_done:
            continue

        if r.sku_id not in pending_by_sku:
            pending_by_sku[r.sku_id] = {
                "brand": r.brand,
                "product": r.product_name,
                "fields": [],
            }
        status = []
        if not sw_done:
            status.append("Swastik pending")
        if not sa_done:
            status.append("Saumya pending")
        pending_by_sku[r.sku_id]["fields"].append(f"{r.field} ({', '.join(status)})")

    if not pending_by_sku:
        print("Zero pending fields! All transcriptions are up to date.")
        return

    print(f"Total SKUs with pending fields: {len(pending_by_sku)}\n")
    for sku_id, data in sorted(pending_by_sku.items()):
        print(f"• [{sku_id}] {data['brand']} - {data['product']}")
        for f in data["fields"]:
            print(f"    - {f}")


def record_single(
    records: List[DualTranscriptionRecord],
    reviewer: str,
    sku_id: str,
    field: str,
    text: str,
    date_str: str,
    notes: Optional[str] = None,
) -> bool:
    target = None
    for r in records:
        if r.sku_id == sku_id and r.field == field:
            target = r
            break

    if not target:
        print(f"Error: Record not found for SKU '{sku_id}' and field '{field}'", file=sys.stderr)
        return False

    rev_norm = reviewer.strip().lower()
    if rev_norm not in ("swastik", "saumya"):
        print(f"Error: Reviewer must be 'swastik' or 'saumya', got '{reviewer}'", file=sys.stderr)
        return False

    if rev_norm == "swastik":
        target.swastik_transcription = text
        target.swastik_date = date_str
    else:
        target.saumya_transcription = text
        target.saumya_date = date_str

    if notes:
        existing = target.adjudication_notes.strip()
        target.adjudication_notes = f"{existing}; {notes}" if existing else notes

    # Check for immediate concurrence if both entered
    if target.swastik_date and target.saumya_date:
        if normalize_text(target.swastik_transcription) == normalize_text(target.saumya_transcription):
            target.adjudicated_ground_truth = target.swastik_transcription
            concur_note = "Exact concurrence between Swastik and Saumya."
            if concur_note not in target.adjudication_notes:
                target.adjudication_notes = f"{target.adjudication_notes}; {concur_note}".strip("; ")

    return True


def run_interactive(engine: AdjudicationEngine, records: List[DualTranscriptionRecord]) -> None:
    print("==================================================================")
    print("  LABELFIT INDIA - INDEPENDENT FOUNDER TRANSCRIPTION ASSISTANT   ")
    print("==================================================================")
    print("\nSelect Active Reviewer:")
    print("  [1] Swastik Tripathi")
    print("  [2] Saumya Tripathi")
    choice = input("Enter 1 or 2 (default 1): ").strip()
    reviewer = "saumya" if choice == "2" else "swastik"
    today_str = datetime.date.today().isoformat()
    rev_name = "Saumya Tripathi" if reviewer == "saumya" else "Swastik Tripathi"
    print(f"\n--> Active reviewer: {rev_name} (Date: {today_str})")

    pending_indices = [
        idx for idx, r in enumerate(records)
        if not (r.saumya_date if reviewer == "saumya" else r.swastik_date)
    ]
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

            record_single(records, reviewer, r.sku_id, r.field, user_text, today_str)
            updated_count += 1
            print(f"  ✓ Saved {r.field} for {r.sku_id}")

    except KeyboardInterrupt:
        print("\n\nSession interrupted by user. Saving current progress...")

    if updated_count > 0:
        save_records(records)
        print(f"\n--> Successfully saved {updated_count} updated fields to: {CSV_PATH}")
        results = engine.evaluate()
        print(f"--> Progress: {results['completed_count']}/{results['total_records']} completed ({results['pending_count']} pending)")
    else:
        print("No changes to save.")


def main():
    parser = argparse.ArgumentParser(
        description="LabelFit India Founder Packaging Transcription Assistant"
    )
    parser.add_argument("--csv", default=str(CSV_PATH), help="Path to transcription worksheet")
    parser.add_argument("--list-pending", action="store_true", help="List all pending SKUs and fields")
    parser.add_argument("--reviewer", choices=["swastik", "saumya"], help="Reviewer identifier")
    parser.add_argument("--sku", help="Target SKU identifier (e.g. SKU-BF-002)")
    parser.add_argument("--field", choices=FIELD_NAMES, help="Target field name")
    parser.add_argument("--text", help="Transcribed literal text from physical packaging")
    parser.add_argument("--date", help="Date of transcription (YYYY-MM-DD, default today)")
    parser.add_argument("--notes", help="Optional adjudication/reviewer notes")
    parser.add_argument("--import-json", help="Path to JSON file containing array of transcriptions")

    args = parser.parse_args()
    csv_file = Path(args.csv)
    if not csv_file.exists():
        print(f"Error: Worksheet not found: {csv_file}", file=sys.stderr)
        sys.exit(1)

    engine = AdjudicationEngine(str(csv_file))
    records = engine.load()

    # 1. List pending
    if args.list_pending:
        list_pending(records, args.reviewer)
        return

    today_str = args.date or datetime.date.today().isoformat()

    # 2. Single record via flags
    if args.sku and args.field:
        if not args.reviewer:
            print("Error: --reviewer (swastik/saumya) is required when using --sku and --field", file=sys.stderr)
            sys.exit(1)
        text_val = args.text if args.text is not None else ""
        if record_single(records, args.reviewer, args.sku, args.field, text_val, today_str, args.notes):
            save_records(records, csv_file)
            print(f"✓ Recorded {args.field} for {args.sku} ({args.reviewer})")
        return

    # 3. Batch JSON import
    if args.import_json:
        json_path = Path(args.import_json)
        if not json_path.exists():
            print(f"Error: Import file not found: {json_path}", file=sys.stderr)
            sys.exit(1)
        with open(json_path, "r", encoding="utf-8") as f:
            entries = json.load(f)
        count = 0
        for entry in entries:
            rev = entry.get("reviewer") or args.reviewer
            sku = entry.get("sku_id") or entry.get("sku")
            fld = entry.get("field")
            txt = entry.get("text", "")
            dt = entry.get("date") or today_str
            nts = entry.get("notes")
            if rev and sku and fld:
                if record_single(records, rev, sku, fld, txt, dt, nts):
                    count += 1
        save_records(records, csv_file)
        print(f"✓ Successfully imported {count} transcriptions from: {json_path}")
        return

    # 4. Fallback to interactive mode
    run_interactive(engine, records)


if __name__ == "__main__":
    main()
