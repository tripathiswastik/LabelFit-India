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
            "clear", "yes", "no", "", "15", "Clean read"
        ])
        # Row 2: Partial mismatch, unsupported hallucinated word
        writer.writerow([
            "IMG_01", "SKU_01", "LittleNourish", "Bengaluru", "English-Latin",
            "clear_flat", "allergenDeclaration", "Contains Milk", "Contains Milk and Peanuts",
            "clear", "yes", "yes", "invented_allergen", "25", "Hallucinated peanuts"
        ])
        # Row 3: Absent field correctly identified as not_visible
        writer.writerow([
            "IMG_02", "SKU_02", "PureBite", "Pune", "Hindi-Devanagari",
            "glare_curved", "preparationAndStorage", "", "",
            "not_visible", "no", "no", "", "8", "No prep text on pouch"
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
        assert age_metrics["evidence_support_pct"] == 100.0
        assert age_metrics["unsupported_text_pct"] == 0.0

        # Check allergenDeclaration (has unsupported text + false clear)
        allergen_metrics = results["by_field"]["allergenDeclaration"]
        assert allergen_metrics["exact_match_pct"] == 0.0
        assert allergen_metrics["unsupported_text_pct"] == 100.0
        assert allergen_metrics["false_clear_count"] == 1

        # Check script breakdown
        assert "English-Latin" in results["by_script"]
        assert "Hindi-Devanagari" in results["by_script"]
        assert results["by_script"]["Hindi-Devanagari"]["exact_match_pct"] == 100.0

    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_50_sku_benchmark_template_integrity():
    """Verifies that docs/benchmark-template.csv contains 50 distinct SKUs with all 6 fields."""
    benchmark_csv = Path(__file__).resolve().parent.parent / "docs" / "benchmark-template.csv"
    assert benchmark_csv.exists(), "benchmark-template.csv should exist"

    evaluator = BenchmarkEvaluator(str(benchmark_csv))
    results = evaluator.evaluate()

    assert results["total_rows"] == 300, "Should contain exactly 300 evaluation rows"
    assert results["unique_skus_count"] == 50, "Should evaluate exactly 50 distinct SKUs"
    assert results["unique_images_count"] == 100, "Should evaluate exactly 100 images (front + info panel)"

    expected_fields = {
        "productName", "ageMarking", "ingredients",
        "allergenDeclaration", "nutritionPanel", "preparationAndStorage"
    }
    assert set(results["by_field"].keys()) == expected_fields
    for field in expected_fields:
        assert results["by_field"][field]["total_rows"] == 50
