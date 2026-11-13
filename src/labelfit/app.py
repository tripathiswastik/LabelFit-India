"""
Streamlit Web UI Prototype for LabelFit India.
Interactive demonstration of baby food label inspection, source-grounding, and uncertainty auditing.
"""

import sys
from pathlib import Path
from typing import Optional

# Ensure package directory is on sys.path for direct streamlit execution
_SRC_ROOT = str(Path(__file__).resolve().parent.parent)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

import streamlit as st
import json
from labelfit.models import LabelInspectionReport
from labelfit.extractor import GeminiLabelExtractor
from labelfit.validator import DeterministicValidator
from labelfit.samples import SAMPLE_CEREAL_6M, SAMPLE_PUREE_GAP_CASE, SAMPLE_INFANT_FORMULA_OUT_OF_SCOPE

st.set_page_config(
    page_title="LabelFit India - Label Inspection",
    page_icon="👶",
    layout="wide"
)

st.title("👶 LabelFit India")
st.subheader("Objective Label Inspection for Packaged Complementary Foods (6+ Months)")
st.caption("Startup Buildathon India 2026 | Google DeepMind & Google Cloud")

# Sidebar setup
st.sidebar.header("Packaging Input")
mode = st.sidebar.radio(
    "Choose Sample or Input Method",
    ["Sample 1: Baby Cereal (6+ Mo)", "Sample 2: Puree (Gap in Prep)", "Sample 3: Infant Formula (Out of Scope)", "Custom Text / OCR"]
)

api_key = st.sidebar.text_input("Gemini API Key (Optional)", type="password", help="Leave blank for local offline rule engine")

if mode == "Sample 1: Baby Cereal (6+ Mo)":
    raw_input_text = SAMPLE_CEREAL_6M
    sample_id = "sample_cereal_6m.txt"
elif mode == "Sample 2: Puree (Gap in Prep)":
    raw_input_text = SAMPLE_PUREE_GAP_CASE
    sample_id = "sample_puree_gap.txt"
elif mode == "Sample 3: Infant Formula (Out of Scope)":
    raw_input_text = SAMPLE_INFANT_FORMULA_OUT_OF_SCOPE
    sample_id = "sample_formula_0_6m.txt"
else:
    sample_id = "custom_label_input.txt"
    raw_input_text = st.sidebar.text_area("Paste visible package label text:", height=250)

report: Optional[LabelInspectionReport] = None
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📷 Visible Package Text / OCR Stream")
    st.text_area("Raw Label Content", raw_input_text, height=380, disabled=True)

with col2:
    st.markdown("### 🔍 LabelFit Evidence View")
    if st.button("Inspect Package Label", type="primary") or raw_input_text:
        extractor = GeminiLabelExtractor(api_key=api_key if api_key else None)
        validator = DeterministicValidator()

        with st.spinner("Extracting candidate fields and auditing visible snippets..."):
            raw_extracted = extractor.extract_from_text(raw_input_text)
            product_name = raw_extracted.get("product_name", "Inspected Product")
            age_info, ingredients, allergens, prep = extractor.parse_to_models(raw_extracted)

            report = validator.inspect_and_generate_report(
                product_name=product_name,
                product_identifier=sample_id,
                raw_text=raw_input_text,
                age_info=age_info,
                ingredients=ingredients,
                allergens=allergens,
                preparation=prep
            )

        # Overview metric cards
        m1, m2 = st.columns(2)
        m1.metric("Field Completeness", f"{int(report.completeness_score * 100)}%")
        m2.metric("Flagged Checks", len(report.flags))

        # 1. Age Marking
        with st.expander("1. Age Suitability Marking", expanded=True):
            if report.age_suitability.stated_age:
                st.write(f"**Stated Age:** `{report.age_suitability.stated_age}`")
                st.write(f"**6+ Months Scope:** {'✅ Verified' if report.age_suitability.meets_6_months_scope else '⚠️ Outside Scope'}")
                if report.age_suitability.source_snippet:
                    st.info(f"Source Quote: \"{report.age_suitability.source_snippet}\"")
            else:
                st.warning("No explicit age suitability marking found.")

        # 2. Ingredients List
        with st.expander("2. Ingredients Panel", expanded=True):
            if report.ingredients.extracted_value:
                st.write(f"**Status:** `{report.ingredients.status.upper()}`")
                st.write(report.ingredients.extracted_value)
                if report.ingredients.source_snippet:
                    st.info(f"Source Quote: \"{report.ingredients.source_snippet}\"")
            else:
                st.warning("Ingredients list not located on visible panel.")

        # 3. Allergen Statement
        with st.expander("3. Allergen Declarations", expanded=True):
            if report.allergens.declared_allergens:
                st.write(f"**Declared Allergens:** {', '.join(report.allergens.declared_allergens)}")
            else:
                st.write("**Declared Allergens:** *None explicitly declared*")
            if report.allergens.precautionary_allergens:
                st.warning(f"**Cross-Contamination Warnings:** {', '.join(report.allergens.precautionary_allergens)}")
            if report.allergens.source_snippet:
                st.info(f"Source Quote: \"{report.allergens.source_snippet}\"")

        # 4. Preparation Steps
        with st.expander("4. Preparation & Hygiene Directions", expanded=True):
            if report.preparation.steps:
                st.write(f"**Water Boiling Mentioned:** {'✅ Yes' if report.preparation.water_boiling_specified else '⚠️ Not Mentioned'}")
                for i, step in enumerate(report.preparation.steps, 1):
                    st.write(f"{i}. {step}")
            else:
                st.warning("Preparation directions not detected.")

st.markdown("---")
st.markdown("### 📋 Verification & Uncertainty Audit Log")
if report is not None:
    for f in report.flags:
        if f.flag_type == "verified":
            st.success(f"**[VERIFIED] {f.field_name.upper()}**: {f.message}")
        elif f.flag_type == "gap":
            st.error(f"**[GAP] {f.field_name.upper()}**: {f.message}")
        elif f.flag_type == "warning":
            st.warning(f"**[WARNING] {f.field_name.upper()}**: {f.message}")
        else:
            st.info(f"**[{f.flag_type.upper()}] {f.field_name.upper()}**: {f.message}")

st.markdown("---")
disclaimer_msg = report.disclaimer if report is not None else "Label information tool only; not medical, safety, or feeding advice."
st.caption(f"**Notice:** {disclaimer_msg}")

