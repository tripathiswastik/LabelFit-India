import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from labelfit.extractor import GeminiLabelExtractor  # noqa: E402

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "test", "fixtures", "guard_cases.json")
with open(FIXTURE, "r", encoding="utf-8") as f:
    CASES = json.load(f)["cases"]


# The same cases run against the Node guards in test/guard_parity.test.js.
@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_guard_parity_python(case):
    raw = {case["field"]: {"value": case["value"], "evidence": case["evidence"], "readStatus": case["readStatus"]}}
    result = GeminiLabelExtractor()._normalize(raw)
    assert result[case["field"]].read_status == case["expected"]


def test_cases_cover_every_field_and_outcome():
    assert len(CASES) >= 30
    assert {c["expected"] for c in CASES} == {"clear", "not_visible", "uncertain"}
