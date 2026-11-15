"""
Unit tests for the Founder Transcription Adjudication Engine (labelfit.adjudication).
"""

import sys
import os
import tempfile
import csv
from pathlib import Path
import pytest

_SRC_ROOT = str(Path(__file__).resolve().parent.parent / "src")
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.adjudication import (
    DualTranscriptionRecord,
    AdjudicationEngine,
    normalize_text,
)


def test_normalize_text():
    assert normalize_text("  Stage 1:   From 6 Months ") == "Stage 1: From 6 Months"
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_dual_transcription_concurrence():
    rec = DualTranscriptionRecord(
        sku_id="SKU-01",
        brand="BrandX",
        product_name="Cereal",
        field="ageMarking",
        swastik_transcription="From 6 Months",
        swastik_date="2026-11-15",
        saumya_transcription="From 6 Months",
        saumya_date="2026-11-15",
    )
    assert rec.is_concurrence is True
    assert rec.has_discrepancy is False
    assert rec.is_adjudicated is True
    assert rec.get_ground_truth() == "From 6 Months"


def test_dual_transcription_discrepancy_and_adjudication():
    # Discrepancy without adjudication raises ValueError
    rec = DualTranscriptionRecord(
        sku_id="SKU-01",
        brand="BrandX",
        product_name="Cereal",
        field="ingredients",
        swastik_transcription="Wheat flour (55%), Milk solids (15%)",
        swastik_date="2026-11-15",
        saumya_transcription="Wheat flour (55%), Milk solids",
        saumya_date="2026-11-15",
    )
    assert rec.is_concurrence is False
    assert rec.has_discrepancy is True
    assert rec.is_adjudicated is False
    with pytest.raises(ValueError, match="Unresolved transcription discrepancy"):
        rec.get_ground_truth()

    # Once adjudicated against physical package, returns verified ground truth
    rec.adjudicated_ground_truth = "Wheat flour (55%), Milk solids (15%)"
    rec.adjudication_notes = "Physical packaging inspected: (15%) is printed on package."
    assert rec.is_adjudicated is True
    assert rec.get_ground_truth() == "Wheat flour (55%), Milk solids (15%)"


def test_adjudication_engine_metrics():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".csv", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "sku_id", "brand", "product_name", "field",
            "swastik_transcription", "swastik_date",
            "saumya_transcription", "saumya_date",
            "adjudicated_ground_truth", "adjudication_notes"
        ])
        # Record 1: Concurrence
        writer.writerow([
            "SKU-01", "BrandA", "Cereal", "productName",
            "Organic Rice Cereal", "2026-11-15",
            "Organic Rice Cereal", "2026-11-15",
            "", ""
        ])
        # Record 2: Discrepancy, resolved
        writer.writerow([
            "SKU-01", "BrandA", "Cereal", "ingredients",
            "Rice flour (80%), Milk", "2026-11-15",
            "Rice flour (80%), Milk solids", "2026-11-15",
            "Rice flour (80%), Milk solids", "Rechecked tin"
        ])
        # Record 3: Discrepancy, unresolved
        writer.writerow([
            "SKU-01", "BrandA", "Cereal", "allergenDeclaration",
            "Contains Milk", "2026-11-15",
            "Contains Dairy", "2026-11-15",
            "", ""
        ])
        temp_csv = f.name

    try:
        engine = AdjudicationEngine(temp_csv)
        records = engine.load()
        assert len(records) == 3

        results = engine.evaluate()
        assert results["total_records"] == 3
        assert results["concurrence_count"] == 1
        assert results["concurrence_rate"] == 33.3
        assert results["discrepancy_count"] == 2
        assert results["unresolved_count"] == 1
        assert results["all_adjudicated"] is False

        report = engine.format_markdown_report(results)
        assert "UNRESOLVED DISCREPANCIES" in report
        assert "SKU-01" in report
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)
