"""
Interval-aware benchmark scoring for LabelFit India.

Complements labelfit.benchmark (exact match and CER) with the numbers that matter most
for a label-transcription tool:

- How often a field marked "Readable" (read_status == clear) is actually wrong.
- Whether a "Readable" field has a number that differs from the pack.
- Uncertainty: Wilson intervals per field, and a SKU-clustered bootstrap for the pooled
  rate (fields from one pack are not independent).
- Honest strata: groups with too few rows or SKUs are suppressed, not shown as percentages.
- Reviewer-dependent metrics (snippet support, unsupported text) are reported only when a
  reviewer has actually filled those columns.

Pending rows are excluded by labelfit.benchmark.BenchmarkEvaluator. None of this is a
clinical, regulatory or safety validation.
"""

import math
import random
import re
import statistics
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

from labelfit.benchmark import BenchmarkEvaluator, compute_cer, is_truthy, normalize_text

Z_95 = 1.959963984540054
CER_THRESHOLD = 0.15
UNREVIEWED_CATEGORIES = {"", "unreviewed", "pending_model_scan"}
DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
NUMBER_PATTERN = re.compile(r"\d+(?:\.\d+)?")


def wilson_interval(successes: int, total: int, z: float = Z_95) -> Optional[Tuple[float, float]]:
    """95% Wilson score interval for a proportion. None when there are no observations."""
    if total <= 0:
        return None
    p = successes / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def extract_numbers(text: Optional[str]) -> List[str]:
    if not text:
        return []
    return sorted(NUMBER_PATTERN.findall(text.translate(DEVANAGARI_DIGITS)))


def numbers_match(ground_truth: Optional[str], prediction: Optional[str]) -> bool:
    return extract_numbers(ground_truth) == extract_numbers(prediction)


def classify_row(row: Dict[str, str]) -> Dict[str, Any]:
    gt = normalize_text(row.get("ground_truth", ""))
    pred = normalize_text(row.get("model_output", ""))
    status = (row.get("read_status", "") or "").strip().lower()
    cer = compute_cer(gt, pred)
    exact = gt == pred
    clear = status == "clear"
    evidence = (row.get("evidence_located", "") or "").strip().lower()
    unsupported = (row.get("unsupported_text", "") or "").strip().lower()
    category = (row.get("error_category", "") or "").strip().lower()
    reviewed = evidence in ("yes", "no") and unsupported in ("yes", "no") and category not in UNREVIEWED_CATEGORIES
    return {
        "field": (row.get("field", "") or "").strip(),
        "sku": (row.get("sku_id", "") or "").strip(),
        "image": (row.get("image_id", "") or "").strip(),
        "brand": (row.get("brand", "") or "").strip(),
        "script": (row.get("package_language_script", "") or "").strip() or "unspecified",
        "condition": (row.get("photo_condition", "") or "").strip() or "unspecified",
        "status": status,
        "cer": cer,
        "exact": exact,
        "clear": clear,
        "wrong_clear": clear and not exact,
        "wrong_clear_cer": clear and cer > CER_THRESHOLD,
        "clear_number_mismatch": clear and not numbers_match(gt, pred),
        "not_visible_miss": status == "not_visible" and bool(gt),
        "hallucinated_absent": (not gt) and bool(pred) and status != "not_visible",
        "reviewed": reviewed,
        "evidence_located": is_truthy(row.get("evidence_located", "")),
        "unsupported": is_truthy(row.get("unsupported_text", "")),
        "review_seconds": _to_float(row.get("review_seconds", "")),
    }


def _to_float(value: Optional[str]) -> Optional[float]:
    try:
        return float(value) if value not in (None, "") else None
    except ValueError:
        return None


