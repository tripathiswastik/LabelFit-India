# Audit checklist

Working checklist from a full review of the repository on 2026-11-15. Tick items as they are done. "Decision" means a founder choice is needed before anyone can act. Severity is a judgement call: **High** can mislead a reader or a user, **Med** weakens the work, **Low** is hygiene.

Not covered by this review: legal or regulatory questions, a live Gemini run, the Streamlit app running, and the older benchmark-building scripts.

## Credibility and honesty

- [ ] **High, decision.** Reconcile the usability sheet, the report banner, and the commit message. `src/labelfit/usability.py` prints a fixed "no real sessions recorded / illustrative simulation" banner on every report, while the sheet holds 8 rows described elsewhere as recorded sessions. Make the banner depend on a status the study owner sets, and keep consent records outside the repo.
- [ ] **High, decision.** Slide 6 of the deck names "Gemini 3.8 Flash", but no recorded live run used that model. Recorded runs requested `3.5` and were answered by `3.6`. Pick one model, confirm it exists for your account, and make code, docs and deck agree.
- [ ] **Med.** `LabelFitIndiaBuildathon2026.pdf` in the repo root is the *input* of `scripts/update_buildathon_pitch.py`, and its text is older than the deck to submit. Submit only `output/pdf/LABEL_CHECK_Startup_Buildathon_2026.pdf`. Do not delete the root file without changing the script.
- [ ] **Med.** "18 live scans" in the pitch notes cannot be verified from the repository. Raw responses and images are not kept, and the old batch script records no prompt fingerprint or image hash. New runs should use `scripts/scan_benchmark.js`.
- [x] Docs that quoted the old Cloud Run guard line and old test names are updated (`CLOUD_RUN_PRODUCTION_AUDIT.md`, `WORKFLOW_SCAN_PROOF.md`).
- [x] `package.json` description no longer says the app "explains" labels.

## Correctness and safety of the tool

- [x] **High.** The Python guards had their own copy of the logic and had not received the Node fixes. Hindi words were fragmented, so unrelated Hindi strings counted as "supported". Both implementations now read one shared vocabulary (`src/labelfit/guard_terms.json`) and pass the same 34 cases (`test/fixtures/guard_cases.json`).
- [x] Digit normalization now covers Devanagari, Bengali, Gurmukhi, Gujarati, Odia, Tamil, Telugu, Kannada, Malayalam and Arabic-Indic digits.
- [ ] **High, decision.** Guard strictness. The guard requires every word of the transcription to appear in the model's short snippet, while a code comment says "zero token overlap". Long fields with a short snippet are downgraded to "Check text" even when the transcription is right. Measure on ground truth before changing: build a replay tool that re-runs saved raw responses through guard variants, and report the share of fields marked Readable next to the rate of wrong Readable reads.
- [ ] **High.** The guards compare the model's value with the model's own snippet. Nothing checks that the snippet is in the image.
- [ ] **Med.** Allergen declarations in scripts other than English and Devanagari can never reach "Readable" (no marker words). Add only with native-speaker review.
- [ ] **Med, review.** The Hindi marker and allergen word lists in `guard_terms.json` have not been reviewed by a native speaker.
- [ ] **Med.** A faithfully copied but nonsensical label (for example "Calories 5mg") is accepted as Readable. Plausibility checks cover only macros over 100 g and iron over 30 mg.
- [ ] **Med.** No scope gate: infant formula and non-food labels are transcribed like any other. The README says they are out of scope but nothing enforces it.
- [ ] **Med.** One panel per image. Composite photos invite mixing text from two products, and there is no flow for combining several panels.
- [ ] **Low.** The age-marking guard patterns are English-only.

## Evidence and validity

- [ ] **High.** No scored baby-food results yet (4 rows from 1 SKU; 50 pending). Run the benchmark with `docs/BENCHMARK_RUNBOOK.md`.
- [ ] **High.** Provenance: the 4 scored rows cannot be reproduced because raw responses and images are not kept. Re-scan with `scripts/scan_benchmark.js`.
- [ ] **Med.** Keep a development set for prompt and guard changes, separate from the SKUs you report on. All photos of one SKU stay in one split.
- [ ] **Med.** The sample is a convenience sample concentrated in a few brands and one script. Report coverage with every result (the scorer does).
- [ ] **Med.** The provider routes model names to other versions over time. Record the model that responded, and re-run if it changes.
- [ ] **Med.** Ground truth is founder-entered; only 54 of 300 transcription rows are adjudicated.
- [ ] **Low.** Keep marketplace and community images out of the repository and out of published material; check each image's licence.

## Privacy, legal, compliance

- [ ] **High.** No privacy or regulatory review is recorded (see `docs/PRIVACY_AND_COMPLIANCE_GATE.md`). Required before any pilot.
- [ ] **Med.** The photo-confirmation checkbox is the only guard against people or personal details in a photo. There is no in-app privacy notice page or terms.
- [ ] **Med.** If usability sessions were run, consent records must exist and stay outside the repository.

## Product, accessibility, UX

- [x] **High.** Status badges were 8px and the privacy, consent and scope text 9–10px. Nothing is under 12px now; the main result text is 14px.
- [x] 30 text colours below the 4.5:1 AA contrast ratio were darkened, including the badges and the privacy notice (2.5:1 before).
- [x] The loading spinner respects `prefers-reduced-motion`.
- [x] Results in an Indian script are tagged with a `lang` attribute so screen readers pick a voice (one language per script; Devanagari is also used for Marathi and Nepali).
- [ ] **Med, review.** Hindi interface. Status wording must mean "text was read clearly" and never sound like "safe". Needs a Hindi reviewer and a comprehension check with caregivers.
- [ ] **Low.** The dropzone is a button that contains another button. No dark mode. No camera-capture shortcut on phones.

## Engineering and process

- [x] CI runs the Node and Python tests and a syntax check on every push and pull request (`.github/workflows/ci.yml`).
- [ ] **Decision.** Add a `LICENSE` file. Which licence is a founder choice.
- [ ] **Med.** Turn on branch protection for `main` so the tests must pass before merging.
- [x] `scripts/batch_scan_prod1.js` no longer reads a machine-specific key path and is marked legacy. Consider deleting it once nothing depends on it.
- [x] Unused imports removed (one older unused local remains in `scripts/adjudicate_transcriptions.py`).
- [ ] **Low.** `test/` (Node) and `tests/` (Python) are easy to confuse; rename when convenient. A few tests check source text instead of behaviour. The browser downscaling has no committed test.
- [ ] **Low.** Delete the merged branch `fixes/honest-claims-and-guards`.

## Business

- [ ] **High.** The problem is unvalidated: no caregiver interviews recorded, and the B2B interview log is empty.
- [ ] **Med.** Differentiation from general-purpose tools that can already read labels needs evidence. The wedge is the evidence snippet, the guards, and the baby-food focus.
- [ ] **Med.** No cost model. Each scan costs money and depends on one provider.
