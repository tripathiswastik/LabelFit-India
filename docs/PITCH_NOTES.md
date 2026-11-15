# LabelFit India: Buildathon pitch notes

## Current project status

LabelFit India is an early working prototype from LABEL CHECK, a two-member team: Swastik Tripathi and Saumya Tripathi. It turns a photo of a package panel into candidate text fields with snippets from the same image and a read status. A local Gemini workflow and server-side checks have been demonstrated.

The repository records 18 live scans of retail package panels and a 10-package, 60-field comparison across mixed grocery categories; only one package in that comparison was complementary food. Separately, the founders have transcribed 10 in-scope complementary-food packages, but a Gemini result is recorded for only one package and four fields. These are workflow checks, not an infant-food accuracy benchmark. Dense nutrition and preparation/storage text remain difficult. Review time and caregiver usability have not been measured.

## 60–90 second pitch

Packaged food labels put important details in small print across different panels. LabelFit India is our early prototype for helping caregivers find the wording printed on packaged complementary foods labelled for babies 6 months and older.

A caregiver photographs one panel. Gemini returns candidate text for the product name, printed age marking, ingredients, allergen declaration, nutrition panel, and preparation or storage wording. Each field appears with a snippet from the image and a read status, so the caregiver can check the words against the pack. Server-side checks downgrade some results when the text and its snippet do not support each other.

We have demonstrated the local photo-to-text workflow and reviewed a small mixed-category sample of 10 packages. That sample included only one complementary-food package, so it does not tell us how well LabelFit works on baby-food labels. We have since transcribed 10 in-scope packages, but only one has a matching Gemini result so far. We will scan the remaining packages and score only matched fields before making category claims. Then we will run consented adult caregiver sessions to see whether the review flow is understandable. After that, we will explore whether brands or retailers need structured label exports. We welcome feedback on the scan protocol and evaluation plan.

## Current evidence and demo status

- **Built:** Local photo upload, Gemini API request path, candidate-field review page, and server-side normalization checks.
- **Demonstrated:** Live scans across 18 retail package panels; an earlier 10-package mixed-category comparison; and founder transcriptions for 10 target-category packages.
- **Scope limitation:** Only one target-category package has a corresponding Gemini result, covering four fields. This is not evidence of performance across baby-food labels.
- **Benchmark finding:** Exact transcription of nutrition panels and preparation/storage wording needs work; the server downgraded some results when snippets did not support all candidate text.
- **Not measured:** Infant-food accuracy across a meaningful sample, adult caregiver task completion, commercial willingness to pay, retention, or revenue.
- **Privacy:** The app sends a photo to Gemini only after user confirmation. `store: false` is not a zero-retention promise; provider handling depends on API tier. Cloud Run analysis remains disabled.

## Short version

LabelFit India is a local prototype that turns a package-panel photo into candidate label text with image snippets and visible read status. It is designed around packaged complementary foods labelled 6+ months. Ten target products have founder transcriptions, but only one has a matching Gemini result, so category accuracy remains untested.

## Slide-by-slide speaker notes

1. **Title:** LABEL CHECK is a two-member team building LabelFit India. Team members are Swastik Tripathi and Saumya Tripathi.
2. **Problem:** Small print and varied package layouts can make exact label wording hard to locate. Caregiver need and severity in India still need validation.
3. **Solution:** Photograph one panel, extract candidate fields, review the image snippet and status, then compare the wording with the package. The product transcribes package text; it does not assess health or allergy risk or direct feeding decisions.
4. **Architecture:** Package photo, Gemini API, Node server checks, review page. A matching snippet is not proof that a transcription is complete or correct.
5. **AI tools:** Gemini API is the current integration. Google AI Studio is planned for prompt and response-schema iteration. Cloud Run analysis is disabled.
6. **Model:** Gemini returns six candidate fields. Read status is not a calibrated confidence score.
7. **Thank You / spoken close:** “We have a working local flow and transcriptions for ten in-scope packages; one package has a matching Gemini run so far. We will complete the paired scans and score only the fields with both a model result and an adjudicated reference, then test the review experience with adult caregivers. We welcome feedback on the scan protocol and evaluation design. Thank you.”

## Judge Q&A

**How do you know the extracted text is correct?**  
We do not yet know how well it performs across its intended category. We compared 10 mixed-category package labels across 60 fields with founder-transcribed text; only one package was complementary food. Separately, ten target-category references are ready, but only one package has a matching Gemini result so far. Dense nutrition tables and preparation/storage text showed weaknesses in the earlier check.

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
