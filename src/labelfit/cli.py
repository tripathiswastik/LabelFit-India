"""
Command Line Interface for LabelFit India.
Inspects baby food package label text and prints structured evidence and gap audit.
"""

import sys
from pathlib import Path
import argparse

# Ensure package directory is on sys.path for direct CLI execution
_SRC_ROOT = str(Path(__file__).resolve().parent.parent)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

from labelfit.extractor import GeminiLabelExtractor
from labelfit.validator import DeterministicValidator
from labelfit.samples import SAMPLE_CEREAL_6M, SAMPLE_PUREE_GAP_CASE, SAMPLE_INFANT_FORMULA_OUT_OF_SCOPE


def run_inspection(text: str, identifier: str = "label_sample"):
    extractor = GeminiLabelExtractor()
    validator = DeterministicValidator()

    print("\n" + "=" * 65)
    print("  LABELFIT INDIA - PACKAGED FOOD LABEL INSPECTION REPORT")
    print("=" * 65)

    raw_extracted = extractor.extract_from_text(text)
    product_name = raw_extracted.get("product_name", "Baby Food Product")
    age_info, ingredients, allergens, preparation = extractor.parse_to_models(raw_extracted)

    report = validator.inspect_and_generate_report(
        product_name=product_name,
        product_identifier=identifier,
        raw_text=text,
        age_info=age_info,
        ingredients=ingredients,
        allergens=allergens,
        preparation=preparation
    )

    print(f"Product:      {report.product_name}")
    print(f"Identifier:   {report.product_identifier}")
    print(f"Timestamp:    {report.inspected_at}")
    print(f"Completeness: {int(report.completeness_score * 100)}%")
    print("-" * 65)

    print("\n[1] AGE SUITABILITY MARKING")
    if report.age_suitability.stated_age:
        status_sym = "[VERIFIED]" if report.age_suitability.meets_6_months_scope else "[OUT OF SCOPE]"
        print(f"  Status:  {status_sym} (Stated: '{report.age_suitability.stated_age}')")
        if report.age_suitability.source_snippet:
            print(f"  Source:  \"{report.age_suitability.source_snippet}\"")
    else:
        print("  Status:  [MISSING] No explicit age suitability found on visible panel.")

    print("\n[2] INGREDIENTS STATEMENT")
    if report.ingredients.extracted_value:
        print(f"  Status:  [{report.ingredients.status.upper()}]")
        print(f"  Details: {report.ingredients.extracted_value}")
        if report.ingredients.source_snippet:
            print(f"  Source:  \"{report.ingredients.source_snippet}\"")
    else:
        print("  Status:  [MISSING] Ingredients panel not detected.")

    print("\n[3] ALLERGEN DECLARATION")
    if report.allergens.is_declared_on_label:
        print(f"  Declared:      {', '.join(report.allergens.declared_allergens)}")
    else:
        print("  Declared:      [NONE DETECTED SEPARATELY]")
    if report.allergens.precautionary_allergens:
        print(f"  Precautionary: {', '.join(report.allergens.precautionary_allergens)}")
    if report.allergens.source_snippet:
        print(f"  Source:        \"{report.allergens.source_snippet}\"")

    print("\n[4] PREPARATION DIRECTIONS")
    if report.preparation.steps:
        print(f"  Steps Count:   {len(report.preparation.steps)}")
        print(f"  Water Boiling: {'[EXPLICITLY STATED]' if report.preparation.water_boiling_specified else '[NOT MENTIONED]'}")
        for idx, step in enumerate(report.preparation.steps, 1):
            print(f"    {idx}. {step}")
    else:
        print("  Status:        [MISSING] No preparation steps found on visible panel.")

    print("\n[5] VERIFICATION FLAGS & UNCERTAINTIES")
    if report.flags:
        for flag in report.flags:
            badge = f"[{flag.flag_type.upper()}]"
            print(f"  * {badge:<15} ({flag.field_name}): {flag.message}")
            if flag.evidence_snippet:
                print(f"      Evidence: \"{flag.evidence_snippet}\"")
    else:
        print("  * No gaps or warnings detected.")

    print("\n" + "-" * 65)
    print(f"NOTICE: {report.disclaimer}")
    print("=" * 65 + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description="LabelFit India CLI Label Inspector")
    parser.add_argument("--sample", choices=["cereal", "puree", "formula"], default="cereal",
                        help="Run inspection on built-in infant food sample dataset")
    parser.add_argument("--file", type=str, default=None,
                        help="Path to custom text or OCR file to inspect")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
        run_inspection(content, identifier=args.file)
    else:
        samples = {
            "cereal": (SAMPLE_CEREAL_6M, "sample_cereal_6m_package"),
            "puree": (SAMPLE_PUREE_GAP_CASE, "sample_puree_missing_prep"),
            "formula": (SAMPLE_INFANT_FORMULA_OUT_OF_SCOPE, "sample_infant_formula_stage1"),
        }
        text, ident = samples[args.sample]
        run_inspection(text, identifier=ident)


if __name__ == "__main__":
    main()

