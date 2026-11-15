#!/usr/bin/env python3
"""
LabelFit India: Caregiver Usability Study Session Runner.
Guided CLI tool for facilitators (Swastik & Saumya) to run
consented adult caregiver usability sessions under docs/USABILITY_STUDY_PROTOCOL.md.
Features real-time task stopwatch timing, zero-tolerance safety checks, CLI flags,
and direct export into docs/usability-evaluation-sheet.csv.
"""

import os
import sys
import csv
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List

_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.usability import UsabilityEvaluator

REPO_ROOT = Path(__file__).resolve().parent.parent
USABILITY_CSV = REPO_ROOT / "docs" / "usability-evaluation-sheet.csv"

CSV_HEADERS = [
    "session_id", "caregiver_id", "sku_id", "task_type",
    "time_without_tool_sec", "time_with_tool_sec",
    "accuracy_check", "understood_read_status",
    "relied_on_physical_pack", "misinterpreted_as_safety_score", "feedback_notes"
]

TASK_TYPES = [
    ("1", "age_marking", "Task 1: Locating Stated Age Suitability (e.g. 'Stage 1: From 6 Months')"),
    ("2", "allergen_declaration", "Task 2: Verifying Allergen Declaration (e.g. 'Contains Milk')"),
    ("3", "preparation_clean_water", "Task 3: Preparation Instructions & Clean Drinking Water"),
    ("4", "ambiguous_panel", "Task 4: Low-Contrast / Curved Panel Review ('Check text' trigger)"),
]

VALID_TASK_CODES = [t[1] for t in TASK_TYPES]


