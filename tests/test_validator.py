"""
Unit and integration tests for DeterministicValidator.
Tests rule engine, evidence grounding, allergen matching, and non-prescriptive invariants.
"""

from labelfit.models import (
    AgeSuitabilityInfo,
    ExtractedField,
    AllergenInfo,
    PreparationInfo
)
from labelfit.validator import DeterministicValidator
from labelfit.samples import SAMPLE_CEREAL_6M, SAMPLE_PUREE_GAP_CASE, SAMPLE_INFANT_FORMULA_OUT_OF_SCOPE


def test_validator_cereal_complete_case():
    validator = DeterministicValidator()
    age_info = AgeSuitabilityInfo(
        stated_age="Stage 1: From 6 to 24 Months",
        source_snippet="Stage 1: From 6 to 24 Months",
        confidence=0.95
    )
    ingredients = ExtractedField(
        field_name="ingredients",
        extracted_value="Organic Rice Flour (55%), Sprouted Green Moong Dal Flour (25%), Milk Solids (15%)",
        source_snippet="Ingredients: Organic Rice Flour (55%), Sprouted Green Moong Dal Flour (25%)",
        confidence=0.95
    )
    allergens = AllergenInfo(
        declared_allergens=["Milk"],
        precautionary_allergens=["May contain traces of soy and gluten."],
        source_snippet="Allergen Information: Contains Milk.",
        is_declared_on_label=True,
        confidence=0.92
    )
    preparation = PreparationInfo(
        steps=["Wash hands", "Boil clean drinking water for 5 minutes", "Pour 75ml", "Add 3 scoops", "Stir"],
        water_boiling_specified=True,
        source_snippet="Boil clean drinking water for 5 minutes and allow it to cool to lukewarm.",
        confidence=0.90
    )

    report = validator.inspect_and_generate_report(
        product_name="LittleNourish Cereal",
        product_identifier="sample_cereal_6m",
        raw_text=SAMPLE_CEREAL_6M,
        age_info=age_info,
        ingredients=ingredients,
        allergens=allergens,
        preparation=preparation
    )

    assert report.completeness_score == 1.0
    assert report.age_suitability.meets_6_months_scope is True
    assert report.preparation.water_boiling_specified is True

    # Check that verified flags were raised
    verified_flags = [f for f in report.flags if f.flag_type == "verified"]
    assert len(verified_flags) >= 3


def test_validator_flags_unverified_source_snippet():
    validator = DeterministicValidator()
    # Snippet that does not exist in raw packaging text
    fake_snippet = "Completely hallucinated text from non-existent panel"

    age_info = AgeSuitabilityInfo(
        stated_age="From 6 Months",
        source_snippet=fake_snippet,
        confidence=0.95
    )
    _, flags = validator.validate_age_marking(age_info, SAMPLE_CEREAL_6M)
    uncertainty_flags = [f for f in flags if f.flag_type == "uncertainty"]
    assert len(uncertainty_flags) == 1
    assert "could not be verified" in uncertainty_flags[0].message


def test_validator_under_6_months_formula_flagged_out_of_scope():
    validator = DeterministicValidator()
    age_info = AgeSuitabilityInfo(
        stated_age="Suitable for 0 to 6 months",
        source_snippet="Suitable for 0 to 6 months",
        confidence=0.90
    )
    validated_age, flags = validator.validate_age_marking(age_info, SAMPLE_INFANT_FORMULA_OUT_OF_SCOPE)
    assert validated_age.minimum_months == 0
    assert validated_age.meets_6_months_scope is False
    warning_flags = [f for f in flags if f.flag_type == "warning"]
    assert len(warning_flags) >= 1
    assert "below 6 months" in warning_flags[0].message


def test_validator_missing_allergen_panel_with_allergenic_ingredient():
    validator = DeterministicValidator()
    ingredients = ExtractedField(
        field_name="ingredients",
        extracted_value="Organic wheat flour, skimmed milk solids, sugar",
        source_snippet="Organic wheat flour, skimmed milk solids, sugar"
    )
    # Allergen panel missing
    allergens = AllergenInfo(declared_allergens=[], is_declared_on_label=False)

    _, flags = validator.validate_allergens(allergens, ingredients, "Organic wheat flour, skimmed milk solids, sugar")
    gap_flags = [f for f in flags if f.flag_type == "gap"]
    assert len(gap_flags) >= 1
    assert "wheat" in gap_flags[0].message or "milk" in gap_flags[0].message
