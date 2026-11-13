"""Optional Streamlit text scratchpad; the main photo prototype is in Node.js."""

import os
import sys
from pathlib import Path

_SRC_ROOT = str(Path(__file__).resolve().parent.parent)
if _SRC_ROOT not in sys.path:
    sys.path.insert(0, _SRC_ROOT)

import streamlit as st

from labelfit.extractor import GeminiLabelExtractor
from labelfit.samples import SAMPLE_CEREAL_6M, SAMPLE_PUREE_GAP_CASE
from labelfit.validator import DeterministicValidator


st.set_page_config(page_title="LabelFit India - text scratchpad", page_icon="L", layout="wide")
st.title("LabelFit India")
st.subheader("Text-only label transcription scratchpad")
st.caption("The photo-reading prototype is the Node.js app. This screen only works with text you paste.")
st.warning(
    "If you choose Gemini, the pasted text is sent to Google. Unpaid API content may be used to improve "
    "Google services and may be reviewed by people. `store: false` is not a zero-retention promise. "
    "Do not submit personal, child, confidential, or sensitive information."
)

sample_choice = st.sidebar.selectbox("Load fictional example", ["None", "Cereal", "Fruit puree"])
sample_text = SAMPLE_CEREAL_6M if sample_choice == "Cereal" else SAMPLE_PUREE_GAP_CASE if sample_choice == "Fruit puree" else ""
raw_text = st.text_area("Paste visible package-label text", value=sample_text, height=300)
use_gemini = st.checkbox("Send this text to Gemini for a candidate transcription", value=False)
privacy_confirmed = st.checkbox("I understand this sends the pasted text to Google and contains no personal or confidential information.", value=False)
api_key = st.text_input("Gemini API key (optional)", type="password") if use_gemini else ""

if st.button("Transcribe fields", type="primary"):
    if use_gemini and not privacy_confirmed:
        st.error("Confirm the data-sharing notice before sending text to Gemini.")
    elif use_gemini and not (api_key or os.getenv("GEMINI_API_KEY")):
        st.error("Enter a Gemini API key or configure GEMINI_API_KEY in the server environment.")
    elif not raw_text.strip():
        st.error("Paste some package-label text first.")
    else:
        selected_key = (api_key or os.getenv("GEMINI_API_KEY", "")) if use_gemini else ""
        try:
            extractor = GeminiLabelExtractor(api_key=selected_key)
            candidates = extractor.extract_from_text(raw_text)
            report = DeterministicValidator().inspect(raw_text, candidates)
            st.caption("Candidate text only. `Supplied-text match` checks the pasted text; it does not verify the package or photo.")
            for field in report.fields.values():
                with st.expander(field.field_name, expanded=True):
                    st.write(f"**Read status:** {field.read_status}")
                    st.text(field.value or "No text found in the supplied text.")
                    if field.evidence:
                        st.write("Model/parser snippet:")
                        st.code(field.evidence)
                    st.write(f"**Supplied-text match:** {'Yes' if field.source_match else 'No'}")
            st.info(report.disclaimer)
        except (RuntimeError, ValueError) as error:
            st.error(str(error))
