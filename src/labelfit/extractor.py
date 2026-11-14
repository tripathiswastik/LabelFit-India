"""Experimental text-only extractor. The Node app remains the photo prototype."""

import json
import os
import re
from typing import Dict, Optional

import requests  # type: ignore

from labelfit.models import FIELD_NAMES, ExtractedField, LabelInspectionReport
from labelfit.prompts import (
    GEMINI_EXTRACTION_SYSTEM_PROMPT,
    GEMINI_JSON_SCHEMA_INSTRUCTION,
    response_schema,
)


MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
MAX_TEXT_CHARS = 30_000
MAX_FIELD_CHARS = 8_000
VALID_STATUSES = {"clear", "uncertain", "not_visible"}


ALLERGEN_DECLARATION_PATTERN = re.compile(
    r'\b(contains?|allergen|allergens?|may\s+contain|traces?|free\s+from|facility|equipment)\b',
    re.IGNORECASE
)
TRUNCATION_SUFFIX_PATTERN = re.compile(r'(?:,|\.\.\.|…|—|-|;|&|\band\b)\s*$', re.IGNORECASE)
CALORIC_OR_GUIDELINE_PATTERN = re.compile(
    r'(?:guideline\s*daily\s*amounts?|gda|rda|kcal|calorie|कैलोरी|energy\s*requirement|daily\s*allowance|adult\s*diet|\b(?:[4-9]|\d{2,})\s*years?\s*old\b)',
    re.IGNORECASE
)


def is_caloric_or_guideline_footnote(value: str, evidence: str) -> bool:
    return bool(
        CALORIC_OR_GUIDELINE_PATTERN.search(value)
        or CALORIC_OR_GUIDELINE_PATTERN.search(evidence)
    )
STOP_WORDS = {'the', 'and', 'for', 'with', 'from', 'this', 'that', 'per', 'net', 'pkg'}

DEVANAGARI_DIGITS = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
}

KNOWN_ALLERGENS = [
    'wheat', 'milk', 'dairy', 'soy', 'soya', 'peanut', 'peanuts',
    'almond', 'almonds', 'cashew', 'cashews', 'walnut', 'walnuts',
    'sesame', 'egg', 'eggs', 'fish', 'gluten', 'oat', 'oats', 'barley'
]


def normalize_digits(text: str) -> str:
    if not text:
        return ""
    for dev, asc in DEVANAGARI_DIGITS.items():
        text = text.replace(dev, asc)
    return text


def extract_numeric_tokens(text: str) -> list:
    if not text:
        return []
    normalized = normalize_digits(text)
    return re.findall(r'\b\d+(?:\.\d+)?\b', normalized)


def has_unbalanced_delimiters(text: str) -> bool:
    if not text:
        return False
    paren = 0
    bracket = 0
    for char in text:
        if char == '(':
            paren += 1
        elif char == ')':
            paren = max(0, paren - 1)
        elif char == '[':
            bracket += 1
        elif char == ']':
            bracket = max(0, bracket - 1)
    return paren > 0 or bracket > 0


def has_hallucinated_allergen(value: str, evidence: str) -> bool:
    if not value or not evidence:
        return False
    val_lower = value.lower()
    ev_lower = evidence.lower()
    for allergen in KNOWN_ALLERGENS:
        pattern = re.compile(rf'\b{allergen}\b', re.IGNORECASE)
        if pattern.search(val_lower) and not pattern.search(ev_lower):
            return True
    return False


def has_impossible_nutrient_value(text: str) -> bool:
    if not text:
        return False
    normalized = normalize_digits(text)
    # Macros over 100g per 100g are physically impossible
    macro_matches = re.finditer(
        r'(?:protein|fat|carbohydrate|sugars?|fibre|fiber|प्रोटीन|वसा|कार्बोहाइड्रेट|प्रथिने)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(?:g|ग्राम|ग्रॅम)',
        normalized,
        re.IGNORECASE
    )
    for m in macro_matches:
        try:
            val = float(m.group(1))
            if val > 100:
                return True
        except ValueError:
            pass

    # Micronutrient: Iron > 30mg/100g in complementary cereal indicates a decimal drop
    iron_matches = re.finditer(
        r'(?:iron|आयरन|लोह)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(?:mg|मिलीग्राम|मि\.?\s*ग्रॅ[म]?|मि\.?\s*ग्रा[म]?)',
        normalized,
        re.IGNORECASE
    )
    for m in iron_matches:
        try:
            val = float(m.group(1))
            if val > 30:
                return True
        except ValueError:
            pass

    return False


