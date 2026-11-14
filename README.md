# LabelFit India

LabelFit India is an idea-stage prototype by LABEL CHECK, a two-member team: Swastik Tripathi and Saumya Tripathi. It reads package text on packaged complementary foods labelled for babies 6+ months, sending a package photo to Gemini and displaying candidate transcriptions with a model-provided snippet and read status. A person must compare every result with the physical pack.

The current build is **label transcription only**. It does not translate, look up products, or explain nutrition. It does not make safety or suitability decisions, interpret allergy risk, diagnose, score health, or tell a caregiver what to feed. Infant formula and foods for special medical purposes are outside this prototype's scope.

## Run locally

Requires Node.js 20 or newer. The app has no npm dependencies.

```powershell
$env:GEMINI_API_KEY = "your-key"
npm start
```

Open <http://127.0.0.1:4173>. The API key remains in the local server process. Do not put it in browser code, commit it, or share it. Without a key the page loads, but analysis is unavailable. Set `GEMINI_MODEL` to a supported Gemini model ID to change the default `gemini-3.8-flash`.

## Experimental Python text scratchpad

This optional tool accepts pasted label text only; it does not read package photos and is not part of the main web flow. It defaults to local heading-based extraction. The Streamlit screen sends text to Gemini only after the user selects that option and confirms the data notice. Unpaid Gemini API content may be used to improve Google services and may be reviewed by people; `store: false` is not a zero-retention promise. Do not paste child, personal, confidential, or sensitive information. Its fictional samples are not real products or labels.

Requires Python 3.10 or newer:

```powershell
python -m pip install -r requirements.txt
python src/labelfit/cli.py --sample cereal
python -m streamlit run src/labelfit/app.py
```

The Python `source_match` indicator only checks whether candidate text appears in the text supplied to the tool. It does not validate a package, photo, or model accuracy. It makes no age, allergy, safety, health, or preparation recommendation.

## Image and provider handling

- The browser creates a temporary preview and sends the selected image to this server only after the user selects **Read this label** and checks the package-only confirmation.
- The server validates the file type and size, forwards the image to Gemini using `store: false`, and does not write it to disk or a database. This is not a zero-retention guarantee: provider handling still depends on the API service and billing tier, and paid API use may still have abuse-monitoring logs. Unpaid Gemini API content may be used to improve Google products and may be reviewed by people. Do not use unpaid service for confidential or personal information.
- Do not upload images containing people, child faces, names, phone numbers, addresses, or other personal details. There are no child profiles or saved scan history.
- The prototype applies a small in-memory per-IP rate limit and allows at most two concurrent analyses. Those limits reset when the process restarts and are not a production spend-control system.

## Scope and known limits

- First category: packaged complementary foods labelled for 6+ months. The printed age phrase is transcribed as printed; it is not converted into feeding guidance.
- Candidate fields: product name, printed age marking, ingredients, printed allergen declaration, nutrition panel, and preparation/storage text.
- Read status (`Readable`, `Check text`, `Not visible`) is a model output, not a calibrated confidence score. A matching-looking snippet does not prove the full field is correct.
- The model can omit, alter, or invent text, especially for small, curved, reflective, multilingual, or low-resolution print. The prototype has not yet been benchmarked; do not claim accuracy.
- Allergen wording is copied only from an explicit declaration. The model is instructed not to infer it from ingredients; this behavior still needs testing.
- No barcode lookup, Open Food Facts integration, local OCR comparison, translation, product explanation, safety scoring, or persistent storage is implemented.
- Cloud Run serves the page with analysis disabled. Do not enable public analysis: there is no account system, durable abuse prevention, or spend cap. A real pilot needs authenticated access, server-side quotas/billing alerts, a privacy review, and a documented deletion/retention approach first.

## Buildathon materials

The repository PDF is the current seven-slide pitch deck (under 5 MB). It describes the local prototype, the planned exploratory 50-SKU validation milestone, and the unvalidated B2B label-digitization hypothesis. [Spoken pitch and judge Q&A notes](docs/PITCH_NOTES.md) are in the docs folder.

## Development checks

```powershell
# Run Node.js security & smoke test suite
npm test

# Syntax & AST checks
node --check server.js
node --check app.js

# Run Python test suite
python -m pytest tests/

# Evaluate benchmark worksheet
python scripts/evaluate_benchmark.py --csv docs/benchmark-template.csv

# Evaluate a caregiver usability dataset only after verified rows are collected
python scripts/evaluate_usability.py --csv docs/usability-evaluation-sheet.csv
```

## Governance & Verification Milestones

- [Workflow Simulation Proof](docs/WORKFLOW_SCAN_PROOF.md): Local simulation check only; no live Gemini API run recorded.
- [Smoke-test notes](docs/SMOKE_TEST_REPORT.md): Synthetic software checks only; no live Gemini result or accuracy evidence.
- [50-SKU Benchmark Report](docs/BENCHMARK_50_SKU_REPORT.md): Illustrative synthetic demonstration check; exercises failure-mode harnesses, not live package accuracy.
- [Caregiver usability protocol](docs/USABILITY_STUDY_PROTOCOL.md) and [evaluation report](docs/USABILITY_EVALUATION_REPORT.md): Protocol demonstration only; no live consented sessions recorded.
- [Cloud Run production audit](docs/CLOUD_RUN_PRODUCTION_AUDIT.md): Spend guard hard-locked (`ANALYSIS_ENABLED = false`), origin checks, and security headers.
- [B2B discovery plan](docs/B2B_DISCOVERY_PLAN.md): Interview hypotheses only; zero customer interviews or pricing evidence recorded.
- [Privacy and regulatory review checklist](docs/PRIVACY_AND_COMPLIANCE_GATE.md): Preliminary engineering notes, not legal advice, a compliance audit, or an approval.
- [Exploratory Validation Plan](docs/VALIDATION_PLAN.md) & [Research & Gaps Review](docs/RESEARCH_AND_GAPS.md): Documented boundaries, non-prescriptive invariants, and uncalibrated read statuses.
