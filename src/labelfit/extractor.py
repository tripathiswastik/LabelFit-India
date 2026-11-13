"""
Gemini API extraction client for LabelFit India.
Supports both live Gemini multimodal/text REST API calls and offline mock mode for deterministic development and CI.
"""

import os
import json
import base64
from typing import Dict, Any, Optional
import requests
from labelfit.models import (
    AgeSuitabilityInfo,
    ExtractedField,
    AllergenInfo,
    PreparationInfo
)
from labelfit.prompts import GEMINI_EXTRACTION_SYSTEM_PROMPT, GEMINI_JSON_SCHEMA_INSTRUCTION


class GeminiLabelExtractor:
    """Extracts candidate label fields from package photographs using Gemini API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = model
        self.endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        )

    def extract_from_text(self, raw_label_text: str) -> Dict[str, Any]:
        """
        Extracts structured fields from raw OCR label text.
        Falls back to deterministic offline parsing if no API key is provided.
        """
        if not self.api_key:
            return self._offline_extract(raw_label_text)

        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}

        payload = {
            "system_instruction": {
                "parts": [{"text": GEMINI_EXTRACTION_SYSTEM_PROMPT}]
            },
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{GEMINI_JSON_SCHEMA_INSTRUCTION}\n\nVisible Package Text:\n{raw_label_text}"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.1
            }
        }

        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                params=params,
                json=payload,
                timeout=30
            )
            response.raise_status()
            data = response.json()
            candidate = data.get("candidates", [{}])[0]
            content_text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "{}")
            return json.loads(content_text)
        except Exception as exc:
            # Fallback to offline parsing if network or key issue
            return self._offline_extract(raw_label_text, error_note=str(exc))

    def _offline_extract(self, raw_text: str, error_note: Optional[str] = None) -> Dict[str, Any]:
        """
        Local deterministic extraction for testing, evaluation, and offline workflows.
        Extracts candidate fields using pattern heuristics without network calls.
        """
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        # Heuristic product name (first significant line)
        product_name = lines[0] if lines else "Unknown Baby Food Product"

        # Age search
        stated_age = None
        age_snippet = None
        for line in lines:
            if any(term in line.lower() for term in ["month", "stage 1", "6+", "6m"]):
                stated_age = line
                age_snippet = line
                break

        # Ingredients search
        ingredients_text = None
        ingredients_snippet = None
        for i, line in enumerate(lines):
            if "ingredient" in line.lower():
                parts = line.split(":", 1)
                if len(parts) > 1 and parts[1].strip():
                    ingredients_text = parts[1].strip()
                elif i + 1 < len(lines):
                    ingredients_text = lines[i + 1]
                ingredients_snippet = line if not ingredients_text else f"Ingredients: {ingredients_text}"
                break

        # Allergen search
        declared = []
        precautionary = []
        allergen_snippet = None
        for line in lines:
            line_l = line.lower()
            if "allergen" in line_l or "contains:" in line_l:
                allergen_snippet = line
                if "contains" in line_l:
                    after_contains = line_l.split("contains", 1)[1].strip(": ")
                    declared = [item.strip().capitalize() for item in after_contains.split(",") if item.strip()]
            if "may contain" in line_l:
                precautionary.append(line.strip())

        # Preparation search
        prep_steps = []
        prep_snippet = None
        in_prep = False
        for line in lines:
            line_l = line.lower()
            if "preparation" in line_l or "directions" in line_l or "how to prepare" in line_l:
                in_prep = True
                prep_snippet = line
                continue
            if in_prep:
                if any(kw in line_l for kw in ["boil", "mix", "wash", "feed", "step", "1.", "2.", "3."]):
                    prep_steps.append(line)
                elif len(prep_steps) > 0 and len(line) < 3:
                    in_prep = False

        return {
            "product_name": product_name,
            "stated_age_marking": {
                "text": stated_age or "",
                "source_snippet": age_snippet or "",
                "confidence": 0.90 if stated_age else 0.0
            },
            "ingredients": {
                "text": ingredients_text or "",
                "source_snippet": ingredients_snippet or "",
                "confidence": 0.88 if ingredients_text else 0.0
            },
            "allergen_declaration": {
                "declared": declared,
                "precautionary": precautionary,
                "source_snippet": allergen_snippet or "",
                "confidence": 0.85 if declared or precautionary else 0.0
            },
            "preparation_instructions": {
                "steps": prep_steps,
                "water_boiling_noted": any("boil" in s.lower() for s in prep_steps),
                "source_snippet": prep_snippet or ("\n".join(prep_steps[:2]) if prep_steps else ""),
                "confidence": 0.85 if prep_steps else 0.0
            },
            "visible_panel_notes": (
                "Processed via offline local extraction engine."
                if not error_note else f"Fallback due to: {error_note}"
            )
        }

    def parse_to_models(self, raw_extracted: Dict[str, Any]) -> tuple:
        """Parses extracted dictionary into structured domain models."""
        age_data = raw_extracted.get("stated_age_marking", {})
        age_info = AgeSuitabilityInfo(
            stated_age=age_data.get("text") or None,
            source_snippet=age_data.get("source_snippet") or None,
            confidence=float(age_data.get("confidence", 0.0))
        )

        ingr_data = raw_extracted.get("ingredients", {})
        ingredients = ExtractedField(
            field_name="ingredients",
            extracted_value=ingr_data.get("text") or None,
            source_snippet=ingr_data.get("source_snippet") or None,
            confidence=float(ingr_data.get("confidence", 0.0))
        )

        allergen_data = raw_extracted.get("allergen_declaration", {})
        allergens = AllergenInfo(
            declared_allergens=allergen_data.get("declared", []),
            precautionary_allergens=allergen_data.get("precautionary", []),
            source_snippet=allergen_data.get("source_snippet") or None,
            is_declared_on_label=bool(allergen_data.get("declared")),
            confidence=float(allergen_data.get("confidence", 0.0))
        )

        prep_data = raw_extracted.get("preparation_instructions", {})
        preparation = PreparationInfo(
            steps=prep_data.get("steps", []),
            water_boiling_specified=bool(prep_data.get("water_boiling_noted", False)),
            source_snippet=prep_data.get("source_snippet") or None,
            confidence=float(prep_data.get("confidence", 0.0))
        )

        return age_info, ingredients, allergens, preparation
