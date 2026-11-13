"""
Deterministic validation engine for LabelFit India.
Cross-references extracted candidate fields against visible package text,
enforces evidence grounding, and flags gaps or ambiguities.
Strictly non-prescriptive: produces zero health, safety, or feeding decisions.
"""

import re
from typing import List, Dict, Tuple, Optional
from labelfit.models import (
    AgeSuitabilityInfo,
    ExtractedField,
    AllergenInfo,
    PreparationInfo,
    VerificationFlag,
    LabelInspectionReport
)

# Reference dictionary of common allergens in Indian packaged foods (FSSAI aligned)
COMMON_ALLERGEN_KEYWORDS = {
    "milk": ["milk", "milk solids", "skimmed milk", "whole milk", "casein", "whey", "lactose"],
    "wheat/gluten": ["wheat", "gluten", "atta", "maida", "suji", "semolina", "barley", "rye", "oats"],
    "soy": ["soy", "soya", "soybean", "soy lecithin"],
    "nuts": ["almond", "badam", "cashew", "kaju", "walnut", "akhrot", "pistachio", "pista", "hazelnut"],
    "peanut": ["peanut", "groundnut", "moongfali"],
    "egg": ["egg", "albumin", "egg powder"],
    "fish": ["fish", "fish oil"],
    "sesame": ["sesame", "til"],
}


