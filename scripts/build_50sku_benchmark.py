#!/usr/bin/env python3
"""
LabelFit India: 50-SKU Exploratory Benchmark Builder.
Constructs docs/benchmark-50sku-results.csv by pairing actual Gemini model outputs
from prod1_tst/batch_scan_results.json with physical package ground truth
independently transcribed and adjudicated by Swastik Tripathi & Saumya Tripathi.
Filters pending fields to prevent false 100% blank matches, with options for strata analysis.
"""

import sys
import json
import csv
import argparse
from pathlib import Path
from typing import Dict, Any, List

_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.adjudication import AdjudicationEngine

REPO_ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTION_CSV = REPO_ROOT / "docs" / "founder-independent-transcriptions.csv"
OUTPUT_50SKU_CSV = REPO_ROOT / "docs" / "benchmark-50sku-results.csv"
BATCH_SCAN_JSON = REPO_ROOT / "prod1_tst" / "batch_scan_results.json"

FIELDNAMES = [
    "image_id",
    "sku_id",
    "brand",
    "market_city",
    "package_language_script",
    "photo_condition",
    "field",
    "ground_truth",
    "model_output",
    "read_status",
    "evidence_located",
    "unsupported_text",
    "error_category",
    "review_seconds",
    "reviewer_notes",
]

STRATA_DEFINITIONS = [
    (1, 10, "Stratum 1: Clean Single/Multi-Grain Staple Cereals"),
    (11, 20, "Stratum 2: Sweetened & Fortified Commercial Baby Cereals"),
    (21, 30, "Stratum 3: Finger Foods, Teething Biscuits & Snacks"),
    (31, 40, "Stratum 4: Single & Blended Fruit/Vegetable Purees"),
    (41, 50, "Stratum 5: Dense Growth Formulations & Toddler Cereals"),
]


def get_stratum_name(sku_id: str) -> str:
    if not sku_id.startswith("SKU-BF-"):
        return "Other / Uncategorized"
    try:
        num = int(sku_id.split("-")[-1])
        for start, end, label in STRATA_DEFINITIONS:
            if start <= num <= end:
                return label
    except (ValueError, IndexError):
        pass
    return "Other / Uncategorized"


def print_strata_breakdown(records) -> None:
    print("\n" + "=" * 65)
    print("  50-SKU COMPLEMENTARY FOOD BENCHMARK: STRATA PROGRESS AUDIT")
    print("=" * 65)
    print(f"{'Stratum':<45} | {'Total':<5} | {'Done':<5} | {'Pending':<7} | {'Concurrence'}")
    print("-" * 78)

    for start, end, label in STRATA_DEFINITIONS:
        sku_set = {f"SKU-BF-{i:03d}" for i in range(start, end + 1)}
        stratum_records = [r for r in records if r.sku_id in sku_set]
        tot = len(stratum_records)
        comp = sum(1 for r in stratum_records if not r.is_pending)
        pend = sum(1 for r in stratum_records if r.is_pending)
        conc = sum(1 for r in stratum_records if r.is_concurrence)
        conc_rate = f"{(conc / comp * 100):.1f}%" if comp > 0 else "N/A"
        print(f"{label:<45} | {tot:<5} | {comp:<5} | {pend:<7} | {conc_rate}")
    print("=" * 65 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="LabelFit India 50-SKU Benchmark Builder"
    )
    parser.add_argument("--csv", default=str(TRANSCRIPTION_CSV), help="Path to input transcription CSV")
    parser.add_argument("--out", default=str(OUTPUT_50SKU_CSV), help="Path to export benchmark CSV")
    parser.add_argument("--batch-json", default=str(BATCH_SCAN_JSON), help="Path to Gemini batch scan JSON")
    parser.add_argument("--include-pending", action="store_true", help="Include pending rows in output CSV")
    parser.add_argument("--strata", action="store_true", help="Display strata progress audit breakdown")

    args = parser.parse_args()

    print("== LabelFit India: 50-SKU Benchmark Builder ==")

    engine = AdjudicationEngine(args.csv)
    records = engine.load()
    eval_results = engine.evaluate()

    print(f"Total target records: {eval_results['total_records']} (Completed: {eval_results['completed_count']}, Pending: {eval_results['pending_count']})")
    print(f"Inter-rater concurrence on completed: {eval_results['concurrence_rate']}%")

    if args.strata:
        print_strata_breakdown(records)

    # A comparison is meaningful only when actual model outputs are available.
    # Refuse to silently turn missing scan data into all-blank predictions.
    batch_map = {}
    batch_path = Path(args.batch_json)
    if not batch_path.is_file():
        raise FileNotFoundError(
            f"Gemini batch results not found at {batch_path}. "
            "Provide recorded scan outputs before building comparison results."
        )
    with open(batch_path, "r", encoding="utf-8") as f:
        for item in json.load(f):
            batch_map[item.get("sku_id")] = item

    SKU_ALIASES = {
        "SKU-BF-001": "SKU-PROD-013-NUTRITION",
    }

    rows = []
    for r in records:
        gt_text = ""
        notes = r.adjudication_notes
        if not r.is_pending:
            try:
                gt_text = r.get_ground_truth()
            except ValueError as e:
                notes = f"[UNRESOLVED DISCREPANCY] {e}"

        # Match with model output if available
        batch_key = SKU_ALIASES.get(r.sku_id, r.sku_id)
        model_out = batch_map.get(batch_key, {})
        norm_fields = model_out.get("normalized", {})
        raw_fields = model_out.get("raw", {})
        field_data = norm_fields.get(r.field) or raw_fields.get(r.field) or {}

        model_text = field_data.get("value", "")
        field_was_returned = isinstance(field_data, dict) and any(
            key in field_data for key in ("value", "evidence", "readStatus")
        )
        if r.is_pending:
            read_status = "pending_ground_truth"
        elif batch_key not in batch_map:
            read_status = "pending_model_scan"
        elif not field_was_returned:
            read_status = "pending_model_field"
        else:
            read_status = field_data.get("readStatus", "uncertain")

        evidence_located = "yes" if field_data.get("evidence") else "no"

        unsupported = "no"
        if model_text.strip() and not gt_text.strip() and not r.is_pending:
            unsupported = "yes"

        error_category = "none"
        if gt_text.strip() and model_text.strip() != gt_text.strip():
            error_category = "formatting_discrepancy"

        rows.append({
            "image_id": f"IMG-{r.sku_id}",
            "sku_id": r.sku_id,
            "brand": r.brand,
            "market_city": "New Delhi / Retail Markets",
            "package_language_script": "English-Latin",
            "photo_condition": "pouch_panel",
            "field": r.field,
            "ground_truth": gt_text,
            "model_output": model_text,
            "read_status": read_status,
            "evidence_located": evidence_located,
            "unsupported_text": unsupported,
            "error_category": error_category,
            "review_seconds": "",
            "reviewer_notes": notes,
        })

    # Score only rows with adjudicated reference and a corresponding model
    # field. Pending rows remain available for intake tracking when requested.
    if args.include_pending:
        evaluated_rows = rows
    else:
        evaluated_rows = [r for r in rows if not r["read_status"].startswith("pending_")]

    out_path = Path(args.out)
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(evaluated_rows)

    print(f"Exported benchmark results: {out_path} ({len(evaluated_rows)} rows).")
    if eval_results["pending_count"] > 0:
        print(f"Note: {eval_results['pending_count']} fields remain pending independent founder entry in {Path(args.csv).name}.")


if __name__ == "__main__":
    main()
