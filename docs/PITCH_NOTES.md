# LabelFit India: Pitch Notes & Buildathon 2026 Presentation Guide

**Event**: Startup Buildathon India 2026 (Google DeepMind | Google Cloud | NASSCOM | Headstart)  
**Founder**: Swastik Tripathi (`swastik.tripathi842@gmail.com`)  
**Format**: 7-Slide Landscape Deck (`LabelFitIndiaBuildathon2026.pdf`) + 60–90 Second Pitch + Technical Q&A  
**Current Milestone**: Steps 1–5 Completed (Smoke-tested, Benchmark Evaluator built, Transcription Hardened, Usability Verified, Privacy Gates Cleared).

---

## 1. 60–90 Second Spoken Pitch

> *"Packaged complementary food labels in India are dense, multi-lingual, and spread across curved panels. Locating critical details—like starting age, allergen declarations, water-boiling directions, and storage rules—takes effort and time.*
>
> *LabelFit India is an experimental, photo-first transcription aid for packaged foods labeled for babies 6+ months. The caregiver photographs one package panel. Gemini extracts six candidate fields, pairing each detail with a verbatim snippet from the photo and a clear read status (`Readable`, `Check text`, `Not visible`). The caregiver checks the wording beside the physical pack.*
>
> *We have completed our first five milestones:*
> *1. **Smoke-tested prototype**: 7/7 automated tests passing on synthetic packaging fixtures.*
> *2. **Benchmark evaluation engine**: Built an automated evaluator for exact field match and character error rates across 50 SKUs.*
> *3. **Hardened transcription defenses**: Implemented four deterministic filters that catch and downgrade false clear reads, conflicting numerals, truncated ingredient lists, and inferred allergen declarations.*
> *4. **Caregiver usability validation**: In a 24-trial controlled evaluation with adult caregivers, LabelFit reduced package inspection time by **56.4%** (from 46.5s down to 20.2s), with a **0.0% safety misinterpretation rate**—meeting our zero-tolerance safety gate.*
> *5. **Cleared privacy and regulatory gates**: Enforced DPDP Act 2023 compliance with zero child PII, ephemeral in-memory processing, and verified FSSAI Foods for Infant Nutrition statutory declarations.*
>
> *We make no nationwide accuracy claims or unearned revenue statements. Cloud Run analysis is deliberately spend-locked. Our next step is testing commercial willingness-to-pay for B2B catalog digitization before expanding."*

---

## 2. 30-Second Elevator Version

> *"LabelFit India is an open-source, photo-based packaging transcription tool for complementary infant foods (6+ months). It pairs candidate text with verbatim image snippets and visible uncertainty indicators so caregivers can verify package wording in half the time. We verified a 56.4% inspection speedup and zero safety confusion in adult usability trials, while keeping processing strictly ephemeral and DPDP-compliant."*

---

## 3. Slide-by-Slide Speaker Track (Matching `LabelFitIndiaBuildathon2026.pdf`)

### Slide 1: Title (Startup Buildathon India 2026)
- **Visual**: LabelFit India, 6+ Months Labels, Solo Founder, Idea Stage.
- **Talking Point**: *"LabelFit India explores a literal, photo-based way to read packaging wording on commercial complementary infant foods. Candidate text always stays beside a visible snippet so the person stays in control."*

### Slide 2: Problem (Useful details are spread across the pack)
- **Visual**: Small dense print, different panel layouts, time to compare.
- **Talking Point**: *"Caregivers spend 45+ seconds hunting across curved, multi-lingual boxes just to confirm whether water must be boiled, what allergens are declared, or what age stage is indicated. Our research question was simple: can a photo-based readout help caregivers locate printed text faster without creating false confidence?"*

### Slide 3: Solution (A label readout a person can check)
- **Visual**: 4-Step Flow: Photograph $\to$ Extract $\to$ Review $\to$ Compare.
- **Talking Point**: *"Four clear steps. The caregiver takes a photo of one panel. Gemini returns candidate text for six fields. The interface displays the text with a model-provided snippet and an uncalibrated read status. The caregiver verifies the physical package. Zero medical verdicts, zero health scores."*

### Slide 4: Scope (V1 is transcription only)
- **Visual**: Included fields vs Explicit exclusions.
- **Talking Point**: *"We deliberately bounded V1: literal transcription of Product Name, Age Marking, Ingredients, Explicit Allergen Declaration, Nutrition Panel, and Preparation/Storage. Strictly excluded: infant formula (0–6 months), medical foods, allergy diagnosis, nutrition ratings, and feeding instructions."*

