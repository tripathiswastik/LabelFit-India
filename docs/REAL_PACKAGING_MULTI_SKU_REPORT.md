# LabelFit India: Multi-SKU Live Scan Audit Report (Real Retail Packaging)

**Date:** 2026-11-15  
**Scope:** Live packaged food transcription audit across authentic Indian retail grocery packages.  
**Notice:** This evaluation records actual model responses and server-side defensive normalizer outcomes. It is an engineering verification check, not a clinical study or nationwide accuracy claim.

---

## 1. Summary of Evaluated SKUs

| SKU ID | Brand | Product Description | Panel Image | Status |
|---|---|---|---|---|
| `SKU-PROD-001` | **Nescafe** | Nescafe Classic Soluble Coffee (90g Jar) | `1000084112.jpg` | ✅ Transcribed |
| `SKU-PROD-002` | **Haldiram's** | Haldiram's Bhujia Sev (1 Kg Pouch) | `1000084113.jpg` | ✅ Transcribed |
| `SKU-PROD-003` | **Maggi** | Maggi Rich Tomato Ketchup Pichkoo (Back Panel) | `1000084114.jpg` | ✅ Transcribed |
| `SKU-PROD-003-FRONT` | **Maggi** | Maggi Rich Tomato Ketchup Pichkoo (Front Panel) | `1000084115.jpg` | ✅ Transcribed |
| `SKU-PROD-004` | **KKK** | KKK Poha Rice Flakes (500g Pouch) | `1000084116.jpg` | ✅ Transcribed |
| `SKU-PROD-005` | **Namaste India** | Namaste India Desi Ghee (Tin Front & Nutrition) | `1000084117.jpg` | ✅ Transcribed |
| `SKU-PROD-005-SIDE` | **Namaste India** | Namaste India Desi Ghee (Tin Side Manufacturer Panel) | `1000084118.jpg` | ✅ Transcribed |
| `SKU-PROD-005-LID` | **Namaste India** | Namaste India Desi Ghee (Tin Top Lid Batch & Dates) | `1000084119.jpg` | ✅ Transcribed |
| `SKU-PROD-006-SIDE` | **Amul** | Amul Pure Ghee (Jar Marketing & Serving Panel) | `1000084120.jpg` | ✅ Transcribed |
| `SKU-PROD-006` | **Amul** | Amul Pure Ghee (500 mL Plastic Jar) | `1000084121.jpg` | ✅ Transcribed |
| `SKU-PROD-007` | **Aravan Traders** | Shakti Kuttu Atta Buckwheat Flour (250g Pouch) | `IMG-20261115-WA0001.jpg` | ✅ Transcribed |
| `SKU-PROD-008` | **Fortune (AWL)** | Fortune Refined Sunflower Seed Oil (1L Pouch) | `IMG-20261115-WA0004.jpg` | ✅ Transcribed |
| `SKU-PROD-009` | **Dabur** | Dabur Hajmola Imli Tasty Digestive Tablets (Bottle) | `IMG-20261115-WA0006.jpg` | ✅ Transcribed |
| `SKU-PROD-010` | **VLCC** | VLCC Cocoa Butter Detan Glow Body Lotion (400ml Bottle) | `IMG-20261115-WA0009.jpg` | ✅ Transcribed |
| `SKU-PROD-011` | **Cadbury** | Cadbury Dairy Milk Chocolate (Back Panel) | `dairymilk.png` | ✅ Transcribed |
| `SKU-PROD-012` | **Conscious Food** | Conscious Food Millet Noodles (162g Pouch) | `millet_noodles_bop.webp` | ✅ Transcribed |
| `SKU-PROD-013-BACK` | **Slurrp Farm** | Slurrp Farm Ragi & Jowar Cereal Stars & Moons (Back Panel) | `shopping.webp` | ✅ Transcribed |
| `SKU-PROD-013-NUTRITION` | **Slurrp Farm** | Slurrp Farm Supergrain Cereal (Side Nutrition & Ingredients Panel) | `shopping (1).webp` | ✅ Transcribed |

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

