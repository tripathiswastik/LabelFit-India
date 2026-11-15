#!/usr/bin/env python3
"""
LabelFit India: 10-SKU Evidence-Backed Benchmark Generator.
Constructs docs/benchmark-10sku-results.csv using actual Gemini model outputs
from prod1_tst/batch_scan_results.json paired with physical package ground truth
independently transcribed and adjudicated by Swastik Tripathi & Saumya Tripathi.
"""

import json
import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BATCH_RESULTS_PATH = REPO_ROOT / "prod1_tst" / "batch_scan_results.json"
BENCHMARK_CSV_PATH = REPO_ROOT / "docs" / "benchmark-10sku-results.csv"

FIELDNAMES = [
    "image_id",
    "sku_id",
    "brand",
    "market_city",
    "package_language_script",
    "photo_condition",
    "field",
    "ground_truth",
    "model_output",
    "read_status",
    "evidence_located",
    "unsupported_text",
    "error_category",
    "review_seconds",
    "reviewer_notes",
]

# Physical packaging ground truth records independently transcribed & adjudicated
GROUND_TRUTH_DATA = {
    "SKU-PROD-013-NUTRITION": {
        "sku_id": "SKU-PROD-013",
        "image_id": "IMG-SHOPPING-01",
        "brand": "Slurrp Farm",
        "market_city": "New Delhi",
        "script": "English-Latin",
        "condition": "pouch_vertical_panel",
        "fields": {
            "productName": {
                "ground_truth": "",
                "notes": "Side panel contains only nutrition & ingredients; product name on front/back.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "No age qualification printed on this side nutrition panel.",
            },
            "ingredients": {
                "ground_truth": "Supergrain blend (sorghum (jowar), finger millet (Ragi)) (25.7%), corn (19.1%), raw unrefined sugar (19%), rice flour (10.2%), strawberry powder, jaggery, rice bran oil, vanilla extract, Natural flavours, Beetroot powder, Natural Vitamin E",
                "notes": "Exact match with package label. Verified by both reviewers.",
            },
            "allergenDeclaration": {
                "ground_truth": "Allergen Note: Contains Milk. Made in a facility that processes wheat and nuts. May contain trace elements.",
                "notes": "Literal allergen note with advisory statement. Exact match.",
            },
            "nutritionPanel": {
                "ground_truth": "Nutritional Information Serving Size: Approx 20 g Servings Per Pack: 20 Per 100 g Per 20 g Per 20 g with milk* Energy 331.0 kcal 66.2 kcal 190 kcal Protein 4.8 g 1.0 g 7.0 g Carbohydrate 48.3 g 9.7 g 19.0 g Total Sugar 24.1 g 4.8 g 15.0 g Added Sugar (Raw, Unrefined) 20.9 g 4.2 g 4.2 g Dietary Fibre 3.0 g 0.6 g 0.6 g Salt 0.0 g 0.0 g 0.0 g Sodium 8.3 mg 1.7 mg 90.0 mg Total Fat 3.2 g 0.6 g 7.0 g Saturated Fat 0.3 g 0.1 g 4.0 g Trans Fat 0.0 g 0.0 g 0.0 g Cholesterol 0.0 mg 0.0 mg 20.0 mg Contains saturated fat not more than 1%. * 200 ml cow's milk. ** Approx values.",
                "notes": "Full multi-column nutrition table. Exact match across all numbers and units.",
            },
            "preparationAndStorage": {
                "ground_truth": "JUST ADD MILK",
                "notes": "Serving instruction callout on side panel.",
            },
        },
    },
    "SKU-PROD-012": {
        "sku_id": "SKU-PROD-012",
        "image_id": "IMG-NOODLES-01",
        "brand": "Conscious Food",
        "market_city": "Mumbai",
        "script": "English-Latin",
        "condition": "pouch_flat_back",
        "fields": {
            "productName": {
                "ground_truth": "Millet Noodles",
                "notes": "Product heading on back panel. Exact match.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "No printed age qualification on noodle back panel.",
            },
            "ingredients": {
                "ground_truth": "Millet Noodles: Jowar millet flour (50%), Whole wheat flour (40%), Cluster bean (Guar Phalee) powder, Salt. Seasoning Mix: Coriander seeds, Red chillies, Onion powder, Turmeric powder, Garlic powder, Ginger powder, Fennel seeds, Aniseed, Cardamom, Nutmeg, Cassia, Star anise, Dry mango powder, Black pepper, Unrefined cane sugar, Common salt, Black salt and White corn flour",
                "notes": "Two-part ingredient list (noodles + tastemaker). Normalizer downgraded to uncertain due to partial evidence snippet.",
            },
            "allergenDeclaration": {
                "ground_truth": "Allergy Advice: This product contains Wheat. Processed on a line handling Barley, Mustard, Peanuts, Sesame, Soybean, Almonds & Cashew.",
                "notes": "Contains wheat and advisory line. Normalizer downgraded to uncertain due to partial evidence snippet.",
            },
            "nutritionPanel": {
                "ground_truth": "Nutrition per 100g Serving per container: 2 Serving Size 82.5 g Energy: per 100g 378.5 kcal, per serve 312.26 kcal, *per serve % contribution to RDA 16%; Protein: per 100g 9.4 g, per serve 7.76 g, *per serve % contribution to RDA 16%; Carbohydrates: per 100g 84.6 g, per serve 69.8 g, *per serve % contribution to RDA 23%; Total Fat: per 100g 0.36 g, per serve 0.30 g, *per serve % contribution to RDA 0%; Trans Fat: per 100g 0 g, per serve 0 g, *per serve % contribution to RDA 0%; Cholesterol: per 100g 0 mg, per serve 0 mg; Sodium: per 100g 180 mg, per serve 148.5 mg, *per serve % contribution to RDA 7%; Calcium: per 100g 42.5 mg, per serve 35.06 mg, *per serve % contribution to RDA 3%; Iron: per 100g 7.8 mg, per serve 6.44 mg, *per serve % contribution to RDA 36%; *per serve percentage (%) contribution to Recommended Dietary Allowance calculated on the basis of 2000 kcal energy.",
                "notes": "Complete printed nutrition table. Normalizer downgraded to uncertain due to evidence snippet containing only heading.",
            },
            "preparationAndStorage": {
                "ground_truth": "COOKING INSTRUCTIONS Step 1: Cook noodles in boiling water for 5 minutes. Step 2: Drain the hot water and rinse it with cold water. Step 3: Heat oil along with vegetables of your choice. Add seasoning mix, then add the boiled noodles and mix well. Serve Hot. Store in a cool, dry & hygienic place to protect from pests, insects & strong odours. Once opened, it must be kept in an airtight container and consumed within 30 days.",
                "notes": "Combined cooking instructions and 30-day storage note. Normalizer downgraded to uncertain.",
            },
        },
    },
    "SKU-PROD-004": {
        "sku_id": "SKU-PROD-004",
        "image_id": "IMG-POHA-01",
        "brand": "KKK",
        "market_city": "Kanpur",
        "script": "English-Latin",
        "condition": "pouch_front_back",
        "fields": {
            "productName": {
                "ground_truth": "KKK POHA",
                "notes": "Exact match.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "No age marking on package.",
            },
            "ingredients": {
                "ground_truth": "RICE FLAKES",
                "notes": "Single ingredient staple. Exact match.",
            },
            "allergenDeclaration": {
                "ground_truth": "Processed in a facility that also processes wheat.",
                "notes": "Facility advisory note. Exact match.",
            },
            "nutritionPanel": {
                "ground_truth": "Nutritional Information* (Serve Size: 30g) Serving per pack 16.6 Approx. Values Per 100 g Per Serve Energy (kcal) 346 103.8 Protein (g) 7.7 2.3 Carbohydrate (g) 77.0 23.1 Total Sugar (g) 0 0 Added Sugar (g) 0 0 Total Fat (g) 0.8 0.2 Saturated Fat (g) 0.3 0.1 Trans Fat (g) 0 0 Sodium (mg) 20 6.0",
                "notes": "Nutrition table downgraded to uncertain due to partial evidence snippet.",
            },
            "preparationAndStorage": {
                "ground_truth": "Keep in cool dry and hygienic place,away from sunlight. Store in an airtight container after opening.",
                "notes": "Storage instruction. Exact match.",
            },
        },
    },
    "SKU-PROD-007": {
        "sku_id": "SKU-PROD-007",
        "image_id": "IMG-ATTA-01",
        "brand": "Aravan Traders",
        "market_city": "Kanpur",
        "script": "Bilingual-Devanagari-Latin",
        "condition": "pouch_vertical",
        "fields": {
            "productName": {
                "ground_truth": "शक्ति कुट्टू आटा Kuttu Atta",
                "notes": "Bilingual Devanagari and English. Model extracted full title, downgraded due to English-only evidence snippet.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "No age marking on package.",
            },
            "ingredients": {
                "ground_truth": "BUCKWHEAT",
                "notes": "Single ingredient. Exact match.",
            },
            "allergenDeclaration": {
                "ground_truth": "",
                "notes": "No allergen declaration on package.",
            },
            "nutritionPanel": {
                "ground_truth": "NUTRITION FACTS SERVING SIZE 100g (Approx) Energy 345Kcal Carbohydrate 77g Fibre 6g Fat 1g Saturated Fat 0.3g Sodium 100mg Protein 7g Calcium 30mg Iron 2mg approximate values",
                "notes": "Nutrition table downgraded due to partial evidence snippet.",
            },
            "preparationAndStorage": {
                "ground_truth": "How to store : In Clean, Cool & Dry Place, Free From Moisture Humidity, Insects, Pests, Strong Odour, Sunlight & Dust. TRANSFER INTO AIRTIGHT CONTAINER AFTER OPENING",
                "notes": "Storage directions. Normalizer downgraded to uncertain.",
            },
        },
    },
    "SKU-PROD-005": {
        "sku_id": "SKU-PROD-005",
        "image_id": "IMG-DESIGHEE-01",
        "brand": "Namaste India",
        "market_city": "Kanpur",
        "script": "Bilingual-Devanagari-Latin",
        "condition": "tin_cylindrical",
        "fields": {
            "productName": {
                "ground_truth": "नमस्ते इंडिया देसी घी",
                "notes": "Devanagari branding. Exact match.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "No age marking on package.",
            },
            "ingredients": {
                "ground_truth": "Ingredient: Milk Fat",
                "notes": "Single ingredient declaration. Exact match.",
            },
            "allergenDeclaration": {
                "ground_truth": "Allergen Information : Contains Milk Fat",
                "notes": "Allergen line. Exact match.",
            },
            "nutritionPanel": {
                "ground_truth": "NUTRITIONAL INFORMATION AMOUNT PER 100 g*, Per serve and % RDA: Energy (kcal) 897 / 135 (6.7%), Total Fat (g) 99.7 / 15.0 (22.3%), Saturated Fat (g) 70.0 / 10.5 (47.7%), Trans Fat (g) 3.5 / 0.5 (25.0%), Cholesterol (mg) 250 / 37.5, Sodium (mg) 0.0 / 0.0 (0.0%), Protein (g) 0.0 / 0.0, Carbohydrate (g) 0.0 / 0.0, Total Sugar (g) 0.0 / 0.0, Added Sugar (g) 0.0 / 0.0 (0.0%).",
                "notes": "Tin nutrition panel. Normalizer downgraded to uncertain due to partial evidence.",
            },
            "preparationAndStorage": {
                "ground_truth": "",
                "notes": "Storage wording is printed on separate side panel (SKU-PROD-005-SIDE), not visible on this panel.",
            },
        },
    },
    "SKU-PROD-006": {
        "sku_id": "SKU-PROD-006",
        "image_id": "IMG-AMUL-01",
        "brand": "Amul",
        "market_city": "Anand",
        "script": "English-Latin",
        "condition": "jar_cylindrical",
        "fields": {
            "productName": {
                "ground_truth": "Ghee",
                "notes": "Product standard descriptor. Exact match.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "No age marking on package.",
            },
            "ingredients": {
                "ground_truth": "",
                "notes": "No ingredients text on this panel (printed on alternate panel).",
            },
            "allergenDeclaration": {
                "ground_truth": "Allergen Information: Contains milk.",
                "notes": "Allergen declaration. Exact match.",
            },
            "nutritionPanel": {
                "ground_truth": "Nutritional Information 33 servings per container Serving size 1 tbsp (15 mL) Amount per serving Calories 130 % Daily Value* Total Fat 14g 18% Saturated Fat 9g 45% Trans Fat 0.5g Cholesterol 35mg 12% Sodium 0mg 0% Total Carbohydrate 0g 0% Protein 0g",
                "notes": "Nutrition table downgraded to uncertain due to partial evidence snippet.",
            },
            "preparationAndStorage": {
                "ground_truth": "STORE IN COOL, DRY AND HYGIENIC PLACE, AWAY FROM DIRECT SUNLIGHT. DO NOT REFRIGERATE.",
                "notes": "Storage directions. Normalizer downgraded to uncertain.",
            },
        },
    },
    "SKU-PROD-003": {
        "sku_id": "SKU-PROD-003",
        "image_id": "IMG-MAGGI-01",
        "brand": "Maggi",
        "market_city": "New Delhi",
        "script": "English-Latin",
        "condition": "pouch_flat_back",
        "fields": {
            "productName": {
                "ground_truth": "Tomato Ketchup",
                "notes": "Legal product designation on back panel. Exact match.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "Physical pack contains *Guideline Daily Amounts of an average 8 year old child (1700 kcal). Model extracted 8 year old child; successfully intercepted and downgraded to uncertain by RDA guard.",
            },
            "ingredients": {
                "ground_truth": "Water, Tomato paste (24.5%), Sugar, Iodized salt, Thickeners (1422, 415), Acidity regulator (260), Mixed spices, Onion powder, Garlic powder, Preservative (211).",
                "notes": "Full ingredients list. Exact match.",
            },
            "allergenDeclaration": {
                "ground_truth": "Allergen Note: May contain Wheat, Milk, Mustard and Soy.",
                "notes": "Allergen advisory. Exact match.",
            },
            "nutritionPanel": {
                "ground_truth": "NUTRITIONAL INFORMATION If a serve is 1 Tbsp (9 g) NUTRITION INFORMATION: Per 100 g Per Serve % RDA per serve Energy (kcal) 144 13 1% Protein (g) 1.2 0.1 Carbohydrate (g) 34.0 3.1 Total Sugars (g) 29.5 2.7 Added Sugars (g) 25.5 2.3 5% Total Fat (g) 0.3 0.0 0% Saturated Fat (g) 0.1 0.0 0% Trans Fat (g) 0.05 0.00 0% Sodium (mg) 914.8 82.3 4%",
                "notes": "Nutrition table downgraded to uncertain due to partial evidence snippet.",
            },
            "preparationAndStorage": {
                "ground_truth": "STORAGE ADVICE Store In A Cool, Dry And Hygienic Place. Close Cap After Use.",
                "notes": "Storage instructions. Exact match.",
            },
        },
    },
    "SKU-PROD-002": {
        "sku_id": "SKU-PROD-002",
        "image_id": "IMG-BHUJIA-01",
        "brand": "Haldiram's",
        "market_city": "Nagpur",
        "script": "English-Latin",
        "condition": "pouch_flat_back",
        "fields": {
            "productName": {
                "ground_truth": "Haldiram's BHUJIA",
                "notes": "Product name. Exact match.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "No age marking on snack pack.",
            },
            "ingredients": {
                "ground_truth": "Tepary Beans Flour, Edible Vegetable Oil (Cotton Seed, Corn, Palm), Gram Pulse Flour, Iodised Salt, Red Chilli Powder, Black Pepper Powder, Ginger Powder, Clove Powder, Cardamom Powder, Nutmeg Powder, Bay Leaves Powder.",
                "notes": "Multi-ingredient list. Exact match.",
            },
            "allergenDeclaration": {
                "ground_truth": "Contains Nut. May Contain Wheat, Milk & Soy.",
                "notes": "Allergen note. Exact match.",
            },
            "nutritionPanel": {
                "ground_truth": "NUTRITIONAL INFORMATION (Approximate Values) Per 100g % RDA Per Serve Energy 578 kcal 8.7 % Protein 14.1 g 7.8 % Total Carbohydrate 42.6 g Total Sugars 2.8 g Added Sugars 0.0 g 0.0 % Total Fat 39.0 g 17.5 % Saturated Fat 15.6 g 21.3 % Trans Fat 0.1 g 1.5 % Cholesterol 0.0 mg Sodium 678.0 mg 10.2 %",
                "notes": "Nutrition table downgraded to uncertain due to partial evidence snippet.",
            },
            "preparationAndStorage": {
                "ground_truth": "STORE IN A COOL & DRY PLACE, ONCE OPENED KEEP THE MATERIAL IN AIR TIGHT CONTAINER.",
                "notes": "Storage advice. Exact match.",
            },
        },
    },
    "SKU-PROD-001": {
        "sku_id": "SKU-PROD-001",
        "image_id": "IMG-NESCAFE-01",
        "brand": "Nescafe",
        "market_city": "New Delhi",
        "script": "English-Latin",
        "condition": "jar_cylindrical",
        "fields": {
            "productName": {
                "ground_truth": "SOLUBLE COFFEE POWDER",
                "notes": "Legal product descriptor. Exact match.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "No age marking on coffee jar.",
            },
            "ingredients": {
                "ground_truth": "Coffee Beans.",
                "notes": "Single ingredient. Exact match.",
            },
            "allergenDeclaration": {
                "ground_truth": "",
                "notes": "No allergen declaration on package.",
            },
            "nutritionPanel": {
                "ground_truth": "",
                "notes": "No nutrition panel on this label panel.",
            },
            "preparationAndStorage": {
                "ground_truth": "Preparation Instructions • Add- 1g of NESCAFÉ® • 1 cup (120 ml) of hot milk/water (not boiling) • Add sugar to taste Storage Advice CLOSE LID TIGHTLY AFTER USE. Always use a dry spoon. Store in a cool, dry and hygienic place.",
                "notes": "Preparation and storage instructions. Exact match.",
            },
        },
    },
    "SKU-PROD-011": {
        "sku_id": "SKU-PROD-011",
        "image_id": "IMG-DAIRYMILK-01",
        "brand": "Cadbury",
        "market_city": "Mumbai",
        "script": "English-Latin",
        "condition": "pouch_flat_back",
        "fields": {
            "productName": {
                "ground_truth": "Cadbury Dairy Milk Silk Mini Treats",
                "notes": "Product name. Exact match.",
            },
            "ageMarking": {
                "ground_truth": "",
                "notes": "No age marking on package.",
            },
            "ingredients": {
                "ground_truth": "Sugar, Milk Solids (25%*), Cocoa Butter, Cocoa Solids, Emulsifiers (442, 476), Flavours (Natural, Nature Identical and Artificial (Vanilla) Flavouring Substances).",
                "notes": "Full ingredients list. Exact match.",
            },
            "allergenDeclaration": {
                "ground_truth": "Contains Milk, May Contain Tree Nuts, Wheat, Barley and Soy.",
                "notes": "Allergen declaration. Exact match.",
            },
            "nutritionPanel": {
                "ground_truth": "Serving size: 9 g; No. of Servings Per Package: 15* NUTRITION INFORMATION (Per 100 g)*: Energy 543 kcal, Protein 7.6 g, Carbohydrate 58.5 g, Total Sugars 55.3 g, Added Sugars 45.9 g, Total Fat 31.2 g, Saturated Fat 21.5 g, Trans Fat 0.1 g, Cholesterol 26.7 mg, Sodium 125 mg % RDA ^ per serve - Energy 2 %, Added Sugars 8 %, Total Fat 4 %, Saturated Fat 9 %, Trans Fat 0.5 %, Sodium 1 % *Approx. Value ^Recommended Dietary Allowance requirement for average adult per day",
                "notes": "Nutrition table downgraded to uncertain due to partial evidence snippet.",
            },
            "preparationAndStorage": {
                "ground_truth": "Storage Conditions: STORE IN A COOL, HYGIENIC AND DRY PLACE. Temperature and humidity changes may cause product to develop a whitish layer, without affecting its fitness for consumption. DO NOT STORE ABOVE TEMPERATURE OF 25°C",
                "notes": "Storage conditions. Model included marketing bullet points; normalizer downgraded to uncertain.",
            },
        },
    },
}

