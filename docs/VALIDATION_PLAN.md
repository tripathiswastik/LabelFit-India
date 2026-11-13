# LabelFit India: exploratory validation plan

## Purpose

Find where photo-based package transcription fails before deciding whether to build further. A 50-product set is an exploratory engineering check, not a nationally representative study or proof of accuracy.

## Sample and ground truth

- Collect 50 locally available packaged complementary-food SKUs whose own packages visibly say 6+ months or equivalent. Keep infant formula and foods for special medical purposes out of scope.
- Seek coverage across English and locally relevant Indian scripts, brands, price bands, panel layouts, print sizes, reflective/curved packs, and photo conditions. Record the mix; do not imply broad coverage if the sample is concentrated.
- Use a consistent photo protocol (front panel and one information panel per image, ordinary phone camera, practical indoor lighting). Keep original image IDs in a restricted local worksheet. Do not commit images or personal data.
- Two people independently transcribe each visible field from the package into the ground-truth sheet. Resolve disagreements by rechecking the physical pack; mark truly unreadable fields as unreadable. Do not use Gemini output to create ground truth.
- Confirm permission and privacy handling for any package photography or user research. Do not photograph people or personal information.

## Fields and scoring

For each image, compare product name, printed age marking, ingredients, explicit allergen declaration, nutrition panel, and preparation/storage text. Preserve source script, spelling, numbers, and units in the ground truth.

Track:

- **Exact field match:** whole field transcription matches after only whitespace normalization. Report numerator and denominator per field; no broad aggregate alone.
- **Character error rate (CER):** edit distance divided by ground-truth character count for text-heavy fields; report per field and per script. Do not use it as a safety metric.
- **Evidence support:** a reviewer can locate the model-provided snippet on the same photographed panel (yes/no/unclear). This checks snippet location, not full field correctness.
- **Unsupported text:** output includes wording not visible in the photo (yes/no, with error category).
- **Missing/uncertain handling:** visible fields marked not visible; absent fields hallucinated; blurry fields marked clear. Count each separately.
- **Review time:** seconds for a reviewer to compare output with package and correct it, measured in a controlled task; distinguish from scan latency.
- **Coverage:** results broken down by script/language, print size, glare/curvature, and image quality. Suppress or flag strata with too few examples.

Do not set a claim threshold in advance to make the model look successful. First define acceptable operational targets with domain reviewers, then test on a separate SKU holdout. All photos of the same SKU must stay in one split so near-identical packaging does not leak between development and evaluation. A small 50-SKU pilot cannot support a nationwide accuracy claim.

## Human review and stop conditions

Before testing with caregivers, obtain expert and privacy review. Initial testing should be an offline transcription audit with adults, not a tool that makes or influences a feeding decision. Stop and investigate if the model:

- turns package wording into safety, allergy, diagnosis, suitability, or feeding advice;
- infers an allergen declaration from ingredients;
- changes age, units, nutrient quantities, or script;
- reports unsupported text as clear/readable; or
- cannot make the provider and image handling understandable to the tester.

## Recordkeeping

Use `benchmark-template.csv` as a blank worksheet. Store image files and any identifiable research material in access-controlled storage with an agreed deletion date. Keep only the minimum data needed for error analysis. Publish sample counts and limitations alongside any result; do not describe these checks as clinical, regulatory, or safety validation.
