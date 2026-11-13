# LabelFit India: pitch notes

## 60-90 second pitch

Packaged baby-food labels can put important details across several panels, and the wording and layout vary from pack to pack. LabelFit India is a solo-founder project exploring a simpler way to read those details for packaged complementary foods labelled for babies 6 months and older.

The first version is deliberately narrow. A caregiver photographs one label panel. Gemini returns candidate text for the product name, printed age marking, ingredients, an explicit allergen declaration, nutrition information, and preparation or storage wording. Each field is shown with a model-provided snippet and a read status, so the person can compare it with the package.

The current prototype transcribes text; it does not interpret health conditions or allergies, rate safety, or tell a caregiver what to feed. The next engineering milestone is an exploratory comparison on 50 locally available products, split by SKU and language, measuring exact field matches, unsupported text, and how often uncertain reads are handled correctly. After that benchmark and privacy/usability review, I will test whether retailers or food brands value label-digitization and export tools. I am building this as an idea-stage solo project, with no traction or accuracy claims yet.

## Short version

LabelFit India is a photo-based label transcription prototype for packaged complementary foods labelled 6+ months. It pairs candidate text with model-provided snippets and visible uncertainty so people can check the package themselves. I am validating transcription quality before deciding what to build next.

## Questions to expect

**How do you know the extracted text is correct?**

I do not claim accuracy yet. The next milestone is a small, exploratory 50-SKU benchmark with ground truth transcribed independently, a holdout by SKU, and results broken down by field and language. It will identify failure modes; it will not establish nationwide performance.

**How is this different from OCR or a product database?**

The current prototype is narrower than a product catalog: it reads a photo and pairs candidate fields with model-provided snippets. Barcode lookup and third-party catalog data are not implemented. The value of this workflow still needs comparison and user validation.

**Does it tell a parent whether food is safe or suitable?**

No. It displays candidate package wording for the person to check. It does not assess safety, interpret allergies or health conditions, make a feeding recommendation, or convert the printed age range into advice.

**What happens to the photo or text?**

In the web prototype, a selected image is sent to Gemini after the user confirms the upload. The local app does not save it, and the request uses `store: false`; that is not a zero-retention promise. Provider handling depends on the API tier. A public pilot needs a reviewed privacy notice, authentication, cost controls, and a clear retention/deletion plan.

**What is the business model?**

There is no validated business model or revenue yet. After accuracy, usability, and privacy gates, I would test whether food brands or retailers will pay for label-digitization/export tools. Consumer-facing paid features would need separate willingness-to-pay research.

**Why start with 6+ months?**

It is a defined first category for the prototype, not an individualized feeding rule. The tool transcribes the package's printed age marking and does not determine whether a product is right for a child.

## Ask for feedback

I am looking for feedback on label readability, representative packaging and language coverage, and a responsible way to evaluate transcription before any caregiver-facing pilot. I am not presenting the prototype as clinically or regulatorily validated.