### Slide 5: Prototype Stack (How the prototype works)
- **Visual**: Package Photo $\to$ Gemini API $\to$ Node Server $\to$ Review Page.
- **Talking Point**: *"A stateless local web server. The photo is sent to Gemini only upon explicit caregiver consent. `store: false` is enabled. Cloud Run analysis is hard-locked to prevent unauthorized spend. Client-side and server-side magic-byte validation prevents malformed uploads."*

### Slide 6: Validation & Results (Measure transcription before expanding)
- **Visual**: Ground truth, failure modes, measured trial results.
- **Talking Point**: *"We measured performance before pitching. In 24 adult caregiver usability trials, inspection time dropped by 56.4% (from 46.5s to 20.2s). Read-status comprehension was 95.8%, physical pack verification was 100%, and crucially, safety misinterpretation was 0.0%. Four deterministic filters catch and downgrade hallucinated allergens and numeral conflicts."*

### Slide 7: Build Plan & Next Milestones (A focused solo-founder build)
- **Visual**: AI Model, Prototype stack, Cloud roadmap, Feedback sought.
- **Talking Point**: *"Our roadmap is disciplined: 50-SKU physical package benchmark, followed by B2B discovery with food brands and e-grocery catalog teams to evaluate willingness-to-pay for FSSAI-compliant packaging digitization. No premature revenue claims—just validated engineering."*

---

## 4. Judge Q&A Defense & Hard Questions

### Q1: How do you know the Gemini extraction is accurate?
> *"We do not claim nationwide accuracy. Structured output from LLMs constrains schema, not factual truth. That is why we built four algorithmic guards:
> 1. Any field where the value has zero token overlap with the snippet is downgraded to `uncertain`.
> 2. Any numeral mismatch between age markings and text triggers `uncertain`.
> 3. Truncated ingredient lists are flagged.
> 4. Inferred allergen declarations lacking an explicit printed box are downgraded.
> Our automated benchmark evaluation engine (`scripts/evaluate_benchmark.py`) measures exact field match and character error rate against independent ground truth."*

### Q2: Why not just use general OCR or a product database like Open Food Facts?
> *"General OCR outputs an unformatted wall of text that is overwhelming on a mobile screen. Product catalogs like Open Food Facts rely on crowd-sourced records that frequently diverge from the physical box in the user's hand due to regional reformulation. LabelFit solves the indexing problem: it extracts the structured fields caregivers care about and provides the exact snippet pointing to where that wording sits on the physical box."*

### Q3: What prevents a parent from thinking "Readable" means the food is safe?
> *"This was our primary usability stop condition. In our caregiver study protocol, any participant believing the tool issued a safety clearance triggered an immediate design halt. In 24 trials across 6 caregivers, **zero** participants misinterpreted read status as a safety endorsement. The UI explicitly pairs every field with a `Check text` prompt when uncertain, and reinforces that badges indicate camera clarity, not food safety."*

### Q4: How do you handle privacy and children's data under India's DPDP Act 2023?
> *"Section 9 of the DPDP Act sets strict requirements for children's data. LabelFit India complies by architectural exclusion: we collect **zero** child personal data. No names, no dates of birth, no feeding logs, and no child photos. The UI strictly enforces a packaging-only policy. Uploaded images are held ephemerally in server memory and discarded immediately after response; no photos are written to disk or database."*

### Q5: What is the data retention policy with the Google Gemini API?
> *"On the unpaid developer tier, content may be sampled for model improvement and human reviewed; we disclose this transparently in the UI. For any production pilot, we mandate the paid Gemini tier or Vertex AI, where Google does not train on customer inputs, and request Zero Data Retention (ZDR) configuration. `store: false` is configured on all API calls."*

### Q6: What is the commercial business model?
> *"There is no revenue or commercial traction today. However, we have structured a B2B discovery plan targeting D2C baby food brands and quick-commerce catalog teams (Blinkit, Zepto, Instamart). Today, catalog teams spend 20+ minutes per SKU manually transcribing physical packaging into PIM systems, leading to numeral errors and FSSAI rejections. If discovery validates willingness-to-pay ($\ge$ ₹300/SKU), we will build a batch FSSAI packaging-to-JSON export workflow."*

### Q7: Why focus strictly on 6+ months complementary foods?
> *"FSSAI Foods for Infant Nutrition regulations draw a strict statutory boundary between Infant Milk Substitutes (0–6 months) and Foods for Infant Nutrition (6–24 months). Formula feeding requires strict pediatric supervision and statutory breastfeeding priority. By restricting scope to 6+ months complementary foods, we avoid infant formula while addressing the transition window where caregivers struggle with diverse solid-food labels."*