class DeterministicValidator:
    """Performs rule-based verification on Gemini candidate extractions."""

    def __init__(self, confidence_threshold: float = 0.70):
        self.confidence_threshold = confidence_threshold

    def normalize(self, text: Optional[str]) -> str:
        """Strip punctuation and lowercase for reliable substring matching."""
        if not text:
            return ""
        return re.sub(r'[\s\W_]+', ' ', text).strip().lower()

    def verify_snippet_grounding(self, snippet: Optional[str], raw_text: str) -> bool:
        """Verifies if the cited source snippet actually appears in the visible text."""
        if not snippet:
            return False
        norm_snippet = self.normalize(snippet)
        norm_raw = self.normalize(raw_text)
        if not norm_snippet:
            return False
        # Exact or partial match of significant phrases (>= 15 chars)
        if norm_snippet in norm_raw:
            return True
        # Chunk check if long snippet
        words = norm_snippet.split()
        if len(words) >= 4:
            subphrase = " ".join(words[:4])
            return subphrase in norm_raw
        return False

    def validate_age_marking(
        self, age_info: AgeSuitabilityInfo, raw_text: str
    ) -> Tuple[AgeSuitabilityInfo, List[VerificationFlag]]:
        """Verifies the stated age marking against complementary-food scope (6+ months)."""
        flags = []
        raw_norm = self.normalize(raw_text)

        # Pattern match for age indications:
        # Check ranges like "0 to 6 months" or "6 to 24 months" first to capture starting bound
        search_target = f"{self.normalize(age_info.stated_age)} {raw_norm}"
        range_match = re.search(r'(\d+)\s*(?:to|-)\s*(\d+)\s*(?:months?|mths?|m\b)', search_target)
        if range_match:
            try:
                detected_months = int(range_match.group(1))
            except ValueError:
                detected_months = None
        else:
            age_patterns = [
                (r'from\s*(\d+)\s*months?', 1),
                (r'(\d+)\s*\+\s*(?:months?|mths?|m\b)?', 1),
                (r'(\d+)\s*(?:months?|mths?|m\b)', 1),
                (r'stage\s*1\s*\(?(\d+)?', 1),
            ]
            for pattern, group_idx in age_patterns:
                match = re.search(pattern, search_target)
                if match and match.group(group_idx):
                    try:
                        detected_months = int(match.group(group_idx))
                        break
                    except ValueError:
                        pass

        # If stated_age provided by extractor, check it
        if age_info.stated_age:
            age_info.meets_6_months_scope = bool(detected_months is not None and detected_months >= 6)
            age_info.minimum_months = detected_months

            is_grounded = self.verify_snippet_grounding(age_info.source_snippet, raw_text)
            if not is_grounded:
                flags.append(VerificationFlag(
                    flag_type="uncertainty",
                    field_name="age_suitability",
                    message="Stated age snippet could not be verified in visible package text.",
                    evidence_snippet=age_info.source_snippet
                ))
            else:
                flags.append(VerificationFlag(
                    flag_type="verified",
                    field_name="age_suitability",
                    message="Stated age verified against package text.",
                    evidence_snippet=age_info.source_snippet
                ))

            if detected_months is not None and detected_months < 6:
                flags.append(VerificationFlag(
                    flag_type="warning",
                    field_name="age_suitability",
                    message="Label indicates age below 6 months; this is outside complementary feeding scope (6+ months).",
                    evidence_snippet=age_info.source_snippet
                ))
        else:
            flags.append(VerificationFlag(
                flag_type="gap",
                field_name="age_suitability",
                message="No explicit age marking found on visible packaging panels.",
                evidence_snippet=None
            ))

        return age_info, flags

    def validate_ingredients(
        self, ingredients: ExtractedField, raw_text: str
    ) -> Tuple[ExtractedField, List[VerificationFlag]]:
        """Verifies ingredient list extraction and snippet completeness."""
        flags = []
        if not ingredients.extracted_value or len(ingredients.extracted_value.strip()) == 0:
            ingredients.status = "missing"
            flags.append(VerificationFlag(
                flag_type="gap",
                field_name="ingredients",
                message="Ingredients list was not located on visible package panels."
            ))
            return ingredients, flags

        is_grounded = self.verify_snippet_grounding(ingredients.source_snippet, raw_text)
        if not is_grounded:
            ingredients.status = "unclear"
            flags.append(VerificationFlag(
                flag_type="uncertainty",
                field_name="ingredients",
                message="Extracted ingredients could not be fully grounded in visible text.",
                evidence_snippet=ingredients.source_snippet
            ))
        else:
            ingredients.status = "verified"
            flags.append(VerificationFlag(
                flag_type="verified",
                field_name="ingredients",
                message="Ingredients list grounded in package text.",
                evidence_snippet=ingredients.source_snippet[:100] + ("..." if len(ingredients.source_snippet or "") > 100 else "")
            ))

        # Check for potential truncation (e.g. cut off by label fold or panel edge)
        last_chars = ingredients.extracted_value.strip()[-1]
        if last_chars in (",", "-", ";", "&"):
            flags.append(VerificationFlag(
                flag_type="uncertainty",
                field_name="ingredients",
                message="Ingredients list appears truncated or cut off at the edge of the visible panel.",
                evidence_snippet=ingredients.extracted_value[-30:]
            ))

        return ingredients, flags

    def validate_allergens(
        self,
        allergen_info: AllergenInfo,
        ingredients_field: ExtractedField,
        raw_text: str
    ) -> Tuple[AllergenInfo, List[VerificationFlag]]:
        """
        Deterministic check comparing declared allergens, precautionary statements,
        and ingredients text against known allergen keyword dictionaries.
        """
        flags = []
        norm_ingredients = self.normalize(ingredients_field.extracted_value)
        norm_raw = self.normalize(raw_text)

        # 1. Check for allergen keywords present in ingredients
        inferred_from_ingredients = []
        for allergen_group, keywords in COMMON_ALLERGEN_KEYWORDS.items():
            for kw in keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', norm_ingredients):
                    inferred_from_ingredients.append(allergen_group)
                    break

        # 2. Check declared allergen grounding
        if allergen_info.declared_allergens:
            allergen_info.is_declared_on_label = True
            is_grounded = self.verify_snippet_grounding(allergen_info.source_snippet, raw_text)
            if is_grounded:
                flags.append(VerificationFlag(
                    flag_type="verified",
                    field_name="allergens",
                    message="Declared allergen statement verified on package.",
                    evidence_snippet=allergen_info.source_snippet
                ))
            else:
                flags.append(VerificationFlag(
                    flag_type="uncertainty",
                    field_name="allergens",
                    message="Allergen statement snippet could not be verified in visible text.",
                    evidence_snippet=allergen_info.source_snippet
                ))
        else:
            allergen_info.is_declared_on_label = False
            # Check if ingredients actually contain allergen items but separate statement is absent
            if inferred_from_ingredients:
                flags.append(VerificationFlag(
                    flag_type="gap",
                    field_name="allergens",
                    message=(
                        "Separate allergen declaration was not located, although ingredients list "
                        "includes potential allergens (" + ", ".join(inferred_from_ingredients) + ")."
                    ),
                    evidence_snippet=None
                ))
            else:
                flags.append(VerificationFlag(
                    flag_type="gap",
                    field_name="allergens",
                    message="No explicit allergen statement identified on visible panels.",
                    evidence_snippet=None
                ))

        # 3. Check precautionary statements (cross-contamination)
        if allergen_info.precautionary_allergens:
            flags.append(VerificationFlag(
                flag_type="precautionary",
                field_name="allergens",
                message="Package contains precautionary cross-contamination notices ('May contain...').",
                evidence_snippet=", ".join(allergen_info.precautionary_allergens)
            ))

        return allergen_info, flags

    def validate_preparation(
        self, prep_info: PreparationInfo, raw_text: str
    ) -> Tuple[PreparationInfo, List[VerificationFlag]]:
        """Verifies preparation steps, clean water boiling, and storage instructions."""
        flags = []
        norm_raw = self.normalize(raw_text)

        # Check for water boiling mentions (critical for infant complementary feeds)
        boil_keywords = ["boil", "boiled", "boiling water", "clean water", "drinking water"]
        has_boiling_mention = any(kw in norm_raw for kw in boil_keywords)
        prep_info.water_boiling_specified = has_boiling_mention

        if prep_info.steps:
            is_grounded = self.verify_snippet_grounding(prep_info.source_snippet, raw_text)
            if is_grounded:
                flags.append(VerificationFlag(
                    flag_type="verified",
                    field_name="preparation",
                    message="Preparation steps grounded in visible package directions.",
                    evidence_snippet=prep_info.source_snippet[:120] + ("..." if len(prep_info.source_snippet or "") > 120 else "")
                ))
            else:
                flags.append(VerificationFlag(
                    flag_type="uncertainty",
                    field_name="preparation",
                    message="Preparation directions snippet could not be matched with visible text.",
                    evidence_snippet=prep_info.source_snippet
                ))

            if not has_boiling_mention:
                flags.append(VerificationFlag(
                    flag_type="gap",
                    field_name="preparation",
                    message="Visible preparation steps do not explicitly state boiling drinking water.",
                    evidence_snippet=None
                ))
        else:
            flags.append(VerificationFlag(
                flag_type="gap",
                field_name="preparation",
                message="Preparation instructions not found on visible packaging panels.",
                evidence_snippet=None
            ))

        return prep_info, flags

    def inspect_and_generate_report(
        self,
        product_name: str,
        product_identifier: str,
        raw_text: str,
        age_info: AgeSuitabilityInfo,
        ingredients: ExtractedField,
        allergens: AllergenInfo,
        preparation: PreparationInfo
    ) -> LabelInspectionReport:
        """Runs deterministic checks across all fields and compiles the final report."""
        all_flags: List[VerificationFlag] = []

        validated_age, age_flags = self.validate_age_marking(age_info, raw_text)
        all_flags.extend(age_flags)

        validated_ingr, ingr_flags = self.validate_ingredients(ingredients, raw_text)
        all_flags.extend(ingr_flags)

        validated_allergens, allergen_flags = self.validate_allergens(allergens, validated_ingr, raw_text)
        all_flags.extend(allergen_flags)

        validated_prep, prep_flags = self.validate_preparation(preparation, raw_text)
        all_flags.extend(prep_flags)

        # Completeness calculation
        total_checks = 4
        passed_checks = sum([
            1 if validated_age.stated_age and validated_age.meets_6_months_scope else 0,
            1 if validated_ingr.status == "verified" else 0,
            1 if validated_allergens.is_declared_on_label else 0,
            1 if len(validated_prep.steps) > 0 else 0
        ])
        completeness = round(passed_checks / total_checks, 2)

        from datetime import datetime
        return LabelInspectionReport(
            product_name=product_name,
            product_identifier=product_identifier,
            inspected_at=datetime.utcnow().isoformat() + "Z",
            raw_ocr_text=raw_text,
            age_suitability=validated_age,
            ingredients=validated_ingr,
            allergens=validated_allergens,
            preparation=validated_prep,
            flags=all_flags,
            completeness_score=completeness
        )
