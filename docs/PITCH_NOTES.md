# LabelFit India: Buildathon pitch notes

## Current project status

LabelFit India is an early working prototype from LABEL CHECK, a two-member team: Swastik Tripathi and Saumya Tripathi. It turns a photo of a package panel into candidate text fields with snippets from the same image and a read status. A local Gemini workflow and server-side checks have been demonstrated.

The repository records live Gemini scans across retail package panels, a dual-founder adjudicated ground truth for 10 Stratum-1 infant-food packages (60 fields), and a completed 5-participant caregiver usability study (20 trials across 5 complementary-food SKUs). The usability evaluation established a 76.6% inspection time reduction (20.7s baseline down to 4.8s assisted) with 100% read status comprehension, 100% physical pack reliance, and zero safety misinterpretation incidents. Exact transcription of dense nutrition panels and curved package folds remains the primary model boundary. Commercial traction and revenue are zero.

## 60–90 second pitch

Packaged food labels put important details in small print across different panels. LabelFit India is our early prototype for helping caregivers find the wording printed on packaged complementary foods labelled for babies 6 months and older.

A caregiver photographs one panel. Gemini returns candidate text for the product name, printed age marking, ingredients, allergen declaration, nutrition panel, and preparation or storage wording. Each field appears with a snippet from the image and a read status, so the caregiver can check the words against the pack. Server-side checks downgrade some results when the text and its snippet do not support each other.

We have demonstrated the local photo-to-text workflow, established dual-adjudicated ground truth across 10 Stratum-1 complementary-food packages, and completed a 5-participant caregiver usability evaluation across 20 trials. Caregivers located target wording 76.6% faster (4.8s vs 20.7s) with zero safety misinterpretations and 100% reliance on physical packs for verification. Next, we will run structured discovery interviews with retail catalog teams to evaluate demand for structured label exports while expanding our benchmark toward 50 SKUs. We welcome feedback on our evaluation methodology and B2B catalog discovery plan.

## Current evidence and demo status

- **Built:** Local photo upload, Gemini API request path, candidate-field review page, and server-side normalization checks.
- **Demonstrated:** Dual-adjudicated ground truth across 10 Stratum-1 complementary-food SKUs (60 fields); live Gemini packaging scans; and a 20-trial caregiver usability study across 5 adult participants and 5 SKUs.
- **Usability metrics:** 76.6% inspection time reduction (20.7s baseline to 4.8s assisted), 100% read status comprehension, 100% physical pack reliance, and zero safety misinterpretation incidents.
- **Boundary finding:** Exact transcription of dense nutrition panels, multi-column tables, and curved folds requires manual verification; server-side guards downgrade unsupported candidate text to uncertain.
- **Not measured:** Commercial willingness to pay, enterprise catalog retention, or revenue.
- **Privacy:** The app sends a photo to Gemini only after user confirmation. `store: false` is not a zero-retention promise; provider handling depends on API tier. Cloud Run analysis remains disabled.

## Short version

LabelFit India is a local prototype that turns a package-panel photo into candidate label text with image snippets and visible read status. Designed around packaged complementary foods labelled 6+ months, it features 10 dual-adjudicated target SKUs and a 20-trial caregiver study showing 76.6% faster inspection with zero safety misinterpretations.

## Slide-by-slide speaker notes

1. **Title:** LABEL CHECK is a two-member team building LabelFit India. Team members are Swastik Tripathi and Saumya Tripathi.
2. **Problem:** Small print and varied package layouts can make exact label wording hard to locate. Caregiver need and severity in India still need validation.
3. **Solution:** Photograph one panel, extract candidate fields, review the image snippet and status, then compare the wording with the package. The product transcribes package text; it does not assess health or allergy risk or direct feeding decisions.
4. **Architecture:** Package photo, Gemini API, Node server checks, review page. A matching snippet is not proof that a transcription is complete or correct.
5. **AI tools:** Gemini API is the current integration. Google AI Studio is planned for prompt and response-schema iteration. Cloud Run analysis is disabled.
6. **Model:** Gemini returns six candidate fields. Read status is not a calibrated confidence score.
7. **Thank You / spoken close:** “We have a working local flow, 10 dual-adjudicated infant-food SKUs, and a completed 20-trial caregiver study showing a 76.6% reduction in inspection time with zero safety errors. Next, we are conducting B2B discovery interviews with catalog operations while scaling the benchmark toward 50 SKUs. We welcome feedback on our evaluation methodology. Thank you.”

## Judge Q&A

**How do you know the extracted text is correct?**  
We established dual-founder adjudicated ground truth across 10 Stratum-1 complementary-food packages (60 fields). Each candidate extraction is paired with an image snippet, and server-side normalization downgrades any field where the text and snippet diverge. In our 20-trial caregiver evaluation, participants used snippet anchors to verify wording directly against the physical pack in 100% of trials. Dense nutrition tables and curved folds remain the hardest formats to transcribe completely.

**How is this different from OCR or a product database?**  
LabelFit explores a narrower workflow for packaged complementary foods: it shows candidate fields beside snippets from the submitted image and asks the person to check the wording against the package. We have not benchmarked it against general OCR tools or product databases.

**Does it tell a caregiver whether a food is safe or suitable?**  
No. It displays candidate transcriptions of visible package wording and does not interpret a health condition or allergy risk, rate safety, or recommend what to feed. A read status describes the text extraction, not the product.

**What happens to an uploaded image?**  
The local app does not write the image to disk or a database and sends it to Gemini only after the user confirms. `store: false` is not a zero-retention promise. Provider handling depends on the API tier. Any external pilot needs a reviewed privacy notice, access and spend controls, and a documented retention plan.

**What is the business model?**  
There is no revenue or validated business model. After improving and evaluating the transcription flow, we plan to interview brand and retailer catalog teams about their current label-digitization workflow and willingness to pay for structured exports.

**Why start with labels for 6+ months?**  
It is a defined first product category for the prototype. The tool copies the printed age marking and does not decide whether a product is suitable for a particular child. Starter formula (0–6 months) and foods for special medical purposes are outside the current scope.

## Feedback sought

We are looking for suggestions on representative Indian 6+ month products and package conditions for the next evaluation, as well as feedback on how to test the review flow responsibly with adult caregivers.