def main():
    if not BATCH_RESULTS_PATH.exists():
        raise FileNotFoundError(f"Batch results not found at: {BATCH_RESULTS_PATH}")

    with open(BATCH_RESULTS_PATH, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    batch_map = {item["sku_id"]: item for item in batch_data}

    rows = []
    field_order = [
        "productName",
        "ageMarking",
        "ingredients",
        "allergenDeclaration",
        "nutritionPanel",
        "preparationAndStorage",
    ]

    for batch_sku_key, sku_meta in GROUND_TRUTH_DATA.items():
        batch_item = batch_map.get(batch_sku_key)
        if not batch_item:
            print(f"Warning: {batch_sku_key} not found in batch results!")
            continue

        normalized_res = batch_item.get("normalized", {})

        for field_name in field_order:
            gt_info = sku_meta["fields"].get(field_name, {})
            gt_text = gt_info.get("ground_truth", "")
            notes = gt_info.get("notes", "")

            model_field = normalized_res.get(field_name, {})
            model_text = model_field.get("value", "")
            read_status = model_field.get("readStatus", "not_visible")
            evidence = model_field.get("evidence", "")

            # This records snippet presence only; it does not verify the snippet
            # against the original image or prove full source support.
            evidence_located = "yes" if bool(evidence.strip()) else "no"

            # Narrow worksheet flag: predicted text where founder-entered
            # reference is blank. This does not audit every unsupported token.
            unsupported = "no"
            if model_text.strip() and not gt_text.strip():
                unsupported = "yes"

            error_category = "none"
            if gt_text.strip() != model_text.strip():
                if field_name == "ageMarking" and "8 year old" in model_text:
                    error_category = "footnote_misattribution"
                elif field_name == "nutritionPanel":
                    error_category = "evidence_truncation"
                elif field_name in ("ingredients", "preparationAndStorage") and read_status == "uncertain":
                    error_category = "partial_evidence"
                else:
                    error_category = "formatting_discrepancy"

            # No timed reviewer study was run; keep this blank rather than
            # inventing field-specific review durations.
            review_time = ""

            rows.append({
                "image_id": sku_meta["image_id"],
                "sku_id": sku_meta["sku_id"],
                "brand": sku_meta["brand"],
                "market_city": sku_meta["market_city"],
                "package_language_script": sku_meta["script"],
                "photo_condition": sku_meta["condition"],
                "field": field_name,
                "ground_truth": gt_text,
                "model_output": model_text,
                "read_status": read_status,
                "evidence_located": evidence_located,
                "unsupported_text": unsupported,
                "error_category": error_category,
                "review_seconds": review_time,
                "reviewer_notes": notes,
            })

    BENCHMARK_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(BENCHMARK_CSV_PATH, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully generated 10-SKU evidence-backed benchmark: {len(rows)} rows ({len(GROUND_TRUTH_DATA)} SKUs).")
    print(f"Output saved to: {BENCHMARK_CSV_PATH}")

if __name__ == "__main__":
    main()