def cluster_bootstrap_rate(groups: Dict[str, Tuple[int, int]], iterations: int = 2000,
                           seed: int = 1, min_groups: int = 5) -> Optional[Tuple[float, float]]:
    """
    95% percentile interval for sum(successes)/sum(totals), resampling whole SKUs.
    groups maps sku -> (successes, total). Returns None with too few SKUs to say anything.
    """
    usable = [v for v in groups.values() if v[1] > 0]
    if len(usable) < min_groups:
        return None
    rng = random.Random(seed)
    rates = []
    for _ in range(iterations):
        draw = [usable[rng.randrange(len(usable))] for _ in usable]
        total = sum(t for _, t in draw)
        if total:
            rates.append(sum(s for s, _ in draw) / total)
    if not rates:
        return None
    rates.sort()
    return (rates[int(0.025 * (len(rates) - 1))], rates[int(math.ceil(0.975 * (len(rates) - 1)))])


def _ci(successes: int, total: int) -> Optional[List[float]]:
    interval = wilson_interval(successes, total)
    return [round(interval[0], 4), round(interval[1], 4)] if interval else None


def summarize(rows: List[Dict[str, str]], pending_excluded: int = 0, min_rows: int = 10,
              min_skus: int = 5, bootstrap_iterations: int = 2000, seed: int = 1) -> Dict[str, Any]:
    items = [classify_row(r) for r in rows]
    skus = {i["sku"] for i in items if i["sku"]}
    result: Dict[str, Any] = {
        "scored_rows": len(items),
        "unique_skus": len(skus),
        "unique_images": len({i["image"] for i in items if i["image"]}),
        "pending_rows_excluded": pending_excluded,
        "thresholds": {"min_rows_per_stratum": min_rows, "min_skus_per_stratum": min_skus, "cer_threshold": CER_THRESHOLD},
        "warnings": [],
    }
    if not items:
        result["warnings"].append("No completed model-output/reference pairs to score.")
        return result

    by_field: Dict[str, Any] = {}
    grouped = defaultdict(list)
    for item in items:
        grouped[item["field"]].append(item)
    for field, group in sorted(grouped.items()):
        n = len(group)
        clear = [g for g in group if g["clear"]]
        exact_k = sum(g["exact"] for g in group)
        by_field[field] = {
            "rows": n,
            "skus": len({g["sku"] for g in group}),
            "exact": exact_k,
            "exact_ci95": _ci(exact_k, n),
            "mean_cer": round(sum(g["cer"] for g in group) / n, 3),
            "readable_rows": len(clear),
            "readable_but_wrong": sum(g["wrong_clear"] for g in clear),
            "readable_but_wrong_ci95": _ci(sum(g["wrong_clear"] for g in clear), len(clear)),
            "readable_but_cer_over_threshold": sum(g["wrong_clear_cer"] for g in clear),
            "readable_with_number_mismatch": sum(g["clear_number_mismatch"] for g in clear),
            "not_visible_but_present": sum(g["not_visible_miss"] for g in group),
            "hallucinated_when_absent": sum(g["hallucinated_absent"] for g in group),
        }
    result["by_field"] = by_field

    clear_all = [i for i in items if i["clear"]]
    wrong_k = sum(i["wrong_clear"] for i in clear_all)
    per_sku: Dict[str, Tuple[int, int]] = {}
    for sku in skus:
        sku_clear = [i for i in clear_all if i["sku"] == sku]
        per_sku[sku] = (sum(i["wrong_clear"] for i in sku_clear), len(sku_clear))
    cluster = cluster_bootstrap_rate(per_sku, bootstrap_iterations, seed)
    result["readable_overall"] = {
        "readable_rows": len(clear_all),
        "wrong": wrong_k,
        "rate": round(wrong_k / len(clear_all), 4) if clear_all else None,
        "row_level_wilson_ci95": _ci(wrong_k, len(clear_all)),
        "sku_cluster_bootstrap_ci95": [round(cluster[0], 4), round(cluster[1], 4)] if cluster else None,
        "number_mismatches": sum(i["clear_number_mismatch"] for i in clear_all),
    }
    if len(skus) < min_skus:
        result["warnings"].append(
            f"Only {len(skus)} SKU(s) scored (fewer than {min_skus}): no SKU-level interval is reported and every figure is anecdotal.")

    def strata(key: str) -> Dict[str, Any]:
        groups = defaultdict(list)
        for item in items:
            groups[item[key]].append(item)
        out = {}
        for name, group in sorted(groups.items()):
            n, group_skus = len(group), len({g["sku"] for g in group})
            if n < min_rows or group_skus < min_skus:
                out[name] = {"rows": n, "skus": group_skus, "suppressed": True}
            else:
                k = sum(g["exact"] for g in group)
                out[name] = {"rows": n, "skus": group_skus, "suppressed": False, "exact": k,
                             "exact_ci95": _ci(k, n), "mean_cer": round(sum(g["cer"] for g in group) / n, 3)}
        return out

    result["by_script"] = strata("script")
    result["by_condition"] = strata("condition")

    sku_attr = {}
    for item in items:
        sku_attr.setdefault(item["sku"], item)
    brand_counts = defaultdict(int)
    script_counts = defaultdict(int)
    condition_counts = defaultdict(int)
    for item in sku_attr.values():
        brand_counts[item["brand"] or "unspecified"] += 1
        script_counts[item["script"]] += 1
        condition_counts[item["condition"]] += 1
    top_brand_share = max(brand_counts.values()) / len(sku_attr) if sku_attr else 0
    result["coverage"] = {
        "skus_by_script": dict(sorted(script_counts.items())),
        "skus_by_condition": dict(sorted(condition_counts.items())),
        "brands": len(brand_counts),
        "top_brand_share": round(top_brand_share, 3),
    }
    if len(script_counts) == 1:
        result["warnings"].append("Only one script/language is represented; do not generalize to other scripts.")
    if len(sku_attr) >= 5 and top_brand_share > 0.4:
        result["warnings"].append(f"One brand makes up {top_brand_share:.0%} of SKUs; the sample is concentrated.")

    reviewed = sum(i["reviewed"] for i in items)
    review = {"rows": len(items), "reviewer_complete": reviewed, "reviewer_pending": len(items) - reviewed}
    if reviewed == len(items):
        located = sum(i["evidence_located"] for i in items)
        review["snippet_located"] = located
        review["snippet_located_ci95"] = _ci(located, len(items))
        review["unsupported_text_rows"] = sum(i["unsupported"] for i in items)
    else:
        review["note"] = ("Snippet-support and unsupported-text metrics are not reported: reviewer columns "
                          "are blank or unreviewed on some rows. Blank does not mean 'no'.")
        result["warnings"].append(f"{len(items) - reviewed} of {len(items)} scored rows still need reviewer columns filled.")
    seconds = [i["review_seconds"] for i in items if i["review_seconds"] is not None]
    review["review_seconds_measured"] = len(seconds)
    if seconds:
        review["review_seconds_median"] = statistics.median(seconds)
    result["review"] = review
    return result


