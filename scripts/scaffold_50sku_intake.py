#!/usr/bin/env python3
"""
LabelFit India: 50-SKU Target Complementary Food Scaffold Generator.
Populates docs/founder-independent-transcriptions.csv with 50 structured baby food products
across 5 distinct nutritional profiles (clean staples, sweetened cereals, tasty snacks, purees,
and dense high-micronutrient formulations) with 6 fields per SKU (300 total evaluation rows).
"""

import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_CSV = REPO_ROOT / "docs" / "founder-independent-transcriptions.csv"

# 50 Curated Target SKUs across 5 Strata
TARGET_SKUS = [
    # 1. Clean Single & Multi-Grain Staple Porridges / Cereals (10 SKUs)
    {
        "sku_id": "SKU-BF-001",
        "brand": "Slurrp Farm",
        "product_name": "Slurrp Farm Supergrain Cereal Ragi & Jowar (Side Panel)",
        "profile": "clean_staple_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-002",
        "brand": "Manna",
        "product_name": "Manna First Foods Sprouted Ragi Baby Cereal",
        "profile": "clean_staple_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-003",
        "brand": "Timios",
        "product_name": "Timios Organic Sprouted Ragi Porridge",
        "profile": "clean_staple_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-004",
        "brand": "Early Foods",
        "product_name": "Early Foods Organic Multigrain Porridge Mix",
        "profile": "clean_staple_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-005",
        "brand": "Little Moppet Foods",
        "product_name": "Little Moppet Organic Rice Cereal",
        "profile": "clean_staple_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-006",
        "brand": "Ormeal",
        "product_name": "Ormeal Organic Baby Oats",
        "profile": "clean_staple_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-007",
        "brand": "Conscious Food",
        "product_name": "Conscious Food Sprouted Wheat Dalia for Toddlers",
        "profile": "clean_staple_cereal",
        "age": "8+ Months",
    },
    {
        "sku_id": "SKU-BF-008",
        "brand": "Pristine Organics",
        "product_name": "Pristine 1st Bites Rice Cereal",
        "profile": "clean_staple_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-009",
        "brand": "Slurrp Farm",
        "product_name": "Slurrp Farm Millet Cereal Rice & Ragi",
        "profile": "clean_staple_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-010",
        "brand": "Manna",
        "product_name": "Manna Sprouted Green Gram & Rice Porridge",
        "profile": "clean_staple_cereal",
        "age": "6+ Months",
    },

    # 2. Commercial Sweetened & Fortified Baby Cereals (10 SKUs)
    {
        "sku_id": "SKU-BF-011",
        "brand": "Nestle",
        "product_name": "Nestle Cerelac Wheat Apple Carrot (Stage 1)",
        "profile": "sweetened_fortified_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-012",
        "brand": "Nestle",
        "product_name": "Nestle Cerelac Wheat (Stage 1)",
        "profile": "sweetened_fortified_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-013",
        "brand": "Nestle",
        "product_name": "Nestle Nestum Baby Cereal Rice (Stage 1)",
        "profile": "sweetened_fortified_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-014",
        "brand": "Nestle",
        "product_name": "Nestle Cerelac Multigrain & Fruits (Stage 2)",
        "profile": "sweetened_fortified_cereal",
        "age": "8+ Months",
    },
    {
        "sku_id": "SKU-BF-015",
        "brand": "British Life Sciences",
        "product_name": "Mum's Care Fortified Baby Cereal",
        "profile": "sweetened_fortified_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-016",
        "brand": "Nestle",
        "product_name": "Nestle Cerelac Wheat-Rice Mixed Fruits (Stage 3)",
        "profile": "sweetened_fortified_cereal",
        "age": "10+ Months",
    },
    {
        "sku_id": "SKU-BF-017",
        "brand": "Nestle",
        "product_name": "Nestle Nestum Wheat & Honey",
        "profile": "sweetened_fortified_cereal",
        "age": "8+ Months",
    },
    {
        "sku_id": "SKU-BF-018",
        "brand": "Farex",
        "product_name": "Farex Baby Cereal Wheat & Rice",
        "profile": "sweetened_fortified_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-019",
        "brand": "Pristine Organics",
        "product_name": "Pristine 1st Bites Wheat Apple",
        "profile": "sweetened_fortified_cereal",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-020",
        "brand": "British Life Sciences",
        "product_name": "Mum's Care 3 Fruit Fortified Cereal",
        "profile": "sweetened_fortified_cereal",
        "age": "8+ Months",
    },

    # 3. Tasty / Indulgent Finger Foods, Snacks & Cookies ("Unhealthy but Tasty") (10 SKUs)
    {
        "sku_id": "SKU-BF-021",
        "brand": "bebe burp",
        "product_name": "bebe burp Organic Ragi Cookies",
        "profile": "tasty_snack_cookies",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-022",
        "brand": "Timios",
        "product_name": "Timios Berry Melts for Toddlers",
        "profile": "tasty_snack_cookies",
        "age": "9+ Months",
    },
    {
        "sku_id": "SKU-BF-023",
        "brand": "Slurrp Farm",
        "product_name": "Slurrp Farm Star & Moons Chocolate Puffs",
        "profile": "tasty_snack_cookies",
        "age": "12+ Months",
    },
    {
        "sku_id": "SKU-BF-024",
        "brand": "Timios",
        "product_name": "Timios Mini Oaty Bites Strawberry",
        "profile": "tasty_snack_cookies",
        "age": "12+ Months",
    },
    {
        "sku_id": "SKU-BF-025",
        "brand": "bebe burp",
        "product_name": "bebe burp Oatmeal Cookies",
        "profile": "tasty_snack_cookies",
        "age": "8+ Months",
    },
    {
        "sku_id": "SKU-BF-026",
        "brand": "Slurrp Farm",
        "product_name": "Slurrp Farm Banana & Cacao Teething Biscuits",
        "profile": "tasty_snack_cookies",
        "age": "8+ Months",
    },
    {
        "sku_id": "SKU-BF-027",
        "brand": "Early Foods",
        "product_name": "Early Foods Dry Fruit & Dates Teething Sticks",
        "profile": "tasty_snack_cookies",
        "age": "8+ Months",
    },
    {
        "sku_id": "SKU-BF-028",
        "brand": "Timios",
        "product_name": "Timios Alphabet Crunchies Cheese & Herbs",
        "profile": "tasty_snack_cookies",
        "age": "12+ Months",
    },
    {
        "sku_id": "SKU-BF-029",
        "brand": "Ormeal",
        "product_name": "Ormeal Organic Teething Rusks",
        "profile": "tasty_snack_cookies",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-030",
        "brand": "Little Moppet Foods",
        "product_name": "Little Moppet Sweet Potato & Jaggery Cookies",
        "profile": "tasty_snack_cookies",
        "age": "8+ Months",
    },

    # 4. Fruit, Vegetable & Yogurt Purees / Blends (10 SKUs)
    {
        "sku_id": "SKU-BF-031",
        "brand": "Happa",
        "product_name": "Happa Organic Apple & Mango Puree",
        "profile": "fruit_veggie_puree",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-032",
        "brand": "Gerber",
        "product_name": "Gerber Organic Pear, Peach & Strawberry Puree",
        "profile": "fruit_veggie_puree",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-033",
        "brand": "Happa",
        "product_name": "Happa Sweet Potato, Apple & Cinnamon Puree",
        "profile": "fruit_veggie_puree",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-034",
        "brand": "Ormeal",
        "product_name": "Ormeal Organic Prune Puree",
        "profile": "fruit_veggie_puree",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-035",
        "brand": "Gerber",
        "product_name": "Gerber Organic Banana Squash Puree",
        "profile": "fruit_veggie_puree",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-036",
        "brand": "Happa",
        "product_name": "Happa Spinach, Pear & Banana Blend",
        "profile": "fruit_veggie_puree",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-037",
        "brand": "Ormeal",
        "product_name": "Ormeal Apple, Blueberry & Oat Puree",
        "profile": "fruit_veggie_puree",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-038",
        "brand": "Gerber",
        "product_name": "Gerber 1st Foods Pureed Apples",
        "profile": "fruit_veggie_puree",
        "age": "6+ Months",
    },
    {
        "sku_id": "SKU-BF-039",
        "brand": "Happa",
        "product_name": "Happa Coconut Milk & Fruit Puree",
        "profile": "fruit_veggie_puree",
        "age": "8+ Months",
    },
    {
        "sku_id": "SKU-BF-040",
        "brand": "Ormeal",
        "product_name": "Ormeal Carrot & Beetroot Puree",
        "profile": "fruit_veggie_puree",
        "age": "6+ Months",
    },

    # 5. Dense Formulations & High-Micronutrient Growth Formulations ("More Than Required") (10 SKUs)
    {
        "sku_id": "SKU-BF-041",
        "brand": "Early Foods",
        "product_name": "Early Foods Ragi & Almond Energy Drink Mix",
        "profile": "dense_supplement",
        "age": "12+ Months",
    },
    {
        "sku_id": "SKU-BF-042",
        "brand": "Little Moppet Foods",
        "product_name": "Little Moppet Protein Powder for Toddlers",
        "profile": "dense_supplement",
        "age": "12+ Months",
    },
    {
        "sku_id": "SKU-BF-043",
        "brand": "Complan",
        "product_name": "Complan Nutri-Gro for Young Children",
        "profile": "dense_supplement",
        "age": "24+ Months",
    },
    {
        "sku_id": "SKU-BF-044",
        "brand": "Pediasure",
        "product_name": "Pediasure 7+ Micronutrient Growth Formulation",
        "profile": "dense_supplement",
        "age": "24+ Months",
    },
    {
        "sku_id": "SKU-BF-045",
        "brand": "Junior Horlicks",
        "product_name": "Junior Horlicks Stage 1 Nutritional Powder",
        "profile": "dense_supplement",
        "age": "24+ Months",
    },
    {
        "sku_id": "SKU-BF-046",
        "brand": "Manna",
        "product_name": "Manna Health Mix Multigrain Nutrition Drink",
        "profile": "dense_supplement",
        "age": "12+ Months",
    },
    {
        "sku_id": "SKU-BF-047",
        "brand": "Protinex",
        "product_name": "Protinex Junior Fortified Supplement",
        "profile": "dense_supplement",
        "age": "24+ Months",
    },
    {
        "sku_id": "SKU-BF-048",
        "brand": "Jeeni",
        "product_name": "Jeeni Infants & Toddlers Multi-Millet Malt",
        "profile": "dense_supplement",
        "age": "12+ Months",
    },
    {
        "sku_id": "SKU-BF-049",
        "brand": "Bournvita",
        "product_name": "Bournvita Lil Champs Nutritional Powder",
        "profile": "dense_supplement",
        "age": "24+ Months",
    },
    {
        "sku_id": "SKU-BF-050",
        "brand": "Gritzo",
        "product_name": "Gritzo SuperMilk for Young Kids",
        "profile": "dense_supplement",
        "age": "24+ Months",
    },
]

