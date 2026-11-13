from labelfit.models import FIELD_NAMES, ExtractedField, LabelInspectionReport


def test_report_serializes_only_fields_and_boundary_notice():
    report = LabelInspectionReport(fields={name: ExtractedField(name) for name in FIELD_NAMES})
    data = report.to_dict()

    assert set(data["fields"]) == set(FIELD_NAMES)
    assert "does not verify the package image" in data["disclaimer"]
    assert "completeness_score" not in data
    assert "safety_score" not in data
