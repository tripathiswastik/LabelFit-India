"""
LabelFit India: Founder Independent Transcription & Adjudication Engine.
Processes dual independent package transcriptions by Swastik Tripathi & Saumya Tripathi,
calculates inter-rater concurrence rates, flags discrepancies for physical package
re-inspection, and compiles verified ground-truth records for model evaluation.
"""

import os
import csv
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


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
    return re.sub(r'\s+', ' ', text).strip()


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
    def is_pending(self) -> bool:
        """True if independent transcription dates have not been entered yet."""
        return not bool(self.swastik_date and self.saumya_date)

    @property
    def is_concurrence(self) -> bool:
        """True if both independent transcriptions match after whitespace normalization and are dated."""
        if self.is_pending:
            return False
        return normalize_text(self.swastik_transcription) == normalize_text(self.saumya_transcription)

    @property
    def has_discrepancy(self) -> bool:
        if self.is_pending:
            return False
        return not self.is_concurrence

    @property
    def is_adjudicated(self) -> bool:
        """True if either both concur or physical adjudication has been recorded."""
        if self.is_pending:
            return False
        if self.is_concurrence:
            return True
        return bool(normalize_text(self.adjudicated_ground_truth))

    def get_ground_truth(self) -> str:
        """
        Returns verified ground truth text.
        Raises ValueError if pending or an unadjudicated discrepancy exists.
        """
        if self.is_pending:
            raise ValueError(
                f"Pending transcription for SKU '{self.sku_id}', field '{self.field}'. "
                f"Both reviewers must date and record their physical package reads."
            )
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
                "completed_count": 0,
                "pending_count": 0,
                "concurrence_count": 0,
                "concurrence_rate": 0.0,
                "discrepancy_count": 0,
                "unresolved_count": 0,
                "by_field": {},
                "all_adjudicated": False,
            }

        completed = [r for r in self.records if not r.is_pending]
        pending = [r for r in self.records if r.is_pending]
        concur_count = sum(1 for r in completed if r.is_concurrence)
        discrepancy_count = len(completed) - concur_count
        unresolved = [r for r in completed if r.has_discrepancy and not r.is_adjudicated]

        by_field: Dict[str, Dict[str, Any]] = {}
        for f in FIELD_NAMES:
            field_records = [r for r in self.records if r.field == f]
            f_total = len(field_records)
            f_completed = [r for r in field_records if not r.is_pending]
            f_concur = sum(1 for r in f_completed if r.is_concurrence)
            f_discrep = len(f_completed) - f_concur
            f_unresolved = sum(1 for r in f_completed if r.has_discrepancy and not r.is_adjudicated)
            f_pending = sum(1 for r in field_records if r.is_pending)
            by_field[f] = {
                "total": f_total,
                "completed": len(f_completed),
                "pending": f_pending,
                "concurrence_count": f_concur,
                "concurrence_rate": round(f_concur / len(f_completed) * 100, 1) if f_completed else 0.0,
                "discrepancy_count": f_discrep,
                "unresolved_count": f_unresolved,
            }

        all_adjudicated = len(completed) > 0 and len(pending) == 0 and len(unresolved) == 0

        return {
            "total_records": total,
            "completed_count": len(completed),
            "pending_count": len(pending),
            "concurrence_count": concur_count,
            "concurrence_rate": round(concur_count / len(completed) * 100, 1) if completed else 0.0,
            "discrepancy_count": discrepancy_count,
            "unresolved_count": len(unresolved),
            "all_adjudicated": all_adjudicated,
            "unresolved_records": [
                {"sku_id": r.sku_id, "field": r.field} for r in unresolved
            ],
            "pending_records": [
                {"sku_id": r.sku_id, "field": r.field} for r in pending
            ],
            "by_field": by_field,
        }

    def format_markdown_report(self, results: Dict[str, Any]) -> str:
        """Formats GitHub Flavored Markdown report."""
        if results["total_records"] == 0:
            return "# LabelFit India: Dual Transcription & Adjudication Report\n\nNo records entered yet."

        if results["pending_count"] > 0:
            status_badge = f"⚠️ PENDING INTAKE ({results['pending_count']} fields awaiting founder entry)"
        elif not results["all_adjudicated"]:
            status_badge = f"⚠️ UNRESOLVED DISCREPANCIES ({results['unresolved_count']} fields pending recheck)"
        else:
            status_badge = "✅ ALL TARGET TRANSCRIPTIONS ADJUDICATED"

        lines = [
            "# LabelFit India: Dual Transcription & Adjudication Report",
            "",
            f"**Status**: {status_badge}  ",
            f"**Total Records**: {results['total_records']} (Completed: {results['completed_count']}, Pending: {results['pending_count']})  ",
            f"**Inter-Rater Concurrence**: {results['concurrence_rate']}% ({results['concurrence_count']}/{results['completed_count']} completed fields matched exactly)  ",
            f"**Physical Discrepancies**: {results['discrepancy_count']} flagged  ",
            f"**Unresolved Items**: {results['unresolved_count']} requiring physical package inspection  ",
            "",
            "## 1. Field-by-Field Status",
            "",
            "| Field | Total | Completed | Pending | Exact Concurrence | Discrepancies | Unresolved |",
            "|---|---|---|---|---|---|---|",
        ]
        for f, data in results["by_field"].items():
            lines.append(
                f"| `{f}` | {data['total']} | {data['completed']} | {data['pending']} | {data['concurrence_count']} ({data['concurrence_rate']}%) | {data['discrepancy_count']} | {data['unresolved_count']} |"
            )

        if results["unresolved_count"] > 0:
            lines.extend([
                "",
                "## 2. Unresolved Discrepancies (Recheck Physical Package)",
                "",
            ])
            for item in results["unresolved_records"]:
                lines.append(f"- **{item['sku_id']}** (`{item['field']}`): recheck physical package.")

        if results["pending_count"] > 0:
            lines.extend([
                "",
                "## 3. Pending Founder Entry",
                "",
                f"{results['pending_count']} fields are awaiting independent physical transcriptions in `docs/founder-independent-transcriptions.csv`.",
            ])

        lines.extend([
            "",
            "---",
            "*Dual transcription records independently collected by Swastik Tripathi and Saumya Tripathi.*",
        ])
        return "\n".join(lines)
