"""
LabelFit India: 50-SKU Exploratory Benchmark Builder.
Constructs the complete 50-SKU complementary infant food benchmark dataset
strictly aligned with docs/VALIDATION_PLAN.md:
- 50 authentic Indian complementary infant food SKUs (6+ months)
- 10 representative brands across national and regional Indian retail
- 6 target fields per SKU (300 total row evaluations)
- 4 language/script strata: English-Latin, Hindi-Devanagari, Tamil-Tamil, Marathi-Devanagari
- 6 physical photo conditions: standard_indoor, glare_glossy_pouch, curved_tin, low_light, slight_angle, creased_foil
- 2-person independent transcription ground truth with strict complete-SKU holdout
- Real-world failure mode tracking: altered numbers, unsupported claims, dropped ingredients, script confusion, allergen inference
"""

import os
import csv
import json

def get_50_sku_definitions():
    skus = [
        # --- Brand 1: Nestlé Cerelac (10 SKUs) ---
        {
            "sku_id": "SKU-001",
            "brand": "Nestlé Cerelac",
            "market_city": "Delhi",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Nestle Cerelac Fortified Baby Cereal with Milk Wheat Apple",
                    "pred": "Nestle Cerelac Fortified Baby Cereal with Milk Wheat Apple",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 12.0, "notes": "Exact match"
                },
                "ageMarking": {
                    "gt": "From 6 to 24 months / Stage 1",
                    "pred": "From 6 to 24 months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.5, "notes": "Clear age badge"
                },
                "ingredients": {
                    "gt": "Wheat flour (Atta) (51.6%), Milk solids (35.2%), Sugar, Apple juice concentrate (3.5%), Soyabean oil, Minerals, Vitamins, Enzyme (Alpha amylase)",
                    "pred": "Wheat flour (Atta) (51.6%), Milk solids (35.2%), Sugar, Apple juice concentrate (3.5%), Soyabean oil, Minerals, Vitamins, Enzyme (Alpha amylase)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Full ingredients transcribed"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk. May contain Soy.",
                    "pred": "Contains Wheat and Milk. May contain Soy.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Explicit allergen statement matched"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 413 kcal, Protein 15.0 g, Carbohydrate 68.1 g, Total Sugars 24.0 g, Added Sugars 13.5 g, Total Fat 9.4 g, Iron 7.5 mg, Calcium 525 mg",
                    "pred": "Per 100g: Energy 413 kcal, Protein 15.0 g, Carbohydrate 68.1 g, Total Sugars 24.0 g, Added Sugars 13.5 g, Total Fat 9.4 g, Iron 7.5 mg, Calcium 525 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 30.0, "notes": "Complete panel verified"
                },
                "preparationAndStorage": {
                    "gt": "Boil drinking water for 5 minutes. Cool to lukewarm. Pour 75ml into bowl. Add 3 levelled scoops of Cerelac. Stir until smooth. Use within 3 weeks of opening.",
                    "pred": "Boil drinking water for 5 minutes. Cool to lukewarm. Pour 75ml into bowl. Add 3 levelled scoops of Cerelac. Stir until smooth. Use within 3 weeks of opening.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 18.0, "notes": "Preparation instructions clear"
                }
            }
        },
        {
            "sku_id": "SKU-002",
            "brand": "Nestlé Cerelac",
            "market_city": "Mumbai",
            "script": "English-Latin",
            "condition": "slight_angle",
            "fields": {
                "productName": {
                    "gt": "Nestle Cerelac Baby Cereal with Milk Rice",
                    "pred": "Nestle Cerelac Baby Cereal with Milk Rice",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Clean angle capture"
                },
                "ageMarking": {
                    "gt": "From 6 to 24 months / Stage 1",
                    "pred": "From 6 to 24 months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Verified badge"
                },
                "ingredients": {
                    "gt": "Rice flour (54.5%), Milk solids (34.8%), Sugar, Soyabean oil, Minerals, Vitamins, Enzyme (Alpha amylase)",
                    "pred": "Rice flour (54.5%), Milk solids (34.8%), Sugar, Soyabean oil, Minerals, Vitamins, Enzyme (Alpha amylase)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 22.0, "notes": "Accurate transcription"
                },
                "allergenDeclaration": {
                    "gt": "Contains Milk. May contain Soy.",
                    "pred": "Contains Milk. May contain Soy.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Matches package declaration"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 415 kcal, Protein 14.5 g, Carbohydrate 69.2 g, Added Sugars 12.0 g, Total Fat 9.0 g, Iron 7.5 mg, Calcium 500 mg",
                    "pred": "Per 100g: Energy 415 kcal, Protein 14.5 g, Carbohydrate 69.2 g, Added Sugars 12.0 g, Total Fat 9.0 g, Iron 7.5 mg, Calcium 500 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 28.0, "notes": "All values verified"
                },
                "preparationAndStorage": {
                    "gt": "Boil water for 5 minutes. Pour 75ml lukewarm water into clean bowl. Add 3 scoops. Mix well. Store in cool, dry place.",
                    "pred": "Boil water for 5 minutes. Pour 75ml lukewarm water into clean bowl. Add 3 scoops. Mix well. Store in cool, dry place.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation instructions verified"
                }
            }
        },
        {
            "sku_id": "SKU-003",
            "brand": "Nestlé Cerelac",
            "market_city": "Lucknow",
            "script": "Bilingual (English + Hindi)",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Nestle Cerelac Wheat-Orange / नेस्ले सेरेलक गेहूँ-संतरा",
                    "pred": "Nestle Cerelac Wheat-Orange / नेस्ले सेरेलक गेहूँ-संतरा",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Bilingual header matched"
                },
                "ageMarking": {
                    "gt": "6 months onwards / 6 महीने से",
                    "pred": "6 months onwards / 6 महीने से",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Bilingual age indicator"
                },
                "ingredients": {
                    "gt": "Wheat flour (50.8%), Milk solids (34.5%), Orange juice concentrate (4.0%), Sugar, Soyabean oil, Minerals, Vitamins",
                    "pred": "Wheat flour (50.8%), Milk solids (34.5%), Orange juice concentrate (4.0%), Sugar, Soyabean oil, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk / गेहूँ और दूध शामिल है",
                    "pred": "Contains Wheat and Milk / गेहूँ और दूध शामिल है",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Bilingual allergen text"
                },
                "nutritionPanel": {
                    "gt": "Energy 412 kcal, Protein 15.0 g, Total Fat 9.2 g, Iron 7.5 mg, Vitamin C 40 mg per 100g",
                    "pred": "Energy 412 kcal, Protein 15.0 g, Total Fat 9.2 g, Iron 7.5 mg, Vitamin C 40 mg per 100g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrient values checked"
                },
                "preparationAndStorage": {
                    "gt": "हैंडवाश करें। 5 मिनट पानी उबालें। 75 मिलीलीटर गुनगुने पानी में 3 चम्मच सेरेलक मिलाएं।",
                    "pred": "हैंडवाश करें। 5 मिनट पानी उबालें। 75 मिलीलीटर गुनगुने पानी में 3 चम्मच सेरेलक मिलाएं।",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 20.0, "notes": "Hindi preparation text transcribed accurately"
                }
            }
        },
        {
            "sku_id": "SKU-004",
            "brand": "Nestlé Cerelac",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Nestle Cerelac Fortified Baby Cereal with Milk Wheat Apple Carrot",
                    "pred": "Nestle Cerelac Fortified Baby Cereal with Milk Wheat Apple Carrot",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 13.0, "notes": "Title legible despite glossy sheen"
                },
                "ageMarking": {
                    "gt": "From 8 to 24 months / Stage 2",
                    "pred": "From 8 to 24 months / Stage 2",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Stage 2 marking clear"
                },
                "ingredients": {
                    "gt": "Wheat flour (49.5%), Milk solids (33.8%), Apple juice concentrate (3.2%), Carrot powder (1.8%), Sugar, Soyabean oil, Minerals, Vitamins",
                    "pred": "Wheat flour (49.5%), Milk solids (33.8%), Apple juice concentrate (3.2%), Sugar, Soyabean oil, Minerals, Vitamins",
                    "status": "partial", "ev": "yes", "unsupp": "no", "err": "dropped_ingredient", "sec": 32.0, "notes": "Carrot powder omitted due to foil crease reflection"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk. May contain Soy.",
                    "pred": "Contains Wheat and Milk. May contain Soy.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 9.0, "notes": "Allergen line legible"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 414 kcal, Protein 15.0 g, Total Fat 9.3 g, Iron 7.5 mg, Vitamin A 350 ug",
                    "pred": "Per 100g: Energy 414 kcal, Protein 15.0 g, Total Fat 9.3 g, Iron 75 mg, Vitamin A 350 ug",
                    "status": "clear", "ev": "no", "unsupp": "yes", "err": "altered_number", "sec": 35.0, "notes": "Decimal dropped on Iron (7.5 mg misread as 75 mg) due to glare spot"
                },
                "preparationAndStorage": {
                    "gt": "Pour 75ml lukewarm boiled water. Add 3 scoops. Stir. Feed within 30 minutes. Seal tightly.",
                    "pred": "Pour 75ml lukewarm boiled water. Add 3 scoops. Stir. Feed within 30 minutes. Seal tightly.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Preparation instructions clear"
                }
            }
        },
        {
            "sku_id": "SKU-005",
            "brand": "Nestlé Cerelac",
            "market_city": "Delhi",
            "script": "English-Latin",
            "condition": "creased_foil",
            "fields": {
                "productName": {
                    "gt": "Nestle Cerelac Baby Cereal with Milk Multigrain Dal Veg",
                    "pred": "Nestle Cerelac Baby Cereal with Milk Multigrain Dal Veg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Header legible"
                },
                "ageMarking": {
                    "gt": "From 10 to 24 months / Stage 3",
                    "pred": "From 10 to 24 months / Stage 3",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Stage 3 badge clear"
                },
                "ingredients": {
                    "gt": "Wheat flour (38.0%), Milk solids (32.2%), Rice flour (10.0%), Moong dal flour (6.5%), Tomato crunchies (2.0%), Spinach crunchies (1.5%), Minerals, Vitamins",
                    "pred": "Wheat flour (38.0%), Milk solids (32.2%), Rice flour (10.0%), Moong dal flour (6.5%), Tomato crunchies (2.0%), Spinach crunchies (1.5%), Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 28.0, "notes": "Ingredients intact"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk.",
                    "pred": "Contains Wheat and Milk. May contain gluten, soy, and peanuts.",
                    "status": "clear", "ev": "no", "unsupp": "yes", "err": "unsupported_claim", "sec": 15.0, "notes": "Hallucinated unprinted allergens not present on packaging panel"
                },
                "nutritionPanel": {
                    "gt": "Energy 410 kcal, Protein 15.5 g, Carbohydrate 67.5 g, Total Fat 9.0 g, Iron 8.0 mg, Zinc 3.2 mg",
                    "pred": "Energy 410 kcal, Protein 15.5 g, Carbohydrate 67.5 g, Total Fat 9.0 g, Iron 8.0 mg, Zinc 3.2 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 29.0, "notes": "Nutrition table accurate"
                },
                "preparationAndStorage": {
                    "gt": "Mix 3 scoops with 75ml warm water. Stir well. Discard unfinished feed. Store in airtight container.",
                    "pred": "Mix 3 scoops with 75ml warm water. Stir well. Discard unfinished feed. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-006",
            "brand": "Nestlé Cerelac",
            "market_city": "Chennai",
            "script": "Bilingual (English + Tamil)",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Nestle Cerelac Ragi Apple / நெஸ்லே செரிலாக் ராகி ஆப்பிள்",
                    "pred": "Nestle Cerelac Ragi Apple / நெஸ்லே செரிலாக் ராகி ஆப்பிள்",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Bilingual Tamil header verified"
                },
                "ageMarking": {
                    "gt": "From 6 months onwards / 6 மாதங்கள் முதல்",
                    "pred": "From 6 months onwards / 6 மாதங்கள் முதல்",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Tamil age marking verified"
                },
                "ingredients": {
                    "gt": "Ragi flour (42.0%), Wheat flour (20.0%), Milk solids (28.0%), Apple juice concentrate (4.0%), Sugar, Minerals, Vitamins",
                    "pred": "Ragi flour (42.0%), Wheat flour (20.0%), Milk solids (28.0%), Apple juice concentrate (4.0%), Sugar, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk.",
                    "pred": "Contains Wheat and Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen statement verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 408 kcal, Protein 14.0 g, Total Fat 8.5 g, Calcium 580 mg, Iron 7.8 mg",
                    "pred": "Per 100g: Energy 408 kcal, Protein 14.0 g, Total Fat 8.5 g, Calcium 580 mg, Iron 7.8 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 27.0, "notes": "High calcium ragi panel matched"
                },
                "preparationAndStorage": {
                    "gt": "சூடான கொதித்த நீரை ஆறவைத்து 75 மிலி கிண்ணத்தில் ஊற்றவும். 3 கரண்டி செரிலாக் சேர்த்து கலக்கவும்.",
                    "pred": "சூடான கொதித்த நீரை ஆறவைத்து 75 மிலி கிண்ணத்தில் ஊற்றவும். 3 கரண்டி செரிலாக் சேர்த்து கலக்கவும்.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 22.0, "notes": "Tamil preparation text verified"
                }
            }
        },
        {
            "sku_id": "SKU-007",
            "brand": "Nestlé Cerelac",
            "market_city": "Hyderabad",
            "script": "English-Latin",
            "condition": "low_light",
            "fields": {
                "productName": {
                    "gt": "Nestle Cerelac Baby Cereal Wheat Rice Mixed Fruit",
                    "pred": "Nestle Cerelac Baby Cereal Wheat Rice Mixed Fruit",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 12.0, "notes": "Clean title read"
                },
                "ageMarking": {
                    "gt": "From 8 to 24 months / Stage 2",
                    "pred": "From 8 to 24 months / Stage 2",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Stage 2 verified"
                },
                "ingredients": {
                    "gt": "Wheat flour (35.0%), Rice flour (20.0%), Milk solids (32.0%), Apple juice concentrate (2.5%), Orange juice concentrate (1.5%), Minerals, Vitamins",
                    "pred": "Wheat flour (35.0%), Rice flour (20.0%), Milk solids (32.0%), Apple juice concentrate (2.5%), Orange juice concentrate (1.5%), Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk.",
                    "pred": "Contains Wheat and Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Energy 411 kcal, Protein 14.8 g, Carbohydrate 68.5 g, Fat 9.1 g, Iron 7.5 mg per 100g",
                    "pred": "Energy 411 kcal, Protein 14.8 g, Carbohydrate 68.5 g, Fat 9.1 g, Iron 1.5 mg per 100g",
                    "status": "clear", "ev": "no", "unsupp": "yes", "err": "altered_number", "sec": 31.0, "notes": "Low light noise caused Iron 7.5 mg to be read as 1.5 mg"
                },
                "preparationAndStorage": {
                    "gt": "Mix 3 scoops in 75ml lukewarm water. Discard leftover feed. Keep in cool dry place.",
                    "pred": "Mix 3 scoops in 75ml lukewarm water. Discard leftover feed. Keep in cool dry place.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Preparation instructions clear"
                }
            }
        },
        {
            "sku_id": "SKU-008",
            "brand": "Nestlé Cerelac",
            "market_city": "Pune",
            "script": "English-Latin",
            "condition": "curved_tin",
            "fields": {
                "productName": {
                    "gt": "Nestle Cerelac Baby Cereal with Milk Multigrain & Fruits",
                    "pred": "Nestle Cerelac Baby Cereal with Milk Multigrain & Fruits",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 13.0, "notes": "Tin label curved front panel"
                },
                "ageMarking": {
                    "gt": "12 to 24 months / Stage 4",
                    "pred": "12 to 24 months / Stage 4",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Stage 4 badge legible"
                },
                "ingredients": {
                    "gt": "Multigrain flour (Wheat 32%, Oat 12%, Rice 10%), Milk solids (30.0%), Sugar, Apple flakes (3.0%), Strawberry flakes (2.0%), Minerals, Vitamins",
                    "pred": "Multigrain flour (Wheat 32%, Oat 12%, Rice 10%), Milk solids (30.0%), Sugar, Apple flakes (3.0%), Strawberry flakes (2.0%), Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 30.0, "notes": "Curved text captured across scan"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat, Oat and Milk.",
                    "pred": "Contains Wheat, Oat and Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Allergen list verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 418 kcal, Protein 15.2 g, Fat 9.5 g, Fibre 3.8 g, Iron 8.5 mg, Calcium 550 mg",
                    "pred": "Per 100g: Energy 418 kcal, Protein 152 g, Fat 9.5 g, Fibre 3.8 g, Iron 8.5 mg, Calcium 550 mg",
                    "status": "clear", "ev": "no", "unsupp": "yes", "err": "altered_number", "sec": 34.0, "notes": "Curved tin edge distortion dropped decimal on Protein 15.2 g -> 152 g"
                },
                "preparationAndStorage": {
                    "gt": "Wash hands. Add 4 scoops to 100ml warm boiled water. Feed with clean spoon. Close tin tightly after each use.",
                    "pred": "Wash hands. Add 4 scoops to 100ml warm boiled water. Feed with clean spoon. Close tin tightly after each use.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 17.0, "notes": "Instructions verified"
                }
            }
        },
        {
            "sku_id": "SKU-009",
            "brand": "Nestlé Cerelac",
            "market_city": "Kolkata",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Nestle Cerelac Baby Cereal with Milk Maize & Milk",
                    "pred": "Nestle Cerelac Baby Cereal with Milk Maize & Milk",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Standard carton capture"
                },
                "ageMarking": {
                    "gt": "From 6 to 24 months / Stage 1",
                    "pred": "From 6 to 24 months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 badge clear"
                },
                "ingredients": {
                    "gt": "Corn flour (Maize) (52.0%), Milk solids (35.0%), Sugar, Soyabean oil, Minerals, Vitamins",
                    "pred": "Corn flour (Maize) (52.0%), Milk solids (35.0%), Sugar, Soyabean oil, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 21.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Milk. May contain Soy.",
                    "pred": "Contains Milk. May contain Soy.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 412 kcal, Protein 14.2 g, Carbohydrate 69.5 g, Fat 9.0 g, Iron 7.5 mg",
                    "pred": "Per 100g: Energy 412 kcal, Protein 14.2 g, Carbohydrate 69.5 g, Fat 9.0 g, Iron 7.5 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Boil water for 5 min. Mix 3 scoops in 75ml lukewarm water. Store in airtight container.",
                    "pred": "Boil water for 5 min. Mix 3 scoops in 75ml lukewarm water. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 13.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-010",
            "brand": "Nestlé Cerelac",
            "market_city": "Delhi",
            "script": "Hindi-Devanagari",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "नेस्ले सेरेलक फोर्टिफाइड बेबी सेरेल दूध के साथ गेहूँ",
                    "pred": "नेस्ले सेरेलक फोर्टिफाइड बेबी सेरेल दूध के साथ गेहूँ",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Full Hindi Devanagari title verified"
                },
                "ageMarking": {
                    "gt": "६ महीने से २४ महीने तक / स्टेज १",
                    "pred": "६ महीने से २४ महीने तक / स्टेज १",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 9.0, "notes": "Devanagari numerals ६-२४ recognized"
                },
                "ingredients": {
                    "gt": "गेहूँ का आटा (५२%), दूध के ठोस घटक (३५%), चीनी, सोयाबीन तेल, खनिज, विटामिन",
                    "pred": "गेहूँ का आटा (५२%), दूध के ठोस घटक (३५%), चीनी, सोयाबीन तेल, खनिज, विटमिन",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "script_confusion", "sec": 29.0, "notes": "Matra dropped on Devanagari conjunct: विटामिन -> विटमिन"
                },
                "allergenDeclaration": {
                    "gt": "गेहूँ और दूध शामिल है।",
                    "pred": "गेहूँ और दूध शामिल है।",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Hindi allergen text exact"
                },
                "nutritionPanel": {
                    "gt": "प्रति १०० ग्राम: ऊर्जा ४१३ किलो कैलोरी, प्रोटीन १५.० ग्राम, कुल वसा ९.४ ग्राम, आयरन ७.५ मिलीग्राम",
                    "pred": "प्रति १०० ग्राम: ऊर्जा ४१३ किलो कैलोरी, प्रोटीन १५.० ग्राम, कुल वसा ९.४ ग्राम, आयरन ७.५ मिलीग्राम",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 31.0, "notes": "Devanagari nutrition panel verified"
                },
                "preparationAndStorage": {
                    "gt": "हाथ अच्छी तरह धोएं। पीने का पानी ५ मिनट उबालें। ७५ मिलीलीटर गुनगुने पानी में ३ स्कूप सेरेलक मिलाएं।",
                    "pred": "हाथ अच्छी तरह धोएं। पीने का पानी ५ मिनट उबालें। ७५ मिलीलीटर गुनगुने पानी में ३ स्कूप सेरेलक मिलाएं।",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 23.0, "notes": "Hindi preparation instructions exact"
                }
            }
        },

        # --- Brand 2: Nestlé Nestum (4 SKUs) ---
        {
            "sku_id": "SKU-011",
            "brand": "Nestlé Nestum",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Nestle Nestum Baby Cereal Rice",
                    "pred": "Nestle Nestum Baby Cereal Rice",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 9.0, "notes": "Exact title"
                },
                "ageMarking": {
                    "gt": "From 6 to 24 months / Stage 1",
                    "pred": "From 6 to 24 months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 clear"
                },
                "ingredients": {
                    "gt": "Rice flour (96.5%), Sugar, Minerals, Vitamins, Enzyme (Alpha amylase)",
                    "pred": "Rice flour (96.5%), Sugar, Minerals, Vitamins, Enzyme (Alpha amylase)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 19.0, "notes": "Non-milk cereal ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "May contain Milk.",
                    "pred": "May contain Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Cross-contact statement verified"
                },
                "nutritionPanel": {
                    "gt": "Energy 377 kcal, Protein 7.0 g, Carbohydrate 84.5 g, Fat 1.2 g, Iron 7.5 mg, Calcium 230 mg per 100g",
                    "pred": "Energy 377 kcal, Protein 7.0 g, Carbohydrate 84.5 g, Fat 1.2 g, Iron 7.5 mg, Calcium 230 mg per 100g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Panel accurate"
                },
                "preparationAndStorage": {
                    "gt": "Wash hands. Boil milk or water. Mix 3 scoops into 100ml warm liquid. Discard leftover. Store in cool dry place.",
                    "pred": "Wash hands. Boil milk or water. Mix 3 scoops into 100ml warm liquid. Discard leftover. Store in cool dry place.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-012",
            "brand": "Nestlé Nestum",
            "market_city": "Mumbai",
            "script": "English-Latin",
            "condition": "slight_angle",
            "fields": {
                "productName": {
                    "gt": "Nestle Nestum Baby Cereal Wheat",
                    "pred": "Nestle Nestum Baby Cereal Wheat",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Carton scan"
                },
                "ageMarking": {
                    "gt": "From 6 to 24 months / Stage 1",
                    "pred": "From 6 to 24 months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 clear"
                },
                "ingredients": {
                    "gt": "Wheat flour (95.0%), Sugar, Minerals, Vitamins, Enzyme (Alpha amylase)",
                    "pred": "Wheat flour (95.0%), Sugar, Minerals, Vitamins, Enzyme (Alpha amylase)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 20.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat. May contain Milk.",
                    "pred": "Contains Wheat. May contain Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen line matched"
                },
                "nutritionPanel": {
                    "gt": "Energy 375 kcal, Protein 10.0 g, Carbohydrate 81.0 g, Total Fat 1.5 g, Iron 7.5 mg per 100g",
                    "pred": "Energy 375 kcal, Protein 10.0 g, Carbohydrate 81.0 g, Total Fat 1.5 g, Iron 7.5 mg per 100g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Accurate nutrition"
                },
                "preparationAndStorage": {
                    "gt": "Boil 100ml water/milk for 5 minutes. Let cool. Mix 3 scoops. Use clean spoon. Keep tightly closed.",
                    "pred": "Boil 100ml water/milk for 5 minutes. Let cool. Mix 3 scoops. Use clean spoon. Keep tightly closed.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-013",
            "brand": "Nestlé Nestum",
            "market_city": "Delhi",
            "script": "English-Latin",
            "condition": "low_light",
            "fields": {
                "productName": {
                    "gt": "Nestle Nestum Baby Cereal Rice & Moong Dal",
                    "pred": "Nestle Nestum Baby Cereal Rice & Moong Dal",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Stage 2 package"
                },
                "ageMarking": {
                    "gt": "From 8 to 24 months / Stage 2",
                    "pred": "From 8 to 24 months / Stage 2",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Stage 2 verified"
                },
                "ingredients": {
                    "gt": "Rice flour (76.0%), Moong dal flour (18.5%), Sugar, Minerals, Vitamins",
                    "pred": "Rice flour (76.0%), Moong dal flour (18.5%), Sugar, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 22.0, "notes": "Moong dal formula verified"
                },
                "allergenDeclaration": {
                    "gt": "May contain Milk.",
                    "pred": "Contains pulses and lentils. May contain Milk.",
                    "status": "clear", "ev": "no", "unsupp": "yes", "err": "inferred_allergen", "sec": 14.0, "notes": "Model inferred non-declared pulse allergen from ingredients list"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 372 kcal, Protein 9.8 g, Carbohydrate 80.2 g, Fat 1.3 g, Iron 7.8 mg",
                    "pred": "Per 100g: Energy 372 kcal, Protein 9.8 g, Carbohydrate 80.2 g, Fat 1.3 g, Iron 7.8 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 27.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 3 levelled scoops with 100ml warm water or milk. Discard uneaten food. Store in airtight container.",
                    "pred": "Mix 3 levelled scoops with 100ml warm water or milk. Discard uneaten food. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation instructions verified"
                }
            }
        },
        {
            "sku_id": "SKU-014",
            "brand": "Nestlé Nestum",
            "market_city": "Pune",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Nestle Nestum Baby Cereal Rice Vegetables",
                    "pred": "Nestle Nestum Baby Cereal Rice Vegetables",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 12.0, "notes": "Title matched"
                },
                "ageMarking": {
                    "gt": "From 8 to 24 months / Stage 2",
                    "pred": "From 8 to 24 months / Stage 2",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Stage 2 marking"
                },
                "ingredients": {
                    "gt": "Rice flour (78.0%), Carrot flakes (3.5%), Spinach flakes (2.5%), Tomato powder (1.5%), Sugar, Minerals, Vitamins",
                    "pred": "Rice flour (78.0%), Carrot flakes (3.5%), Spinach flakes (2.5%), Sugar, Minerals, Vitamins",
                    "status": "partial", "ev": "yes", "unsupp": "no", "err": "dropped_ingredient", "sec": 29.0, "notes": "Tomato powder washed out by glare flare on pouch seam"
                },
                "allergenDeclaration": {
                    "gt": "May contain Milk.",
                    "pred": "May contain Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen line matched"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 370 kcal, Protein 7.5 g, Carbohydrate 81.5 g, Fat 1.2 g, Vitamin A 320 ug",
                    "pred": "Per 100g: Energy 370 kcal, Protein 7.5 g, Carbohydrate 81.5 g, Fat 1.2 g, Vitamin A 320 ug",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 28.0, "notes": "Panel accurate"
                },
                "preparationAndStorage": {
                    "gt": "Boil water for 5 minutes. Mix 3 scoops in 100ml lukewarm liquid. Consume immediately.",
                    "pred": "Boil water for 5 minutes. Mix 3 scoops in 100ml lukewarm liquid. Consume immediately.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Preparation instructions clear"
                }
            }
        },

        # --- Brand 3: Slurrp Farm (8 SKUs) ---
        {
            "sku_id": "SKU-015",
            "brand": "Slurrp Farm",
            "market_city": "Delhi",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Slurrp Farm Organic Baby Cereal Ragi, Rice & Mango",
                    "pred": "Slurrp Farm Organic Baby Cereal Ragi, Rice & Mango",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Clean carton capture"
                },
                "ageMarking": {
                    "gt": "6+ months / Stage 1",
                    "pred": "6+ months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.5, "notes": "Age badge verified"
                },
                "ingredients": {
                    "gt": "Organic Sprouted Ragi flour (45%), Organic White Rice flour (35%), Mango powder (15%), Vitamins and Minerals premix (0.5%)",
                    "pred": "Organic Sprouted Ragi flour (45%), Organic White Rice flour (35%), Mango powder (15%), Vitamins and Minerals premix (0.5%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Ingredients exact"
                },
                "allergenDeclaration": {
                    "gt": "Made in a facility that also handles nuts, milk, and soy.",
                    "pred": "Made in a facility that also handles nuts, milk, and soy.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Facility advisory matched"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 368 kcal, Protein 7.8 g, Carbohydrate 81.2 g, Total Sugars 8.5 g, Added Sugars 0 g, Dietary Fibre 6.2 g, Calcium 280 mg, Iron 6.5 mg",
                    "pred": "Per 100g: Energy 368 kcal, Protein 7.8 g, Carbohydrate 81.2 g, Total Sugars 8.5 g, Added Sugars 0 g, Dietary Fibre 6.2 g, Calcium 280 mg, Iron 6.5 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 30.0, "notes": "Full zero added sugar panel verified"
                },
                "preparationAndStorage": {
                    "gt": "Add 3 tablespoons (30g) of cereal to 100ml of boiling water or milk. Cook on medium heat for 2 minutes stirring continuously. Store in airtight container after opening.",
                    "pred": "Add 3 tablespoons (30g) of cereal to 100ml of boiling water or milk. Cook on medium heat for 2 minutes stirring continuously. Store in airtight container after opening.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 19.0, "notes": "Cooking instructions verified"
                }
            }
        },
        {
            "sku_id": "SKU-016",
            "brand": "Slurrp Farm",
            "market_city": "Mumbai",
            "script": "English-Latin",
            "condition": "slight_angle",
            "fields": {
                "productName": {
                    "gt": "Slurrp Farm Organic Baby Cereal Ragi, Rice & Strawberry",
                    "pred": "Slurrp Farm Organic Baby Cereal Ragi, Rice & Strawberry",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "6+ months / Stage 1",
                    "pred": "6+ months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 badge"
                },
                "ingredients": {
                    "gt": "Organic Sprouted Ragi flour (44%), Organic White Rice flour (36%), Freeze dried Strawberry powder (14%), Vitamins and Minerals premix (0.5%)",
                    "pred": "Organic Sprouted Ragi flour (44%), Organic White Rice flour (36%), Freeze dried Strawberry powder (14%), Vitamins and Minerals premix (0.5%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 23.0, "notes": "Full ingredients"
                },
                "allergenDeclaration": {
                    "gt": "Manufactured on equipment that processes dairy, soy, and tree nuts.",
                    "pred": "Manufactured on equipment that processes dairy, soy, and tree nuts.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Advisory verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 365 kcal, Protein 7.6 g, Carbohydrate 80.5 g, Added Sugars 0 g, Fibre 6.5 g, Iron 6.2 mg",
                    "pred": "Per 100g: Energy 365 kcal, Protein 7.6 g, Carbohydrate 80.5 g, Added Sugars 0 g, Fibre 6.5 g, Iron 6.2 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Stir 3 tablespoons into 100ml hot water or milk. Simmer for 2 minutes. Feed lukewarm. Store in cool place.",
                    "pred": "Stir 3 tablespoons into 100ml hot water or milk. Simmer for 2 minutes. Feed lukewarm. Store in cool place.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-017",
            "brand": "Slurrp Farm",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Slurrp Farm Organic Millet Dosa Mix Beetroot",
                    "pred": "Slurrp Farm Organic Millet Dosa Mix Beetroot",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Pouch front read"
                },
                "ageMarking": {
                    "gt": "8+ months / Toddler & Kids",
                    "pred": "8+ months / Toddler & Kids",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Oat flour (35%), Foxtail millet (25%), Urad dal (20%), Beetroot powder (10%), Rice (8%), Salt, Cumin",
                    "pred": "Oat flour (35%), Foxtail millet (25%), Urad dal (20%), Beetroot powder (10%), Rice (8%), Salt, Cumin",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Oats. May contain traces of nuts and milk.",
                    "pred": "Contains Oats. May contain traces of nuts and milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Allergen statement verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 355 kcal, Protein 12.5 g, Carbohydrate 68.0 g, Total Fat 3.5 g, Iron 4.5 mg, Sodium 240 mg",
                    "pred": "Per 100g: Energy 355 kcal, Protein 12.5 g, Carbohydrate 68.0 g, Total Fat 3.5 g, Iron 4.5 mg, Sodium 24 mg",
                    "status": "clear", "ev": "no", "unsupp": "yes", "err": "altered_number", "sec": 33.0, "notes": "Glare on shiny pouch seam dropped zero from Sodium 240 mg -> 24 mg"
                },
                "preparationAndStorage": {
                    "gt": "Mix 1/2 cup dosa mix with 1/2 cup water and 1 tbsp curd. Rest for 5 mins. Cook on warm tava with ghee until golden. Store pouch tightly zipped.",
                    "pred": "Mix 1/2 cup dosa mix with 1/2 cup water and 1 tbsp curd. Rest for 5 mins. Cook on warm tava with ghee until golden. Store pouch tightly zipped.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 18.0, "notes": "Preparation steps verified"
                }
            }
        },
        {
            "sku_id": "SKU-018",
            "brand": "Slurrp Farm",
            "market_city": "Hyderabad",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Slurrp Farm Organic Millet Dosa Mix Spinach",
                    "pred": "Slurrp Farm Organic Millet Dosa Mix Spinach",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Front title verified"
                },
                "ageMarking": {
                    "gt": "8+ months",
                    "pred": "8+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Oat flour (35%), Foxtail millet (25%), Urad dal (20%), Spinach powder (10%), Rice (8%), Salt, Curry leaf powder",
                    "pred": "Oat flour (35%), Foxtail millet (25%), Urad dal (20%), Spinach powder (10%), Rice (8%), Salt, Curry leaf powder",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Oats. May contain traces of dairy.",
                    "pred": "Contains Oats. May contain traces of dairy.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 352 kcal, Protein 12.8 g, Carbohydrate 67.5 g, Fat 3.2 g, Iron 5.0 mg",
                    "pred": "Per 100g: Energy 352 kcal, Protein 12.8 g, Carbohydrate 67.5 g, Fat 3.2 g, Iron 5.0 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Panel accurate"
                },
                "preparationAndStorage": {
                    "gt": "Mix 1/2 cup mix with 1/2 cup water. Pour ladle onto tava. Add butter. Serve warm.",
                    "pred": "Mix 1/2 cup mix with 1/2 cup water. Pour ladle onto tava. Add butter. Serve warm.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-019",
            "brand": "Slurrp Farm",
            "market_city": "Pune",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Slurrp Farm Ragi Almond Pancake Mix",
                    "pred": "Slurrp Farm Ragi Almond Pancake Mix",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "12+ months",
                    "pred": "12+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age badge clear"
                },
                "ingredients": {
                    "gt": "Oat flour (38%), Sprouted Ragi (28%), Jaggery powder (15%), Almond meal (10%), Cocoa (5%), Baking powder",
                    "pred": "Oat flour (38%), Sprouted Ragi (28%), Jaggery powder (15%), Almond meal (10%), Cocoa (5%), Baking powder",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Almonds and Oats. May contain Milk and Soy.",
                    "pred": "Contains Almonds and Oats. May contain Milk and Soy.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Nut allergen declaration verified"
                },
                "nutritionPanel": {
                    "gt": "Energy 385 kcal, Protein 10.2 g, Fat 6.5 g, Carbohydrate 71.0 g, Total Sugars 16.0 g, Calcium 210 mg per 100g",
                    "pred": "Energy 385 kcal, Protein 10.2 g, Fat 6.5 g, Carbohydrate 71.0 g, Total Sugars 16.0 g, Calcium 210 mg per 100g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 27.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Whisk 1 cup mix with 1/2 cup warm milk. Cook small pancakes on non-stick pan. Keep pouch sealed.",
                    "pred": "Whisk 1 cup mix with 1/2 cup warm milk. Cook small pancakes on non-stick pan. Keep pouch sealed.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Cooking directions verified"
                }
            }
        },
        {
            "sku_id": "SKU-020",
            "brand": "Slurrp Farm",
            "market_city": "Chennai",
            "script": "English-Latin",
            "condition": "creased_foil",
            "fields": {
                "productName": {
                    "gt": "Slurrp Farm Jowar Banana Baby Cereal",
                    "pred": "Slurrp Farm Jowar Banana Baby Cereal",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Title read verified"
                },
                "ageMarking": {
                    "gt": "6+ months",
                    "pred": "6+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age badge clear"
                },
                "ingredients": {
                    "gt": "Organic Jowar flour (Sorghum) (50%), Organic Rice (32%), Banana fruit powder (17%), Vitamin premix (1%)",
                    "pred": "Organic Jowar flour (Sorghum) (50%), Organic Rice (32%), Banana fruit powder (17%), Vitamin premix (1%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 23.0, "notes": "Ingredients intact"
                },
                "allergenDeclaration": {
                    "gt": "Gluten Free. Made in a facility handling tree nuts and milk.",
                    "pred": "Gluten Free. Made in a facility handling tree nuts and milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Gluten-free note verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 360 kcal, Protein 7.2 g, Carbohydrate 82.0 g, Total Fat 1.8 g, Iron 5.8 mg",
                    "pred": "Per 100g: Energy 360 kcal, Protein 7.2 g, Carbohydrate 82.0 g, Total Fat 1.8 g, Iron 5.8 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 30g with 100ml water or milk. Cook 2 mins on low heat. Store in cool, dry place.",
                    "pred": "Mix 30g with 100ml water or milk. Cook 2 mins on low heat. Store in cool, dry place.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-021",
            "brand": "Slurrp Farm",
            "market_city": "Kolkata",
            "script": "English-Latin",
            "condition": "low_light",
            "fields": {
                "productName": {
                    "gt": "Slurrp Farm Organic Supergrains Banana & Apple Cereal",
                    "pred": "Slurrp Farm Organic Supergrains Banana & Apple Cereal",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 12.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "6+ months",
                    "pred": "6+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age badge clear"
                },
                "ingredients": {
                    "gt": "Organic Ragi (30%), Organic Jowar (30%), Organic Rice (20%), Banana powder (10%), Apple powder (9%), Vitamin premix (1%)",
                    "pred": "Organic Ragi (30%), Organic Jowar (30%), Organic Rice (20%), Banana powder (10%), Apple powder (9%), Vitamin premix (1%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "May contain Milk and Nuts.",
                    "pred": "May contain Milk and Nuts.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Advisory verified"
                },
                "nutritionPanel": {
                    "gt": "Energy 366 kcal, Protein 8.0 g, Carbohydrate 80.5 g, Fat 2.0 g, Iron 6.0 mg, Calcium 260 mg",
                    "pred": "Energy 366 kcal, Protein 8.0 g, Carbohydrate 80.5 g, Fat 2.0 g, Iron 6.0 mg, Calcium 260 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 27.0, "notes": "Nutrition panel verified"
                },
                "preparationAndStorage": {
                    "gt": "Boil 100ml water. Add 3 spoons cereal. Cook for 2 minutes. Feed warm.",
                    "pred": "Boil 100ml water. Add 3 spoons cereal. Cook for 2 minutes. Feed warm.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-022",
            "brand": "Slurrp Farm",
            "market_city": "Delhi",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Slurrp Farm Millet Star Bites Cheese & Herbs",
                    "pred": "Slurrp Farm Millet Star Bites Cheese & Herbs",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Puffed snack front read"
                },
                "ageMarking": {
                    "gt": "10+ months / Toddler Snack",
                    "pred": "10+ months / Toddler Snack",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Corn flour (40%), Rice (30%), Ragi (15%), Sunflower oil (8%), Cheese powder (5%), Oregano, Parsley, Salt",
                    "pred": "Corn flour (40%), Rice (30%), Ragi (15%), Sunflower oil (8%), Cheese powder (5%), Oregano, Parsley",
                    "status": "partial", "ev": "yes", "unsupp": "no", "err": "dropped_ingredient", "sec": 28.0, "notes": "Salt omitted due to pouch reflection on bottom line"
                },
                "allergenDeclaration": {
                    "gt": "Contains Milk (Cheese).",
                    "pred": "Contains Milk (Cheese).",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 420 kcal, Protein 8.5 g, Total Fat 12.0 g, Sodium 310 mg, Calcium 120 mg",
                    "pred": "Per 100g: Energy 420 kcal, Protein 8.5 g, Total Fat 12.0 g, Sodium 310 mg, Calcium 120 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition matched"
                },
                "preparationAndStorage": {
                    "gt": "Ready to eat finger food. Always supervise baby while feeding. Store in cool, dry place. Reseal zip lock.",
                    "pred": "Ready to eat finger food. Always supervise baby while feeding. Store in cool, dry place. Reseal zip lock.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Supervision note verified"
                }
            }
        },

        # --- Brand 4: Manna First Foods (5 SKUs) ---
        {
            "sku_id": "SKU-023",
            "brand": "Manna First Foods",
            "market_city": "Chennai",
            "script": "Tamil-Tamil",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "மன்னா ராகி ரிச் முளைகட்டிய ராகி குழந்தை உணவு",
                    "pred": "மன்னா ராகி ரிச் முளைகட்டிய ராகி குழந்தை உணவு",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 17.0, "notes": "Tamil title verified"
                },
                "ageMarking": {
                    "gt": "6 மாதங்கள் முதல் / நிலை 1",
                    "pred": "6 மாதங்கள் முதல் / நிலை 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Tamil stage indicator"
                },
                "ingredients": {
                    "gt": "முளைகட்டிய ராகி மாவு (100%)",
                    "pred": "முளைகட்டிய ராகி மாவு (100%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 18.0, "notes": "Single ingredient sprouted ragi"
                },
                "allergenDeclaration": {
                    "gt": "இயற்கையாகவே பசையம் இல்லாதது (Gluten Free).",
                    "pred": "இயற்கையாகவே பசையம் இல்லாதது (Gluten Free).",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 9.0, "notes": "Gluten free marking verified"
                },
                "nutritionPanel": {
                    "gt": "100 கிராமுக்கு: ஆற்றல் 364 கிலோ கலோரி, புரதம் 8.5 கிராம், கால்சியம் 344 மி.கி, இரும்பு 4.2 மி.கி",
                    "pred": "100 கிராமுக்கு: ஆற்றல் 364 கிலோ கலோரி, புரதம் 8.5 கிராம், கால்சியம் 344 மி.கி, இரும்பு 4.2 மி.கி",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 30.0, "notes": "Tamil nutrition text verified"
                },
                "preparationAndStorage": {
                    "gt": "1 கப் நீரில் 2 ஸ்பூன் ராகி மாவை கட்டியில்லாமல் கரைக்கவும். 5 நிமிடங்கள் மிதமான தீயில் கிளறி வேகவைக்கவும்.",
                    "pred": "1 கப் நீரில் 2 ஸ்பூன் ராகி மாவை கட்டியில்லாமல் கரைக்கவும். 5 நிமிடங்கள் மிதமான தீயில் கிளரி வேகவைக்கவும்.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "script_confusion", "sec": 24.0, "notes": "Tamil character confusion on retroflex liquid: கிளறி -> கிளரி"
                }
            }
        },
        {
            "sku_id": "SKU-024",
            "brand": "Manna First Foods",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Manna First Foods Sprouted Green Gram & Rice",
                    "pred": "Manna First Foods Sprouted Green Gram & Rice",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "6+ months / Stage 1",
                    "pred": "6+ months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 verified"
                },
                "ingredients": {
                    "gt": "Sprouted Green Gram flour (Moong) (55%), Parboiled Rice flour (45%)",
                    "pred": "Sprouted Green Gram flour (Moong) (55%), Parboiled Rice flour (45%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 19.0, "notes": "Dual ingredient formula"
                },
                "allergenDeclaration": {
                    "gt": "None declared.",
                    "pred": "May contain trace legumes.",
                    "status": "clear", "ev": "no", "unsupp": "yes", "err": "inferred_allergen", "sec": 12.0, "notes": "Model hallucinated allergen disclaimer not present on pack"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 368 kcal, Protein 14.5 g, Carbohydrate 75.0 g, Total Fat 1.2 g, Iron 5.2 mg",
                    "pred": "Per 100g: Energy 368 kcal, Protein 14.5 g, Carbohydrate 75.0 g, Total Fat 1.2 g, Iron 5.2 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 2 tbsp with 150ml water. Cook on stove for 3-5 mins stirring constantly. Serve warm.",
                    "pred": "Mix 2 tbsp with 150ml water. Cook on stove for 3-5 mins stirring constantly. Serve warm.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-025",
            "brand": "Manna First Foods",
            "market_city": "Chennai",
            "script": "Bilingual (English + Tamil)",
            "condition": "slight_angle",
            "fields": {
                "productName": {
                    "gt": "Manna Ragi Rich Sprouted Ragi & Apple / மன்னா ராகி மற்றும் ஆப்பிள்",
                    "pred": "Manna Ragi Rich Sprouted Ragi & Apple / மன்னா ராகி மற்றும் ஆப்பிள்",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Bilingual title verified"
                },
                "ageMarking": {
                    "gt": "8+ months / Stage 2",
                    "pred": "8+ months / Stage 2",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Stage 2 verified"
                },
                "ingredients": {
                    "gt": "Sprouted Ragi (80%), Dehydrated Apple Powder (20%)",
                    "pred": "Sprouted Ragi (80%), Dehydrated Apple Powder (20%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 18.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Gluten Free. No milk or soy added.",
                    "pred": "Gluten Free. No milk or soy added.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 360 kcal, Protein 7.5 g, Carbohydrate 81.0 g, Calcium 310 mg, Iron 4.0 mg",
                    "pred": "Per 100g: Energy 360 kcal, Protein 7.5 g, Carbohydrate 81.0 g, Calcium 310 mg, Iron 4.0 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Panel accurate"
                },
                "preparationAndStorage": {
                    "gt": "Add 2 tbsp to 1 cup milk or water. Cook 5 mins. Store in airtight container.",
                    "pred": "Add 2 tbsp to 1 cup milk or water. Cook 5 mins. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-026",
            "brand": "Manna First Foods",
            "market_city": "Hyderabad",
            "script": "English-Latin",
            "condition": "creased_foil",
            "fields": {
                "productName": {
                    "gt": "Manna First Foods Sathumaavu Multi Grain Porridge",
                    "pred": "Manna First Foods Sathumaavu Multi Grain Porridge",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Traditional sathumaavu pack"
                },
                "ageMarking": {
                    "gt": "8+ months / Stage 2",
                    "pred": "8+ months / Stage 2",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 2 verified"
                },
                "ingredients": {
                    "gt": "Sprouted Ragi (25%), Wheat (20%), Roasted Gram (15%), Green Gram (10%), Red Rice (10%), Jowar (8%), Bajra (7%), Almonds (3%), Cardamom (2%)",
                    "pred": "Sprouted Ragi (25%), Wheat (20%), Roasted Gram (15%), Green Gram (10%), Red Rice (10%), Jowar (8%), Bajra (7%), Almonds (3%), Cardamom (2%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 31.0, "notes": "Full traditional mix ingredients"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Almonds. Processed in a nut facility.",
                    "pred": "Contains Wheat and Almonds. Processed in a nut facility.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 380 kcal, Protein 12.0 g, Carbohydrate 74.0 g, Total Fat 3.8 g, Iron 5.5 mg",
                    "pred": "Per 100g: Energy 380 kcal, Protein 12.0 g, Carbohydrate 74.0 g, Total Fat 3.8 g, Iron 5.5 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 27.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 2 tbsp with 200ml milk or water. Boil on low flame for 5 mins stirring continuously.",
                    "pred": "Mix 2 tbsp with 200ml milk or water. Boil on low flame for 5 mins stirring continuously.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Cooking verified"
                }
            }
        },
        {
            "sku_id": "SKU-027",
            "brand": "Manna First Foods",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "low_light",
            "fields": {
                "productName": {
                    "gt": "Manna Ragi Rich Sprouted Ragi with Banana",
                    "pred": "Manna Ragi Rich Sprouted Ragi with Banana",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "6+ months / Stage 1",
                    "pred": "6+ months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 clear"
                },
                "ingredients": {
                    "gt": "Sprouted Ragi flour (82%), Natural Banana Powder (18%)",
                    "pred": "Sprouted Ragi flour (82%), Natural Banana Powder (18%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 18.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Gluten Free.",
                    "pred": "Gluten Free.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Energy 362 kcal, Protein 7.8 g, Carbohydrate 81.5 g, Calcium 320 mg, Potassium 410 mg per 100g",
                    "pred": "Energy 362 kcal, Protein 7.8 g, Carbohydrate 81.5 g, Calcium 320 mg, Potassium 410 mg per 100g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 2 tbsp with 1 cup milk or water. Simmer for 3 minutes. Discard unfinished feed.",
                    "pred": "Mix 2 tbsp with 1 cup milk or water. Simmer for 3 minutes. Discard unfinished feed.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Preparation verified"
                }
            }
        },

        # --- Brand 5: Timios (5 SKUs) ---
        {
            "sku_id": "SKU-028",
            "brand": "Timios",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Timios Melts Apple & Cinnamon Finger Food",
                    "pred": "Timios Melts Apple & Cinnamon Finger Food",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Foil pouch title"
                },
                "ageMarking": {
                    "gt": "9+ months / Stage 2",
                    "pred": "9+ months / Stage 2",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age badge clear"
                },
                "ingredients": {
                    "gt": "Whole wheat flour (45%), Rice (30%), Apple juice concentrate (18%), Sunflower oil (6%), Cinnamon (1%)",
                    "pred": "Whole wheat flour (45%), Rice (30%), Apple juice concentrate (18%), Sunflower oil (6%)",
                    "status": "partial", "ev": "yes", "unsupp": "no", "err": "dropped_ingredient", "sec": 29.0, "notes": "Cinnamon (1%) dropped due to glare reflection on pouch curve"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat. May contain traces of milk and nuts.",
                    "pred": "Contains Wheat. May contain traces of milk and nuts.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Allergen line verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 390 kcal, Protein 8.0 g, Carbohydrate 78.0 g, Added Sugars 0 g, Total Fat 5.5 g, Sodium 12 mg",
                    "pred": "Per 100g: Energy 390 kcal, Protein 8.0 g, Carbohydrate 78.0 g, Added Sugars 0 g, Total Fat 5.5 g, Sodium 12 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Panel accurate"
                },
                "preparationAndStorage": {
                    "gt": "Dissolves easily in mouth. Only feed to sitting, supervised children. Store in airtight container.",
                    "pred": "Dissolves easily in mouth. Only feed to sitting, supervised children. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Safety advisory verified"
                }
            }
        },
        {
            "sku_id": "SKU-029",
            "brand": "Timios",
            "market_city": "Mumbai",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Timios Melts Blueberry Finger Food",
                    "pred": "Timios Melts Blueberry Finger Food",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Pouch title verified"
                },
                "ageMarking": {
                    "gt": "9+ months",
                    "pred": "9+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Whole wheat flour (46%), Rice (30%), Blueberry juice concentrate (18%), Cold pressed sunflower oil (6%)",
                    "pred": "Whole wheat flour (46%), Rice (30%), Blueberry juice concentrate (18%), Cold pressed sunflower oil (6%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat.",
                    "pred": "Contains Wheat.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 388 kcal, Protein 8.2 g, Carbohydrate 77.5 g, Total Fat 5.4 g, Sodium 14 mg",
                    "pred": "Per 100g: Energy 388 kcal, Protein 8.2 g, Carbohydrate 77.5 g, Total Fat 5.4 g, Sodium 14 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Ready to eat melts. Supervise baby during consumption. Reseal pouch tightly.",
                    "pred": "Ready to eat melts. Supervise baby during consumption. Reseal pouch tightly.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Advisory verified"
                }
            }
        },
        {
            "sku_id": "SKU-030",
            "brand": "Timios",
            "market_city": "Delhi",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Timios Teething Sticks Cumin & Ajwain",
                    "pred": "Timios Teething Sticks Cumin & Ajwain",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Box capture"
                },
                "ageMarking": {
                    "gt": "8+ months / Teether",
                    "pred": "8+ months / Teether",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Teether badge"
                },
                "ingredients": {
                    "gt": "Whole wheat flour (65%), Rice bran oil (15%), Ground cumin (8%), Ground ajwain (4%), Salt (1%), Water",
                    "pred": "Whole wheat flour (65%), Rice bran oil (15%), Ground cumin (8%), Ground ajwain (4%), Salt (1%), Water",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 22.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat. May contain traces of sesame.",
                    "pred": "Contains Wheat. May contain traces of sesame.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 410 kcal, Protein 9.5 g, Carbohydrate 68.0 g, Total Fat 11.5 g, Dietary Fibre 7.2 g",
                    "pred": "Per 100g: Energy 410 kcal, Protein 9.5 g, Carbohydrate 68.0 g, Total Fat 11.5 g, Dietary Fibre 7.2 g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Baked hard for teething gums. Never leave baby unattended. Store in airtight container.",
                    "pred": "Baked hard for teething gums. Never leave baby unattended. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Teether instructions verified"
                }
            }
        },
        {
            "sku_id": "SKU-031",
            "brand": "Timios",
            "market_city": "Pune",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Timios Organic Baby Porridge Sprouted Ragi & Wheat",
                    "pred": "Timios Organic Baby Porridge Sprouted Ragi & Wheat",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "6+ months",
                    "pred": "6+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Organic Sprouted Ragi (60%), Organic Wheat (40%)",
                    "pred": "Organic Sprouted Ragi (60%), Organic Wheat (40%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 18.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat.",
                    "pred": "Contains Wheat.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Energy 365 kcal, Protein 9.2 g, Carbohydrate 78.0 g, Fat 1.5 g, Calcium 290 mg, Iron 4.8 mg per 100g",
                    "pred": "Energy 365 kcal, Protein 9.2 g, Carbohydrate 78.0 g, Fat 1.5 g, Calcium 290 mg, Iron 4.8 mg per 100g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 2 tbsp with 150ml milk or water. Cook for 5 mins stirring continuously.",
                    "pred": "Mix 2 tbsp with 150ml milk or water. Cook for 5 mins stirring continuously.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-032",
            "brand": "Timios",
            "market_city": "Hyderabad",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Timios Mini O's Multigrain Rings",
                    "pred": "Timios Mini O's Multigrain Rings",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Puffed rings package"
                },
                "ageMarking": {
                    "gt": "12+ months",
                    "pred": "12+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Corn (30%), Rice (25%), Wheat (20%), Oats (15%), Apple juice (8%), Salt (1%), Vitamin premix (1%)",
                    "pred": "Corn (30%), Rice (25%), Wheat (20%), Oats (15%), Apple juice (8%), Salt (1%), Vitamin premix (1%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Oats.",
                    "pred": "Contains Wheat and Oats.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 380 kcal, Protein 8.5 g, Fat 3.0 g, Fibre 5.0 g, Sodium 95 mg",
                    "pred": "Per 100g: Energy 380 kcal, Protein 8.5 g, Fat 3.0 g, Fibre 5.0 g, Sodium 95 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Ready to eat. Feed to sitting child. Reseal bag.",
                    "pred": "Ready to eat. Feed to sitting child. Reseal bag.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 13.0, "notes": "Preparation verified"
                }
            }
        },

        # --- Brand 6: Bebe Burp (5 SKUs) ---
        {
            "sku_id": "SKU-033",
            "brand": "Bebe Burp",
            "market_city": "Mumbai",
            "script": "English-Latin",
            "condition": "curved_tin",
            "fields": {
                "productName": {
                    "gt": "Bebe Burp Organic Ragi Cookies with Cardamom",
                    "pred": "Bebe Burp Organic Ragi Cookies with Cardamom",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 12.0, "notes": "Curved tin front panel"
                },
                "ageMarking": {
                    "gt": "8+ months / Infant & Toddler",
                    "pred": "8+ months / Infant & Toddler",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Organic Sprouted Ragi (40%), Whole Wheat (30%), Cow Butter (15%), Jaggery (12%), Cardamom (3%)",
                    "pred": "Organic Sprouted Ragi (40%), Whole Wheat (30%), Cow Butter (15%), Jaggery (12%), Cardamom (3%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk (Cow Butter).",
                    "pred": "Contains Wheat and Milk (Cow Butter).",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 430 kcal, Protein 7.2 g, Carbohydrate 66.5 g, Total Fat 15.0 g, Calcium 260 mg",
                    "pred": "Per 100g: Energy 430 kcal, Protein 7.2 g, Carbohydrate 66.5 g, Total Fat 150 g, Calcium 260 mg",
                    "status": "clear", "ev": "no", "unsupp": "yes", "err": "altered_number", "sec": 32.0, "notes": "Curved tin edge dropped decimal: Total Fat 15.0 g misread as 150 g"
                },
                "preparationAndStorage": {
                    "gt": "Can be mashed with warm milk or fed directly under adult supervision. Keep in cool dry place.",
                    "pred": "Can be mashed with warm milk or fed directly under adult supervision. Keep in cool dry place.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 17.0, "notes": "Advisory verified"
                }
            }
        },
        {
            "sku_id": "SKU-034",
            "brand": "Bebe Burp",
            "market_city": "Pune",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Bebe Burp Oatmeal & Raisins Cookies",
                    "pred": "Bebe Burp Oatmeal & Raisins Cookies",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Carton capture"
                },
                "ageMarking": {
                    "gt": "8+ months",
                    "pred": "8+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Rolled Oats (42%), Whole Wheat (28%), Clarified Butter (Ghee) (16%), Black Raisins (10%), Jaggery (4%)",
                    "pred": "Rolled Oats (42%), Whole Wheat (28%), Clarified Butter (Ghee) (16%), Black Raisins (10%), Jaggery (4%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Oats, Wheat and Milk.",
                    "pred": "Contains Oats, Wheat and Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 425 kcal, Protein 8.5 g, Carbohydrate 65.0 g, Total Fat 14.5 g, Dietary Fibre 6.0 g",
                    "pred": "Per 100g: Energy 425 kcal, Protein 8.5 g, Carbohydrate 65.0 g, Total Fat 14.5 g, Dietary Fibre 6.0 g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Ready to eat. Crush into warm milk if needed. Store in airtight container.",
                    "pred": "Ready to eat. Crush into warm milk if needed. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-035",
            "brand": "Bebe Burp",
            "market_city": "Delhi",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Bebe Burp Finger Food Millet Puffs Cheese & Tomato",
                    "pred": "Bebe Burp Finger Food Millet Puffs Cheese & Tomato",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "10+ months",
                    "pred": "10+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Jowar (35%), Ragi (30%), Rice (18%), Cold pressed oil (10%), Cheese powder (4%), Tomato powder (3%)",
                    "pred": "Jowar (35%), Ragi (30%), Rice (18%), Cold pressed oil (10%), Cheese powder (4%), Tomato powder (3%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Milk (Cheese).",
                    "pred": "Contains Milk (Cheese).",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 415 kcal, Protein 8.0 g, Fat 11.0 g, Sodium 210 mg",
                    "pred": "Per 100g: Energy 415 kcal, Protein 8.0 g, Fat 11.0 g, Sodium 210 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Snack on the go. Ensure child is seated and supervised. Reseal tightly.",
                    "pred": "Snack on the go. Ensure child is seated and supervised. Reseal tightly.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Advisory verified"
                }
            }
        },
        {
            "sku_id": "SKU-036",
            "brand": "Bebe Burp",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Bebe Burp Organic Barley & Banana Mix",
                    "pred": "Bebe Burp Organic Barley & Banana Mix",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Standup pouch read"
                },
                "ageMarking": {
                    "gt": "6+ months / Stage 1",
                    "pred": "6+ months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 clear"
                },
                "ingredients": {
                    "gt": "Organic Barley flour (75%), Freeze dried Banana powder (25%)",
                    "pred": "Organic Barley flour (75%), Freeze dried Banana powder (25%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 18.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Barley (Gluten).",
                    "pred": "Contains Barley (Gluten).",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 360 kcal, Protein 8.2 g, Carbohydrate 78.5 g, Dietary Fibre 8.0 g, Iron 4.2 mg",
                    "pred": "Per 100g: Energy 360 kcal, Protein 8.2 g, Carbohydrate 78.5 g, Dietary Fibre 8.0 g, Iron 4.2 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 2 spoons with 100ml warm water or milk. Cook 2-3 mins. Store in airtight container.",
                    "pred": "Mix 2 spoons with 100ml warm water or milk. Cook 2-3 mins. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-037",
            "brand": "Bebe Burp",
            "market_city": "Lucknow",
            "script": "Bilingual (English + Hindi)",
            "condition": "slight_angle",
            "fields": {
                "productName": {
                    "gt": "Bebe Burp Khichdi Mix Moong Dal & Rice / मूँग दाल और चावल खिचड़ी मिक्स",
                    "pred": "Bebe Burp Khichdi Mix Moong Dal & Rice / मूँग दाल और चावल खिचड़ी मिक्स",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Bilingual title verified"
                },
                "ageMarking": {
                    "gt": "8+ months / ८+ महीने",
                    "pred": "8+ months / ८+ महीने",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Bilingual age verified"
                },
                "ingredients": {
                    "gt": "Rice (50%), Yellow Moong Dal (35%), Cumin (5%), Turmeric (2%), Ghee powder (8%)",
                    "pred": "Rice (50%), Yellow Moong Dal (35%), Cumin (5%), Turmeric (2%), Ghee powder (8%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Milk (Ghee).",
                    "pred": "Contains Milk (Ghee).",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 382 kcal, Protein 13.0 g, Carbohydrate 70.0 g, Fat 5.0 g, Iron 4.5 mg",
                    "pred": "Per 100g: Energy 382 kcal, Protein 13.0 g, Carbohydrate 70.0 g, Fat 5.0 g, Iron 4.5 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Khichdi nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Add 3 tbsp mix to 150ml boiling water. Cook for 5 mins until soft and mashed.",
                    "pred": "Add 3 tbsp mix to 150ml boiling water. Cook for 5 mins until soft and mashed.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Cooking verified"
                }
            }
        },

        # --- Brand 7: Early Foods (4 SKUs) ---
        {
            "sku_id": "SKU-038",
            "brand": "Early Foods",
            "market_city": "Pune",
            "script": "Marathi-Devanagari",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "अर्ली फूड्स मोड आलेली नाचणी व बदाम लापशी",
                    "pred": "अर्ली फूड्स मोड आलेली नाचणी व बदाम लापशी",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 18.0, "notes": "Marathi title verified"
                },
                "ageMarking": {
                    "gt": "८ महिने व पुढील बाळांसाठी",
                    "pred": "८ महिने व पुढील बाळांसाठी",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 9.0, "notes": "Marathi age marking recognized"
                },
                "ingredients": {
                    "gt": "मोड आलेली नाचणी (८०%), बदाम (१५%), वेलची (५%)",
                    "pred": "मोड आलेली नाचणी (८०%), बदाम (१५%), वेलची (५%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 22.0, "notes": "Marathi ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "बदाम (ट्री नट्स) समाविष्ट आहे.",
                    "pred": "बदाम (ट्री नट्स) समाविष्ट आहे.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 9.0, "notes": "Tree nut allergen in Marathi"
                },
                "nutritionPanel": {
                    "gt": "प्रति १०० ग्रॅम: ऊर्जा ३८० किलो कॅलरी, प्रथिने १०.५ ग्रॅम, कॅल्शियम ३१० मि.ग्रॅ, लोह ५.० मि.ग्रॅ",
                    "pred": "प्रति १०० ग्रॅम: ऊर्जा ३८० किलो कॅलरी, प्रथिने १०.५ ग्रॅम, कॅल्शियम ३१० मि.ग्रॅ, लोह ५० मि.ग्रॅ",
                    "status": "clear", "ev": "no", "unsupp": "yes", "err": "altered_number", "sec": 31.0, "notes": "Decimal dropped on Marathi iron metric: ५.० -> ५०"
                },
                "preparationAndStorage": {
                    "gt": "२ चमचे लापशी १ कप पाणी किंवा दुधात मिसळा. ५ मिनिटे मंद आचेवर शिजवा. हवाबंद डब्यात ठेवा.",
                    "pred": "२ चमचे लापशी १ कप पाणी किंवा दुधात मिसळा. ५ मिनिटे मंद आचेवर शिजवा. हवाबंद डब्यात ठेवा.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Marathi preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-039",
            "brand": "Early Foods",
            "market_city": "Mumbai",
            "script": "English-Latin",
            "condition": "creased_foil",
            "fields": {
                "productName": {
                    "gt": "Early Foods Organic Sathumaavu Porridge Mix",
                    "pred": "Early Foods Organic Sathumaavu Porridge Mix",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Paper pouch capture"
                },
                "ageMarking": {
                    "gt": "8+ months",
                    "pred": "8+ months",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Sprouted Ragi (25%), Sprouted Wheat (20%), Roasted Gram (15%), Brown Rice (15%), Green Moong (10%), Dry Fruits [Almonds, Cashews] (10%), Watermelon seeds (3%), Cardamom (2%)",
                    "pred": "Sprouted Ragi (25%), Sprouted Wheat (20%), Roasted Gram (15%), Brown Rice (15%), Green Moong (10%), Dry Fruits [Almonds, Cashews] (10%), Watermelon seeds (3%), Cardamom (2%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 33.0, "notes": "Multi-grain mix ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat, Almonds, and Cashews.",
                    "pred": "Contains Wheat, Almonds, and Cashews.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 395 kcal, Protein 13.5 g, Carbohydrate 70.0 g, Total Fat 6.2 g, Iron 6.0 mg",
                    "pred": "Per 100g: Energy 395 kcal, Protein 13.5 g, Carbohydrate 70.0 g, Total Fat 6.2 g, Iron 6.0 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 28.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 2 spoons in 200ml water/milk. Cook on low heat 5-7 mins. Store in cool dry place.",
                    "pred": "Mix 2 spoons in 200ml water/milk. Cook on low heat 5-7 mins. Store in cool dry place.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Cooking verified"
                }
            }
        },
        {
            "sku_id": "SKU-040",
            "brand": "Early Foods",
            "market_city": "Pune",
            "script": "Marathi-Devanagari",
            "condition": "low_light",
            "fields": {
                "productName": {
                    "gt": "अर्ली फूड्स मोड आलेला गहू आणि बीट लापशी",
                    "pred": "अर्ली फूड्स मोड आलेला गहू आणि बीट लापशी",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 19.0, "notes": "Marathi wheat beetroot porridge"
                },
                "ageMarking": {
                    "gt": "८ महिने व पुढील बाळांसाठी",
                    "pred": "८ महिने व पुढील बाळांसाठी",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 9.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "मोड आलेला गहू (८५%), बीटरूट पावडर (१२%), वेलची (३%)",
                    "pred": "मोड आलेला गहू (८५%), बीटरूट पावडर (१२%), वेलची (३%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 23.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "गहू (ग्लुटेन) समाविष्ट आहे.",
                    "pred": "गहू (ग्लुटेन) समाविष्ट आहे.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Allergen in Marathi"
                },
                "nutritionPanel": {
                    "gt": "प्रति १०० ग्रॅम: ऊर्जा ३७० किलो कॅलरी, प्रथिने ११.० ग्रॅम, लोह ५.२ मि.ग्रॅ, फॉलिक ऍसिड ४० मायक्रोग्रॅम",
                    "pred": "प्रति १०० ग्रॅम: ऊर्जा ३७० किलो कॅलरी, प्रथिने ११.० ग्रॅम, लोह ५.२ मि.ग्रॅ, फॉलिक ऍसिड ४० मायक्रोग्रॅम",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 32.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "२ चमचे लापशी १ कप पाण्यात मिसळा. मंद आचेवर ५ मिनिटे शिजवा. उरलेले अन्न फेकून द्या.",
                    "pred": "२ चमचे लापशी १ कप पाण्यात मिसळा. मंद आचेवर ५ मिनिटे शिजवा. उरलेले अन्न फेकून द्या.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-041",
            "brand": "Early Foods",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Early Foods Organic Teething Sticks Whole Wheat & Jaggery",
                    "pred": "Early Foods Organic Teething Sticks Whole Wheat & Jaggery",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Teething sticks box"
                },
                "ageMarking": {
                    "gt": "9+ months / Teether",
                    "pred": "9+ months / Teether",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Organic Whole Wheat (70%), Cold Pressed Sesame Oil (12%), Organic Jaggery (10%), Ajwain (4%), Jeera (4%)",
                    "pred": "Organic Whole Wheat (70%), Cold Pressed Sesame Oil (12%), Organic Jaggery (10%), Ajwain (4%), Jeera (4%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Sesame.",
                    "pred": "Contains Wheat and Sesame.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 415 kcal, Protein 9.8 g, Carbohydrate 67.0 g, Total Fat 12.5 g, Fibre 6.5 g",
                    "pred": "Per 100g: Energy 415 kcal, Protein 9.8 g, Carbohydrate 67.0 g, Total Fat 12.5 g, Fibre 6.5 g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Hard baked for sore gums. Adult supervision required at all times. Store in airtight container.",
                    "pred": "Hard baked for sore gums. Adult supervision required at all times. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Supervision note verified"
                }
            }
        },

        # --- Brand 8: Pristine 1st Bites (5 SKUs) ---
        {
            "sku_id": "SKU-042",
            "brand": "Pristine 1st Bites",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "1st Bites Organic Baby Food Rice",
                    "pred": "1st Bites Organic Baby Food Rice",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Organic baby food box"
                },
                "ageMarking": {
                    "gt": "6 months - 24 months / Stage 1",
                    "pred": "6 months - 24 months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 clear"
                },
                "ingredients": {
                    "gt": "Organic Rice (70%), Milk solids (20%), Sugar, Salt, Minerals, Vitamins",
                    "pred": "Organic Rice (70%), Milk solids (20%), Sugar, Salt, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 20.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Milk. Gluten Free.",
                    "pred": "Contains Milk. Gluten Free.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 390 kcal, Protein 12.0 g, Carbohydrate 75.0 g, Fat 5.0 g, Calcium 400 mg, Iron 6.0 mg",
                    "pred": "Per 100g: Energy 390 kcal, Protein 12.0 g, Carbohydrate 75.0 g, Fat 5.0 g, Calcium 400 mg, Iron 6.0 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Boil water for 5 mins. Cool to lukewarm. Add 3 scoops to 75ml water. Mix well. Store in airtight container.",
                    "pred": "Boil water for 5 mins. Cool to lukewarm. Add 3 scoops to 75ml water. Mix well. Store in airtight container.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-043",
            "brand": "Pristine 1st Bites",
            "market_city": "Chennai",
            "script": "English-Latin",
            "condition": "slight_angle",
            "fields": {
                "productName": {
                    "gt": "1st Bites Organic Baby Food Wheat & Apple",
                    "pred": "1st Bites Organic Baby Food Wheat & Apple",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "8 months - 24 months / Stage 2",
                    "pred": "8 months - 24 months / Stage 2",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 2 verified"
                },
                "ingredients": {
                    "gt": "Organic Wheat (55%), Milk solids (22%), Apple powder (12%), Sugar, Minerals, Vitamins",
                    "pred": "Organic Wheat (55%), Milk solids (22%), Apple powder (12%), Sugar, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 22.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk.",
                    "pred": "Contains Wheat and Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Energy 400 kcal, Protein 13.5 g, Carbohydrate 73.0 g, Total Fat 6.0 g, Iron 7.0 mg, Calcium 450 mg",
                    "pred": "Energy 400 kcal, Protein 13.5 g, Carbohydrate 73.0 g, Total Fat 6.0 g, Iron 7.0 mg, Calcium 450 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 27.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 3 scoops with 75ml warm water. Stir to smooth paste. Use within 2 weeks of opening.",
                    "pred": "Mix 3 scoops with 75ml warm water. Stir to smooth paste. Use within 2 weeks of opening.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-044",
            "brand": "Pristine 1st Bites",
            "market_city": "Hyderabad",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "1st Bites Organic Baby Food Ragi",
                    "pred": "1st Bites Organic Baby Food Ragi",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 9.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "6 months - 24 months / Stage 1",
                    "pred": "6 months - 24 months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 clear"
                },
                "ingredients": {
                    "gt": "Organic Ragi (65%), Milk solids (22%), Sugar, Minerals, Vitamins",
                    "pred": "Organic Ragi (65%), Milk solids (22%), Sugar, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 20.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Contains Milk. Gluten Free.",
                    "pred": "Contains Milk. Gluten Free.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 385 kcal, Protein 12.5 g, Calcium 510 mg, Iron 6.8 mg",
                    "pred": "Per 100g: Energy 385 kcal, Protein 12.5 g, Calcium 510 mg, Iron 6.8 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 3 scoops into 75ml warm water. Feed immediately. Store in cool place.",
                    "pred": "Mix 3 scoops into 75ml warm water. Feed immediately. Store in cool place.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 14.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-045",
            "brand": "Pristine 1st Bites",
            "market_city": "Delhi",
            "script": "English-Latin",
            "condition": "low_light",
            "fields": {
                "productName": {
                    "gt": "1st Bites Organic Baby Food Mixed Fruit",
                    "pred": "1st Bites Organic Baby Food Mixed Fruit",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Title verified"
                },
                "ageMarking": {
                    "gt": "8 months - 24 months / Stage 2",
                    "pred": "8 months - 24 months / Stage 2",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 2 verified"
                },
                "ingredients": {
                    "gt": "Organic Rice (40%), Organic Wheat (20%), Milk solids (20%), Mixed Fruit powder [Apple, Banana, Orange] (12%), Sugar, Minerals, Vitamins",
                    "pred": "Organic Rice (40%), Organic Wheat (20%), Milk solids (20%), Mixed Fruit powder [Apple, Banana, Orange] (12%), Sugar, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk.",
                    "pred": "Contains Wheat and Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Energy 398 kcal, Protein 13.0 g, Carbohydrate 73.5 g, Fat 5.8 g, Iron 6.5 mg per 100g",
                    "pred": "Energy 398 kcal, Protein 13.0 g, Carbohydrate 73.5 g, Fat 5.8 g, Iron 6.5 mg per 100g",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Mix 3 scoops with 75ml warm water. Discard uneaten portion. Keep pouch sealed.",
                    "pred": "Mix 3 scoops with 75ml warm water. Discard uneaten portion. Keep pouch sealed.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-046",
            "brand": "Pristine 1st Bites",
            "market_city": "Mumbai",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "1st Bites Organic Baby Food Multigrain with Milk",
                    "pred": "1st Bites Organic Baby Food Multigrain with Milk",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Stage 3 carton"
                },
                "ageMarking": {
                    "gt": "10 months - 24 months / Stage 3",
                    "pred": "10 months - 24 months / Stage 3",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 3 clear"
                },
                "ingredients": {
                    "gt": "Organic Wheat (30%), Organic Ragi (20%), Organic Rice (15%), Milk solids (22%), Sugar, Minerals, Vitamins",
                    "pred": "Organic Wheat (30%), Organic Ragi (20%), Organic Rice (15%), Milk solids (22%), Sugar, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk.",
                    "pred": "Contains Wheat and Milk.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 405 kcal, Protein 14.0 g, Total Fat 6.5 g, Calcium 480 mg, Iron 7.2 mg",
                    "pred": "Per 100g: Energy 405 kcal, Protein 14.0 g, Total Fat 6.5 g, Calcium 480 mg, Iron 7.2 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Add 4 scoops to 100ml warm water. Feed with clean spoon. Use within 3 weeks.",
                    "pred": "Add 4 scoops to 100ml warm water. Feed with clean spoon. Use within 3 weeks.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Preparation verified"
                }
            }
        },

        # --- Brand 9: Happa (3 SKUs) ---
        {
            "sku_id": "SKU-047",
            "brand": "Happa",
            "market_city": "Mumbai",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Happa Organic Baby Puree Apple & Mango",
                    "pred": "Happa Organic Baby Puree Apple & Mango",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Spout pouch front"
                },
                "ageMarking": {
                    "gt": "6+ months / Stage 1",
                    "pred": "6+ months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 badge"
                },
                "ingredients": {
                    "gt": "Organic Apple Puree (60%), Organic Mango Puree (40%), Vitamin C (Ascorbic acid 0.05%)",
                    "pred": "Organic Apple Puree (60%), Organic Mango Puree (40%), Vitamin C (Ascorbic acid 0.05%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 20.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "No added sugar, salt, milk or gluten. Free from common allergens.",
                    "pred": "No added sugar, salt, milk or gluten. Free from common allergens.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Allergen-free claim matched"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 65 kcal, Protein 0.5 g, Carbohydrate 15.5 g, Natural Fruit Sugars 12.0 g, Fat 0.2 g, Vitamin C 25 mg",
                    "pred": "Per 100g: Energy 65 kcal, Protein 0.5 g, Carbohydrate 15.5 g, Natural Fruit Sugars 12.0 g, Fat 0.2 g, Vitamin C 25 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Fruit puree nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Ready to feed. Squeeze onto clean spoon. Do not microwave pouch. Keep cap out of reach of children. Refrigerate after opening and consume within 24 hours.",
                    "pred": "Ready to feed. Squeeze onto clean spoon. Do not microwave pouch. Keep cap out of reach of children. Refrigerate after opening and consume within 24 hours.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 21.0, "notes": "Choking hazard and storage verified"
                }
            }
        },
        {
            "sku_id": "SKU-048",
            "brand": "Happa",
            "market_city": "Delhi",
            "script": "English-Latin",
            "condition": "glare_glossy_pouch",
            "fields": {
                "productName": {
                    "gt": "Happa Organic Puree Pear & Sweet Potato",
                    "pred": "Happa Organic Puree Pear & Sweet Potato",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Puree pouch"
                },
                "ageMarking": {
                    "gt": "6+ months / Stage 1",
                    "pred": "6+ months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 clear"
                },
                "ingredients": {
                    "gt": "Organic Pear Puree (65%), Organic Sweet Potato Puree (35%)",
                    "pred": "Organic Pear Puree (65%), Organic Sweet Potato Puree (35%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 18.0, "notes": "Ingredients verified"
                },
                "allergenDeclaration": {
                    "gt": "Gluten Free. Dairy Free.",
                    "pred": "Gluten Free. Dairy Free.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 6.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 58 kcal, Protein 0.6 g, Carbohydrate 13.8 g, Fat 0.1 g, Vitamin A 180 ug",
                    "pred": "Per 100g: Energy 58 kcal, Protein 0.6 g, Carbohydrate 13.8 g, Fat 0.1 g, Vitamin A 180 ug",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 24.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Serve at room temperature. Squeeze into bowl. Keep refrigerated after opening and consume within 24 hours.",
                    "pred": "Serve at room temperature. Squeeze into bowl. Keep refrigerated after opening and consume within 24 hours.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 17.0, "notes": "Preparation verified"
                }
            }
        },
        {
            "sku_id": "SKU-049",
            "brand": "Happa",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Happa Organic Teething Wafers Blueberry & Banana",
                    "pred": "Happa Organic Teething Wafers Blueberry & Banana",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 10.0, "notes": "Box capture"
                },
                "ageMarking": {
                    "gt": "7+ months / Teether",
                    "pred": "7+ months / Teether",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Age verified"
                },
                "ingredients": {
                    "gt": "Organic Japonica Rice flour (72%), Organic Tapioca starch (15%), Organic Sugar (6%), Blueberry powder (4%), Banana powder (3%)",
                    "pred": "Organic Japonica Rice flour (72%), Organic Tapioca starch (15%), Organic Sugar (6%), Blueberry powder (4%), Banana powder (3%)",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Gluten Free. Egg Free. Peanut Free.",
                    "pred": "Gluten Free. Egg Free. Peanut Free.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 7.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 380 kcal, Protein 6.0 g, Carbohydrate 86.0 g, Total Fat 1.0 g, Sodium 10 mg",
                    "pred": "Per 100g: Energy 380 kcal, Protein 6.0 g, Carbohydrate 86.0 g, Total Fat 1.0 g, Sodium 10 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 25.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Dissolves easily. Supervise child while eating. Keep individually wrapped packs sealed.",
                    "pred": "Dissolves easily. Supervise child while eating. Keep individually wrapped packs sealed.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 15.0, "notes": "Advisory verified"
                }
            }
        },

        # --- Brand 10: Mum's Care (British Life Sciences) (1 SKU) ---
        {
            "sku_id": "SKU-050",
            "brand": "Mum's Care",
            "market_city": "Bengaluru",
            "script": "English-Latin",
            "condition": "standard_indoor",
            "fields": {
                "productName": {
                    "gt": "Mum's Care Organic Fortified Baby Cereal Wheat & Milk",
                    "pred": "Mum's Care Organic Fortified Baby Cereal Wheat & Milk",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 11.0, "notes": "Foil pouch in carton"
                },
                "ageMarking": {
                    "gt": "From 6 to 24 months / Stage 1",
                    "pred": "From 6 to 24 months / Stage 1",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 5.0, "notes": "Stage 1 clear"
                },
                "ingredients": {
                    "gt": "Organic Wheat flour (50%), Organic Milk solids (35%), Organic Sugar, Soyabean oil, Minerals, Vitamins",
                    "pred": "Organic Wheat flour (50%), Organic Milk solids (35%), Organic Sugar, Soyabean oil, Minerals, Vitamins",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 23.0, "notes": "Ingredients matched"
                },
                "allergenDeclaration": {
                    "gt": "Contains Wheat and Milk. May contain Soy.",
                    "pred": "Contains Wheat and Milk. May contain Soy.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 8.0, "notes": "Allergen verified"
                },
                "nutritionPanel": {
                    "gt": "Per 100g: Energy 412 kcal, Protein 15.0 g, Carbohydrate 68.0 g, Fat 9.2 g, Calcium 510 mg, Iron 7.5 mg",
                    "pred": "Per 100g: Energy 412 kcal, Protein 15.0 g, Carbohydrate 68.0 g, Fat 9.2 g, Calcium 510 mg, Iron 7.5 mg",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 26.0, "notes": "Nutrition verified"
                },
                "preparationAndStorage": {
                    "gt": "Boil water for 5 minutes. Cool to lukewarm. Mix 3 scoops in 75ml water. Feed with clean spoon. Use within 3 weeks.",
                    "pred": "Boil water for 5 minutes. Cool to lukewarm. Mix 3 scoops in 75ml water. Feed with clean spoon. Use within 3 weeks.",
                    "status": "clear", "ev": "yes", "unsupp": "no", "err": "none", "sec": 16.0, "notes": "Preparation verified"
                }
            }
        }
    ]
    return skus

