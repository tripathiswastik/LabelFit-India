# LabelFit India: Multi-SKU Live Scan Audit Report (Real Retail Packaging)

**Date:** 2026-11-15  
**Scope:** Live packaged food transcription audit across authentic Indian retail grocery packages.  
**Notice:** This log shows model output and normalizer status only; it does not compare output with ground truth or independently verify text against package photos. A retained `clear` status is not an accuracy result. The batch script uses its own prompt and model fallback chain, so this does not measure the web app flow. Photos and raw scan records are local-only and are not included in this repository, so this report cannot be independently reproduced from the repository alone.

---

**Coverage:** 22 reported outputs for 23 scanner-configured panels. `SKU-PROD-018` is configured in the scanner but has no entry in this report; the repository does not include a failure record explaining why.

## 1. Summary of Evaluated SKUs

| SKU ID | Brand | Product Description | Panel Image | Status |
|---|---|---|---|---|
| `SKU-PROD-001` | **Nescafe** | Nescafe Classic Soluble Coffee (90g Jar) | `1000084112.jpg` | Output available |
| `SKU-PROD-002` | **Haldiram's** | Haldiram's Bhujia Sev (1 Kg Pouch) | `1000084113.jpg` | Output available |
| `SKU-PROD-003` | **Maggi** | Maggi Rich Tomato Ketchup Pichkoo (Back Panel) | `1000084114.jpg` | Output available |
| `SKU-PROD-003-FRONT` | **Maggi** | Maggi Rich Tomato Ketchup Pichkoo (Front Panel) | `1000084115.jpg` | Output available |
| `SKU-PROD-004` | **KKK** | KKK Poha Rice Flakes (500g Pouch) | `1000084116.jpg` | Output available |
| `SKU-PROD-005` | **Namaste India** | Namaste India Desi Ghee (Tin Front & Nutrition) | `1000084117.jpg` | Output available |
| `SKU-PROD-005-SIDE` | **Namaste India** | Namaste India Desi Ghee (Tin Side Manufacturer Panel) | `1000084118.jpg` | Output available |
| `SKU-PROD-005-LID` | **Namaste India** | Namaste India Desi Ghee (Tin Top Lid Batch & Dates) | `1000084119.jpg` | Output available |
| `SKU-PROD-006-SIDE` | **Amul** | Amul Pure Ghee (Jar Marketing & Serving Panel) | `1000084120.jpg` | Output available |
| `SKU-PROD-006` | **Amul** | Amul Pure Ghee (500 mL Plastic Jar) | `1000084121.jpg` | Output available |
| `SKU-PROD-007` | **Aravan Traders** | Shakti Kuttu Atta Buckwheat Flour (250g Pouch) | `IMG-20261115-WA0001.jpg` | Output available |
| `SKU-PROD-008` | **Fortune (AWL)** | Fortune Refined Sunflower Seed Oil (1L Pouch) | `IMG-20261115-WA0004.jpg` | Output available |
| `SKU-PROD-009` | **Dabur** | Dabur Hajmola Imli Tasty Digestive Tablets (Bottle) | `IMG-20261115-WA0006.jpg` | Output available |
| `SKU-PROD-010` | **VLCC** | VLCC Cocoa Butter Detan Glow Body Lotion (400ml Bottle) | `IMG-20261115-WA0009.jpg` | Output available |
| `SKU-PROD-011` | **Cadbury** | Cadbury Dairy Milk Chocolate (Back Panel) | `dairymilk.png` | Output available |
| `SKU-PROD-012` | **Conscious Food** | Conscious Food Millet Noodles (162g Pouch) | `millet_noodles_bop.webp` | Output available |
| `SKU-PROD-013-BACK` | **Slurrp Farm** | Slurrp Farm Ragi & Jowar Cereal Stars & Moons (Back Panel) | `shopping.webp` | Output available |
| `SKU-PROD-013-NUTRITION` | **Slurrp Farm** | Slurrp Farm Supergrain Cereal (Side Nutrition & Ingredients Panel) | `shopping (1).webp` | Output available |
| `SKU-PROD-014` | **Nestle Maggi** | Maggi 2-Minute Masala Noodles (70g Pouch Back Panel) | `maggi-2-minute-noodles-1000x1000.webp` | Output available |
| `SKU-PROD-015` | **Nestle Maggi** | Maggi Nutri-Licious Masala Atta Noodles (Back Panel) | `MaggiAttaNoodlesIngredients.jpg` | Output available |
| `SKU-PROD-016` | **McCain** | McCain Veggie Burger Patty (360g Pack Back Panel) | `mccain-popular-vege-burger-patty-1000x1000.webp` | Output available |
| `SKU-PROD-017` | **Nestle Maggi** | Maggi 2-Minute Masala Noodles (70g Pack Back & Recipe Panel) | `s-l400.jpg` | Output available |

