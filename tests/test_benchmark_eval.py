"""
Unit tests for the Benchmark Evaluation Engine (labelfit.benchmark).
"""

import sys
from pathlib import Path
import os
import tempfile
import csv

# Ensure src is on sys.path for direct pytest execution
_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.benchmark import (
    normalize_text,
    levenshtein_distance,
    compute_cer,
    BenchmarkEvaluator
)


def test_normalize_text():
    assert normalize_text("  Stage 1:   From 6 Months\n") == "Stage 1: From 6 Months"
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_levenshtein_distance():
    assert levenshtein_distance("kitten", "sitting") == 3
    assert levenshtein_distance("flour", "flour") == 0
    assert levenshtein_distance("", "milk") == 4
    assert levenshtein_distance("milk", "") == 4


def test_compute_cer():
    # Exact match
    assert compute_cer("wheat", "wheat") == 0.0
    # Both empty
    assert compute_cer("", "") == 0.0
    # 1 edit in 5 chars
    assert compute_cer("wheat", "wheet") == 0.2
    # Cap at 1.0
    assert compute_cer("a", "zzzzzzzz") == 1.0


def test_benchmark_evaluator_metrics():
    # Create temporary benchmark CSV
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "image_id", "sku_id", "brand", "market_city", "package_language_script",
            "photo_condition", "field", "ground_truth", "model_output", "read_status",
            "evidence_located", "unsupported_text", "error_category", "review_seconds", "reviewer_notes"
        ])
        # Row 1: Exact match, verified evidence
        writer.writerow([
            "IMG_01", "SKU_01", "LittleNourish", "Bengaluru", "English-Latin",
            "clear_flat", "ageMarking", "Stage 1: From 6 Months", "Stage 1: From 6 Months",
            "clear", "yes", "no", "", "", "Clean read"
        ])
        # Row 2: Partial mismatch, unsupported hallucinated word
        writer.writerow([
            "IMG_01", "SKU_01", "LittleNourish", "Bengaluru", "English-Latin",
            "clear_flat", "allergenDeclaration", "Contains Milk", "Contains Milk and Peanuts",
            "clear", "yes", "yes", "invented_allergen", "", "Hallucinated peanuts"
        ])
        # Row 3: Absent field correctly identified as not_visible
        writer.writerow([
            "IMG_02", "SKU_02", "PureBite", "Pune", "Hindi-Devanagari",
            "glare_curved", "preparationAndStorage", "", "",
            "not_visible", "no", "no", "", "", "No prep text on pouch"
        ])
        temp_csv = f.name

    try:
        evaluator = BenchmarkEvaluator(temp_csv)
        results = evaluator.evaluate()

        assert results["total_rows"] == 3
        assert results["unique_skus_count"] == 2
        assert results["unique_images_count"] == 2

        # Check ageMarking
        age_metrics = results["by_field"]["ageMarking"]
        assert age_metrics["exact_match_pct"] == 100.0
        assert age_metrics["mean_cer"] == 0.0
        assert age_metrics["snippet_present_pct"] == 100.0
        assert age_metrics["worksheet_flagged_pct"] == 0.0

        # Check allergenDeclaration (has unsupported text + false clear)
        allergen_metrics = results["by_field"]["allergenDeclaration"]
        assert allergen_metrics["exact_match_pct"] == 0.0
        assert allergen_metrics["worksheet_flagged_pct"] == 100.0
        assert allergen_metrics["false_clear_count"] == 1

        # Check script breakdown
        assert "English-Latin" in results["by_script"]
        assert "Hindi-Devanagari" in results["by_script"]
        assert results["by_script"]["Hindi-Devanagari"]["exact_match_pct"] == 100.0

    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_pending_scan_rows_are_excluded_from_metrics():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "image_id", "sku_id", "brand", "market_city", "package_language_script",
            "photo_condition", "field", "ground_truth", "model_output", "read_status",
            "evidence_located", "unsupported_text", "error_category", "review_seconds", "reviewer_notes"
        ])
        writer.writerow([
            "IMG_01", "SKU_01", "Manna", "Delhi", "English-Latin",
            "pouch_panel", "ingredients", "Sprouted Ragi (100%)", "",
            "pending_model_scan", "no", "no", "pending_model_scan", "", "Awaiting Gemini output"
        ])
        temp_csv = f.name

    try:
        results = BenchmarkEvaluator(temp_csv).evaluate()
        assert results["total_rows"] == 0
        assert results["pending_rows_count"] == 1
        assert "Pending rows not scored: 1" in BenchmarkEvaluator(temp_csv).format_text_report(results)
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_pending_scan_rows_are_not_scored():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "image_id", "sku_id", "brand", "market_city", "package_language_script",
            "photo_condition", "field", "ground_truth", "model_output", "read_status",
            "evidence_located", "unsupported_text", "error_category", "review_seconds", "reviewer_notes"
        ])
        writer.writerow([
            "IMG_01", "SKU_01", "Manna", "Delhi", "English-Latin",
            "pouch_panel", "ingredients", "Sprouted Ragi (100%)", "",
            "pending_model_scan", "no", "no", "", "", "No Gemini output recorded"
        ])
        temp_csv = f.name

    try:
        results = BenchmarkEvaluator(temp_csv).evaluate()
        assert results["total_rows"] == 0
        assert results["pending_rows_count"] == 1
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_blank_benchmark_template_integrity():
    """Verifies that the reusable benchmark template is blank and has a valid schema."""
    benchmark_csv = Path(__file__).resolve().parent.parent / "docs" / "benchmark-template.csv"
    assert benchmark_csv.exists(), "benchmark-template.csv should exist"

    import csv
    with open(benchmark_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)

    expected_headers = [
        "image_id", "sku_id", "brand", "market_city",
        "package_language_script", "photo_condition", "field",
        "ground_truth", "model_output", "read_status",
        "evidence_located", "unsupported_text", "error_category",
        "review_seconds", "reviewer_notes",
    ]
    assert header == expected_headers, f"Header mismatch: {header} vs {expected_headers}"

    evaluator = BenchmarkEvaluator(str(benchmark_csv))
    results = evaluator.evaluate()
    assert results["total_rows"] == 0


def test_recorded_10_package_benchmark_integrity():
    """Checks that recorded audit rows remain separate from the blank template."""
    benchmark_csv = Path(__file__).resolve().parent.parent / "docs" / "benchmark-10sku-results.csv"
    evaluator = BenchmarkEvaluator(str(benchmark_csv))
    results = evaluator.evaluate()
    assert results["total_rows"] == 60
    assert results["unique_skus_count"] == 10
    expected_fields = {
        "productName", "ageMarking", "ingredients",
        "allergenDeclaration", "nutritionPanel", "preparationAndStorage"
    }
    assert set(results["by_field"].keys()) == expected_fields
    assert all(data["mean_review_seconds"] is None for data in results["by_field"].values())


def test_50sku_status_csv_scores_only_recorded_pairs():
    """Pending scans must be visible in progress counts but absent from score denominators."""
    benchmark_csv = Path(__file__).resolve().parent.parent / "docs" / "benchmark-50sku-results.csv"
    results = BenchmarkEvaluator(str(benchmark_csv)).evaluate()
    assert results["total_rows"] == 12
    assert results["pending_rows_count"] == 42
    assert results["unique_skus_count"] == 3