def append_trial(row: Dict[str, Any], path: Path = USABILITY_CSV) -> None:
    file_exists = path.exists()
    needs_header = not file_exists or path.stat().st_size == 0
    with open(path, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if needs_header:
            writer.writeheader()
        writer.writerow(row)


def time_task(prompt_label: str) -> float:
    print(f"\n--> Timing {prompt_label}:")
    print("    Press ENTER to START timer when caregiver begins looking...")
    input()
    start_time = time.time()
    print("    [TIMER RUNNING...] Press ENTER immediately when caregiver locates/verifies wording...")
    input()
    elapsed = round(time.time() - start_time, 1)
    print(f"    Elapsed time: {elapsed} seconds")
    override = input(f"    Press ENTER to accept ({elapsed}s) or type manual seconds: ").strip()
    if override:
        try:
            return float(override)
        except ValueError:
            pass
    return elapsed


def prompt_bool(question: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    ans = input(f"{question} {suffix}: ").strip().lower()
    if not ans:
        return default
    return ans in ("y", "yes", "true", "1")


def run_interactive(csv_path: Path) -> None:
    print("==================================================================")
    print("  LABELFIT INDIA - ADULT CAREGIVER USABILITY STUDY RUNNER        ")
    print("  Protocol: docs/USABILITY_STUDY_PROTOCOL.md                      ")
    print("  CRITICAL BOUNDARY: Adults 18+ only; zero child involvement.      ")
    print("==================================================================")

    session_id = input("\nEnter Session ID (e.g. SESS-01): ").strip() or "SESS-01"
    caregiver_id = input("Enter Caregiver ID (e.g. CG-01): ").strip() or "CG-01"
    sku_id = input("Enter Tested Package SKU (e.g. SKU-BF-001): ").strip() or "SKU-BF-001"

    print("\nSelect Task Type:")
    for key, code, desc in TASK_TYPES:
        print(f"  [{key}] {desc}")
    task_choice = input("Enter choice (1-4, default 1): ").strip() or "1"
    task_code = dict((k, c) for k, c, _ in TASK_TYPES).get(task_choice, "age_marking")

    print("\n" + "=" * 50)
    print("PART A: Baseline Measurement (Physical Pack Alone, No Tool)")
    print("Hand physical package to caregiver with specific prompt.")
    time_without = time_task("Physical Package Alone")

    print("\n" + "=" * 50)
    print("PART B: Assisted Measurement (Physical Pack + LabelFit Tool)")
    print("Caregiver reviews LabelFit candidate readout on laptop/screen.")
    time_with = time_task("Assisted with LabelFit")

    time_delta = round(((time_without - time_with) / time_without) * 100, 1) if time_without else 0.0
    print(f"\n--> Time reduction: {time_delta}% ({time_without}s down to {time_with}s)")

    print("\n" + "=" * 50)
    print("PART C: Verification & Safety Comprehension Audit")
    accuracy_ok = prompt_bool("1. Did the caregiver correctly identify the printed label text?", default=True)
    status_understood = prompt_bool("2. Did the caregiver understand 'Readable'/'Check text' as model transcription hints (NOT safety scores)?", default=True)
    relied_physical = prompt_bool("3. Did the caregiver inspect/verify against the physical package?", default=True)

    print("\n⚠️ ZERO-TOLERANCE SAFETY BOUNDARY CHECK:")
    misinterpreted_safety = prompt_bool("4. Did the caregiver misinterpret 'Readable' as an endorsement of food safety or health advice?", default=False)
    if misinterpreted_safety:
        print("\n" + "!" * 65)
        print(" [CRITICAL SAFETY GATE TRIGGERED]")
        print(" Caregiver misinterpreted read-status as a safety endorsement!")
        print(" Under protocol rules, investigate immediately before continuing.")
        print("!" * 65)

    notes = input("\nParticipant qualitative notes / verbatim feedback: ").strip()

    row = {
        "session_id": session_id,
        "caregiver_id": caregiver_id,
        "sku_id": sku_id,
        "task_type": task_code,
        "time_without_tool_sec": f"{time_without:.1f}",
        "time_with_tool_sec": f"{time_with:.1f}",
        "accuracy_check": "true" if accuracy_ok else "false",
        "understood_read_status": "true" if status_understood else "false",
        "relied_on_physical_pack": "true" if relied_physical else "false",
        "misinterpreted_as_safety_score": "true" if misinterpreted_safety else "false",
        "feedback_notes": notes,
    }

    append_trial(row, csv_path)
    print(f"\n--> Successfully recorded trial to: {csv_path}")

    # Summary
    try:
        evaluator = UsabilityEvaluator(str(csv_path))
        results = evaluator.evaluate()
        if results.get("total_trials", 0) > 0:
            print(f"\n--> Cumulative Study Progress: {results['total_trials']} trials across {results['unique_caregivers']} caregivers.")
            print(f"--> Average Time Reduction: {results['time_reduction_pct']}% ({results['mean_time_without_sec']}s -> {results['mean_time_with_sec']}s)")
            print(f"--> Read Status Comprehension: {results['status_comprehension_rate']*100:.1f}%")
            print(f"--> Safety Misinterpretation Incidents: {results['safety_misinterpretation_count']} (Target: 0)")
    except Exception as e:
        print(f"Evaluation note: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="LabelFit India Caregiver Usability Study Session Runner"
    )
    parser.add_argument("--csv", default=str(USABILITY_CSV), help="Path to usability CSV file")
    parser.add_argument("--session-id", help="Session ID (e.g. SESS-01)")
    parser.add_argument("--caregiver-id", help="Caregiver ID (e.g. CG-01)")
    parser.add_argument("--sku-id", help="Tested SKU ID (e.g. SKU-BF-001)")
    parser.add_argument("--task-type", choices=VALID_TASK_CODES, help="Usability task code")
    parser.add_argument("--time-without", type=float, help="Baseline time in seconds (physical pack alone)")
    parser.add_argument("--time-with", type=float, help="Assisted time in seconds (with LabelFit)")
    parser.add_argument("--accuracy", default="true", choices=["true", "false"], help="Label reading accuracy")
    parser.add_argument("--status-understood", default="true", choices=["true", "false"], help="Understood read-status")
    parser.add_argument("--relied-physical", default="true", choices=["true", "false"], help="Inspected physical pack")
    parser.add_argument("--misinterpreted-safety", default="false", choices=["true", "false"], help="Misinterpreted safety (Target: false)")
    parser.add_argument("--notes", default="", help="Qualitative feedback notes")
    parser.add_argument("--import-json", help="Path to JSON file containing array of usability trials")

    args = parser.parse_args()
    csv_file = Path(args.csv)

    # 1. Single trial via flags
    if args.session_id and args.caregiver_id and args.sku_id and args.task_type:
        time_without = args.time_without if args.time_without is not None else 0.0
        time_with = args.time_with if args.time_with is not None else 0.0
        row = {
            "session_id": args.session_id,
            "caregiver_id": args.caregiver_id,
            "sku_id": args.sku_id,
            "task_type": args.task_type,
            "time_without_tool_sec": f"{time_without:.1f}",
            "time_with_tool_sec": f"{time_with:.1f}",
            "accuracy_check": args.accuracy,
            "understood_read_status": args.status_understood,
            "relied_on_physical_pack": args.relied_physical,
            "misinterpreted_as_safety_score": args.misinterpreted_safety,
            "feedback_notes": args.notes,
        }
        append_trial(row, csv_file)
        print(f"✓ Recorded usability trial {args.session_id} / {args.task_type} to: {csv_file}")
        return

    # 2. Batch JSON import
    if args.import_json:
        json_path = Path(args.import_json)
        if not json_path.exists():
            print(f"Error: Import file not found: {json_path}", file=sys.stderr)
            sys.exit(1)
        with open(json_path, "r", encoding="utf-8") as f:
            entries = json.load(f)
        count = 0
        for entry in entries:
            row = {
                "session_id": entry.get("session_id", "SESS-01"),
                "caregiver_id": entry.get("caregiver_id", "CG-01"),
                "sku_id": entry.get("sku_id", "SKU-BF-001"),
                "task_type": entry.get("task_type", "age_marking"),
                "time_without_tool_sec": str(entry.get("time_without_tool_sec", "0.0")),
                "time_with_tool_sec": str(entry.get("time_with_tool_sec", "0.0")),
                "accuracy_check": "true" if entry.get("accuracy_check", True) else "false",
                "understood_read_status": "true" if entry.get("understood_read_status", True) else "false",
                "relied_on_physical_pack": "true" if entry.get("relied_on_physical_pack", True) else "false",
                "misinterpreted_as_safety_score": "true" if entry.get("misinterpreted_as_safety_score", False) else "false",
                "feedback_notes": entry.get("feedback_notes", ""),
            }
            append_trial(row, csv_file)
            count += 1
        print(f"✓ Successfully imported {count} usability trials from: {json_path}")
        return

    # 3. Fallback to interactive mode
    run_interactive(csv_file)


if __name__ == "__main__":
    main()