---

## 2. Model Output & Normalizer Status

### SKU-PROD-001: Nescafe — Nescafe Classic Soluble Coffee (90g Jar)
- **Image**: `1000084112.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | SOLUBLE COFFEE POWDER | `SOLUBLE COFFEE POWDER` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Coffee Beans. | `Ingredient Coffee Beans.` | Clear status retained; not independently verified |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `clear` | Preparation Instructions • Add- 1g of NESCAFÉ® • 1 cup (120 ... | `Preparation Instructions • Add- 1g of NE...` | Clear status retained; not independently verified |

### SKU-PROD-002: Haldiram's — Haldiram's Bhujia Sev (1 Kg Pouch)
- **Image**: `1000084113.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Haldiram's BHUJIA | `Haldiram's BHUJIA` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Tepary Beans Flour, Edible Vegetable Oil (Cotton Seed, Corn,... | `INGREDIENTS: Tepary Beans Flour, Edible ...` | Clear status retained; not independently verified |
| **allergenDeclaration** | `clear` | `clear` | Contains Nut. May Contain Wheat, Milk & Soy. | `Allergen Information: Contains Nut. May ...` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITIONAL INFORMATION (Approximate Values) Per 100g % RDA ... | `NUTRITIONAL INFORMATION (Approximate Val...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | STORE IN A COOL & DRY PLACE, ONCE OPENED KEEP THE MATERIAL I... | `STORE IN A COOL & DRY PLACE, ONCE OPENED...` | Clear status retained; not independently verified |

### SKU-PROD-003: Maggi — Maggi Rich Tomato Ketchup Pichkoo (Back Panel)
- **Image**: `1000084114.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Tomato Ketchup | `Tomato Ketchup` | Clear status retained; not independently verified |
| **ageMarking** | `clear` | `uncertain` | 8 year old child | `8 year old child` | ⚠️ Downgraded by Normalizer |
| **ingredients** | `clear` | `clear` | Water, Tomato paste (24.5%), Sugar, Iodized salt, Thickeners... | `Water, Tomato paste (24.5%), Sugar, Iodi...` | Clear status retained; not independently verified |
| **allergenDeclaration** | `clear` | `clear` | Allergen Note: May contain Wheat, Milk, Mustard and Soy. | `Allergen Note: May contain Wheat, Milk, ...` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITIONAL INFORMATION If a serve is 1 Tbsp (9 g) NUTRITION... | `NUTRITIONAL INFORMATION If a serve is 1 ...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | STORAGE ADVICE Store In A Cool, Dry And Hygienic Place. Clos... | `STORAGE ADVICE Store In A Cool, Dry And ...` | Clear status retained; not independently verified |

### SKU-PROD-003-FRONT: Maggi — Maggi Rich Tomato Ketchup Pichkoo (Front Panel)
- **Image**: `1000084115.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Maggi Rich tomato Ketchup Pichkoo | `Maggi Rich tomato Ketchup Pichkoo` | Clear status retained; not independently verified |
| **ageMarking** | `clear` | `uncertain` | 8 year old child | `8 year old child` | ⚠️ Downgraded by Normalizer |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `clear` | `uncertain` | 1 Tbsp = Energy 7 kcal 0% % of Guideline Daily Amounts of an... | `1 Tbsp = Energy 7 kcal 0%` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |

### SKU-PROD-004: KKK — KKK Poha Rice Flakes (500g Pouch)
- **Image**: `1000084116.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | KKK POHA | `KKK POHA` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | RICE FLAKES | `Ingredients: RICE FLAKES` | Clear status retained; not independently verified |
| **allergenDeclaration** | `clear` | `clear` | Processed in a facility that also processes wheat. | `Allergen Information: Processed in a fac...` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `uncertain` | Nutritional Information* (Serve Size: 30g) Serving per pack ... | `Nutritional Information* (Serve Size: 30...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | Keep in cool dry and hygienic place,away from sunlight. Stor... | `Keep in cool dry and hygienic place,away...` | Clear status retained; not independently verified |

### SKU-PROD-005: Namaste India — Namaste India Desi Ghee (Tin Front & Nutrition)
- **Image**: `1000084117.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `uncertain` | नमस्ते इंडिया देसी घी | `नमस्ते इंडिया` | ⚠️ Downgraded by Normalizer |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Ingredient: Milk Fat | `Ingredient: Milk Fat` | Clear status retained; not independently verified |
| **allergenDeclaration** | `clear` | `clear` | Allergen Information : Contains Milk Fat | `Allergen Information : Contains Milk Fat` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITIONAL INFORMATION AMOUNT PER 100 g*, Per serve and % R... | `NUTRITIONAL INFORMATION AMOUNT PER 100 g...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |

### SKU-PROD-005-SIDE: Namaste India — Namaste India Desi Ghee (Tin Side Manufacturer Panel)
- **Image**: `1000084118.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | namaste india Desi Ghee | `namaste india Agmark Desi Ghee` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `clear` | BEST BEFORE TWELVE MONTHS FROM MANUFACTURING WHEN STORED IN ... | `BEST BEFORE TWELVE MONTHS FROM MANUFACTU...` | Clear status retained; not independently verified |

### SKU-PROD-005-LID: Namaste India — Namaste India Desi Ghee (Tin Top Lid Batch & Dates)
- **Image**: `1000084119.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |

### SKU-PROD-006-SIDE: Amul — Amul Pure Ghee (Jar Marketing & Serving Panel)
- **Image**: `1000084120.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Amul Pure Ghee | `Amul Pure Ghee` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `uncertain` | For Enhanced Taste: Add a spoon of ghee to your food and mul... | `Add a spoon of ghee to your food and mul...` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-006: Amul — Amul Pure Ghee (500 mL Plastic Jar)
- **Image**: `1000084121.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Ghee | `Ghee` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `clear` | `clear` | Allergen Information: Contains milk. | `Allergen Information: Contains milk.` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `uncertain` | Nutritional Information 33 servings per container Serving si... | `Nutritional Information` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | STORE IN COOL, DRY AND HYGIENIC PLACE, AWAY FROM DIRECT SUN ... | `STORE IN COOL, DRY AND HYGIENIC PLACE` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-007: Aravan Traders — Shakti Kuttu Atta Buckwheat Flour (250g Pouch)
- **Image**: `IMG-20261115-WA0001.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `uncertain` | शक्ति कुट्टू आटा Kuttu Atta | `Kuttu Atta` | ⚠️ Downgraded by Normalizer |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | BUCKWHEAT | `INGREDIENT : BUCKWHEAT` | Clear status retained; not independently verified |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITION FACTS SERVING SIZE 100g (Approx) Energy 345Kcal Ca... | `NUTRITION FACTS` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | How to store : In Clean, Cool & Dry Place, Free From Moistur... | `TRANSFER INTO AIRTIGHT CONTAINER AFTER O...` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-008: Fortune (AWL) — Fortune Refined Sunflower Seed Oil (1L Pouch)
- **Image**: `IMG-20261115-WA0004.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | REFINED SUNFLOWER SEED OIL | `REFINED SUNFLOWER SEED OIL` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `uncertain` | Please refer to the bracketed portion of the batch code prin... | `Refined Sunflower Oil, Antioxidants (INS...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `clear` | `uncertain` | Nutritional Information Serving Size : 15 ml/13.65 g (1 tabl... | `Nutritional Information Serving Size : 1...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | USE BY DATE IS VALID IF STORED IN A COOL, DRY PLACE. KEEP AW... | `USE BY DATE IS VALID IF STORED IN A COOL...` | Clear status retained; not independently verified |

### SKU-PROD-009: Dabur — Dabur Hajmola Imli Tasty Digestive Tablets (Bottle)
- **Image**: `IMG-20261115-WA0006.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `uncertain` | `uncertain` | Hajmola Imli Tasty Digestive Tablets | `Imli Tasty Digestive Tablets` | ℹ️ uncertain |
| **ageMarking** | `clear` | `uncertain` | Children: 1 tablet | `Children: 1 tablet` | ⚠️ Downgraded by Normalizer |
| **ingredients** | `clear` | `uncertain` | Composition: Each Tablet is prepared/derived from: Powder mi... | `Composition: Each Tablet is prepared/der...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `uncertain` | Storage: Store in cool and dry place, protected from moistur... | `Store in cool and dry place, protected f...` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-010: VLCC — VLCC Cocoa Butter Detan Glow Body Lotion (400ml Bottle)
- **Image**: `IMG-20261115-WA0009.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | VLCC COCOA BUTTER DETAN GLOW | `VLCC COCOA BUTTER DETAN GLOW` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `uncertain` | Aqua, Paraffinum liquidum, Sunflower (Helianthus annuus) See... | `Ingredients: Aqua, Paraffinum liquidum, ...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `clear` | Directions For Use : Apply liberally all over your body afte... | `Directions For Use : Apply liberally all...` | Clear status retained; not independently verified |

### SKU-PROD-011: Cadbury — Cadbury Dairy Milk Chocolate (Back Panel)
- **Image**: `dairymilk.png` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Cadbury Dairy Milk Silk Mini Treats | `Cadbury Dairy Milk Silk Mini Treats` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Sugar, Milk Solids (25%*), Cocoa Butter, Cocoa Solids, Emuls... | `Ingredients: Sugar, Milk Solids (25%*), ...` | Clear status retained; not independently verified |
| **allergenDeclaration** | `clear` | `clear` | Contains Milk, May Contain Tree Nuts, Wheat, Barley and Soy. | `Allergen Information: Contains Milk, May...` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `uncertain` | Serving size: 9 g; No. of Servings Per Package: 15* NUTRITIO... | `NUTRITION INFORMATION (Per 100 g)*: Ener...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | 1 Eat it. Lock it. Repeat. 2 Store it in your fridge. Raid i... | `Storage Conditions: STORE IN A COOL, HYG...` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-012: Conscious Food — Conscious Food Millet Noodles (162g Pouch)
- **Image**: `millet_noodles_bop.webp` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Millet Noodles | `Millet Noodles:` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `uncertain` | Millet Noodles: Jowar millet flour (50%), Whole wheat flour ... | `Ingredients: Millet Noodles: Jowar mille...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `clear` | `uncertain` | Allergy Advice: This product contains Wheat. Processed on a ... | `Allergy Advice: This product contains Wh...` | ⚠️ Downgraded by Normalizer |
| **nutritionPanel** | `clear` | `uncertain` | Nutrition per 100g Serving per container: 2 Serving Size 82.... | `Nutrition per 100g` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | COOKING INSTRUCTIONS Step 1: Cook noodles in boiling water f... | `COOKING INSTRUCTIONS` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-013-BACK: Slurrp Farm — Slurrp Farm Ragi & Jowar Cereal Stars & Moons (Back Panel)
- **Image**: `shopping.webp` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | Slurrp Farm's Crunch | `WHAT'S IN SLURRP FARM'S CRUNCH?` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **allergenDeclaration** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **nutritionPanel** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **preparationAndStorage** | `clear` | `uncertain` | Add milk to our stars and moons, for the perfect breakfast o... | `HOW TO STORE Keep it in a cool, dry plac...` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-013-NUTRITION: Slurrp Farm — Slurrp Farm Supergrain Cereal (Side Nutrition & Ingredients Panel)
- **Image**: `shopping (1).webp` | **Model**: `gemini-3.5-flash-lite`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Supergrain blend (sorghum (jowar), finger millet (Ragi)) (25... | `Supergrain blend (sorghum (jowar), finge...` | Clear status retained; not independently verified |
| **allergenDeclaration** | `clear` | `clear` | Allergen Note: Contains Milk. Made in a facility that proces... | `Allergen Note: Contains Milk. Made in a ...` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `clear` | Nutritional Information Serving Size: Approx 20 g Servings P... | `Nutritional Information Serving Size: Ap...` | Clear status retained; not independently verified |
| **preparationAndStorage** | `clear` | `clear` | JUST ADD MILK | `JUST ADD MILK` | Clear status retained; not independently verified |

### SKU-PROD-014: Nestle Maggi — Maggi 2-Minute Masala Noodles (70g Pouch Back Panel)
- **Image**: `maggi-2-minute-noodles-1000x1000.webp` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | MAGGI Masala Noodles | `MAGGI® Masala Noodles` | Clear status retained; not independently verified |
| **ageMarking** | `clear` | `uncertain` | 14-17 year old teenagers | `14-17 year old teenagers` | ⚠️ Downgraded by Normalizer |
| **ingredients** | `clear` | `uncertain` | Noodles: Refined wheat flour (Maida), Palm oil, Iodized salt... | `INGREDIENTS Noodles: Refined wheat flour...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `clear` | `clear` | Contains Wheat & Nut. May contains Milk, Mustard, Oats And S... | `Contains Wheat & Nut. May contains Milk,...` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITIONAL INFORMATION If a serve is 70 g Per 100g Per serv... | `NUTRITIONAL INFORMATION If a serve is 70...` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `clear` | STORAGE ADVICE STORE IN A COOL, DRY & HYGIENIC PLACE TO PROT... | `STORAGE ADVICE STORE IN A COOL, DRY & HY...` | Clear status retained; not independently verified |

### SKU-PROD-015: Nestle Maggi — Maggi Nutri-Licious Masala Atta Noodles (Back Panel)
- **Image**: `MaggiAttaNoodlesIngredients.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `uncertain` | INGREDIENTS: Noodles: Wheat flour (atta) (85.3%), Palm oil, ... | `INGREDIENTS: Noodles: Wheat flour (atta)...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `clear` | `clear` | MAY CONTAIN MILK AND SOYA. | `MAY CONTAIN MILK AND SOYA.` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `uncertain` | If a serve is 72.5g NUTRITION INFORMATION Per 100g Per Serve... | `NUTRITION INFORMATION` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | STORE IN A COOL, DRY & HYGIENIC PLACE TO PROTECT FROM INSECT... | `STORE IN A COOL, DRY & HYGIENIC PLACE` | ⚠️ Downgraded by Normalizer |

### SKU-PROD-016: McCain — McCain Veggie Burger Patty (360g Pack Back Panel)
- **Image**: `mccain-popular-vege-burger-patty-1000x1000.webp` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | McCain Veggie Burger Patty : Vegetable Product (Frozen) | `McCain Veggie Burger Patty : Vegetable P...` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `clear` | Vegetables (70%) [Potato, Carrot, Peas], Bread Crumb (Refine... | `INGREDIENTS : Vegetables (70%) [Potato, ...` | Clear status retained; not independently verified |
| **allergenDeclaration** | `clear` | `clear` | Contains Wheat. May contain Barley, Milk & Soy. | `Contains Wheat May contain Barley, Milk ...` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `clear` | Nutritional Information* (Frozen Product). 360 g Pack contai... | `Nutritional Information* (Frozen Product...` | Clear status retained; not independently verified |
| **preparationAndStorage** | `clear` | `clear` | Storage: KEEP FROZEN AT -18°C OR BELOW. METHOD OF PREPARATIO... | `Storage: KEEP FROZEN AT -18°C OR BELOW M...` | Clear status retained; not independently verified |

### SKU-PROD-017: Nestle Maggi — Maggi 2-Minute Masala Noodles (70g Pack Back & Recipe Panel)
- **Image**: `s-l400.jpg` | **Model**: `gemini-3.6-flash`

| Field | Model Status | Normalizer Status | Normalized Text | Model-Provided Snippet | Normalizer Outcome |
|---|---|---|---|---|---|
| **productName** | `clear` | `clear` | MAGGI EASY PEA-SY Masala mattar Recipe | `MAGGI EASY PEA-SY Masala mattar Recipe` | Clear status retained; not independently verified |
| **ageMarking** | `not_visible` | `not_visible` | *(empty)* | `none` | ℹ️ not_visible |
| **ingredients** | `clear` | `uncertain` | INGREDIENTS: Noodles: Refined wheat flour (Maida), Palm oil,... | `INGREDIENTS: Noodles: Refined wheat flou...` | ⚠️ Downgraded by Normalizer |
| **allergenDeclaration** | `clear` | `clear` | MAY CONTAIN MILK SOLIDS, MUSTARD AND SOYA. | `MAY CONTAIN MILK SOLIDS, MUSTARD AND SOY...` | Clear status retained; not independently verified |
| **nutritionPanel** | `clear` | `uncertain` | NUTRITION INFORMATION If a serve is 70g: Per 100g: Energy (k... | `NUTRITION INFORMATION` | ⚠️ Downgraded by Normalizer |
| **preparationAndStorage** | `clear` | `uncertain` | 1. START QUICK Sauté green peas, beans, onions and tomatoes ... | `STORE IN A COOL, DRY & HYGIENIC PLACE TO...` | ⚠️ Downgraded by Normalizer |