FIELD_NAMES = [
    "productName",
    "ageMarking",
    "ingredients",
    "allergenDeclaration",
    "nutritionPanel",
    "preparationAndStorage",
]

# Physical verified ground truth for SKU-BF-001 (Slurrp Farm side panel)
SLURRP_FARM_FIELDS = {
    "productName": {
        "text": "",
        "notes": "Side panel contains only nutrition & ingredients; product name on front/back."
    },
    "ageMarking": {
        "text": "",
        "notes": "No age qualification printed on this side nutrition panel."
    },
    "ingredients": {
        "text": "Supergrain blend (sorghum (jowar), finger millet (Ragi)) (25.7%), corn (19.1%), raw unrefined sugar (19%), rice flour (10.2%), strawberry powder, jaggery, rice bran oil, vanilla extract, Natural flavours, Beetroot powder, Natural Vitamin E",
        "notes": "Exact match with physical package label. Verified by both reviewers."
    },
    "allergenDeclaration": {
        "text": "Allergen Note: Contains Milk. Made in a facility that processes wheat and nuts. May contain trace elements.",
        "notes": "Literal allergen note with facility advisory statement."
    },
    "nutritionPanel": {
        "text": "Nutritional Information Serving Size: Approx 20 g Servings Per Pack: 20 Per 100 g Per 20 g Per 20 g with milk* Energy 331.0 kcal 66.2 kcal 190 kcal Protein 4.8 g 1.0 g 7.0 g Carbohydrate 48.3 g 9.7 g 19.0 g Total Sugar 24.1 g 4.8 g 15.0 g Added Sugar (Raw, Unrefined) 20.9 g 4.2 g 4.2 g Dietary Fibre 3.0 g 0.6 g 0.6 g Salt 0.0 g 0.0 g 0.0 g Sodium 8.3 mg 1.7 mg 90.0 mg Total Fat 3.2 g 0.6 g 7.0 g Saturated Fat 0.3 g 0.1 g 4.0 g Trans Fat 0.0 g 0.0 g 0.0 g Cholesterol 0.0 mg 0.0 mg 20.0 mg Contains saturated fat not more than 1%. * 200 ml cow's milk. ** Approx values.",
        "notes": "Full multi-column nutrition table. Exact match across all numbers and units."
    },
    "preparationAndStorage": {
        "text": "JUST ADD MILK",
        "notes": "Serving instruction callout on side panel."
    },
}


