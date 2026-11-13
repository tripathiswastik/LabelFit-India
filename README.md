# LabelFit India

> An early mobile and web prototype for making packaged complementary-food labels (6+ months) easier to read in India. It extracts visible label wording, grounds each field in short evidence snippets, and makes uncertainty visible so caregivers can inspect package information directly.

LabelFit strictly avoids product safety checks, health scores, allergy conclusions, diagnoses, or feeding advice.

---

## 1. Quickstart

### Option A: Run Node.js Web Prototype (Zero-Dependency)
Requires Node.js 20 or newer. Uses native Node.js HTTP server.

```powershell
$env:GEMINI_API_KEY = "your-gemini-api-key"
npm start
```
Open [http://127.0.0.1:4173](http://127.0.0.1:4173). The API key remains strictly in the local server process; it is never exposed to the frontend or committed to source control. If no key is set, the page still loads with status indicators.

### Option B: Run Python Inspection CLI & Test Suite
Requires Python 3.7+ with standard libraries or pytest.

```powershell
# Run the complete test suite
python -m pytest tests/

# Run CLI inspection against built-in packaging datasets
python src/labelfit/cli.py --sample cereal
python src/labelfit/cli.py --sample puree
python src/labelfit/cli.py --sample formula
```

---

## 2. Project Overview

- **Project / Startup Name**: LabelFit India
- **Event**: Startup Buildathon India 2026 (Google DeepMind | Google Cloud | H2S | NASSCOM | Headstart)
- **Stage**: Ideation & Early Prototype
- **Target Market**: India (caregivers reviewing packaged baby foods labelled 6+ months)
- **Team**: Solo Founder — Swastik Tripathi
  - **Email**: swastik.tripathi842@gmail.com
  - **LinkedIn**: [Swastik Tripathi](https://www.linkedin.com/in/swastik-tripathi-52333511a/)
  - **GitHub**: [tripathiswastik](https://github.com/tripathiswastik/)
  - **Background**: Computer Science graduate (B.Tech CSE, IIT Kanpur Applied Data Science & Machine Intelligence Certificate); backend & integrations engineer on Oracle ERP / SCM systems at Birlasoft (Cummins projects).

---

## 3. Problem & Value Proposition

### Problem
Caregivers comparing packaged complementary foods for babies 6+ months face dense, inconsistent, multi-panel label text. Locating age suitability markings, allergen warnings, ingredient listings, and preparation directions takes considerable effort and attention under high-stakes conditions.

### Solution
A structured label-reading tool that extracts and displays key package data with supporting source snippets and visible uncertainty indicators:
1. **Intake**: Photograph package panel or upload image.
2. **Structured Extraction**: Gemini multimodal model (`gemini-3.8-flash` / `gemini-1.5-flash`) parses candidate fields:
   - Product name
   - Age marking
   - Ingredients list
   - Allergen statement (declared & precautionary)
   - Nutrition panel
   - Preparation and storage text
3. **Deterministic Verification**: Code compares extractions against visible package text and reference dictionaries, highlighting exact evidence snippets and flagging missing or uncertain fields.
4. **Non-Prescriptive Philosophy**: Strictly avoids health scores, safety ratings, allergy diagnoses, or feeding advice. Decisions remain entirely with the caregiver.

---

## 4. Technical Architecture

```
[Package Photo / Upload]
           │
           ▼
[Gemini API: Structured Extraction]
  - Age marking
  - Ingredients
  - Allergen statement
  - Nutrition panel
  - Preparation text
           │
           ▼
[Deterministic Code Checks]
  - Evidence snippet validation
  - Confidence & completeness audit
  - Flag gaps & low-confidence matches
           │
           ▼
[LabelFit Interface]
  - Evidence-backed summary
  - Visible source snippets & uncertainty flags
```

### Proposed Cloud Infrastructure (Google Cloud)
- **Model / Extraction**: Gemini API (structured JSON output mode).
- **Compute**: Google Cloud Run (stateless API orchestration for intake and verification).
- **Storage**: Google Cloud Firestore (product metadata, versioned label reference sets; zero storage of child profiles).
- **Privacy & Data Handling**: Ephemeral processing of package images; no child PII collected or stored.

---

## 5. Repository Structure

```
LabelFit India/
├── README.md                          # Project documentation & Buildathon record
├── LabelFitIndiaBuildathon2026.pdf    # Official 7-slide pitch deck
├── package.json                       # Node.js prototype configuration
├── server.js                          # Native Node.js HTTP server & Gemini proxy
├── index.html                         # Web prototype markup
├── app.js                             # Client-side file intake & rendering
├── styles.css                         # Clean, responsive web UI styling
├── pyproject.toml                     # Python package & dependency specifications
├── requirements.txt                   # Python environment requirements
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

---

## 6. Submission & Asset Records

- **Pitch Deck**: [LabelFitIndiaBuildathon2026.pdf](file:///d:/ag-ai/LabelFit%20India/LabelFitIndiaBuildathon2026.pdf)
- **Pitch Deck Cloud URL**: `https://storage.googleapis.com/vision-hack2skill-production/innovator/USER02521174/1794568982620-LabelFitIndiaBuildathon2026v4.pdf`
- **Submission Updates Logged**: 2026-11-13 (16:53:57 & 16:56:16 IST)
- **Next Validation Gate**: Qualitative validation of label extraction schemas with caregivers, infant nutrition specialists, and food labelling regulatory experts before prototype build.