### SKU-PROD-003: Maggi — Maggi Rich Tomato Ketchup Pichkoo (Back Panel)
- **Image**: `1000084114.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Tomato Ketchup | `Tomato Ketchup` | ✅ Clear Match |
| **ageMarking** | `clear` | `uncertain` | 8 year old child | `8 year old child` | ⚠️ Downgraded by Normalizer |
| **ingredients** | `clear` | `clear` | Water, Tomato paste (24.5%), Sugar, Iodized salt, Thickeners... | `Water, Tomato paste (24.5%), Sugar, Iodi...` | ✅ Clear Match |
| **allergenDeclaration** | `clear` | `clear` | Allergen Note: May contain Wheat, Milk, Mustard and Soy. | `Allergen Note: May contain Wheat, Milk, ...` | ✅ Clear Match |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITIONAL INFORMATION If a serve is 1 Tbsp (9 g) NUTRITION... | `NUTRITIONAL INFORMATION If a serve is 1 ...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | STORAGE ADVICE Store In A Cool, Dry And Hygienic Place. Clos... | `STORAGE ADVICE Store In A Cool, Dry And ...` | ✅ Clear Match |

### SKU-PROD-003-FRONT: Maggi — Maggi Rich Tomato Ketchup Pichkoo (Front Panel)
- **Image**: `1000084115.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Maggi Rich tomato Ketchup Pichkoo | `Maggi Rich tomato Ketchup Pichkoo` | ✅ Clear Match |
| **ageMarking** | `clear` | `uncertain` | 8 year old child | `8 year old child` | ⚠️ Downgraded by Normalizer |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `clear` | `uncertain` | 1 Tbsp = Energy 7 kcal 0% % of Guideline Daily Amounts of an... | `1 Tbsp = Energy 7 kcal 0%` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |

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

### SKU-PROD-005: Namaste India — Namaste India Desi Ghee (Tin Front & Nutrition)
- **Image**: `1000084117.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | नमस्ते इंडिया देसी घी | `नमस्ते इंडिया` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Ingredient: Milk Fat | `Ingredient: Milk Fat` | ✅ Clear Match |
| **allergenDeclaration** | `clear` | `clear` | Allergen Information : Contains Milk Fat | `Allergen Information : Contains Milk Fat` | ✅ Clear Match |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITIONAL INFORMATION AMOUNT PER 100 g*, Per serve and % R... | `NUTRITIONAL INFORMATION AMOUNT PER 100 g...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |

### SKU-PROD-005-SIDE: Namaste India — Namaste India Desi Ghee (Tin Side Manufacturer Panel)
- **Image**: `1000084118.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | namaste india Desi Ghee | `namaste india Agmark Desi Ghee` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `clear` | BEST BEFORE TWELVE MONTHS FROM MANUFACTURING WHEN STORED IN ... | `BEST BEFORE TWELVE MONTHS FROM MANUFACTU...` | ✅ Clear Match |

### SKU-PROD-005-LID: Namaste India — Namaste India Desi Ghee (Tin Top Lid Batch & Dates)
- **Image**: `1000084119.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |

### SKU-PROD-006-SIDE: Amul — Amul Pure Ghee (Jar Marketing & Serving Panel)
- **Image**: `1000084120.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Amul Pure Ghee | `Amul Pure Ghee` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `uncertain` | For Enhanced Taste: Add a spoon of ghee to your food and mul... | `Add a spoon of ghee to your food and mul...` | ⚠️ Downgraded by Normalizer |

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

### SKU-PROD-007: Aravan Traders — Shakti Kuttu Atta Buckwheat Flour (250g Pouch)
- **Image**: `IMG-20261115-WA0001.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `uncertain` | शक्ति कुट्टू आटा Kuttu Atta | `Kuttu Atta` | ⚠️ Downgraded by Normalizer |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | BUCKWHEAT | `INGREDIENT : BUCKWHEAT` | ✅ Clear Match |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITION FACTS SERVING SIZE 100g (Approx) Energy 345Kcal Ca... | `NUTRITION FACTS` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | How to store : In Clean, Cool & Dry Place, Free From Moistur... | `TRANSFER INTO AIRTIGHT CONTAINER AFTER O...` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-008: Fortune (AWL) — Fortune Refined Sunflower Seed Oil (1L Pouch)
- **Image**: `IMG-20261115-WA0004.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | REFINED SUNFLOWER SEED OIL | `REFINED SUNFLOWER SEED OIL` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `uncertain` | Please refer to the bracketed portion of the batch code prin... | `Refined Sunflower Oil, Antioxidants (INS...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `clear` | `uncertain` | Nutritional Information Serving Size : 15 ml/13.65 g (1 tabl... | `Nutritional Information Serving Size : 1...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | USE BY DATE IS VALID IF STORED IN A COOL, DRY PLACE. KEEP AW... | `USE BY DATE IS VALID IF STORED IN A COOL...` | ✅ Clear Match |

