"""
LabelFit India: Founder Independent Transcription & Adjudication Engine.
Processes dual independent package transcriptions by Swastik Tripathi & Saumya Tripathi,
calculates inter-rater concurrence rates, flags discrepancies for physical package
re-inspection, and compiles verified ground-truth records for model evaluation.
"""

import os
import sys
import csv
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional


FIELD_NAMES = (
    "productName",
    "ageMarking",
    "ingredients",
    "allergenDeclaration",
    "nutritionPanel",
    "preparationAndStorage",
)

CSV_HEADERS = [
    "sku_id",
    "brand",
    "product_name",
    "field",
    "swastik_transcription",
    "swastik_date",
    "saumya_transcription",
    "saumya_date",
    "adjudicated_ground_truth",
    "adjudication_notes",
]


def normalize_text(text: Optional[str]) -> str:
    """Collapses whitespace and strips leading/trailing spaces for exact comparison."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', str(text)).strip()


@dataclass
class DualTranscriptionRecord:
    sku_id: str
    brand: str
    product_name: str
    field: str
    swastik_transcription: str
    swastik_date: str
    saumya_transcription: str
    saumya_date: str
    adjudicated_ground_truth: str = ""
    adjudication_notes: str = ""

    @property
    def is_concurrence(self) -> bool:
        """True if both independent transcriptions match after whitespace normalization."""
        return normalize_text(self.swastik_transcription) == normalize_text(self.saumya_transcription)

    @property
    def has_discrepancy(self) -> bool:
        return not self.is_concurrence

    @property
    def is_adjudicated(self) -> bool:
        """True if either both concur or physical adjudication has been recorded."""
        if self.is_concurrence:
            return True
        return bool(normalize_text(self.adjudicated_ground_truth))

    def get_ground_truth(self) -> str:
        """
        Returns verified ground truth text.
        Raises ValueError if a discrepancy has not been resolved against the physical package.
        """
        if self.is_concurrence:
            return normalize_text(self.swastik_transcription)
        adjudicated = normalize_text(self.adjudicated_ground_truth)
        if not adjudicated:
            raise ValueError(
                f"Unresolved transcription discrepancy for SKU '{self.sku_id}', field '{self.field}'. "
                f"Recheck physical package and enter adjudicated_ground_truth before evaluating."
            )
        return adjudicated


class AdjudicationEngine:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.records: List[DualTranscriptionRecord] = []

    def load(self) -> List[DualTranscriptionRecord]:
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Transcription worksheet not found: {self.csv_path}")

        records: List[DualTranscriptionRecord] = []
        with open(self.csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sku_id = (row.get("sku_id") or "").strip()
                field = (row.get("field") or "").strip()
                if not sku_id or not field:
                    continue
                records.append(DualTranscriptionRecord(
                    sku_id=sku_id,
                    brand=(row.get("brand") or "").strip(),
                    product_name=(row.get("product_name") or "").strip(),
                    field=field,
                    swastik_transcription=row.get("swastik_transcription") or "",
                    swastik_date=(row.get("swastik_date") or "").strip(),
                    saumya_transcription=row.get("saumya_transcription") or "",
                    saumya_date=(row.get("saumya_date") or "").strip(),
                    adjudicated_ground_truth=row.get("adjudicated_ground_truth") or "",
                    adjudication_notes=row.get("adjudication_notes") or "",
                ))
        self.records = records
        return records

    def evaluate(self) -> Dict[str, Any]:
        """Calculates inter-rater agreement, discrepancy rates, and adjudication status."""
        total = len(self.records)
        if total == 0:
            return {
                "total_records": 0,
                "concurrence_count": 0,
                "concurrence_rate": 0.0,
                "discrepancy_count": 0,
                "unresolved_count": 0,
                "by_field": {},
                "all_adjudicated": False,
            }

        concur_count = sum(1 for r in self.records if r.is_concurrence)
        discrepancy_count = total - concur_count
        unresolved = [r for r in self.records if r.has_discrepancy and not r.is_adjudicated]

        by_field: Dict[str, Dict[str, Any]] = {}
        for f in FIELD_NAMES:
            field_records = [r for r in self.records if r.field == f]
            f_total = len(field_records)
            f_concur = sum(1 for r in field_records if r.is_concurrence)
            f_discrep = f_total - f_concur
            f_unresolved = sum(1 for r in field_records if r.has_discrepancy and not r.is_adjudicated)
            by_field[f] = {
                "total": f_total,
                "concurrence_count": f_concur,
                "concurrence_rate": round(f_concur / f_total * 100, 1) if f_total else 0.0,
                "discrepancy_count": f_discrep,
                "unresolved_count": f_unresolved,
            }

        return {
            "total_records": total,
            "concurrence_count": concur_count,
            "concurrence_rate": round(concur_count / total * 100, 1),
            "discrepancy_count": discrepancy_count,
            "unresolved_count": len(unresolved),
            "all_adjudicated": len(unresolved) == 0,
            "unresolved_records": [
                {"sku_id": r.sku_id, "field": r.field} for r in unresolved
            ],
            "by_field": by_field,
        }

    def format_markdown_report(self, results: Dict[str, Any]) -> str:
        """Formats GitHub Flavored Markdown report."""
        if results["total_records"] == 0:
            return "# LabelFit India: Dual Transcription & Adjudication Report\n\nNo records entered yet."

        status_badge = "✅ ALL DISCREPANCIES ADJUDICATED" if results["all_adjudicated"] else "⚠️ UNRESOLVED DISCREPANCIES PENDING RECHECK"
        lines = [
            "# LabelFit India: Dual Transcription & Adjudication Report",
            "",
            f"**Status**: {status_badge}  ",
            f"**Total Fields Transcribed**: {results['total_records']}  ",
            f"**Inter-Rater Concurrence**: {results['concurrence_rate']}% ({results['concurrence_count']}/{results['total_records']} fields matched exactly)  ",
            f"**Physical Discrepancies**: {results['discrepancy_count']} flagged  ",
            f"**Unresolved Items**: {results['unresolved_count']} requiring physical package inspection  ",
            "",
            "## 1. Field-by-Field Inter-Rater Agreement",
            "",
            "| Field | Total Records | Exact Concurrence | Agreement Rate | Discrepancies | Unresolved |",
            "|---|---|---|---|---|---|",
        ]
        for f, data in results["by_field"].items():
            lines.append(
                f"| `{f}` | {data['total']} | {data['concurrence_count']} | {data['concurrence_rate']}% | {data['discrepancy_count']} | {data['unresolved_count']} |"
            )

        if results["unresolved_count"] > 0:
            lines.extend([
                "",
                "## 2. Unresolved Discrepancies (Action Required)",
                "",
                "The following fields differ between independent transcriptions and must be verified against the physical pack:",
                "",
            ])
            for item in results["unresolved_records"]:
                lines.append(f"- **{item['sku_id']}** (`{item['field']}`): recheck physical package.")

        lines.extend([
            "",
            "---",
            "*Dual transcription records independently collected by Swastik Tripathi and Saumya Tripathi.*",
        ])
        return "\n".join(lines)
