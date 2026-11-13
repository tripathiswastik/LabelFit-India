"""Small data structures for literal, source-linked label transcription."""

from dataclasses import asdict, dataclass
from typing import Dict


FIELD_NAMES = (
    "productName",
    "ageMarking",
    "ingredients",
    "allergenDeclaration",
    "nutritionPanel",
    "preparationAndStorage",
)


@dataclass
class ExtractedField:
    """A candidate transcription. `source_match` only checks supplied text."""

    field_name: str
    value: str = ""
    evidence: str = ""
    read_status: str = "uncertain"
    source_match: bool = False

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass
class LabelInspectionReport:
    """An in-memory report; it contains no age, allergy, safety, or health verdict."""

    fields: Dict[str, ExtractedField]
    disclaimer: str = (
        "Candidate text only. Check every transcription against the package. "
        "The text-match indicator compares against the supplied text and does not verify the package image."
    )

    def to_dict(self) -> Dict[str, object]:
        return {
            "fields": {name: item.to_dict() for name, item in self.fields.items()},
            "disclaimer": self.disclaimer,
        }