### SKU-PROD-009: Dabur — Dabur Hajmola Imli Tasty Digestive Tablets (Bottle)
- **Image**: `IMG-20261115-WA0006.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `uncertain` | `uncertain` | Hajmola Imli Tasty Digestive Tablets | `Imli Tasty Digestive Tablets` | ℹ️ uncertain |
| **ageMarking** | `clear` | `uncertain` | Children: 1 tablet | `Children: 1 tablet` | ⚠️ Downgraded by Normalizer |
| **ingredients** | `clear` | `uncertain` | Composition: Each Tablet is prepared/derived from: Powder mi... | `Composition: Each Tablet is prepared/der...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `uncertain` | Storage: Store in cool and dry place, protected from moistur... | `Store in cool and dry place, protected f...` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-010: VLCC — VLCC Cocoa Butter Detan Glow Body Lotion (400ml Bottle)
- **Image**: `IMG-20261115-WA0009.jpg` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | VLCC COCOA BUTTER DETAN GLOW | `VLCC COCOA BUTTER DETAN GLOW` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `uncertain` | Aqua, Paraffinum liquidum, Sunflower (Helianthus annuus) See... | `Ingredients: Aqua, Paraffinum liquidum, ...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `clear` | Directions For Use : Apply liberally all over your body afte... | `Directions For Use : Apply liberally all...` | ✅ Clear Match |

### SKU-PROD-011: Cadbury — Cadbury Dairy Milk Chocolate (Back Panel)
- **Image**: `dairymilk.png` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Cadbury Dairy Milk Silk Mini Treats | `Cadbury Dairy Milk Silk Mini Treats` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Sugar, Milk Solids (25%*), Cocoa Butter, Cocoa Solids, Emuls... | `Ingredients: Sugar, Milk Solids (25%*), ...` | ✅ Clear Match |
| **allergenDeclaration** | `clear` | `clear` | Contains Milk, May Contain Tree Nuts, Wheat, Barley and Soy. | `Allergen Information: Contains Milk, May...` | ✅ Clear Match |
| **nutritionPanel** | `clear` | `uncertain` | Serving size: 9 g; No. of Servings Per Package: 15* NUTRITIO... | `NUTRITION INFORMATION (Per 100 g)*: Ener...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | 1 Eat it. Lock it. Repeat. 2 Store it in your fridge. Raid i... | `Storage Conditions: STORE IN A COOL, HYG...` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-012: Conscious Food — Conscious Food Millet Noodles (162g Pouch)
- **Image**: `millet_noodles_bop.webp` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Millet Noodles | `Millet Noodles:` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `uncertain` | Millet Noodles: Jowar millet flour (50%), Whole wheat flour ... | `Ingredients: Millet Noodles: Jowar mille...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `clear` | `uncertain` | Allergy Advice: This product contains Wheat. Processed on a ... | `Allergy Advice: This product contains Wh...` | ⚠️ Downgraded by Normalizer |
| **nutritionPanel** | `clear` | `uncertain` | Nutrition per 100g Serving per container: 2 Serving Size 82.... | `Nutrition per 100g` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | COOKING INSTRUCTIONS Step 1: Cook noodles in boiling water f... | `COOKING INSTRUCTIONS` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-013-BACK: Slurrp Farm — Slurrp Farm Ragi & Jowar Cereal Stars & Moons (Back Panel)
- **Image**: `shopping.webp` | **Model**: `gemini-3.6-flash`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Slurrp Farm's Crunch | `WHAT'S IN SLURRP FARM'S CRUNCH?` | ✅ Clear Match |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `uncertain` | Add milk to our stars and moons, for the perfect breakfast o... | `HOW TO STORE Keep it in a cool, dry plac...` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-013-NUTRITION: Slurrp Farm — Slurrp Farm Supergrain Cereal (Side Nutrition & Ingredients Panel)
- **Image**: `shopping (1).webp` | **Model**: `gemini-3.5-flash-lite`

| Field | Stated Status | Normalized Status | Normalized Text | Evidence Snippet | Defense Audit |
|---|---|---|---|---|---|
| **productName** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Supergrain blend (sorghum (jowar), finger millet (Ragi)) (25... | `Supergrain blend (sorghum (jowar), finge...` | ✅ Clear Match |
| **allergenDeclaration** | `clear` | `clear` | Allergen Note: Contains Milk. Made in a facility that proces... | `Allergen Note: Contains Milk. Made in a ...` | ✅ Clear Match |
| **nutritionPanel** | `clear` | `clear` | Nutritional Information Serving Size: Approx 20 g Servings P... | `Nutritional Information Serving Size: Ap...` | ✅ Clear Match |
| **preparationAndStorage** | `clear` | `clear` | JUST ADD MILK | `JUST ADD MILK` | ✅ Clear Match |
