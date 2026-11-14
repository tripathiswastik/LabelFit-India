"""
LabelFit India: Benchmark Evaluation Module.
Evaluates exploratory label transcription benchmarks from docs/benchmark-template.csv.
Computes Exact Field Match (EFM), Character Error Rate (CER), evidence support ratios,
unsupported text rates, and review latency broken down by field and script.
"""

import os
import sys
import csv
import re
import json
import argparse
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict


def normalize_text(text: Optional[str]) -> str:
    """Collapses whitespace and strips leading/trailing spaces."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()


def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes standard edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def compute_cer(gt: str, pred: str) -> float:
    """
    Computes Character Error Rate = distance / len(gt).
    Returns 0.0 if both strings are empty.
    """
    norm_gt = normalize_text(gt)
    norm_pred = normalize_text(pred)
    if not norm_gt and not norm_pred:
        return 0.0
    if not norm_gt:
        return 1.0  # Entire prediction is inserted when ground truth is empty
    dist = levenshtein_distance(norm_gt, norm_pred)
    return min(1.0, dist / len(norm_gt))


def is_truthy(val: Optional[str]) -> bool:
    if not val:
        return False
    return val.strip().lower() in ("yes", "true", "1", "y")


class BenchmarkEvaluator:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.rows: List[Dict[str, str]] = []
        self._load_csv()

    def _load_csv(self):
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Benchmark CSV not found: {self.csv_path}")

        with open(self.csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            required_cols = {
                "sku_id", "field", "ground_truth", "model_output",
                "read_status", "evidence_located", "unsupported_text"
            }
            if not reader.fieldnames or not required_cols.issubset(set(reader.fieldnames)):
                missing = required_cols - set(reader.fieldnames or [])
                raise ValueError(f"CSV missing mandatory benchmark columns: {missing}")
            self.rows = [r for r in reader if any(r.values())]

    def evaluate(self) -> Dict[str, Any]:
        """Calculates comprehensive benchmark metrics."""
        total_rows = len(self.rows)
        if total_rows == 0:
            return {"total_rows": 0, "message": "CSV contains no data rows."}

        fields_agg = defaultdict(lambda: {
            "total": 0, "exact_matches": 0, "total_cer": 0.0,
            "evidence_supported": 0, "unsupported_text": 0,
            "false_clear": 0, "false_not_visible": 0, "hallucinated_absent": 0,
            "review_seconds": []
        })

        scripts_agg = defaultdict(lambda: {"total": 0, "exact_matches": 0, "total_cer": 0.0})
        conditions_agg = defaultdict(lambda: {"total": 0, "exact_matches": 0, "total_cer": 0.0})
        unique_skus = set()
        unique_images = set()

        for r in self.rows:
            sku = r.get("sku_id", "").strip()
            img = r.get("image_id", "").strip()
            if sku: unique_skus.add(sku)
            if img: unique_images.add(img)

            field = r.get("field", "unknown").strip()
            script = r.get("package_language_script", "unspecified").strip() or "unspecified"
            condition = r.get("photo_condition", "standard").strip() or "standard"

            gt = r.get("ground_truth", "")
            pred = r.get("model_output", "")
            read_status = r.get("read_status", "").strip().lower()
            ev_loc = is_truthy(r.get("evidence_located", ""))
            unsupp = is_truthy(r.get("unsupported_text", ""))

            # Review time
            sec_str = r.get("review_seconds", "").strip()
            if sec_str:
                try:
                    fields_agg[field]["review_seconds"].append(float(sec_str))
                except ValueError:
                    pass

            norm_gt = normalize_text(gt)
            norm_pred = normalize_text(pred)
            is_exact = (norm_gt == norm_pred)
            cer = compute_cer(gt, pred)

            f_stats = fields_agg[field]
            f_stats["total"] += 1
            if is_exact: f_stats["exact_matches"] += 1
            f_stats["total_cer"] += cer
            if ev_loc: f_stats["evidence_supported"] += 1
            if unsupp: f_stats["unsupported_text"] += 1

            if read_status == "clear" and (unsupp or cer > 0.15):
                f_stats["false_clear"] += 1
            if read_status == "not_visible" and norm_gt:
                f_stats["false_not_visible"] += 1
            if not norm_gt and norm_pred and read_status != "not_visible":
                f_stats["hallucinated_absent"] += 1

            s_stats = scripts_agg[script]
            s_stats["total"] += 1
            if is_exact: s_stats["exact_matches"] += 1
            s_stats["total_cer"] += cer

            c_stats = conditions_agg[condition]
            c_stats["total"] += 1
            if is_exact: c_stats["exact_matches"] += 1
            c_stats["total_cer"] += cer

        field_summary = {}
        for f, data in fields_agg.items():
            tot = data["total"]
            efm_pct = round((data["exact_matches"] / tot) * 100, 1) if tot else 0.0
            avg_cer = round(data["total_cer"] / tot, 3) if tot else 0.0
            ev_pct = round((data["evidence_supported"] / tot) * 100, 1) if tot else 0.0
            unsupp_pct = round((data["unsupported_text"] / tot) * 100, 1) if tot else 0.0
            avg_sec = round(sum(data["review_seconds"]) / len(data["review_seconds"]), 1) if data["review_seconds"] else None

            field_summary[f] = {
                "total_rows": tot,
                "exact_match_ratio": f"{data['exact_matches']}/{tot}",
                "exact_match_pct": efm_pct,
                "mean_cer": avg_cer,
                "evidence_support_pct": ev_pct,
                "unsupported_text_pct": unsupp_pct,
                "false_clear_count": data["false_clear"],
                "false_not_visible_count": data["false_not_visible"],
                "hallucinated_absent_count": data["hallucinated_absent"],
                "mean_review_seconds": avg_sec
            }

        script_summary = {}
        for s, data in scripts_agg.items():
            tot = data["total"]
            script_summary[s] = {
                "total": tot,
                "exact_match_pct": round((data["exact_matches"] / tot) * 100, 1) if tot else 0.0,
                "mean_cer": round(data["total_cer"] / tot, 3) if tot else 0.0
            }

        condition_summary = {}
        for c, data in conditions_agg.items():
            tot = data["total"]
            condition_summary[c] = {
                "total": tot,
                "exact_match_pct": round((data["exact_matches"] / tot) * 100, 1) if tot else 0.0,
                "mean_cer": round(data["total_cer"] / tot, 3) if tot else 0.0
            }

        return {
            "total_rows": total_rows,
            "unique_skus_count": len(unique_skus),
            "unique_images_count": len(unique_images),
            "by_field": field_summary,
            "by_script": script_summary,
            "by_condition": condition_summary
        }

    def format_text_report(self, results: Dict[str, Any]) -> str:
        if results.get("total_rows", 0) == 0:
            return "No benchmark data rows to display."

        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("  LABELFIT INDIA - BENCHMARK EVALUATION AUDIT REPORT (SYNTHETIC DEMO)")
        lines.append("=" * 80)
        lines.append(f"Total Rows:     {results['total_rows']}")
        lines.append(f"Unique SKUs:    {results['unique_skus_count']}")
        lines.append(f"Unique Images:  {results['unique_images_count']}")
        lines.append("-" * 80)

        lines.append("\n[1] FIELD-BY-FIELD ACCURACY & EVIDENCE AUDIT:")
        lines.append(f"{'Field':<24} | {'Exact Match':<12} | {'CER':<6} | {'Evidence%':<10} | {'Unsupp%':<8} | {'False Clear':<11}")
        lines.append("-" * 80)
        for f, data in results["by_field"].items():
            efm = f"{data['exact_match_pct']}% ({data['exact_match_ratio']})"
            cer = f"{data['mean_cer']:.3f}"
            ev = f"{data['evidence_support_pct']}%"
            un = f"{data['unsupported_text_pct']}%"
            fc = str(data["false_clear_count"])
            lines.append(f"{f:<24} | {efm:<12} | {cer:<6} | {ev:<10} | {un:<8} | {fc:<11}")

        lines.append("\n[2] STRATA BREAKDOWN BY SCRIPT:")
        lines.append(f"{'Script / Language':<24} | {'Samples':<8} | {'Exact Match %':<14} | {'Mean CER':<8}")
        lines.append("-" * 60)
        for s, data in results["by_script"].items():
            lines.append(f"{s:<24} | {data['total']:<8} | {data['exact_match_pct']:<14}% | {data['mean_cer']:<8.3f}")

        lines.append("\n[3] STRATA BREAKDOWN BY PHOTO CONDITION:")
        lines.append(f"{'Condition':<24} | {'Samples':<8} | {'Exact Match %':<14} | {'Mean CER':<8}")
        lines.append("-" * 60)
        for c, data in results["by_condition"].items():
            lines.append(f"{c:<24} | {data['total']:<8} | {data['exact_match_pct']:<14}% | {data['mean_cer']:<8.3f}")

        lines.append("\n" + "=" * 80)
        lines.append("Note: Synthetic demonstration check (50 SKUs). Exercises failure-mode harnesses.")
        lines.append("      Does not represent live empirical model output on physical packaging photos.")
        lines.append("=" * 80 + "\n")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Evaluate LabelFit India benchmark dataset.")
    parser.add_argument("--csv", default=os.path.join("docs", "benchmark-template.csv"),
                        help="Path to benchmark CSV (defaults to docs/benchmark-template.csv)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON metrics to stdout")
    parser.add_argument("--export-markdown", type=str, default=None,
                        help="Optional file path to write Markdown summary report")
    args = parser.parse_args()

    evaluator = BenchmarkEvaluator(args.csv)
    results = evaluator.evaluate()

    if args.json:
        print(json.dumps(results, indent=2))
        return

    text_report = evaluator.format_text_report(results)
    print(text_report)

    if args.export_markdown:
        with open(args.export_markdown, "w", encoding="utf-8") as f:
            f.write(f"# Benchmark Audit Report\n\n```\n{text_report}\n```\n")
        print(f"Report saved to: {args.export_markdown}")


if __name__ == "__main__":
    main()

