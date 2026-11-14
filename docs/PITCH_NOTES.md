# LabelFit India: Buildathon pitch notes

## Current project status

LabelFit India is an idea-stage project by the two-member LABEL CHECK team, with a local photo-upload prototype and a Gemini API request path. The team is Swastik Tripathi and Somya Tripathi. The repository has automated checks for request handling, response normalization, synthetic image intake, and the disabled Cloud Run analysis path. These are software checks; they do not establish that Gemini reads package text accurately or that caregivers benefit from the interface.

No live Gemini scan output, completed physical-package accuracy benchmark, documented caregiver study, verified customer interviews, revenue, or traction is available in the repository. Treat the usability CSV and B2B evidence rows as unverified until the founder can provide source records. Do not present their numbers, quotes, or interest signals as results.

## 60-90 second pitch

Packaged complementary-food labels can spread details across several panels, and small print and varied layouts can make it slow to find exact wording. We are the two-member LABEL CHECK team exploring a photo-first way to locate printed details on packaged complementary foods labelled for babies 6 months and older.

A person photographs one label panel. The configured Gemini API returns candidate text for six fields: product name, printed age marking, ingredients, explicit allergen declaration, nutrition information, and preparation or storage wording. Each candidate is paired with a model-provided snippet and a read status so the person can compare it with the package.

The project is at an early prototype stage. Automated tests cover parts of the software flow, but a live model result and field-level accuracy have not been demonstrated. The next milestone is an exploratory benchmark on 50 locally available products, held out by SKU and reviewed across languages. After accuracy, usability, and privacy review, I plan to test whether brands or retailers need structured label digitization. The business case is still a hypothesis. As we move to the Thank You slide, I will close with that benchmark as our next step and invite feedback.

## Current evidence and demo status

- **Built:** Local photo-upload interface, server-side Gemini request path, response normalization, source-snippet checks, and a separate text-only extraction scratchpad.
- **Automated checks:** Node and Python test suites cover software behavior. Synthetic packaging fixtures exercise file intake and missing-field handling.
- **Not measured:** Gemini transcription accuracy, caregiver task performance, safety-status comprehension, willingness to pay, active users, and revenue.
- **Demo guidance:** A synthetic image can demonstrate upload handling after a local smoke test. Do not present a synthetic fixture test as a live Gemini scan or an accuracy result.

## Short version

LabelFit India is an early photo-based transcription prototype for packaged complementary foods labelled 6+ months. It pairs candidate label fields with model-provided snippets and read status so a person can check the printed wording. Its next milestone is an exploratory 50-SKU accuracy benchmark.

## Slide-by-slide speaker notes

1. **Title:** LABEL CHECK is a two-member team building LabelFit India, a photo-first label transcription prototype. The team members are Swastik Tripathi and Somya Tripathi.
2. **Problem:** Caregivers can struggle to quickly locate exact wording across dense package panels. The scale and importance of the problem in India still need caregiver validation.
3. **Solution:** Photograph one panel, extract candidate fields, review the snippet and status, then compare against the physical package. The product displays package text; it does not interpret health or allergy risk or direct feeding decisions.
4. **Architecture:** Package photo, Gemini API, Node server checks, review page. A snippet match does not prove the text is correct.
5. **AI tools:** Gemini API is the current integration; Google AI Studio is planned for prompt and schema iteration. Cloud Run analysis is not enabled.
6. **Model:** Gemini returns six candidate fields. Read status is a model output and is not a calibrated confidence score.
7. **Thank You / spoken close:** As this slide appears, say: “Our next step is to benchmark 50 local products, then review accuracy, usability and privacy before testing the business case. We welcome feedback on the benchmark and the workflow. Thank you.”

## Judge Q&A

**How do you know the extracted text is correct?**  
We do not have an accuracy result yet. The repository includes an evaluator for a future independently transcribed SKU set. The next step is to run it on held-out products and publish errors by field and language. Software tests are not model-accuracy tests.

**How is this different from OCR or a product database?**  
The project is exploring a narrower workflow for packaged complementary foods: candidate fields are shown beside snippets from the submitted image. General OCR and product catalogs are useful comparison points. I have not yet benchmarked LabelFit against them or established that its workflow is more accurate or useful.

**Does it tell a caregiver whether a food is safe or suitable?**  
No. It presents candidate transcriptions of visible package wording. It does not rate safety, diagnose, interpret allergy risk, or recommend what to feed. Read status describes the model's read, not the product.

**What happens to an uploaded image?**  
The local app does not write the image to disk or a database, and sends it to Gemini only after the user confirms. `store: false` is not a zero-retention promise. Provider handling depends on the API tier. Any external pilot needs a reviewed privacy notice, access and spend controls, and a documented retention plan.

**What is the business model?**  
There is no validated business model or revenue. After transcription and privacy checks, I plan to interview brand and retailer catalog teams about their current workflow and willingness to pay for structured label digitization. No interviews or pricing signals should be claimed until they are documented.

**Why start with labels for 6+ months?**  
It is a defined first category for the prototype. The tool copies the printed age marking and does not decide whether a product is suitable for a particular child. Formula and foods for special medical purposes are outside the current scope.

## Feedback sought

I am looking for feedback on representative packaging, scripts and languages for the benchmark, evaluation design, and how to test the workflow responsibly before any caregiver-facing pilot.
