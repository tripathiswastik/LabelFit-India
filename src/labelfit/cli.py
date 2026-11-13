"""Offline-first, text-only label transcription worksheet."""

import argparse
import sys
from pathlib import Path

_SRC_ROOT = str(Path(__file__).resolve().parent.parent)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.extractor import GeminiLabelExtractor
from labelfit.samples import SAMPLE_CEREAL_6M, SAMPLE_PUREE_GAP_CASE
from labelfit.validator import DeterministicValidator


def run_inspection(text: str):
    extractor = GeminiLabelExtractor()
    candidates = extractor.extract_from_text(text)
    report = DeterministicValidator().inspect(text, candidates)
    print("LabelFit India - candidate label text")
    print("Text-only prototype. Every result requires checking against the package.")
    print("The text-match column compares against supplied text; it does not verify a photo or label.")
    for field in report.fields.values():
        print(f"\n{field.field_name}")
        print(f"  Read status: {field.read_status}")
        print(f"  Candidate text: {field.value or '[not visible in supplied text]'}")
        print(f"  Model/parser snippet: {field.evidence or '[none]'}")
        print(f"  Supplied-text match: {'yes' if field.source_match else 'no'}")
    print(f"\n{report.disclaimer}")
    return report


def main():
    parser = argparse.ArgumentParser(description="LabelFit text-only transcription prototype")
    parser.add_argument("--sample", choices=["cereal", "puree"], default=None,
                        help="Use a fictional sample label")
    parser.add_argument("--file", help="Read label text from a local text file")
    args = parser.parse_args()
    if args.sample and args.file:
        parser.error("Choose either --sample or --file.")
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.sample == "puree":
        text = SAMPLE_PUREE_GAP_CASE
    else:
        text = SAMPLE_CEREAL_6M
    run_inspection(text)


if __name__ == "__main__":
    main()