def extract_significant_tokens(text: str) -> set:
    if not text:
        return set()
    tokens = re.findall(r'\b\w+\b', text.lower())
    return {t for t in tokens if len(t) >= 2 and t not in STOP_WORDS}


def has_token_support(value: str, evidence: str) -> bool:
    if not value or not evidence:
        return False
    val_tokens = extract_significant_tokens(value)
    ev_tokens = extract_significant_tokens(evidence)
    if not val_tokens or not ev_tokens:
        return True
    return val_tokens.issubset(ev_tokens)


def has_conflicting_numbers(value: str, evidence: str) -> bool:
    val_nums = extract_numeric_tokens(value)
    ev_nums = extract_numeric_tokens(evidence)
    for number in val_nums:
        if number not in ev_nums:
            return True
        ev_nums.remove(number)
    return False


class GeminiLabelExtractor:
    """Extract literal candidate fields from text, offline by default."""

    def __init__(self, api_key: Optional[str] = None, model: str = MODEL):
        # Never infer consent to send data from an environment variable.
        self.api_key = api_key or ""
        self.model = model

    def extract_from_text(self, raw_label_text: str) -> Dict[str, ExtractedField]:
        if not isinstance(raw_label_text, str) or not raw_label_text.strip():
            raise ValueError("Enter package-label text first.")
        if len(raw_label_text) > MAX_TEXT_CHARS:
            raise ValueError("Text is too long for this prototype (maximum 30,000 characters).")

        if self.api_key:
            return self._gemini_extract(raw_label_text)
        return self._offline_extract(raw_label_text)

    def _gemini_extract(self, raw_text: str) -> Dict[str, ExtractedField]:
        request = {
            "model": self.model,
            "store": False,
            "system_instruction": GEMINI_EXTRACTION_SYSTEM_PROMPT,
            "input": [
                {"type": "text", "text": GEMINI_JSON_SCHEMA_INSTRUCTION},
                {"type": "text", "text": "Untrusted package-label text follows:\n" + raw_text},
            ],
            "response_format": {
                "type": "text",
                "mime_type": "application/json",
                "schema": response_schema(),
            },
            "generation_config": {"max_output_tokens": 1800},
        }
        try:
            response = requests.post(
                API_URL,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": self.api_key,
                    "Api-Revision": "2026-05-20",
                },
                json=request,
                timeout=(5, 30),
            )
            response.raise_for_status()
            interaction = response.json()
            output_text = ""
            if interaction.get("status") == "completed":
                for step in reversed(interaction.get("steps", [])):
                    if step.get("type") != "model_output":
                        continue
                    for part in step.get("content", []):
                        if part.get("type") == "text" and isinstance(part.get("text"), str):
                            output_text = part["text"]
                            break
                    if output_text:
                        break
            if not output_text or len(output_text) > 24_000:
                raise ValueError
            return self._normalize(json.loads(output_text))
        except Exception as exc:
            # Avoid echoing request URLs, provider payloads, or user text in the UI.
            raise RuntimeError("Gemini could not return a usable transcription. Check the server and try again.") from exc

    def _offline_extract(self, raw_text: str) -> Dict[str, ExtractedField]:
        """Extract exact line candidates by headings; never infer label meaning."""
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        candidates = {name: "" for name in FIELD_NAMES}
        product_lines = [line for line in lines if not line.lower().startswith("fictional sample")]
        if product_lines:
            candidates["productName"] = product_lines[0]

        keyword_groups = {
            "ageMarking": ("month", "months", "mths", "stage "),
            "ingredients": ("ingredient",),
            "allergenDeclaration": ("allergen", "contains:", "may contain"),
            "nutritionPanel": ("nutrition", "nutritional information"),
            "preparationAndStorage": ("preparation", "directions", "storage", "how to prepare"),
        }
        for line in lines:
            lowered = line.lower()
            for field_name, keywords in keyword_groups.items():
                if field_name == "allergenDeclaration" and lowered.rstrip().endswith(":"):
                    continue
                if not candidates[field_name] and any(word in lowered for word in keywords):
                    candidates[field_name] = line

        result = {}
        for name, value in candidates.items():
            result[name] = ExtractedField(
                field_name=name,
                value=value[:MAX_FIELD_CHARS],
                evidence=value[:300],
                read_status="uncertain" if value else "not_visible",
            )
        return result

    def _normalize(self, raw: object) -> Dict[str, ExtractedField]:
        if not isinstance(raw, dict):
            raise RuntimeError("Gemini returned an unexpected transcription format.")
        result = {}
        for name in FIELD_NAMES:
            item = raw.get(name)
            if not isinstance(item, dict):
                item = {}
            value = item.get("value") if isinstance(item.get("value"), str) else ""
            evidence = item.get("evidence") if isinstance(item.get("evidence"), str) else ""
            status = item.get("readStatus")
            if status not in VALID_STATUSES:
                status = "uncertain"
            value = value.strip()[:MAX_FIELD_CHARS]
            evidence = evidence.strip()[:300]
            if not value and not evidence:
                status = "not_visible"
            elif not value or not evidence or status != "clear":
                status = "uncertain"
            else:
                # Step 3 Guard 1: Unsupported clear read
                if not has_token_support(value, evidence):
                    status = "uncertain"
                # Step 3 Guard 2: Numeral conflict in key fields (ageMarking, preparationAndStorage, nutritionPanel)
                elif name in ("ageMarking", "preparationAndStorage", "nutritionPanel") and has_conflicting_numbers(value, evidence):
                    status = "uncertain"
                # Step 4 Guard: Age marking must not be a nutritional guideline or caloric reference footnote
                elif name == "ageMarking" and is_caloric_or_guideline_footnote(value, evidence):
                    status = "uncertain"
                # Step 3 Guard 3: Ingredient or prep truncation (trailing punctuation or unclosed delimiters)
                elif name in ("ingredients", "preparationAndStorage") and (TRUNCATION_SUFFIX_PATTERN.search(value) or has_unbalanced_delimiters(value)):
                    status = "uncertain"
                # Step 3 Guard 4: Allergen declaration guards (must have marker AND no hallucinated unprinted allergens)
                elif name == "allergenDeclaration" and (not ALLERGEN_DECLARATION_PATTERN.search(evidence) or has_hallucinated_allergen(value, evidence)):
                    status = "uncertain"
                # Step 3 Guard 5: Nutrition plausibility guard (macronutrient >100g, iron >30mg)
                elif name == "nutritionPanel" and has_impossible_nutrient_value(value):
                    status = "uncertain"

            result[name] = ExtractedField(name, value, evidence, status)
        return result

    def parse_to_report(self, raw_extracted: Dict[str, ExtractedField], raw_text: str) -> LabelInspectionReport:
        fields = {}
        normalized_raw = " ".join(raw_text.split()).casefold()
        for name in FIELD_NAMES:
            item = raw_extracted.get(name, ExtractedField(name))
            normalized_value = " ".join(item.value.split()).casefold()
            normalized_evidence = " ".join(item.evidence.split()).casefold()
            match = bool(
                normalized_value
                and normalized_evidence
                and normalized_value in normalized_raw
                and normalized_evidence in normalized_raw
            )
            fields[name] = ExtractedField(
                field_name=name,
                value=item.value,
                evidence=item.evidence,
                read_status=item.read_status if match else ("uncertain" if item.value or item.evidence else "not_visible"),
                source_match=match,
            )
        return LabelInspectionReport(fields=fields)
