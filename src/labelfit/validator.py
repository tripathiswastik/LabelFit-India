"""Text-match checks only; these checks do not validate the package or product."""

from labelfit.extractor import GeminiLabelExtractor
from labelfit.models import LabelInspectionReport


class DeterministicValidator:
    """Checks whether candidate values/snippets occur in supplied text."""

    def inspect(self, raw_text: str, extracted: dict) -> LabelInspectionReport:
        return GeminiLabelExtractor().parse_to_report(extracted, raw_text)
