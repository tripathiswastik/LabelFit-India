import pytest

from labelfit.extractor import GeminiLabelExtractor
from labelfit.models import FIELD_NAMES
from labelfit.samples import SAMPLE_CEREAL_6M, SAMPLE_PUREE_GAP_CASE


def test_offline_extractor_returns_six_fields_and_no_inferred_age_or_allergen():
    fields = GeminiLabelExtractor(api_key="").extract_from_text(SAMPLE_CEREAL_6M)

    assert set(fields) == set(FIELD_NAMES)
    assert fields["ageMarking"].value == "Age marking: 6+ months"
    assert fields["allergenDeclaration"].value == "Allergen declaration: Contains milk."
    assert fields["preparationAndStorage"].value.startswith("Preparation and storage:")


def test_missing_declaration_stays_not_visible_even_when_ingredient_contains_milk():
    fields = GeminiLabelExtractor(api_key="").extract_from_text(SAMPLE_PUREE_GAP_CASE)
    assert fields["allergenDeclaration"].value == ""
    assert fields["allergenDeclaration"].read_status == "not_visible"


def test_text_length_is_bounded_before_model_request():
    with pytest.raises(ValueError, match="too long"):
        GeminiLabelExtractor(api_key="").extract_from_text("x" * 30_001)


def test_schema_ignores_extra_model_fields_and_downgrades_missing_evidence():
    fields = GeminiLabelExtractor(api_key="")._normalize({
        "productName": {"value": "Example", "evidence": "", "readStatus": "clear"},
        "notes": ["extra model text"],
    })
    assert fields["productName"].read_status == "uncertain"
    assert "notes" not in fields


def test_gemini_is_not_enabled_implicitly_from_environment(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    assert GeminiLabelExtractor().api_key == ""


def test_step3_unsupported_clear_read_downgraded_to_uncertain():
    extractor = GeminiLabelExtractor()
    fields = extractor._normalize({
        "productName": {
            "value": "LittleNourish Fruit Puree",
            "evidence": "Manufactured in Pune Maharashtra",
            "readStatus": "clear",
        }
    })
    assert fields["productName"].read_status == "uncertain"


def test_step3_conflicting_numerals_in_age_marking_downgraded():
    extractor = GeminiLabelExtractor()
    fields = extractor._normalize({
        "ageMarking": {
            "value": "From 1 Month",
            "evidence": "Stage 1: From 6 to 24 Months",
            "readStatus": "clear",
        }
    })
    assert fields["ageMarking"].read_status == "uncertain"


def test_step3_truncated_ingredients_downgraded_to_uncertain():
    extractor = GeminiLabelExtractor()
    fields = extractor._normalize({
        "ingredients": {
            "value": "Organic rice flour, sprouted dal flour, milk solids,",
            "evidence": "Ingredients: Organic rice flour, sprouted dal flour, milk solids,",
            "readStatus": "clear",
        }
    })
    assert fields["ingredients"].read_status == "uncertain"


def test_step3_allergen_inferred_from_ingredients_downgraded():
    extractor = GeminiLabelExtractor()
    inferred = extractor._normalize({
        "allergenDeclaration": {
            "value": "Contains Milk",
            "evidence": "Ingredients: Skimmed milk solids (15%), Rice flour",
            "readStatus": "clear",
        }
    })
    assert inferred["allergenDeclaration"].read_status == "uncertain"

    explicit = extractor._normalize({
        "allergenDeclaration": {
            "value": "Contains Milk",
            "evidence": "Allergen Declaration: Contains Milk.",
            "readStatus": "clear",
        }
    })
    assert explicit["allergenDeclaration"].read_status == "clear"
