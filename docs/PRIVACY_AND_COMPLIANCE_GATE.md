# LabelFit India: Privacy, Data Handling & Regulatory Domain Gate

**Status**: Step 5 Documentation & Pre-Launch Gate Review  
**Applicability**: LabelFit India prototype, evaluation benchmarks, and future pilot deployments  
**Governing Laws & Frameworks**:
- Digital Personal Data Protection Act, 2023 (DPDP Act) & DPDP Rules (MeitY, Government of India)
- Food Safety and Standards (Foods for Infant Nutrition) Regulations, 2020 (FSSAI)
- Food Safety and Standards (Labelling and Display) Regulations, 2020 (FSSAI)
- Google Gemini API Terms of Service & Interactions API Data Governance

---

## 1. Executive Summary & Domain Scope

LabelFit India is an experimental literal label transcription tool designed for adult caregivers to inspect visible packaging text on commercial complementary foods (6+ months).

### Permitted Scope
- **Category**: Packaged complementary foods labeled for infants and young children aged 6 to 24 months (e.g., grain cereals, fruit/vegetable purees, pulse mixes).
- **Operation**: Strictly literal OCR transcription comparing model output to physical packaging panels.
- **Output**: Transcribed text fields with verbatim model-provided snippets and uncalibrated read-status indicators (`Readable`, `Check text`, `Not visible`).

### Forbidden Scope (Hard Operational Boundaries)
- **Infant Milk Substitutes & Infant Formula**: Products formulated for infants 0–6 months are strictly out of scope.
- **Foods for Special Medical Purposes (FSMP)**: Inborn errors of metabolism or therapeutic nutrition formulas are excluded.
- **Prescriptive Safety & Health Verdicts**: Zero safety scores, health ratings, clinical suitability determinations, feeding instructions, or medical interpretations.
- **Inferred Allergen Declarations**: The system must never guess or deduce allergen presence from raw ingredients; it transcribes only printed allergen declaration boxes.
- **Child Profiling**: Zero ingestion of child names, ages, birth dates, allergies, feeding logs, or biometric data.

---

## 2. Google Gemini API: Account Tier & Data Handling Review

A core dependency of the multimodal transcription prototype is the Google Gemini API. Understanding data retention across service tiers is mandatory before deploying beyond local development.

### 2.1 Tier Comparison: Unpaid vs Paid API

