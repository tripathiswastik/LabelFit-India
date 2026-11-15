# LabelFit India: Buildathon pitch notes

## Current project status

LabelFit India is an early working prototype from LABEL CHECK, a two-member team: Swastik Tripathi and Saumya Tripathi. It turns a package-panel photo into candidate text fields with snippets from the same image and a read status. The local prototype uses the Gemini API, with Gemini 3.8 Flash as its default model, plus server-side response checks. The website is deployed on Cloud Run through GitHub Actions; Gemini analysis is disabled in that public deployment.

Ten target products have founder-entered label references. The recorded Gemini comparison covers six fields across two SKUs, so it is not an accuracy estimate. The usability sheet contains 20 illustrative protocol rows, not results from live caregiver sessions. Exact transcription of dense nutrition panels and curved package folds remains a known challenge. Commercial traction and revenue are zero.

## 60–90 second pitch

Packaged food labels put important details in small print across different panels. LabelFit India is our early prototype for helping caregivers find the wording printed on packaged complementary foods labelled for babies 6 months and older.

A caregiver photographs one panel. Gemini returns candidate text for the product name, printed age marking, ingredients, allergen declaration, nutrition panel, and preparation or storage wording. Each field appears with a snippet from the image and a read status, so the caregiver can check the words against the pack. Server-side checks downgrade some results when the text and its snippet do not support each other.

We have a working local photo-to-text flow and a deployed website; analysis remains off on Cloud Run while access, spend, and privacy controls are incomplete. Our current benchmark has four paired fields from one product, which is not enough to claim accuracy. Next, we plan to pair scans against references for the ten prepared products, expand the benchmark toward 50 SKUs, and then run a consented usability study with adult caregivers. After the core transcription workflow has been evaluated, we will speak with retailers and food brands about whether structured label exports address a real catalog need. We welcome feedback on the evaluation plan and deployment safeguards.

## Current evidence and demo status

- **Built:** Local photo upload, Gemini API request path, candidate-field review page, and server-side normalization checks.
- **Demonstrated:** Local Gemini photo-to-text flow, server-side normalization, and a deployed Cloud Run website. Gemini analysis is disabled on the deployed site.
- **Benchmark status:** Founder-entered references are prepared for 10 target products. Four Gemini fields from one SKU are paired; this is a workflow check, not an accuracy estimate.
- **Usability status:** The repository contains 20 illustrative protocol rows; no live caregiver sessions are documented. No user-benefit or safety outcome is claimed.
- **Boundary finding:** Exact transcription of dense nutrition panels, multi-column tables, and curved folds requires manual verification; server-side guards downgrade unsupported candidate text to uncertain.
- **Not measured:** Commercial willingness to pay, enterprise catalog retention, or revenue.
- **Privacy:** The app sends a photo to Gemini only after user confirmation. `store: false` is not a zero-retention promise; provider handling depends on API tier. Cloud Run analysis remains disabled.

## Short version

LabelFit India is an early label-transcription prototype for packaged complementary foods labelled 6+ months. It uses Gemini to return candidate label text with image snippets and a read status for the user to check. Its website is deployed on Cloud Run, with Gemini analysis disabled there. The next target is a paired benchmark across 10 prepared products, expanding toward 50, followed by a consented adult-caregiver usability study.

## Slide-by-slide speaker notes

1. **Title:** LABEL CHECK is a two-member team building LabelFit India. Team members are Swastik Tripathi and Saumya Tripathi.
2. **Problem:** Small print and varied package layouts can make exact label wording hard to locate. Caregiver need and severity in India still need validation.
3. **Solution:** Photograph one panel, extract candidate fields, review the image snippet and status, then compare the wording with the package. The product transcribes package text; it does not assess health or allergy risk or direct feeding decisions.
4. **Architecture:** Package photo, Gemini API, Node server checks, review page. A matching snippet is not proof that a transcription is complete or correct.
5. **AI tools:** Gemini API is in the local prototype; Google AI Studio is planned for prompt and schema iteration. GitHub Actions deploys the site to Cloud Run. The deployed site's analysis endpoint remains disabled.
6. **Model and expected enabled experience:** Gemini 3.8 Flash is the server's default model and can be configured. When online analysis is enabled behind the required controls, the review page is intended to show six candidate fields, a photo snippet, and a read status (Readable, Check text, or Not visible) for each field. The person compares the wording with the pack. The deployed Cloud Run site currently has analysis disabled; read status is not calibrated and is not a product verdict.
7. **Thank You / spoken close:** “We have a working local prototype and a website deployed on Cloud Run, with analysis kept disabled there for now. Our current paired benchmark is six fields across two products. Next, we’ll pair scans against the ten prepared references, expand toward 50 products, and then test the review flow with consented adult caregivers. We welcome feedback on these milestones and the controls needed before enabling analysis online. Thank you.”

## Judge Q&A

**How do you know the extracted text is correct?**  
We do not yet have enough paired Gemini outputs to estimate accuracy: the current comparison covers six fields across two SKUs. Ten target products have founder-entered references, and the next step is to pair scans with those references and report results by field and package condition. The 20 rows in the usability sheet are illustrative protocol data, not live caregiver observations. Dense nutrition tables and curved folds remain challenging.

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
