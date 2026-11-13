"""
Tests for domain models in labelfit.models.
"""

from labelfit.models import (
    ExtractedField,
    AllergenInfo,
    AgeSuitabilityInfo,
    PreparationInfo,
    VerificationFlag,
    LabelInspectionReport
)


def test_extracted_field_serialization():
    field = ExtractedField(
        field_name="ingredients",
        extracted_value="Organic Rice Flour",
        source_snippet="Ingredients: Organic Rice Flour",
        confidence=0.95,
        status="verified"
    )
    d = field.to_dict()
    assert d["field_name"] == "ingredients"
    assert d["confidence"] == 0.95
    assert d["status"] == "verified"


def test_inspection_report_contains_non_prescriptive_disclaimer():
    report = LabelInspectionReport(
        product_name="Sample Infant Cereal",
        product_identifier="sample_sku_01",
        inspected_at="2026-11-13T12:00:00Z",
        raw_ocr_text="Sample raw packaging text",
        age_suitability=AgeSuitabilityInfo(stated_age="From 6 Months", meets_6_months_scope=True),
        ingredients=ExtractedField(field_name="ingredients", status="verified"),
        allergens=AllergenInfo(is_declared_on_label=True),
        preparation=PreparationInfo(water_boiling_specified=True)
    )
    # Enforce non-prescriptive invariant
    assert "not assess nutritional safety" in report.disclaimer
    assert "feeding instructions" in report.disclaimer
    assert not hasattr(report, "safety_score")
    assert not hasattr(report, "health_verdict")
