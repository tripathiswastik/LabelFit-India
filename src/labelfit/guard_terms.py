"""Shared guard vocabulary and digit handling, loaded from guard_terms.json.

server.js reads the same JSON file, so word lists and numeral systems stay identical
in the Node and Python guards. Behaviour is checked against shared test cases in
test/fixtures/guard_cases.json (see tests/test_guard_parity.py and test/guard_parity.test.js).
"""

import json
from pathlib import Path
from typing import List

_TERMS_PATH = Path(__file__).with_name("guard_terms.json")

with open(_TERMS_PATH, "r", encoding="utf-8") as _f:
    TERMS = json.load(_f)

ALLERGEN_MARKERS_ENGLISH: List[str] = TERMS["allergen_declaration_markers"]["english"]
ALLERGEN_MARKERS_DEVANAGARI: List[str] = TERMS["allergen_declaration_markers"]["devanagari"]
KNOWN_ALLERGENS_ENGLISH: List[str] = TERMS["known_allergens"]["english"]
KNOWN_ALLERGENS_DEVANAGARI: List[str] = TERMS["known_allergens"]["devanagari"]
_DIGIT_ZEROS = [ord(z) for z in TERMS["digit_zeros"]]


def normalize_digits(text: str) -> str:
    """Rewrites Indian-script and Arabic-Indic digits as ASCII 0-9; leaves everything else alone."""
    if not text:
        return ""
    out = []
    for ch in text:
        cp = ord(ch)
        for zero in _DIGIT_ZEROS:
            if zero <= cp <= zero + 9:
                out.append(str(cp - zero))
                break
        else:
            out.append(ch)
    return "".join(out)
