"""
LabelFit India: Adult Caregiver Usability Evaluation Engine.
Analyzes caregiver trial data from docs/usability-evaluation-sheet.csv.
Computes inspection time reduction, read-status comprehension, physical package
verification rates, and enforces the zero-tolerance safety misinterpretation boundary.
"""

import os
import sys
import csv
import json
import argparse
from typing import List, Dict, Any, Optional
from collections import defaultdict


def is_truthy(val: Optional[str]) -> bool:
    """Parses boolean representation from CSV strings."""
    if not val:
        return False
    return val.strip().lower() in ("yes", "true", "1", "y", "t", "pass")


def parse_float(val: Optional[str], default: float = 0.0) -> float:
    """Safely converts string to float."""
    if not val:
        return default
    try:
        return float(val.strip())
    except ValueError:
        return default


class UsabilityEvaluator:
    # Targets established in docs/USABILITY_STUDY_PROTOCOL.md
    SAFETY_MISINTERPRETATION_TARGET: float = 0.0
    TIME_REDUCTION_TARGET_PCT: float = 30.0
    STATUS_COMPREHENSION_TARGET: float = 0.85
    PHYSICAL_VERIFICATION_TARGET: float = 0.90

    REQUIRED_COLUMNS = {
        "session_id",
        "caregiver_id",
        "sku_id",
        "task_type",
        "time_without_tool_sec",
        "time_with_tool_sec",
        "accuracy_check",
        "understood_read_status",
        "relied_on_physical_pack",
        "misinterpreted_as_safety_score",
    }

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.rows: List[Dict[str, str]] = []
        self._load_csv()

    def _load_csv(self):
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Usability CSV not found: {self.csv_path}")

        with open(self.csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError(f"Usability CSV has no headers: {self.csv_path}")

            missing = self.REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing:
                raise ValueError(
                    f"Usability CSV missing required columns: {sorted(list(missing))}"
                )

            for row in reader:
                # Skip empty lines
                if any(v.strip() for v in row.values() if v):
                    self.rows.append(row)

    def evaluate(self) -> Dict[str, Any]:
        """Calculates aggregate and per-task usability metrics."""
        total_trials = len(self.rows)
        if total_trials == 0:
            return {
                "total_trials": 0,
                "unique_caregivers": 0,
                "safety_gate_passed": None,
                "mean_time_without_sec": 0.0,
                "mean_time_with_sec": 0.0,
                "time_reduction_pct": 0.0,
                "accuracy_check_rate": 0.0,
                "status_comprehension_rate": 0.0,
                "physical_verification_rate": 0.0,
                "safety_misinterpretation_count": 0,
                "safety_misinterpretation_rate": 0.0,
                "by_task": {},
                "by_caregiver": {},
            }

        caregivers = set()
        skus = set()

        total_time_without = 0.0
        total_time_with = 0.0
        total_reduction_pct_sum = 0.0

        accuracy_count = 0
        status_comprehended_count = 0
        relied_physical_count = 0
        safety_misinterpretation_count = 0

        # Groupers
        by_task_rows = defaultdict(list)
        by_caregiver_rows = defaultdict(list)

        for row in self.rows:
            cg_id = row.get("caregiver_id", "").strip()
            caregivers.add(cg_id)
            skus.add(row.get("sku_id", "").strip())
            task = row.get("task_type", "").strip()

            t_without = parse_float(row.get("time_without_tool_sec"))
            t_with = parse_float(row.get("time_with_tool_sec"))
            total_time_without += t_without
            total_time_with += t_with

            # Individual trial reduction percentage
            if t_without > 0:
                trial_red = ((t_without - t_with) / t_without) * 100.0
            else:
                trial_red = 0.0
            total_reduction_pct_sum += trial_red

            if is_truthy(row.get("accuracy_check")):
                accuracy_count += 1
            if is_truthy(row.get("understood_read_status")):
                status_comprehended_count += 1
            if is_truthy(row.get("relied_on_physical_pack")):
                relied_physical_count += 1
            if is_truthy(row.get("misinterpreted_as_safety_score")):
                safety_misinterpretation_count += 1

            by_task_rows[task].append((t_without, t_with, row))
            by_caregiver_rows[cg_id].append((t_without, t_with, row))

        mean_without = total_time_without / total_trials
        mean_with = total_time_with / total_trials
        aggregate_reduction_pct = (
            ((total_time_without - total_time_with) / total_time_without * 100.0)
            if total_time_without > 0
            else 0.0
        )
        avg_trial_reduction_pct = total_reduction_pct_sum / total_trials

        safety_misinterpretation_rate = safety_misinterpretation_count / total_trials
        safety_gate_passed = (safety_misinterpretation_count == 0)

        # Breakdowns
        by_task = {}
        for task, entries in by_task_rows.items():
            cnt = len(entries)
            tw_sum = sum(e[0] for e in entries)
            tw_with_sum = sum(e[1] for e in entries)
            acc = sum(1 for e in entries if is_truthy(e[2].get("accuracy_check")))
            comp = sum(1 for e in entries if is_truthy(e[2].get("understood_read_status")))
            phys = sum(1 for e in entries if is_truthy(e[2].get("relied_on_physical_pack")))
            misint = sum(1 for e in entries if is_truthy(e[2].get("misinterpreted_as_safety_score")))

            task_red = ((tw_sum - tw_with_sum) / tw_sum * 100.0) if tw_sum > 0 else 0.0
            by_task[task] = {
                "trials": cnt,
                "mean_time_without_sec": round(tw_sum / cnt, 1),
                "mean_time_with_sec": round(tw_with_sum / cnt, 1),
                "time_reduction_pct": round(task_red, 1),
                "accuracy_check_rate": round(acc / cnt, 3),
                "status_comprehension_rate": round(comp / cnt, 3),
                "physical_verification_rate": round(phys / cnt, 3),
                "safety_misinterpretations": misint,
            }

        return {
            "total_trials": total_trials,
            "unique_caregivers": len(caregivers),
            "unique_skus": len(skus),
            "mean_time_without_sec": round(mean_without, 1),
            "mean_time_with_sec": round(mean_with, 1),
            "time_reduction_pct": round(aggregate_reduction_pct, 1),
            "avg_trial_reduction_pct": round(avg_trial_reduction_pct, 1),
            "accuracy_check_rate": round(accuracy_count / total_trials, 3),
            "status_comprehension_rate": round(status_comprehended_count / total_trials, 3),
            "physical_verification_rate": round(relied_physical_count / total_trials, 3),
            "safety_misinterpretation_count": safety_misinterpretation_count,
            "safety_misinterpretation_rate": round(safety_misinterpretation_rate, 4),
            "safety_gate_passed": safety_gate_passed,
            "by_task": by_task,
        }

    def format_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generates a structured GitHub Flavored Markdown summary report."""
        if results["total_trials"] == 0:
            return "\n".join([
                "# LabelFit India: Caregiver Usability Evaluation Report",
                "",
                "**Status: NOT EVALUATED**",
                "",
                "No verified trial rows are available. No usability or safety-gate result can be calculated.",
            ])

        passed_badge = "✅ PASSED" if results["safety_gate_passed"] else "❌ FAILED (SAFETY VIOLATION)"
        time_target_met = "✅ Met" if results["time_reduction_pct"] >= self.TIME_REDUCTION_TARGET_PCT else "⚠️ Under Target"
        comp_target_met = "✅ Met" if results["status_comprehension_rate"] >= self.STATUS_COMPREHENSION_TARGET else "⚠️ Under Target"
        phys_target_met = "✅ Met" if results["physical_verification_rate"] >= self.PHYSICAL_VERIFICATION_TARGET else "⚠️ Under Target"

        lines = [
            "# LabelFit India: Caregiver Usability Evaluation Report",
            "",
            f"**Safety Gate Status**: {passed_badge}  ",
            f"**Total Trials**: {results['total_trials']} across {results['unique_caregivers']} caregivers and {results['unique_skus']} SKUs  ",
            "",
            "## 1. Core Success Criteria vs Protocol Targets",
            "",
            "| Metric | Measured Result | Protocol Target | Assessment |",
            "|---|---|---|---|",
            f"| **Safety Misinterpretation Rate** | **{results['safety_misinterpretation_rate']*100:.1f}%** ({results['safety_misinterpretation_count']} incidents) | **0.0%** (Zero Tolerance) | {passed_badge} |",
            f"| **Time to Locate Information** | **{results['mean_time_with_sec']}s** vs {results['mean_time_without_sec']}s ({results['time_reduction_pct']}% faster) | >= {self.TIME_REDUCTION_TARGET_PCT:.0f}% reduction | {time_target_met} |",
            f"| **Read Status Comprehension** | **{results['status_comprehension_rate']*100:.1f}%** | >= {self.STATUS_COMPREHENSION_TARGET*100:.0f}% | {comp_target_met} |",
            f"| **Physical Pack Verification** | **{results['physical_verification_rate']*100:.1f}%** | >= {self.PHYSICAL_VERIFICATION_TARGET*100:.0f}% | {phys_target_met} |",
            f"| **Wording Accuracy Check** | **{results['accuracy_check_rate']*100:.1f}%** | Baseline Verification | Tracked |",
            "",
            "## 2. Per-Task Breakdown",
            "",
            "| Task Type | Trials | Time Without (s) | Time With (s) | Time Delta (%) | Status Comp. | Physical Check | Safety Misint. |",
            "|---|---|---|---|---|---|---|---|",
        ]

        for task, data in results["by_task"].items():
            lines.append(
                f"| `{task}` | {data['trials']} | {data['mean_time_without_sec']}s | {data['mean_time_with_sec']}s | -{data['time_reduction_pct']}% | {data['status_comprehension_rate']*100:.0f}% | {data['physical_verification_rate']*100:.0f}% | {data['safety_misinterpretations']} |"
            )

        lines.extend([
            "",
            "## Interpretation limits",
            "",
            "These descriptive results apply only to the rows supplied. They do not establish general user benefit, product safety, or performance outside the recorded participants, tasks, and packages.",
        ])

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Evaluate LabelFit India caregiver usability study data.")
    parser.add_argument(
        "--csv",
        default=os.path.join("docs", "usability-evaluation-sheet.csv"),
        help="Path to usability evaluation CSV (default: docs/usability-evaluation-sheet.csv)",
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON results")
    parser.add_argument(
        "--export-markdown",
        type=str,
        default=None,
        help="Path to export markdown evaluation report",
    )
    args = parser.parse_args()

    evaluator = UsabilityEvaluator(args.csv)
    results = evaluator.evaluate()

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        report = evaluator.format_markdown_report(results)
        print(report)

    if args.export_markdown:
        with open(args.export_markdown, "w", encoding="utf-8") as f:
            f.write(evaluator.format_markdown_report(results))
        print(f"\nReport exported to: {args.export_markdown}")

    if results["safety_gate_passed"] is False:
        print(
            "\n[CRITICAL FAILURE] Usability study triggered safety stop condition: "
            f"{results['safety_misinterpretation_count']} participant(s) misinterpreted read status as safety score.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

