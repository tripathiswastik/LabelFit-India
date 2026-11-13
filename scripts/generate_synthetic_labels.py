"""
Generates synthetic baby-food label test fixtures for smoke-testing LabelFit India.
Produces normal, blurred, missing-field, and corrupted packaging images.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "test", "fixtures")
os.makedirs(FIXTURES_DIR, exist_ok=True)

NORMAL_LABEL_LINES = [
    "LittleNourish Organic Rice & Moong Dal",
    "STAGE 1: FROM 6 TO 24 MONTHS",
    "--------------------------------------------------",
    "Ingredients: Organic Rice Flour (55%), Sprouted",
    "Moong Dal Flour (25%), Milk Solids (15%), Sunflower Oil,",
    "Minerals (Calcium, Iron), Vitamins (A, C, D3).",
    "--------------------------------------------------",
    "Allergen Declaration: Contains Milk.",
    "May contain traces of soy and gluten.",
    "--------------------------------------------------",
    "Nutrition (per 100g): Energy 410 kcal, Protein 12g,",
    "Carbohydrate 72g, Sugar (natural) 6g, Fat 8g.",
    "--------------------------------------------------",
    "Preparation Directions:",
    "1. Wash hands thoroughly before preparation.",
    "2. Boil clean drinking water for 5 minutes; let cool.",
    "3. Mix 3 level scoops (25g) with 75ml lukewarm water.",
    "4. Feed immediately with clean spoon. Discard leftovers.",
    "Storage: Store in airtight container in cool, dry place.",
]

MISSING_FIELDS_LINES = [
    "PureBite Single-Grain Baby Porridge",
    "STAGE 1: 6+ MONTHS",
    "--------------------------------------------------",
    "Ingredients: 100% Organic Spelt Grain.",
    "--------------------------------------------------",
    "Nutrition (per 100g): Energy 360 kcal, Protein 11g.",
    "Storage: Store in a dry place.",
]


def render_label_image(lines, width=650, height=520, bg_color="#F8F7F2", text_color="#202A25"):
    image = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Use default bitmap font
    y_offset = 25
    for line in lines:
        if line.startswith("LittleNourish") or line.startswith("PureBite"):
            draw.text((30, y_offset), line, fill="#1B4D3E")
            y_offset += 28
        elif "STAGE" in line:
            draw.text((30, y_offset), line, fill="#B87B31")
            y_offset += 24
        elif line.startswith("---"):
            draw.line([(30, y_offset + 5), (width - 30, y_offset + 5)], fill="#D0D5CD", width=1)
            y_offset += 16
        else:
            draw.text((30, y_offset), line, fill=text_color)
            y_offset += 20

    return image


def main():
    print("Generating synthetic packaging label fixtures...")

    # 1. Normal, clean label
    normal_img = render_label_image(NORMAL_LABEL_LINES)
    normal_path = os.path.join(FIXTURES_DIR, "synthetic_normal.png")
    normal_img.save(normal_path)
    print(f"Created: {normal_path} ({os.path.getsize(normal_path)} bytes)")

    # 2. Blurry label (heavy Gaussian blur simulating out-of-focus camera)
    blurry_img = normal_img.filter(ImageFilter.GaussianBlur(radius=3.5))
    blurry_path = os.path.join(FIXTURES_DIR, "synthetic_blurry.png")
    blurry_img.save(blurry_path)
    print(f"Created: {blurry_path} ({os.path.getsize(blurry_path)} bytes)")

    # 3. Label with missing fields (no allergen statement, no preparation directions)
    missing_img = render_label_image(MISSING_FIELDS_LINES, height=320)
    missing_path = os.path.join(FIXTURES_DIR, "synthetic_missing_fields.png")
    missing_img.save(missing_path)
    print(f"Created: {missing_path} ({os.path.getsize(missing_path)} bytes)")

    # 4. Invalid / corrupted file (plain text with .png extension)
    invalid_path = os.path.join(FIXTURES_DIR, "synthetic_invalid.png")
    with open(invalid_path, "wb") as f:
        f.write(b"NOT_A_REAL_PNG_FILE_CORRUPT_MAGIC_BYTES_1234567890")
    print(f"Created: {invalid_path} ({os.path.getsize(invalid_path)} bytes)")

    print("All synthetic fixtures generated successfully.")


if __name__ == "__main__":
    main()