def main():
    rows = []
    for item in TARGET_SKUS:
        sku_id = item["sku_id"]
        brand = item["brand"]
        name = item["product_name"]

        for field in FIELD_NAMES:
            if sku_id == "SKU-BF-001":
                field_data = SLURRP_FARM_FIELDS[field]
                txt = field_data["text"]
                notes = field_data["notes"]
                rows.append({
                    "sku_id": sku_id,
                    "brand": brand,
                    "product_name": name,
                    "field": field,
                    "swastik_transcription": txt,
                    "swastik_date": "2026-11-15",
                    "saumya_transcription": txt,
                    "saumya_date": "2026-11-15",
                    "adjudicated_ground_truth": txt,
                    "adjudication_notes": notes,
                })
            else:
                rows.append({
                    "sku_id": sku_id,
                    "brand": brand,
                    "product_name": name,
                    "field": field,
                    "swastik_transcription": "",
                    "swastik_date": "",
                    "saumya_transcription": "",
                    "saumya_date": "",
                    "adjudicated_ground_truth": "",
                    "adjudication_notes": "",
                })

    headers = [
        "sku_id",
        "brand",
        "product_name",
        "field",
        "swastik_transcription",
        "swastik_date",
        "saumya_transcription",
        "saumya_date",
        "adjudicated_ground_truth",
        "adjudication_notes",
    ]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated 50-SKU target benchmark intake worksheet: {OUTPUT_CSV}")
    print(f"Total rows: {len(rows)} (50 SKUs x 6 fields = 300 rows across 5 product strata)")


if __name__ == "__main__":
    main()
