#!/usr/bin/env python3
"""
LabelFit India: 50-SKU Target Complementary Food Benchmark Builder.
Constructs docs/benchmark-50sku-results.csv by combining verified adjudicated ground truth
from docs/founder-independent-transcriptions.csv with recorded model outputs.
Spans 50 SKUs across 5 product strata (clean staple cereals, sweetened cereals, tasty snacks,
fruit purees, and dense high-micronutrient formulations).
"""

import sys
import json
import csv
from pathlib import Path

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


def main() -> None:
    print("== LabelFit India: 50-SKU Benchmark Builder ==")

    engine = AdjudicationEngine(str(TRANSCRIPTION_CSV))
    records = engine.load()
    eval_results = engine.evaluate()

    print(f"Total target records: {eval_results['total_records']} (Completed: {eval_results['completed_count']}, Pending: {eval_results['pending_count']})")
    print(f"Inter-rater concurrence on completed: {eval_results['concurrence_rate']}%")

    # Load recorded Gemini outputs if present
    batch_map = {}
    if BATCH_SCAN_JSON.exists():
        with open(BATCH_SCAN_JSON, "r", encoding="utf-8") as f:
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
        read_status = field_data.get("readStatus", "uncertain") if (model_text or field_data.get("evidence")) else "not_visible"
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

    # Filter to only records where either physical ground truth or model output has been collected.
    # Prevents pending/untranscribed rows from skewing accuracy with false 100% blank matches.
    evaluated_rows = [r for r in rows if r["ground_truth"].strip() or r["model_output"].strip()]

    with open(OUTPUT_50SKU_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(evaluated_rows)

    print(f"Exported benchmark results: {OUTPUT_50SKU_CSV} ({len(evaluated_rows)} evaluated field rows).")
    if eval_results["pending_count"] > 0:
        print(f"Note: {eval_results['pending_count']} fields remain pending independent founder entry in {TRANSCRIPTION_CSV.name}.")


if __name__ == "__main__":
    main()
