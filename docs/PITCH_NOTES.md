# LabelFit India: Buildathon pitch notes

## Current project status

LabelFit India is an early-stage prototype by the two-member LABEL CHECK team (Swastik Tripathi and Saumya Tripathi). The project provides a photo-first packaging transcription workflow with automated defensive normalization and token-subset evidence checking.

The repository includes:
- **Live Gemini Multimodal Scans:** 18 retail packaging panels across 12 distinct brands (`gemini-3.6-flash` / `gemini-3.5-flash-lite`), audited in `docs/REAL_PACKAGING_MULTI_SKU_REPORT.md`.
- **10-SKU Empirical Benchmark:** 60 evaluated field records across 10 authentic retail packages, evaluated against physical package ground truth independently transcribed and adjudicated by Swastik and Saumya (`docs/BENCHMARK_EVALUATION_REPORT.md`).
- **Defensive Normalizer Guards:** Automated token-subset checks, FSSAI caloric/RDA guideline footnote downgrades, and medicine/supplement dosage filters in both Node.js (`server.js`) and Python (`src/labelfit/extractor.py`).
- **Caregiver Study Protocol:** Documented testing methodology in `docs/USABILITY_STUDY_PROTOCOL.md`; usability worksheet (`docs/usability-evaluation-sheet.csv`) remains blank pending consented adult caregiver sessions.
- **B2B Discovery Plan:** Neutral interview guide in `docs/B2B_DISCOVERY_PLAN.md`; zero commercial revenue or paid traction claimed.

## 60-90 second pitch

Packaged complementary-food labels spread details across multiple panels, where small print and dense tables make exact wording hard to find. We are the two-member LABEL CHECK team exploring a photo-first way to locate printed label details on packaged complementary foods labelled for babies 6 months and older.

A caregiver photographs one package panel. The Gemini API extracts candidate text for six fields: product name, printed age marking, ingredients, explicit allergen declaration, nutrition information, and preparation or storage wording. Each candidate is paired with a source snippet and an uncalibrated read status (`clear`, `uncertain`, `not_visible`). Our server-side defenses verify that evidence tokens support every clear read, downgrading unverified text.

In our empirical 10-SKU benchmark across 60 evaluated field records on authentic packages, product names and allergen declarations achieved 100% exact match, ingredients reached 80%, and our defensive normalizer successfully caught edge cases—such as FSSAI 8-year-old caloric guidelines misattributed as infant age markings and evidence truncation on complex nutrition tables. 

Our next steps are to conduct small, consented adult caregiver usability sessions under our protocol and interview brand and retailer catalog teams to test the commercial demand for structured label ingestion. As we move to the Thank You slide, we welcome feedback on our evaluation design and packaging coverage. Thank you.

## Current evidence and demo status

- **Built:** Local photo-upload interface, server-side Gemini request path, token-subset response normalizer, and text extraction engine.
- **Automated checks:** 30 Node.js unit/smoke tests and 34 Python pytest tests passing.
- **Empirical benchmark:** 10 SKUs / 60 fields audited (`docs/BENCHMARK_EVALUATION_REPORT.md`): 100% EFM on product name and allergen declaration; 90% on age marking; 80% on ingredients; 50% on prep/storage; 30% on nutrition tables.
- **Not measured:** Adult caregiver task completion timings, commercial willingness to pay, active user retention, and revenue.
- **Demo guidance:** Use live scan proofs from `prod1_tst/` (e.g. Slurrp Farm Supergrain Cereal or Cadbury Dairy Milk) to demonstrate literal transcription and normalizer defensive downgrades.

## Short version

LabelFit India is a photo-based label transcription prototype for packaged complementary foods (6+ months). It pairs candidate label fields with source snippets and an uncalibrated read status, backed by an empirical 10-SKU benchmark and automated server defenses against hallucinated text and guideline footnotes.

## Slide-by-slide speaker notes

1. **Title:** LABEL CHECK is a two-member team building LabelFit India, a photo-first label transcription prototype. The team members are Swastik Tripathi and Saumya Tripathi.
2. **Problem:** Caregivers can struggle to quickly locate exact wording across dense package panels. The scale and importance of the problem in India still need caregiver validation.
3. **Solution:** Photograph one panel, extract candidate fields, review the snippet and status, then compare against the physical package. The product displays package text; it does not interpret health or allergy risk or direct feeding decisions.
4. **Architecture:** Package photo, Gemini API, Node server defensive guards, review page. A snippet match does not prove the text is correct; token-subset checks enforce evidence backing.
5. **AI tools:** Gemini API is the current integration (`gemini-3.6-flash` and `gemini-3.5-flash-lite`); Google AI Studio is planned for prompt and schema iteration. Cloud Run analysis is disabled until spend and privacy controls exist.
6. **Model:** Gemini returns six candidate fields. Read status is a model output and is not a calibrated confidence score.
7. **Thank You / spoken close:** As this slide appears, say: “Our next step is to expand the benchmark to 50 local products, run consented caregiver usability sessions, and test the B2B catalog digitization case. We welcome your feedback. Thank you.”

## Judge Q&A

**How do you know the extracted text is correct?**  
We benchmarked 10 local retail products across 60 field evaluations against dual-transcribed ground truth by both founders. Product name and allergen statements achieved 100% exact match, while complex nutrition tables revealed evidence truncation that our server normalizer actively caught and downgraded. Software tests are separate from model accuracy evaluations.

**How is this different from OCR or a product database?**  
The project explores a narrower workflow for packaged complementary foods: candidate fields are shown beside snippets from the submitted image with strict token-subset defensive guards. General OCR and product catalogs are useful comparison points; we have not yet benchmarked LabelFit against them.

**Does it tell a caregiver whether a food is safe or suitable?**  
No. It presents candidate transcriptions of visible package wording. It does not rate safety, diagnose, interpret allergy risk, or recommend what to feed. Read status describes the model's read, not the product.

**What happens to an uploaded image?**  
The local app does not write the image to disk or a database, and sends it to Gemini only after the user confirms. `store: false` is not a zero-retention promise. Provider handling depends on the API tier. Any external pilot needs a reviewed privacy notice, access and spend controls, and a documented retention plan.

**What is the business model?**  
There is no validated business model or revenue. After transcription and privacy checks, I plan to interview brand and retailer catalog teams about their current workflow and willingness to pay for structured label digitization. No interviews or pricing signals should be claimed until they are documented.

**Why start with labels for 6+ months?**  
It is a defined first category for the prototype. The tool copies the printed age marking and does not decide whether a product is suitable for a particular child. Starter formula (0-6 months) and foods for special medical purposes are strictly outside the current scope.

## Feedback sought

We are looking for feedback on representative packaging, scripts and languages for expanding the benchmark, evaluation design, and how to test the workflow responsibly with adult caregivers before any external pilot.