def evaluate_csv(csv_path: str, **kwargs) -> Dict[str, Any]:
    evaluator = BenchmarkEvaluator(csv_path)
    return summarize(evaluator.rows, pending_excluded=evaluator.pending_rows_count, **kwargs)


def _pct(value: Optional[float]) -> str:
    return "n/a" if value is None else f"{value * 100:.1f}%"


def _interval(ci: Optional[List[float]]) -> str:
    return "n/a" if not ci else f"{ci[0] * 100:.0f}–{ci[1] * 100:.0f}%"


def format_markdown(summary: Dict[str, Any]) -> str:
    lines = ["# Benchmark scorecard with uncertainty", ""]
    lines.append(f"Scored rows: **{summary['scored_rows']}** across **{summary.get('unique_skus', 0)}** SKUs "
                 f"({summary.get('unique_images', 0)} images). Pending rows excluded: {summary['pending_rows_excluded']}.")
    lines.append("")
    if not summary["scored_rows"]:
        lines.extend(summary["warnings"] or ["Nothing to score."])
        return "\n".join(lines) + "\n"
    if summary["warnings"]:
        lines.append("**Read this first**")
        lines.extend(f"- {w}" for w in summary["warnings"])
        lines.append("")

    ro = summary["readable_overall"]
    lines.append("## When the tool says “Readable”, how often is it wrong?")
    lines.append("")
    lines.append(f"{ro['wrong']} of {ro['readable_rows']} fields marked Readable did not exactly match the reference "
                 f"({_pct(ro['rate'])}). Row-level 95% interval: {_interval(ro['row_level_wilson_ci95'])}. "
                 f"SKU-clustered 95% interval: {_interval(ro['sku_cluster_bootstrap_ci95'])}. "
                 f"Readable fields with a number that differs from the pack: {ro['number_mismatches']}.")
    lines.append("")
    lines.append("The SKU-clustered interval is the honest one: fields from the same pack are not independent. "
                 "It is blank when there are too few SKUs.")
    lines.append("")

    lines.append("## By field")
    lines.append("")
    lines.append("| Field | Rows | Exact match (95% interval) | Mean CER | Readable | Readable but wrong | Readable, number differs | Not visible but present | Invented when absent |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for field, d in summary["by_field"].items():
        lines.append(f"| {field} | {d['rows']} | {d['exact']}/{d['rows']} ({_interval(d['exact_ci95'])}) | {d['mean_cer']:.3f} | "
                     f"{d['readable_rows']} | {d['readable_but_wrong']} | {d['readable_with_number_mismatch']} | "
                     f"{d['not_visible_but_present']} | {d['hallucinated_when_absent']} |")
    lines.append("")

    for title, key in (("By script / language", "by_script"), ("By photo condition", "by_condition")):
        lines.append(f"## {title}")
        lines.append("")
        lines.append("| Group | Rows | SKUs | Exact match (95% interval) | Mean CER |")
        lines.append("| --- | --- | --- | --- | --- |")
        for name, d in summary[key].items():
            if d["suppressed"]:
                lines.append(f"| {name} | {d['rows']} | {d['skus']} | too few to report | too few to report |")
            else:
                lines.append(f"| {name} | {d['rows']} | {d['skus']} | {d['exact']}/{d['rows']} ({_interval(d['exact_ci95'])}) | {d['mean_cer']:.3f} |")
        lines.append("")

    cov = summary["coverage"]
    lines.append("## Sample coverage")
    lines.append("")
    lines.append(f"Brands: {cov['brands']} (largest brand: {cov['top_brand_share']:.0%} of SKUs). "
                 f"SKUs by script: {cov['skus_by_script']}. SKUs by photo condition: {cov['skus_by_condition']}.")
    lines.append("")

    rv = summary["review"]
    lines.append("## Reviewer-dependent metrics")
    lines.append("")
    lines.append(f"Reviewer columns complete on {rv['reviewer_complete']} of {rv['rows']} rows.")
    if "snippet_located" in rv:
        lines.append(f"Snippet located on the photo: {rv['snippet_located']}/{rv['rows']} ({_interval(rv['snippet_located_ci95'])}). "
                     f"Rows with unsupported text: {rv['unsupported_text_rows']}.")
    else:
        lines.append(rv["note"])
    if rv["review_seconds_measured"]:
        lines.append(f"Median review time over {rv['review_seconds_measured']} measured rows: {rv['review_seconds_median']} s.")
    else:
        lines.append("Review time was not measured.")
    lines.append("")
    lines.append("## Limits")
    lines.append("")
    lines.append("- Exact match means whitespace-normalized equality with the adjudicated reference text.")
    lines.append("- Intervals describe sampling uncertainty only. A convenience sample of packs does not support claims about all products.")
    lines.append("- Not a clinical, regulatory, or safety validation, and not evidence about caregiver outcomes.")
    return "\n".join(lines) + "\n"