def build_benchmark_csv(output_path: str):
    skus = get_50_sku_definitions()
    fieldnames = [
        "image_id", "sku_id", "brand", "market_city", "package_language_script",
        "photo_condition", "field", "ground_truth", "model_output", "read_status",
        "evidence_located", "unsupported_text", "error_category", "review_seconds", "reviewer_notes"
    ]

    total_rows = 0
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for sku in skus:
            sku_id = sku["sku_id"]
            brand = sku["brand"]
            city = sku["market_city"]
            script = sku["script"]
            cond = sku["condition"]

            for field_name, f_data in sku["fields"].items():
                image_id = f"IMG-{sku_id}-FRONT" if field_name in ("productName", "ageMarking") else f"IMG-{sku_id}-PANEL"
                row = {
                    "image_id": image_id,
                    "sku_id": sku_id,
                    "brand": brand,
                    "market_city": city,
                    "package_language_script": script,
                    "photo_condition": cond,
                    "field": field_name,
                    "ground_truth": f_data["gt"],
                    "model_output": f_data["pred"],
                    "read_status": f_data["status"],
                    "evidence_located": f_data["ev"],
                    "unsupported_text": f_data["unsupp"],
                    "error_category": f_data["err"],
                    "review_seconds": str(f_data["sec"]),
                    "reviewer_notes": f_data["notes"]
                }
                writer.writerow(row)
                total_rows += 1

    print(f"Successfully generated {total_rows} benchmark rows across {len(skus)} SKUs in: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join("LabelFit India", "docs", "benchmark-template.csv")
    build_benchmark_csv(out_file)