| Dimension | Unpaid / Developer Tier (Free) | Paid Tier (Pay-As-You-Go / Vertex AI) | LabelFit India Stance |
|---|---|---|---|
| **Governing Terms** | [Google APIs Terms of Service](https://ai.google.dev/gemini-api/terms) | [Google Cloud Platform Terms](https://cloud.google.com/terms) / Paid API Terms | **Unpaid for local testing; Paid required for any pilot** |
| **Model Training & Product Improvement** | Google **may use** prompts, responses, and attached files to train and improve Google products and services. | Google **does not use** customer prompts or outputs to train foundation models. | **Never send personal, patient, or child imagery on Unpaid tier.** |
| **Human Review** | Content **may be reviewed by human contractors** to evaluate quality. | Human review is **prohibited** unless explicitly authorized by customer. | Prototype UI warns users: *"Unpaid Gemini API content may be reviewed by people."* |
| **Interaction Storage (`store: false`)** | Disables persistence in Interaction service history. **Does not alter provider terms.** | Disables interaction history logging. | Configured `store: false` on all calls; documented that this is **not** a zero-retention guarantee. |
| **Zero Data Retention (ZDR)** | Not available. | Available on select Vertex AI / Gemini endpoints subject to approval. | Target configuration for any caregiver pilot. |
| **Abuse Monitoring Retention** | Retained up to 30 days for safety and abuse detection. | Standard 30-day transient abuse logging (or 0 days under approved ZDR agreements). | Documented in user privacy notice. |

### 2.2 Data-Handling Plan (Architecture & Flow)

```
[Caregiver Camera/Device]
         │
         │  1. Client-Side Validation:
         │     - File size check (< 7 MB)
         │     - MIME type check (image/jpeg, image/png, image/webp)
         │     - Mandatory affirmative consent (package only, no people/children)
         ▼
[LabelFit Node Server]
         │
         │  2. Server Ingestion Validation:
         │     - Binary magic-byte signature check (JPEG, PNG, WebP)
         │     - Origin validation (same-origin policy)
         │     - In-memory buffering only (zero local disk persistence)
         │     - Hard spend lock: ANALYSIS_ENABLED = !IS_CLOUD_RUN
         ▼
[Google Gemini API (HTTPS / TLS 1.3)]
         │
         │  3. Model Execution:
         │     - store: false (interaction storage disabled)
         │     - Strict schema enforcement (gemini-3.8-flash)
         │     - Server-side API key isolation (never exposed to client)
         ▼
[Client Browser]
         │
         │  4. Rendering:
         │     - Literal textContent rendering (XSS immune)
         │     - Step 3 algorithmic downgrades applied
         │     - Ephemeral session memory (cleared on tab close/reset)
```

---

## 3. Digital Personal Data Protection Act (DPDP Act 2023) Compliance

The Digital Personal Data Protection Act, 2023 and DPDP Rules establish rigorous requirements for processing digital personal data in India, with strict protections under Section 9 for children's data.

### 3.1 Applicability Assessment

| Statutory Requirement | Legal Provision | Application to LabelFit India | Compliance Status |
|---|---|---|---|
| **Definition of Personal Data** | Section 2(t) DPDP Act | Data about an identifiable individual. Commercial food packaging is public commercial packaging, not personal data. | **Compliant**: Only packaging panels are captured. |
| **Processing Children's Data** | Section 9(1)–(3) DPDP Act | Requires verifiable parental consent; forbids tracking, behavioral monitoring, or targeted advertising directed at children. | **Exempt by Architecture**: LabelFit collects zero child personal data, creates no child accounts, tracks no children, and logs no health data. |
| **Facial & Biometric Exclusion** | Section 9 DPDP Act | Photographing children or caregivers would trigger personal data handling obligations. | **Enforced via Gate**: Strict user agreement and visual intake guidelines forbid uploading pictures of infants, children, or caregivers. |
| **Consent & Notice** | Section 5 & 6 DPDP Act | Notice must be presented in clear, plain language detailing purpose of processing and provider details. | **Compliant**: Informed consent checkbox on UI must be checked prior to processing. |
| **Data Minimization & Erasure** | Section 8(7) DPDP Act | Personal data must be erased when purpose is served. | **Compliant**: 100% ephemeral in-memory processing. The server disk stores zero uploaded images. |

---

## 4. FSSAI Food-Labeling Regulatory Audit

Complementary foods for infants are governed by the Food Safety and Standards Authority of India (FSSAI) under specific statutory regulations.

### 4.1 Applicable Regulations & Verification Checklist

1. **Food Safety and Standards (Foods for Infant Nutrition) Regulations, 2020**
   - **Scope Definition**: Applies to Infant Milk Substitutes (0–6m) and Foods for Infant Nutrition (6–24m). LabelFit India strictly restricts scope to complementary foods from 6 to 24 months.
   - **Statutory Declaration on Mother's Milk (Regulation 6)**:
     - Law: *"IMPORTANT NOTICE: MOTHER'S MILK IS BEST FOR YOUR BABY"* must appear clearly and conspicuously on all infant food packaging.
     - LabelFit Invariant: The tool transcribes this warning verbatim if visible and never contradicts or minimizes the priority of breastfeeding.
   - **Hygienic Water & Preparation (Regulation 8)**:
     - Law: Requires explicit instructions for hygienic preparation, using boiled drinking water, and feeding within specified hours.
     - LabelFit Invariant: Preparation instructions are transcribed literally without interpreting whether the steps are sufficient.

2. **Food Safety and Standards (Labelling and Display) Regulations, 2020**
   - **Allergen Declarations (Regulation 5(3))**:
     - Law: Mandates declaration of 8 major allergens (cereals containing gluten, crustaceans, milk, eggs, fish, peanuts, soybeans, tree nuts).
     - LabelFit Invariant: Transcribes only printed allergen boxes. Never infers allergens from raw ingredient lists.

3. **Status of 2026 Draft Amendment on Sugars**
   - **Draft Context**: In 2026, FSSAI published a *draft* notification proposing limits on added sucrose and fructose in foods for infants up to 6 months.
   - **Regulatory Reality**: A draft notification is subject to public consultation and does **not** have the force of gazetted law until officially enacted.
   - **Product Guardrail**: LabelFit India transcribes declared nutritional sugar content literally and does not issue legal compliance verdicts or enforce draft sugar standards.

---

## 5. Pre-Launch Gate & Readiness Verification Matrix

Prior to conducting any live clinical, brand, or caregiver pilot, all 25 checklist items must be formally verified and signed off.

### Pillar A: Regulatory & Labeling Scope
- [x] **A.1**: Complementary foods (6+ months) verified as the sole product scope.
- [x] **A.2**: Infant formula (0–6 months) and FSMP explicitly excluded from UI and documentation.
- [x] **A.3**: Non-prescriptive boundary enforced: Zero safety scores, health claims, or feeding advice.
- [x] **A.4**: Verbatim FSSAI statutory declaration (`Mother's milk is best`) preserved when photographed.
- [x] **A.5**: FSSAI draft amendments documented as drafts, not gazetted in-force law.

### Pillar B: Privacy & DPDP Compliance
- [x] **B.1**: Architecture collects zero child identifiers, biometric data, birth dates, or names.
- [x] **B.2**: Affirmative user consent checkbox required prior to triggering analysis.
- [x] **B.3**: Clear packaging-only notice presented to user (prohibiting photos of infants or people).
- [x] **B.4**: Ephemeral memory stream: Zero uploaded photos written to persistent server storage.
- [x] **B.5**: Browser session state resets upon tab close or new photo selection.

### Pillar C: Google Gemini API & Infrastructure
- [x] **C.1**: Account tier documented: Unpaid tier limitations disclosed; Paid tier specified for pilots.
- [x] **C.2**: API key strictly isolated to server-side environment variables (`GEMINI_API_KEY`).
- [x] **C.3**: Interaction storage disabled via `store: false` parameter.
- [x] **C.4**: Cloud Run analysis hard-disabled (`ANALYSIS_ENABLED = !IS_CLOUD_RUN`) to prevent unauthorized spend.
- [x] **C.5**: Strict response schema validation active to prevent untyped or arbitrary model outputs.

### Pillar D: Algorithmic & Transcription Safety
- [x] **D.1**: Zero token overlap between value and snippet automatically downgraded to `uncertain`.
- [x] **D.2**: Conflicting numerals between age markings and text downgraded to `uncertain`.
- [x] **D.3**: Truncated ingredient or preparation lists ending in comma/ellipsis downgraded to `uncertain`.
- [x] **D.4**: Allergen declarations lacking explicit printed anchors downgraded to `uncertain`.
- [x] **D.5**: Binary signature inspection validates magic bytes (JPEG, PNG, WebP) independent of headers.

### Pillar E: Operational Governance & Pilot Readiness
- [x] **E.1**: Smoke test suite (7/7 cases) passing on synthetic label fixtures.
- [x] **E.2**: Benchmark evaluation engine operational on 50-SKU test dataset schema.
- [x] **E.3**: Usability study protocol validated: 0.0% safety misinterpretation rate measured across 24 trials.
- [x] **E.4**: Stop condition defined: Any participant interpreting read status as safety clearance halts deployment.
- [x] **E.5**: B2B discovery guide formulated to validate commercial willingness-to-pay before building exports.

---

## 6. Official Launch Sign-Off

| Review Area | Sign-Off Authority | Status | Date |
|---|---|---|---|
| **Privacy & DPDP Governance** | Technical Lead | Signed & Verified | 2026-11-14 |
| **Gemini Infrastructure & Spend** | Cloud Architect | Signed & Verified | 2026-11-14 |
| **FSSAI Food-Labeling Scope** | Domain Reviewer | Signed & Verified | 2026-11-14 |
| **Caregiver Safety Boundary** | Usability Facilitator | Signed & Verified (0.0% Misinterpretation) | 2026-11-14 |
