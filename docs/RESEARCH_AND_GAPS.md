# LabelFit India: research and gap review

Reviewed 13 November 2026 against the current repository and the product plan. This is product research, not legal advice or a regulatory determination.

## Product definition

**V1:** a photo-first transcription aid for packaged complementary foods labelled for babies 6+ months. It extracts what the pack visibly says, keeps a model-provided snippet beside each field, and marks uncertain or absent text. The caregiver checks the original package.

**Out of scope:** infant formula and foods for special medical purposes; interpreting health conditions or allergies; safety, suitability, nutrition-quality, or compliance verdicts; feeding directions; age conversion; translation; product recommendations; child profiles; saved scans; barcode/catalog lookup.

This narrow definition avoids turning label transcription into an unsupported health claim. WHO describes complementary feeding as generally beginning around 6 months and continuing through 23 months; that public-health context does not make an individual package or food appropriate for a particular child. [WHO complementary-feeding guideline](https://www.who.int/publications/i/item/9789240081864)

## Research findings and decisions

| Question / doubt | Finding | Decision in this repo |
|---|---|---|
| Is “6+ months” a simple universal product rule? | WHO guidance is population-level. FSSAI materials distinguish complementary foods from infant formula and foods for special medical purposes. | Keep the scope to printed package claims for complementary foods; do not infer readiness, age, suitability, or feeding advice. Exclude formula and special medical-purpose foods. Recheck the current Gazette before any regulated launch. [FSSAI infant nutrition compendium](https://fssai.gov.in/upload/uploadfiles/files/Comp_IFR_VERSION-II_04_01_2024.pdf) |
| Can the app decide a food is safe, harmful, or allergen-free? | No. A photo transcription does not establish product safety, individual allergy risk, or clinical suitability. | State the boundary once in the scope notice; no verdicts, scores, diagnosis, or feeding directions. Transcribe only an explicit printed allergen declaration; never infer it from ingredients. |
| Does Gemini structured output guarantee correctness? | No. Google says structured output constrains format, and application-side validation remains necessary. Vision OCR may still misread or omit text. | Validate the response shape and evidence presence; downgrade incomplete fields to `uncertain`; show the model read status as uncalibrated and require comparison with the pack. [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output?lang=rest) |
| Does `store: false` mean no data retention? | No. It opts out of Interaction-object storage, not every service log or provider data practice. Unpaid service content may be used to improve Google services and may be human reviewed; paid service use has different terms and abuse-monitoring handling. | Keep the notice explicit, avoid personal/confidential uploads, send no child profile, and do not promise zero retention. A real pilot should select and document an appropriate API tier and review current terms. [Interactions storage](https://ai.google.dev/gemini-api/docs/interactions-overview), [Gemini API terms](https://ai.google.dev/gemini-api/terms), [abuse monitoring and ZDR](https://ai.google.dev/gemini-api/docs/zdr) |
| Is a local prototype safe to expose publicly? | The prototype has no sign-in, durable quotas, billing guardrails, or user/session model. In-memory throttling is resettable. | Cloud Run analysis is hard-disabled. Do not enable it by environment flag. A pilot needs authentication, server-side quota and spend controls, monitoring, and a reviewed retention/deletion approach. |
| Should Open Food Facts be a V1 dependency? | Its catalog is community-contributed; product completeness and accuracy vary. Its database and images have separate open licenses and attribution/share-alike conditions. | No integration in V1. If added later, identify catalog data as community-sourced and secondary to package photos; review API limits, attribution, and licenses first. [OFF API documentation](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/), [OFF licensing guide](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/tutorials/license-be-on-the-legal-side/) |
| Is a 50-SKU test enough to claim accuracy in India? | No. It is a small exploratory test and can overrepresent brands, scripts, packaging styles, or regions. | Use it only to expose failure modes and decide whether to continue; report counts and strata, not a broad accuracy claim. Keep test images and labels permissioned and out of the repository. |
| Does the legal environment require another check? | FSSAI lists a 2026 *draft* infant-nutrition amendment about sucrose/fructose for products for infants up to 6 months; a draft is not an in-force requirement. FSSAI compendia are ready references, not legal documents. India’s DPDP Act and Rules use phased commencement, including child-data provisions. | No legal/compliance verdict in the product. Recheck current Gazette notifications, final FSSAI rules, DPDP commencement, consent, and child-data requirements with qualified counsel before a public or child-directed pilot. Do not present the draft as law. [FSSAI draft notice](https://fssai.gov.in/food-law/notifications?notification=draft-notification), [FSSAI regulations](https://fssai.gov.in/food-law/regulations), [DPDP Act](https://www.meity.gov.in/static/uploads/2024/02/Digital-Personal-Data-Protection-Act-2023-1.pdf), [commencement notification](https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf), [DPDP Rules](https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf) |

## Repository changes made from this review

- Replaced numeric-confidence semantics with `clear`, `uncertain`, and `not_visible` read statuses and evidence-gated normalization.
- Kept printed text in its original language/script and prohibited translation, unit normalization, allergen inference, health interpretation, and instruction-following from package text.
- Added upload consent for package-only images, package-size and MIME/signature checks, request limits, response-shape checks, and browser text rendering via `textContent`.
- Kept the API key on the server, set `store: false`, removed third-party font loading, and clarified that provider handling is not the same as local file persistence.
- Disabled Gemini analysis on Cloud Run because this prototype has no authentication or durable spend controls.
- Updated the page and README to describe current capability as transcription only; lookup and explanation are later possibilities, not implemented features.
- Added a validation protocol and a blank benchmark worksheet. No claim of extraction accuracy is made.

## Launch gates still open

1. Run the small benchmark in `VALIDATION_PLAN.md`, then review false reads and unsupported text field by field.
2. Obtain domain review from a pediatric nutrition / food-labeling expert before any caregiver-facing trial; do not present this as medical or regulatory approval.
3. Decide whether any user research with caregivers or children is needed; obtain ethics, consent, privacy, and child-data review before recruiting.
4. Pick the paid/unpaid Gemini service tier deliberately, review current terms, configure budget controls, and revise the privacy notice for the chosen deployment.
5. Before public access, implement authentication, durable rate limits, abuse protection, operational monitoring, and a tested deletion/retention process.
6. Recheck current FSSAI and DPDP Gazette requirements with qualified counsel before launch.
7. Validate whether the product-market and business hypotheses merit further work; no revenue, adoption, or partner traction is established.
