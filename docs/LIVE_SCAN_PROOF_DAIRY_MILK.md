# LabelFit India: Live Gemini Scan Proof (Cadbury Dairy Milk)

**Status:** Live Model Execution Proof (One Package Demonstration)  
**Date:** 2026-11-15 (Execution timestamp: 2026-11-14T21:20:44Z)  
**Code Version:** Commit `7e64575`  
**Notice:** This scan records one live execution of the literal transcription pipeline. It demonstrates software integration and normalization guard behavior on a real packaged food image; it does **not** establish overall model accuracy, clinical safety, OCR reliability, or consumer comprehension.

---

## 1. Execution Parameters

- **Input Image:** [dairy milk/27b6e6f6-7bd0-4080-bb40-fc99ceae8d2a_15251_2.avif](file:///d:/ag-ai/LabelFit%20India/dairy%20milk/27b6e6f6-7bd0-4080-bb40-fc99ceae8d2a_15251_2.avif)
  - Content: Back-of-pack information panel of *Cadbury Dairy Milk Silk Mini Treats* (135g pouch).
  - Privacy Check: Verified package-only photograph. Contains zero people, faces, hands, or personal information.
  - Conversion: Decoded via Windows WIC and rendered to PNG ([dairy milk/dairymilk.png](file:///d:/ag-ai/LabelFit%20India/dairy%20milk/dairymilk.png), 1200 × 1286 px, 593 KB) to satisfy image MIME type boundaries.
- **Model ID Requested:** `gemini-3.5-flash`
- **Model ID Responded:** `gemini-3.6-flash` (Google API server-side routing)
- **API Endpoint:** `https://generativelanguage.googleapis.com/v1beta/interactions`
- **API Revision:** `2026-05-20`
- **Storage Setting:** `store: false` (Interaction-object storage opted out)
- **Secret Hygiene:** API key loaded strictly from environment memory; zero credentials written to repository or logs.
- **Cloud Run Status:** Local execution; Cloud Run analysis spend guard remains hard-disabled.

---

## 2. Raw Model Extraction Output

```json
{
  "productName": {
    "value": "Cadbury Dairy Milk SILK Mini Treats",
    "evidence": "Cadbury Dairy Milk, SILK Mini Treats",
    "readStatus": "clear"
  },
  "ageMarking": {
    "value": "",
    "evidence": "",
    "readStatus": "not_visible"
  },
  "ingredients": {
    "value": "Ingredients: Sugar, Milk Solids (25%*), Cocoa Butter, Cocoa Solids, Emulsifiers (442, 476), Flavours (Natural, Nature Identical and Artificial (Vanilla) Flavouring Substances).",
    "evidence": "Ingredients: Sugar, Milk Solids (25%*), Cocoa Butter, Cocoa Solids, Emulsifiers (442, 476), Flavours (Natural, Nature Identical and Artificial (Vanilla) Flavouring Substances).",
    "readStatus": "clear"
  },
  "allergenDeclaration": {
    "value": "Allergen Information: Contains Milk, May Contain Tree Nuts, Wheat, Barley and Soy.",
    "evidence": "Allergen Information: Contains Milk, May Contain Tree Nuts, Wheat, Barley and Soy.",
    "readStatus": "clear"
  },
  "nutritionPanel": {
    "value": "Serving size: 9 g; No. of Servings Per Package: 15* NUTRITION INFORMATION (Per 100 g)*: Energy 543 kcal, Protein 7.6 g, Carbohydrate 58.5 g, Total Sugars 55.3 g, Added Sugars 45.9 g, Total Fat 31.2 g, Saturated Fat 21.5 g, Trans Fat 0.1 g, Cholesterol 26.7 mg, Sodium 125 mg % RDA ^ per serve - Energy 2 %, Added Sugars 8 %, Total Fat 4 %, Saturated Fat 9 %, Trans Fat 0.5 %, Sodium 1 % *Approx. Value ^Recommended Dietary Allowance requirement for average adult per day",
    "evidence": "Serving size: 9 g; No. of Servings Per Package: 15* NUTRITION INFORMATION (Per 100 g)*: Energy 543 kcal, Protein 7.6 g, Carbohydrate 58.5 g, Total Sugars 55.3 g, Added Sugars 45.9 g, Total Fat 31.2 g, Saturated Fat 21.5 g, Trans Fat 0.1 g, Cholesterol 26.7 mg, Sodium 125 mg",
    "readStatus": "clear"
  },
  "preparationAndStorage": {
    "value": "Store it in your fridge. Raid it at your will. Storage Conditions: STORE IN A COOL, HYGIENIC AND DRY PLACE. Temperature and humidity changes may cause product to develop a whitish layer, without affecting its fitness for consumption. DO NOT STORE ABOVE TEMPERATURE OF 25°C",
    "evidence": "Storage Conditions: STORE IN A COOL, HYGIENIC AND DRY PLACE. Temperature and humidity changes may cause product to develop a whitish layer, without affecting its fitness for consumption. DO NOT STORE ABOVE TEMPERATURE OF 25°C",
    "readStatus": "clear"
  }
}
```

---

## 3. Server Normalization & Physical Packaging Audit

Each candidate field was normalized through `server.js` (`normalizeExtraction`) and audited against the physical package label:

| Target Field | Model Stated Status | Normalized Server Status | Physical Package Comparison & Defense Audit |
|---|---|---|---|
| **Product Name** | `clear` | `clear` | **Verified Match.** Packaging top-left header reads `Cadbury Dairy Milk Silk Mini Treats`. Token overlap is complete. |
| **Age Marking** | `not_visible` | `not_visible` | **Verified Correct Invariant.** Package is standard confectionery with zero infant or child age markings. The model correctly output empty value/evidence with `not_visible` rather than hallucinating an age range. |
| **Ingredients** | `clear` | `clear` | **Verified Exact Match.** Full transcription matches package panel verbatim (`Sugar, Milk Solids (25%*), Cocoa Butter, Cocoa Solids, Emulsifiers (442, 476)...`). No truncation or delimiter imbalance. |
| **Allergen Declaration** | `clear` | `clear` | **Verified Exact Match.** Matches printed warning: `Allergen Information: Contains Milk, May Contain Tree Nuts, Wheat, Barley and Soy.`. No unprinted allergens hallucinated. |
| **Nutrition Panel** | `clear` | `uncertain` *(Downgraded)* | **Normalization Defense Triggered.** The model transcribed the `% RDA per serve` rows in `value`, but omitted them from its `evidence` snippet. The server-side `hasTokenSupport` and `hasConflictingNumbers` guards detected unsupported tokens and conflicting numbers, safely downgrading the stated `clear` status to `uncertain`. |
| **Preparation & Storage** | `clear` | `uncertain` *(Downgraded)* | **Normalization Defense Triggered.** The model included informal marketing copy (`Store it in your fridge. Raid it at your will.`) in `value`, but anchored its evidence snippet only to the formal storage warning. Server token-subset validation caught the extra tokens and downgraded the field to `uncertain`. |

---

## 4. Key Takeaways & Limitations

1. **Demonstration, Not Validation:** This single scan confirms the local pipeline, prompt shaping, and server-side defensive normalizers operate as intended on a real packaging photo. It does not substantiate benchmark metrics across varied photo conditions or regional languages.
2. **Effective Defense Invariants:** The automatic downgrade of `nutritionPanel` and `preparationAndStorage` proves that the server normalization rules successfully prevent partial or under-evidenced model outputs from being presented to users as `clear`.
3. **Out-of-Scope Confectionery Note:** This package is an adult/family confectionery product, not a complementary infant food (6+ months). As expected, `ageMarking` returned `not_visible`. The 10-SKU benchmark will focus strictly on in-scope complementary infant food packages.
