from labelfit.extractor import GeminiLabelExtractor
from labelfit.samples import SAMPLE_CEREAL_6M
from labelfit.validator import DeterministicValidator


def test_offline_fields_are_literal_text_candidates():
    extractor = GeminiLabelExtractor(api_key="")
    fields = extractor.extract_from_text(SAMPLE_CEREAL_6M)
    report = DeterministicValidator().inspect(SAMPLE_CEREAL_6M, fields)

    assert report.fields["ageMarking"].value == "Age marking: 6+ months"
    assert report.fields["allergenDeclaration"].value == "Allergen declaration: Contains milk."
    assert report.fields["ingredients"].value == "Ingredients: Rice flour, lentil flour, milk powder."
    assert report.fields["allergenDeclaration"].source_match is True
    assert report.fields["allergenDeclaration"].read_status == "uncertain"


def test_ingredients_do_not_create_an_allergen_declaration():
    text = "Example product\nIngredients: wheat flour, milk powder."
    fields = GeminiLabelExtractor(api_key="").extract_from_text(text)
    report = DeterministicValidator().inspect(text, fields)

    assert report.fields["ingredients"].value == "Ingredients: wheat flour, milk powder."
    assert report.fields["allergenDeclaration"].value == ""
    assert report.fields["allergenDeclaration"].read_status == "not_visible"


def test_unmatched_model_output_is_downgraded():
    extractor = GeminiLabelExtractor(api_key="")
    fields = extractor._normalize({
        "productName": {"value": "invented product", "evidence": "invented product", "readStatus": "clear"}
    })
    report = DeterministicValidator().inspect("real package text", fields)

    assert report.fields["productName"].source_match is False
    assert report.fields["productName"].read_status == "uncertain"
    assert not hasattr(report, "completeness_score")
