"""
Tests for GeminiLabelExtractor offline heuristics and model parsing.
"""

from labelfit.extractor import GeminiLabelExtractor
from labelfit.samples import SAMPLE_CEREAL_6M, SAMPLE_PUREE_GAP_CASE


def test_extractor_offline_cereal_extraction():
    extractor = GeminiLabelExtractor()
    extracted = extractor.extract_from_text(SAMPLE_CEREAL_6M)

    assert "stated_age_marking" in extracted
    assert "ingredients" in extracted
    assert "allergen_declaration" in extracted
    assert "preparation_instructions" in extracted

    age_info, ingredients, allergens, prep = extractor.parse_to_models(extracted)
    assert age_info.stated_age is not None
    assert "months" in age_info.stated_age.lower()
    assert ingredients.extracted_value is not None
    assert "rice flour" in ingredients.extracted_value.lower()
    assert len(prep.steps) >= 3


def test_extractor_offline_puree_gap_detection():
    extractor = GeminiLabelExtractor()
    extracted = extractor.extract_from_text(SAMPLE_PUREE_GAP_CASE)

    age_info, ingredients, allergens, prep = extractor.parse_to_models(extracted)
    assert age_info.stated_age is not None
    assert "6" in age_info.stated_age
    assert ingredients.extracted_value is not None
    # Puree has no preparation steps
    assert len(prep.steps) == 0
