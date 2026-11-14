# LabelFit India: Synthetic prototype smoke checks

**Scope:** Automated software checks using synthetic images and mocked or disabled provider paths. These checks do not demonstrate a live Gemini scan, OCR accuracy, safety, caregiver usability, privacy compliance, or production readiness.

The smoke suite exercises request validation, server behavior without a Gemini key, response normalization, consent reset behavior, and the Cloud Run analysis lock. Synthetic image fixtures are fictional test data and are not real commercial products. Acceptance of a valid image by the parser is not evidence that the model can read it.

Run `npm test` and `node --check server.js` / `node --check app.js` for current checks. Record the actual date, runtime versions, command output, and commit for each future run. Do not copy prior test counts into this report without rerunning on the current checkout.

## Limits

No live Gemini call was verified as part of these synthetic tests. The fixture suite does not benchmark transcription against independent ground truth. Cloud Run analysis remains disabled; the lock does not provide durable authentication, abuse prevention, or spend management.
