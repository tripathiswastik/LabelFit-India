#!/usr/bin/env python3
"""
LabelFit India: Caregiver Usability Study Session Runner.
Guided interactive CLI tool for facilitators (Swastik & Saumya) to run
consented adult caregiver usability sessions under docs/USABILITY_STUDY_PROTOCOL.md.
Features real-time task stopwatch timing, zero-tolerance safety checks, and
direct export into docs/usability-evaluation-sheet.csv.
"""

import os
import sys
import csv
import time
from pathlib import Path

_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.usability import UsabilityEvaluator

REPO_ROOT = Path(__file__).resolve().parent.parent
USABILITY_CSV = REPO_ROOT / "docs" / "usability-evaluation-sheet.csv"

TASK_TYPES = [
    ("1", "age_marking", "Task 1: Locating Stated Age Suitability (e.g. 'Stage 1: From 6 Months')"),
    ("2", "allergen_declaration", "Task 2: Verifying Allergen Declaration (e.g. 'Contains Milk')"),
    ("3", "preparation_clean_water", "Task 3: Preparation Instructions & Clean Drinking Water"),
    ("4", "ambiguous_panel", "Task 4: Low-Contrast / Curved Panel Review ('Check text' trigger)"),
]


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


def main():
    print("==================================================================")
    print("  LABELFIT INDIA - ADULT CAREGIVER USABILITY STUDY RUNNER        ")
    print("  Protocol: docs/USABILITY_STUDY_PROTOCOL.md                      ")
    print("  CRITICAL BOUNDARY: Adults 18+ only; zero child involvement.      ")
    print("==================================================================")

    # 1. Session Setup
    session_id = input("\nEnter Session ID (e.g. SESS-01): ").strip() or "SESS-01"
    caregiver_id = input("Enter Caregiver ID (e.g. CG-01): ").strip() or "CG-01"
    sku_id = input("Enter Tested Package SKU (e.g. SKU-BF-001): ").strip() or "SKU-BF-001"

    print("\nSelect Task Type:")
    for key, code, desc in TASK_TYPES:
        print(f"  [{key}] {desc}")
    task_choice = input("Enter choice (1-4, default 1): ").strip() or "1"
    task_code = dict((k, c) for k, c, _ in TASK_TYPES).get(task_choice, "age_marking")

    # 2. Timing Measurements
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

    # 3. Post-Task Verification Checks
    print("\n" + "=" * 50)
    print("PART C: Verification & Safety Comprehension Audit")
    accuracy_ok = prompt_bool("1. Did the caregiver correctly identify the printed label text?", default=True)
    status_understood = prompt_bool("2. Did the caregiver understand 'Readable'/'Check text' as model transcription hints (NOT safety scores)?", default=True)
    relied_physical = prompt_bool("3. Did the caregiver inspect/verify against the physical package?", default=True)
    
    # 4. Zero-Tolerance Safety Gate Check
    print("\n⚠️ ZERO-TOLERANCE SAFETY BOUNDARY CHECK:")
    misinterpreted_safety = prompt_bool("4. Did the caregiver misinterpret 'Readable' as an endorsement of food safety or health advice?", default=False)
    if misinterpreted_safety:
        print("\n" + "!" * 65)
        print(" [CRITICAL SAFETY GATE TRIGGERED]")
        print(" Caregiver misinterpreted read-status as a safety endorsement!")
        print(" Under protocol rules, investigate immediately before continuing.")
        print("!" * 65)

    notes = input("\nParticipant qualitative notes / verbatim feedback: ").strip()

    # 5. Save to CSV
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

    file_exists = USABILITY_CSV.exists()
    headers = [
        "session_id", "caregiver_id", "sku_id", "task_type",
        "time_without_tool_sec", "time_with_tool_sec",
        "accuracy_check", "understood_read_status",
        "relied_on_physical_pack", "misinterpreted_as_safety_score", "feedback_notes"
    ]

    with open(USABILITY_CSV, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists or USABILITY_CSV.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row)

    print(f"\n--> Successfully recorded trial to: {USABILITY_CSV}")

    # 6. Run live evaluation
    try:
        evaluator = UsabilityEvaluator(str(USABILITY_CSV))
        results = evaluator.evaluate()
        if results.get("total_trials", 0) > 0:
            print(f"\n--> Cumulative Study Progress: {results['total_trials']} trials across {results['unique_caregivers']} caregivers.")
            print(f"--> Average Time Reduction: {results['time_reduction_pct']}% ({results['mean_time_without_sec']}s -> {results['mean_time_with_sec']}s)")
            print(f"--> Read Status Comprehension: {results['status_comprehension_rate']*100:.1f}%")
            print(f"--> Safety Misinterpretation Incidents: {results['safety_misinterpretation_count']} (Target: 0)")
    except Exception as e:
        print(f"Evaluation note: {e}")


if __name__ == "__main__":
    main()
