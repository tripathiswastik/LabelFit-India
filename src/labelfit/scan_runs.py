"""
Copy finished scan runs (from scripts/scan_benchmark.js) into a benchmark worksheet.

Safety rules, enforced in code and covered by tests:
- Only rows whose read_status is exactly "pending_model_scan" are changed.
- ground_truth is never read for filling and never modified.
- A row that already has model_output is never overwritten.
- Images whose scan failed are skipped, so a failed scan can never become a "miss".
- Reviewer judgment columns are reset to "unreviewed"; the scan cannot make them.
"""

import csv
import io
import json
import os
from typing import Any, Dict, List, Optional

FIELD_NAMES = (
    "productName", "ageMarking", "ingredients",
    "allergenDeclaration", "nutritionPanel", "preparationAndStorage",
)
PENDING_SCAN = "pending_model_scan"
UNREVIEWED = "unreviewed"
VALID_STATUSES = {"clear", "uncertain", "not_visible"}


def load_run(run_dir: str):
    """Returns (run_meta, {image_id: record}) from a run folder."""
    meta_path = os.path.join(run_dir, "run.json")
    if not os.path.exists(meta_path):
        raise FileNotFoundError(f"Not a scan run folder (no run.json): {run_dir}")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    records: Dict[str, Dict[str, Any]] = {}
    for name in sorted(os.listdir(run_dir)):
        if not name.endswith(".json") or name == "run.json":
            continue
        with open(os.path.join(run_dir, name), "r", encoding="utf-8") as f:
            record = json.load(f)
        if record.get("image_id"):
            records[record["image_id"]] = record
    return meta, records


def _read_worksheet(path: str):
    with open(path, "rb") as f:
        raw = f.read()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    rows = list(reader)
    return reader.fieldnames or [], rows, has_bom, newline


def _write_worksheet(path: str, fieldnames: List[str], rows: List[Dict[str, str]], has_bom: bool, newline: str):
    with open(path, "w", encoding="utf-8-sig" if has_bom else "utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator=newline)
        writer.writeheader()
        writer.writerows(rows)


def apply_run(worksheet_path: str, run_dir: str, dry_run: bool = False) -> Dict[str, Any]:
    meta, records = load_run(run_dir)
    fieldnames, rows, has_bom, newline = _read_worksheet(worksheet_path)
    required = {"image_id", "field", "ground_truth", "model_output", "read_status",
                "evidence_located", "unsupported_text", "error_category", "reviewer_notes"}
    missing = required - set(fieldnames)
    if missing:
        raise ValueError(f"Worksheet is missing columns: {sorted(missing)}")

    summary = {
        "filled_rows": 0, "images_filled": set(), "skipped_failed_scan": set(),
        "skipped_no_record": set(), "skipped_already_has_output": 0,
        "skipped_not_pending": 0, "skipped_unknown_field": 0,
    }
    model_name = next((r.get("model_responded") for r in records.values() if r.get("model_responded")),
                      meta.get("model_requested"))
    stamp = (f"[auto-filled from run {meta.get('run_id')}; model {model_name}; "
             f"prompt {meta.get('prompt_fingerprint')}; reviewer columns pending]")

    for row in rows:
        status = (row.get("read_status") or "").strip().lower()
        image_id = (row.get("image_id") or "").strip()
        if status != PENDING_SCAN:
            if image_id in records:
                summary["skipped_not_pending"] += 1
            continue
        record = records.get(image_id)
        if record is None:
            summary["skipped_no_record"].add(image_id)
            continue
        if record.get("error") or not record.get("normalized"):
            summary["skipped_failed_scan"].add(image_id)
            continue
        field = (row.get("field") or "").strip()
        if field not in FIELD_NAMES:
            summary["skipped_unknown_field"] += 1
            continue
        if (row.get("model_output") or "").strip():
            summary["skipped_already_has_output"] += 1
            continue
        result = record["normalized"].get(field) or {}
        read_status = result.get("readStatus")
        if read_status not in VALID_STATUSES:
            summary["skipped_failed_scan"].add(image_id)
            continue

        row["model_output"] = result.get("value", "")
        row["read_status"] = read_status
        # Placeholders in pending rows were not judgments. Reviewers fill these in later.
        row["evidence_located"] = ""
        row["unsupported_text"] = ""
        row["error_category"] = UNREVIEWED
        notes = (row.get("reviewer_notes") or "").strip()
        row["reviewer_notes"] = f"{notes}; {stamp}" if notes else stamp
        summary["filled_rows"] += 1
        summary["images_filled"].add(image_id)

    if not dry_run and summary["filled_rows"]:
        _write_worksheet(worksheet_path, fieldnames, rows, has_bom, newline)

    return {
        "run_id": meta.get("run_id"),
        "dry_run": dry_run,
        "filled_rows": summary["filled_rows"],
        "images_filled": sorted(summary["images_filled"]),
        "skipped_failed_scan": sorted(summary["skipped_failed_scan"]),
        "skipped_no_record": sorted(summary["skipped_no_record"]),
        "skipped_already_has_output": summary["skipped_already_has_output"],
        "skipped_not_pending": summary["skipped_not_pending"],
        "skipped_unknown_field": summary["skipped_unknown_field"],
    }
