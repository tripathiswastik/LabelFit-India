"""
Unit tests for the Caregiver Usability Evaluation Engine (labelfit.usability).
"""

import sys
from pathlib import Path
import os
import tempfile
import csv
import pytest

# Ensure src is on sys.path for direct pytest execution
_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.usability import (
    is_truthy,
    parse_float,
    UsabilityEvaluator,
)


def test_is_truthy():
    assert is_truthy("true") is True
    assert is_truthy("True") is True
    assert is_truthy("1") is True
    assert is_truthy("yes") is True
    assert is_truthy("YES") is True
    assert is_truthy("y") is True
    assert is_truthy("pass") is True
    assert is_truthy("false") is False
    assert is_truthy("0") is False
    assert is_truthy("no") is False
    assert is_truthy("") is False
    assert is_truthy(None) is False


def test_parse_float():
    assert parse_float("12.5") == 12.5
    assert parse_float(" 42 ") == 42.0
    assert parse_float("invalid", default=5.0) == 5.0
    assert parse_float("", default=0.0) == 0.0
    assert parse_float(None, default=0.0) == 0.0


def test_usability_evaluator_metrics():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "session_id", "caregiver_id", "sku_id", "task_type",
            "time_without_tool_sec", "time_with_tool_sec",
            "accuracy_check", "understood_read_status",
            "relied_on_physical_pack", "misinterpreted_as_safety_score", "feedback_notes"
        ])
        # Row 1: 50s down to 20s (60% reduction), accurate, understood, relied
        writer.writerow([
            "S1", "CG1", "SKU1", "age_marking",
            "50.0", "20.0", "true", "true", "true", "false", "Fast lookup"
        ])
        # Row 2: 40s down to 20s (50% reduction), accurate, understood, relied
        writer.writerow([
            "S2", "CG2", "SKU1", "allergen_declaration",
            "40.0", "20.0", "true", "true", "true", "false", "Good snippet"
        ])
        temp_csv = f.name

    try:
        evaluator = UsabilityEvaluator(temp_csv)
        results = evaluator.evaluate()

        assert results["total_trials"] == 2
        assert results["unique_caregivers"] == 2
        assert results["mean_time_without_sec"] == 45.0
        assert results["mean_time_with_sec"] == 20.0
        # Aggregate reduction: (90 - 40) / 90 * 100 = 55.6%
        assert results["time_reduction_pct"] == pytest.approx(55.6, 0.1)
        assert results["accuracy_check_rate"] == 1.0
        assert results["status_comprehension_rate"] == 1.0
        assert results["physical_verification_rate"] == 1.0
        assert results["safety_misinterpretation_count"] == 0
        assert results["safety_gate_passed"] is True

        # Check by_task breakdown
        assert "age_marking" in results["by_task"]
        assert "allergen_declaration" in results["by_task"]
        assert results["by_task"]["age_marking"]["trials"] == 1
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_safety_gate_failure_on_misinterpretation():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "session_id", "caregiver_id", "sku_id", "task_type",
            "time_without_tool_sec", "time_with_tool_sec",
            "accuracy_check", "understood_read_status",
            "relied_on_physical_pack", "misinterpreted_as_safety_score", "feedback_notes"
        ])
        writer.writerow([
            "S1", "CG1", "SKU1", "age_marking",
            "30.0", "15.0", "true", "false", "true", "true", "Thought it was a medical clearance"
        ])
        temp_csv = f.name

    try:
        evaluator = UsabilityEvaluator(temp_csv)
        results = evaluator.evaluate()

        assert results["safety_misinterpretation_count"] == 1
        assert results["safety_misinterpretation_rate"] == 1.0
        assert results["safety_gate_passed"] is False
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        UsabilityEvaluator("non_existent_file.csv")


def test_missing_columns_raises_error():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["session_id", "caregiver_id"])  # missing other columns
        writer.writerow(["S1", "CG1"])
        temp_csv = f.name

    try:
        with pytest.raises(ValueError, match="missing required columns"):
            UsabilityEvaluator(temp_csv)
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_empty_dataset_handling():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "session_id", "caregiver_id", "sku_id", "task_type",
            "time_without_tool_sec", "time_with_tool_sec",
            "accuracy_check", "understood_read_status",
            "relied_on_physical_pack", "misinterpreted_as_safety_score", "feedback_notes"
        ])
        temp_csv = f.name

    try:
        evaluator = UsabilityEvaluator(temp_csv)
        results = evaluator.evaluate()
        assert results["total_trials"] == 0
        assert results["safety_gate_passed"] is None
        assert results["time_reduction_pct"] == 0.0
        assert "NOT EVALUATED" in evaluator.format_markdown_report(results)
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_format_markdown_report():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "session_id", "caregiver_id", "sku_id", "task_type",
            "time_without_tool_sec", "time_with_tool_sec",
            "accuracy_check", "understood_read_status",
            "relied_on_physical_pack", "misinterpreted_as_safety_score", "feedback_notes"
        ])
        writer.writerow([
            "S1", "CG1", "SKU1", "age_marking",
            "40.0", "15.0", "true", "true", "true", "false", "Clear read"
        ])
        temp_csv = f.name

    try:
        evaluator = UsabilityEvaluator(temp_csv)
        results = evaluator.evaluate()
        report = evaluator.format_markdown_report(results)
        assert "# LabelFit India: Caregiver Usability Evaluation Report" in report
        assert "PASSED" in report
        assert "`age_marking`" in report
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_caregiver_usability_study_dataset_integrity():
    """Verifies that docs/usability-evaluation-sheet.csv exists with valid protocol columns."""
    usability_csv = Path(__file__).resolve().parent.parent / "docs" / "usability-evaluation-sheet.csv"
    assert usability_csv.exists(), "usability-evaluation-sheet.csv must exist"

    import csv
    with open(usability_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)

    expected_headers = [
        "session_id", "caregiver_id", "sku_id", "task_type",
        "time_without_tool_sec", "time_with_tool_sec",
        "accuracy_check", "understood_read_status",
        "relied_on_physical_pack", "misinterpreted_as_safety_score",
        "feedback_notes"
    ]
    assert header == expected_headers, f"Header mismatch: {header} vs {expected_headers}"

    evaluator = UsabilityEvaluator(str(usability_csv))
    results = evaluator.evaluate()
    assert results is not None
    # When populated with consented live sessions, verify protocol safety gates
    if results["total_trials"] > 0:
        assert results["safety_misinterpretation_count"] == 0, "Safety gate strictly requires 0 misinterpretations"
        assert results["safety_gate_passed"] is True, "Safety gate must pass"
        assert results["time_reduction_pct"] >= 30.0, "Time reduction must meet or exceed 30% protocol target"
        assert results["status_comprehension_rate"] >= 0.85, "Read status comprehension must be >= 85%"
        assert results["physical_verification_rate"] >= 0.90, "Physical pack verification must be >= 90%"
