# LabelFit India: exploratory validation plan

## Purpose

Find where photo-based package transcription fails before deciding whether to build further. The completed engineering check used 10 mixed-category products, including only one complementary-food package. The next evaluation must focus on packaged complementary foods labelled 6+ months. Any sample remains exploratory, not nationally representative or proof of safety.

## Sample and ground truth

- Collect a new target-category sample of locally available packaged complementary-food SKUs whose own packages visibly say 6+ months or equivalent. The existing mixed-category benchmark does not count toward infant-food accuracy results. Keep infant formula and foods for special medical purposes out of scope. Start with 10 in-scope SKUs, then expand toward 50 only after sourcing, transcription, and evaluation are repeatable.
- Seek coverage across English and locally relevant Indian scripts, brands, price bands, panel layouts, print sizes, reflective/curved packs, and photo conditions. Record the mix; do not imply broad coverage if the sample is concentrated.
- Use a consistent photo protocol (front panel and one information panel per image, ordinary phone camera, practical indoor lighting). Keep original image IDs in a restricted local worksheet. Do not commit images or personal data.
- Both founders independently transcribe each visible field from the package before comparing with model output. Save dated transcripts and an adjudication record; resolve disagreements by rechecking the physical pack. Mark truly unreadable fields as unreadable. Do not use Gemini output to create ground truth.
- Confirm permission and privacy handling for any package photography or user research. Do not photograph people or personal information.

## Fields and scoring

For each image, compare product name, printed age marking, ingredients, explicit allergen declaration, nutrition panel, and preparation/storage text. Preserve source script, spelling, numbers, and units in the ground truth.

Track:

- **Exact field match:** whole field transcription matches after only whitespace normalization. Report numerator and denominator per field; no broad aggregate alone.
- **Character error rate (CER):** edit distance divided by ground-truth character count for text-heavy fields; report per field and per script. Do not use it as a safety metric.
- **Snippet presence and support:** distinguish whether a snippet exists from whether a reviewer can locate it on the photographed panel. Presence alone is not evidence support; neither proves the full field is correct.
- **Unsupported text:** a reviewer checks whether output includes wording not visible in the photo (yes/no, with error category). The current benchmark's worksheet flag only identifies predictions on blank reference fields and is not a complete unsupported-text audit.
- **Missing/uncertain handling:** visible fields marked not visible; absent fields hallucinated; blurry fields marked clear. Count each separately.
- **Review time:** seconds for a reviewer to compare output with package and correct it, measured in a controlled task; distinguish from scan latency. Existing benchmark review-time values were assigned by field type, not measured, and must not be reported as usability evidence.
- **Coverage:** results broken down by script/language, print size, glare/curvature, and image quality. Suppress or flag strata with too few examples.

Do not set a claim threshold in advance to make the model look successful. First define acceptable operational targets with domain reviewers, then test on a separate SKU holdout. All photos of the same SKU must stay in one split so near-identical packaging does not leak between development and evaluation. Neither a 10- nor 50-SKU pilot supports a nationwide accuracy claim.

## Human review and stop conditions

Before testing with caregivers, obtain expert and privacy review. Initial testing should be an offline transcription audit with adults, not a tool that makes or influences a feeding decision. Stop and investigate if the model:

- turns package wording into safety, allergy, diagnosis, suitability, or feeding advice;
- infers an allergen declaration from ingredients;
- changes age, units, nutrient quantities, or script;
- reports unsupported text as clear/readable; or
- cannot make the provider and image handling understandable to the tester.

## Recordkeeping

Use `benchmark-template.csv` as a blank worksheet. For each sample, retain a stable package-image reference and source/permission record; two dated literal transcriptions; the actual model output, model ID, prompt/code version, and run date; and an adjudication record for disagreements. Keep image files and identifiable research material in access-controlled storage with an agreed deletion date. Keep only the minimum data needed for error analysis. Publish sample counts and limitations alongside any result; do not describe these checks as clinical, regulatory, or safety validation. Do not use hand-authored outputs or outputs copied from ground truth as model evaluation data. The existing repository benchmark can be scored from its CSV, but its source photos and raw batch output are not committed, so the generation step is not independently reproducible from this repository alone.
