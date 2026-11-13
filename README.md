# LabelFit India

LabelFit is an idea-stage, solo-founder prototype for reading package text on packaged complementary foods labelled for babies 6+ months. It sends a package photo to Gemini and displays candidate transcriptions with a model-provided snippet and a read status. A person must compare every result with the physical pack.

The current build is **label transcription only**. It does not translate, look up products, or explain nutrition. It does not make safety or suitability decisions, interpret allergy risk, diagnose, score health, or tell a caregiver what to feed. Infant formula and foods for special medical purposes are outside this prototype's scope.

## Run locally

Requires Node.js 20 or newer. The app has no npm dependencies.

```powershell
$env:GEMINI_API_KEY = "your-key"
npm start
```

Open <http://127.0.0.1:4173>. The API key remains in the local server process. Do not put it in browser code, commit it, or share it. Without a key the page loads, but analysis is unavailable. Set `GEMINI_MODEL` to a supported Gemini model ID to change the default `gemini-3.8-flash`.

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

## Development checks

```powershell
npm test
node --check server.js
node --check app.js
```

See [the research and launch-gap review](docs/RESEARCH_AND_GAPS.md) and [the validation protocol](docs/VALIDATION_PLAN.md) before testing with caregivers or making public accuracy claims.
