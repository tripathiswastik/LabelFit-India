# LabelFit India

> Mobile inspection tool helping caregivers read and verify packaged complementary-food labels for babies 6+ months in India.

---

## 1. Project Overview

- **Project / Startup Name**: LabelFit India
- **Event**: Startup Buildathon India 2026 (Google DeepMind | Google Cloud | H2S | NASSCOM | Headstart)
- **Stage**: Ideation
- **Target Market**: India (caregivers reviewing packaged baby foods labelled 6+ months)
- **Team**: Solo Founder — Swastik Tripathi
  - **Email**: swastik.tripathi842@gmail.com
  - **LinkedIn**: [Swastik Tripathi](https://www.linkedin.com/in/swastik-tripathi-52333511a/)
  - **GitHub**: [tripathiswastik](https://github.com/tripathiswastik/)
  - **Background**: Computer Science graduate (B.Tech CSE, IIT Kanpur Applied Data Science & Machine Intelligence Certificate); backend & integrations engineer on Oracle ERP / SCM systems at Birlasoft (Cummins projects).

---

## 2. Problem & Value Proposition

### Problem
Caregivers comparing packaged complementary foods for babies 6+ months face dense, inconsistent, multi-panel label text. Locating age suitability markings, allergen warnings, ingredient listings, and preparation directions takes considerable effort and attention under high-stakes conditions.

### Solution
A structured label-reading tool that extracts and displays key package data with supporting source snippets and visible uncertainty indicators:
1. **Scan / Enter**: Photograph package or enter barcode.
2. **Structured Extraction**: Gemini API parses candidate fields (age marking, ingredients, allergen statement, preparation text).
3. **Deterministic Verification**: Code compares extractions against visible package text and reference dictionaries, highlighting exact evidence snippets and flagging missing or uncertain fields.
4. **Non-Prescriptive Philosophy**: Strictly avoids health scores, safety ratings, allergy diagnoses, or feeding advice. Decisions remain entirely with the caregiver.

---

## 3. Technical Architecture

```
[Package Photo / Barcode]
           │
           ▼
[Gemini API: Structured Extraction]
  - Age marking
  - Ingredients
  - Allergen statement
  - Preparation text
           │
           ▼
[Deterministic Code Checks]
  - Text snippet validation
  - Confidence & completeness audit
  - Flag gaps / low-confidence matches
           │
           ▼
[LabelFit Interface]
  - Evidence-backed summary
  - Visible source snippets & uncertainty flags
```

### Proposed Cloud Infrastructure (Google Cloud)
- **Model / Extraction**: Gemini API (via Google AI Studio for prompt engineering & structured JSON schemas).
- **Compute**: Google Cloud Run (stateless API orchestration for intake and verification).
- **Storage**: Google Cloud Firestore (product metadata, versioned label reference sets; zero storage of child profiles).
- **Privacy & Data Handling**: Ephemeral processing of package images; no child PII collected or stored.

---

## 4. Submission & Asset Records

- **Pitch Deck**: [LabelFitIndiaBuildathon2026.pdf](file:///d:/ag-ai/LabelFit%20India/LabelFitIndiaBuildathon2026.pdf)
- **Pitch Deck Cloud URL**: `https://storage.googleapis.com/vision-hack2skill-production/innovator/USER02521174/1794568982620-LabelFitIndiaBuildathon2026v4.pdf`
- **Submission Updates Logged**: 2026-11-13 (16:53:57 & 16:56:16 IST)
- **Next Validation Gate**: Qualitative validation of label extraction schemas with caregivers, infant nutrition specialists, and food labelling regulatory experts before prototype build.

---

## 5. Repository Structure & Quickstart

### Project Layout
```
LabelFit India/
├── README.md                          # Project documentation & Buildathon record
├── LabelFitIndiaBuildathon2026.pdf    # Official 7-slide pitch deck
├── pyproject.toml                     # Package & dependency specifications
├── requirements.txt                   # Environment requirements
├── src/
│   └── labelfit/
│       ├── __init__.py
│       ├── models.py                  # Domain models (ExtractedField, AllergenInfo, Report)
│       ├── prompts.py                 # Gemini API system prompts & structured JSON instructions
│       ├── extractor.py               # Gemini API client with offline deterministic fallback
│       ├── validator.py               # Deterministic rule engine & evidence grounding
│       ├── cli.py                     # Command-line inspection interface
│       ├── app.py                     # Streamlit web UI prototype
│       └── samples/                   # Representative packaged baby food datasets
└── tests/
    ├── test_models.py                 # Model serialization & non-prescriptive contract tests
    ├── test_extractor.py              # Candidate extraction tests
    └── test_validator.py              # Rule engine, grounding & allergen detection tests
```

### Running Tests
```bash
python -m pytest tests/
```

### Running the CLI Inspector
```bash
# Run against standard 6+ month baby cereal sample
python src/labelfit/cli.py --sample cereal

# Run against fruit puree sample (detects preparation instruction gap)
python src/labelfit/cli.py --sample puree

# Run against 0-6 month infant formula (detects out-of-scope warning)
python src/labelfit/cli.py --sample formula
```

### Running the Interactive Web App
```bash
streamlit run src/labelfit/app.py
```


