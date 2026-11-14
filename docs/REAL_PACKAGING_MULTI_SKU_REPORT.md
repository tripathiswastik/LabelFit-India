# LabelFit India: Multi-SKU Live Scan Audit Report (Real Retail Packaging)

**Date:** 2026-11-14  
**Scope:** Live packaged food transcription audit across authentic Indian retail grocery packages.  
**Notice:** This evaluation records actual model responses and server-side defensive normalizer outcomes. It is an engineering verification check, not a clinical study or nationwide accuracy claim.

---

## 1. Summary of Evaluated SKUs

| SKU ID | Brand | Product Description | Panel Image | Status |
|---|---|---|---|---|
| `SKU-PROD-001` | **Nescafe** | Nescafe Classic Soluble Coffee (90g Jar) | `1000084112.jpg` | ✅ Transcribed |
| `SKU-PROD-002` | **Haldiram's** | Haldiram's Bhujia Sev (1 Kg Pouch) | `1000084113.jpg` | ✅ Transcribed |
| `SKU-PROD-003` | **Maggi** | Maggi Rich Tomato Ketchup Pichkoo (75g Pouch) | `1000084114.jpg` | ✅ Transcribed |
| `SKU-PROD-004` | **KKK** | KKK Poha Rice Flakes (500g Pouch) | `1000084116.jpg` | ✅ Transcribed |
| `SKU-PROD-005` | **Namaste India** | Namaste India Desi Ghee (1L Tin Can) | `1000084117.jpg` | ✅ Transcribed |
| `SKU-PROD-006` | **Amul** | Amul Pure Ghee (500 mL Plastic Jar) | `1000084121.jpg` | ✅ Transcribed |

---

## 2. Field-by-Field Results & Defense Audit

### SKU-PROD-001: Nescafe — Nescafe Classic Soluble Coffee (90g Jar)
- **Image**: `1000084112.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | SOLUBLE COFFEE POWDER | `SOLUBLE COFFEE POWDER` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Coffee Beans. | `Ingredient Coffee Beans.` | ✅ Clear Match |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `clear` | Preparation Instructions • Add- 1g of NESCAFÉ® • 1 cup (120 ... | `Preparation Instructions • Add- 1g of NE...` | ✅ Clear Match |

### SKU-PROD-002: Haldiram's — Haldiram's Bhujia Sev (1 Kg Pouch)
- **Image**: `1000084113.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Haldiram's BHUJIA | `Haldiram's BHUJIA` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Tepary Beans Flour, Edible Vegetable Oil (Cotton Seed, Corn,... | `INGREDIENTS: Tepary Beans Flour, Edible ...` | ✅ Clear Match |
| **allergenDeclaration** | `clear` | `clear` | Contains Nut. May Contain Wheat, Milk & Soy. | `Allergen Information: Contains Nut. May ...` | ✅ Clear Match |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITIONAL INFORMATION (Approximate Values) Per 100g % RDA ... | `NUTRITIONAL INFORMATION (Approximate Val...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | STORE IN A COOL & DRY PLACE, ONCE OPENED KEEP THE MATERIAL I... | `STORE IN A COOL & DRY PLACE, ONCE OPENED...` | ✅ Clear Match |

### SKU-PROD-003: Maggi — Maggi Rich Tomato Ketchup Pichkoo (75g Pouch)
- **Image**: `1000084114.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Tomato Ketchup | `Tomato Ketchup` | ✅ Clear Match |
| **ageMarking** | `clear` | `uncertain` | 8 year old child | `8 year old child` | ⚠️ Downgraded by Normalizer (RDA Footnote) |
| **ingredients** | `clear` | `clear` | Water, Tomato paste (24.5%), Sugar, Iodized salt, Thickeners... | `Water, Tomato paste (24.5%), Sugar, Iodi...` | ✅ Clear Match |
| **allergenDeclaration** | `clear` | `clear` | Allergen Note: May contain Wheat, Milk, Mustard and Soy. | `Allergen Note: May contain Wheat, Milk, ...` | ✅ Clear Match |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITIONAL INFORMATION If a serve is 1 Tbsp (9 g) NUTRITION... | `NUTRITIONAL INFORMATION If a serve is 1 ...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | STORAGE ADVICE Store In A Cool, Dry And Hygienic Place. Clos... | `STORAGE ADVICE Store In A Cool, Dry And ...` | ✅ Clear Match |

### SKU-PROD-004: KKK — KKK Poha Rice Flakes (500g Pouch)
- **Image**: `1000084116.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | KKK POHA | `KKK POHA` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | RICE FLAKES | `Ingredients: RICE FLAKES` | ✅ Clear Match |
| **allergenDeclaration** | `clear` | `clear` | Processed in a facility that also processes wheat. | `Allergen Information: Processed in a fac...` | ✅ Clear Match |
| **nutritionPanel** | `clear` | `uncertain` | Nutritional Information* (Serve Size: 30g) Serving per pack ... | `Nutritional Information* (Serve Size: 30...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | Keep in cool dry and hygienic place,away from sunlight. Stor... | `Keep in cool dry and hygienic place,away...` | ✅ Clear Match |

### SKU-PROD-005: Namaste India — Namaste India Desi Ghee (1L Tin Can)
- **Image**: `1000084117.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | नमस्ते इंडिया देसी घी | `नमस्ते इंडिया` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Ingredient: Milk Fat | `Ingredient: Milk Fat` | ✅ Clear Match |
| **allergenDeclaration** | `clear` | `clear` | Allergen Information : Contains Milk Fat | `Allergen Information : Contains Milk Fat` | ✅ Clear Match |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITIONAL INFORMATION AMOUNT PER 100 g*, Per serve and % R... | `NUTRITIONAL INFORMATION AMOUNT PER 100 g...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |

### SKU-PROD-006: Amul — Amul Pure Ghee (500 mL Plastic Jar)
- **Image**: `1000084121.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Ghee | `Ghee` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `clear` | `clear` | Allergen Information: Contains milk. | `Allergen Information: Contains milk.` | ✅ Clear Match |
| **nutritionPanel** | `clear` | `uncertain` | Nutritional Information 33 servings per container Serving si... | `Nutritional Information` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | STORE IN COOL, DRY AND HYGIENIC PLACE, AWAY FROM DIRECT SUN ... | `STORE IN COOL, DRY AND HYGIENIC PLACE` | ⚠️ Downgraded by Normalizer |
