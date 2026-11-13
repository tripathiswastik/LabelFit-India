# LabelFit India

An early prototype for making packaged complementary food labels easier to read. It extracts visible label wording and short evidence snippets so a caregiver can inspect the package information. It does not decide whether a product is safe or suitable, assess allergy risk, or give medical or feeding advice.

## Run locally

Requires Node.js 20 or newer. No npm packages are needed.

```powershell
$env:GEMINI_API_KEY = "your-key"
npm start
```

Open http://127.0.0.1:4173. The key stays in the local server process; do not put it in frontend code or commit it. If no key is set, the page still opens but image analysis is unavailable.

## Prototype boundaries

- Initial focus: packaged complementary foods labelled for babies 6+ months.
- It reads candidate label fields from one photo: product name, age marking, ingredients, allergen statement, nutrition panel, and preparation/storage text.
- The results are machine-read text, not verified facts. Compare each evidence snippet with the physical package. Blurry text can be misread or omitted.
- The current prototype sends the selected image to the Gemini API only when Analyze is clicked. It does not save the image or create a child profile.
- This is not a product safety check, allergy checker, health score, diagnosis, or instruction tool.

## Next steps

1. Try clear front/back label photos and record extraction errors.
2. Add local OCR as a comparison path and keep confidence/evidence visible.
3. Review privacy, model terms, label coverage, and domain feedback before testing with caregivers.
