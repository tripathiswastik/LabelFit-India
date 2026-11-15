# Interface languages and translation review

LabelFit can show its interface in more than one Indian language. This file explains what is translated, how a translation gets reviewed, and how to add a language.

## What is and is not translated

- **Translated:** the interface, meaning headings, buttons, hints, the consent and privacy text, the status labels, field names, and client-side error messages.
- **Never translated:** the label text itself. The model is told to keep the printed language, script, numbers and wording, and the app shows it as returned. A Hindi pack stays Hindi on an English page, and an English pack stays English on a Hindi page (each is tagged with its own `lang` so screen readers use the right voice).
- **Left in English on purpose:** the project-status section ("Why this focus", "Build roadmap") and the footer. They state what has and has not been shown, and a claim must not drift between languages.
- **Still English:** messages that come from the server (for example "too many scans"). Translating those needs error codes from the server.

## Current status

| Language | Code | Status |
| --- | --- | --- |
| English | `en` | Source language |
| Hindi | `hi` | **Draft, not reviewed.** Not offered in the picker; reviewers preview it at `/?lang=hi`, which shows a draft banner. |

An unreviewed language is never applied from a saved choice and never appears in the picker. Only `"reviewed": true` in a locale file's `_meta` turns that on, and the tests require a reviewer name and date with it.

## How a reviewer works

1. **Get the sheet.** `node scripts/export_locale_review.js hi --out hi-review.csv` writes English beside the translation, with columns for your decision, a corrected translation, and notes.
2. **See it in context.** Start the app (`npm start`) and open `http://127.0.0.1:4173/?lang=hi`.
3. **Check these, in this order:**
   - **The three status labels** (`statusReadable`, `statusCheck`, `statusNotVisible`). They must say that the *text was read clearly*, that the user should *check the text*, and that a field was *not visible*. They must not sound like approval of the food: nothing like "OK", "good", "safe", "correct".
   - **Consent and privacy text** (`consent`, `privacyCopy`). The photo is sent to Gemini; on the unpaid tier it may be used to improve Google services and may be reviewed by people; no personal or confidential information; the app does not save the photo; `store:false` is not a promise of zero retention. A weak translation here can make the consent meaningless.
   - **Scope text** (`scopeText`). It does not give food-safety verdicts, diagnose, interpret allergy risk, or tell caregivers what to feed.
   - **Everything else** reads naturally to a caregiver (not word-for-word), read aloud. Numbers, units and `{model}`, `{name}`, `{status}` are unchanged.
4. **Send corrections back.** Someone edits `locales/<code>.json`; the tests check keys, placeholders and the points above.
5. **Check comprehension with real readers** before switching it on: adult caregivers who read that language, using the badge-comprehension question in `USABILITY_STUDY_PROTOCOL.md`, repeated in that language. English results do not carry over.
6. **Switch it on.** Set `_meta.reviewed` to `true` and fill in `reviewedBy` and `reviewedOn`.

## Adding a language

1. Copy `locales/en.json` to `locales/<code>.json` (two or three lowercase letters, for example `bn`, `ta`, `mr`).
2. Fill in `_meta` (`code`, `nativeName`, `englishName`), keep `"reviewed": false`, and translate every string. The tests fail if a key is missing or empty or a placeholder changes.
3. Add an entry for the language to `APPROVAL_WORDS` in `test/i18n.test.js`: the words that would make a status label sound like approval. The test refuses a language that has none, so someone has to think about it.
4. Run `npm test`, then follow the review steps above.

Right-to-left languages such as Urdu need layout work that has not been done; only left-to-right scripts are supported so far. Check each script on a real phone, because older Android versions can lack fonts for some Indian scripts.

## Related

- Guard word lists for allergens and numerals are separate and also need native review: `src/labelfit/guard_terms.json`.
- Interface language does not change what the model reads. To read another script well, check the scans (see `BENCHMARK_RUNBOOK.md`).
