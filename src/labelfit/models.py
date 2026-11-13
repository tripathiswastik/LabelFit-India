"""
Core data models for LabelFit India.
Represents candidate label extractions, source grounding, and verification reports.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime


@dataclass
class ExtractedField:
    """Represents a candidate field extracted from packaging text."""
    field_name: str
    extracted_value: Optional[str] = None
    source_snippet: Optional[str] = None
    confidence: float = 0.0
    status: str = "missing"  # "verified", "unclear", "missing"
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AllergenInfo:
    """Declared and precautionary allergen statements found on package."""
    declared_allergens: List[str] = field(default_factory=list)
    precautionary_allergens: List[str] = field(default_factory=list)
    source_snippet: Optional[str] = None
    is_declared_on_label: bool = False
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgeSuitabilityInfo:
    """Age suitability marking extracted from packaging."""
    stated_age: Optional[str] = None
    minimum_months: Optional[int] = None
    meets_6_months_scope: bool = False
    source_snippet: Optional[str] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PreparationInfo:
    """Preparation and handling directions extracted from packaging."""
    steps: List[str] = field(default_factory=list)
    water_boiling_specified: bool = False
    storage_instruction: Optional[str] = None
    source_snippet: Optional[str] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VerificationFlag:
    """Deterministic validation flag or uncertainty indicator."""
    flag_type: str  # "verified", "gap", "uncertainty", "precautionary"
    field_name: str
    message: str
    evidence_snippet: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LabelInspectionReport:
    """
    Final inspection report presenting extracted evidence, gaps, and uncertainty.
    Strictly non-prescriptive: contains zero health, safety, or feeding decisions.
    """
    product_name: str
    product_identifier: str  # Barcode or image filename
    inspected_at: str
    raw_ocr_text: str
    age_suitability: AgeSuitabilityInfo
    ingredients: ExtractedField
    allergens: AllergenInfo
    preparation: PreparationInfo
    flags: List[VerificationFlag] = field(default_factory=list)
    completeness_score: float = 0.0
    disclaimer: str = (
        "LabelFit India is an objective label reading and inspection tool. "
        "It does not assess nutritional safety, provide feeding instructions, "
        "or replace healthcare or pediatric guidance."
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
