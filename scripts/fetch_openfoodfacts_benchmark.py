#!/usr/bin/env python3
"""
LabelFit India: Open Food Facts India Complementary Food Fetcher & Benchmark Ingest.
Queries Open Food Facts for Indian complementary foods (6+ months), extracts product
metadata and high-resolution packaging photo URLs (front, ingredients, nutrition),
and formats candidate rows for the benchmark harness.
"""

import os
import sys
import json
import csv
import time
import argparse
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

USER_AGENT = "LabelFitIndia-BenchmarkFetcher/1.0 (+https://github.com/tripathiswastik/LabelFit-India; contact: swastik.tripathi842@gmail.com)"

# FSSAI Complementary scope keywords vs 0-6m Formula exclusion
COMPLEMENTARY_KEYWORDS = [
    "cereal", "ragi", "oats", "wheat", "rice", "porridge", "puree",
    "biscuit", "cookie", "stage 2", "stage 3", "stage 4", "6 months",
    "6+", "7+", "8+", "10+", "12+", "nestum", "cerelac", "burp",
    "manna", "slurrp", "timios", "jeeni", "mum's care"
]

EXCLUDED_FORMULA_KEYWORDS = [
    "stage 1", "infant formula 1", "lactogen 1", "dexolac 1",
    "nan pro 1", "similac 1", "0-6 months", "0 to 6 months", "starter infant formula"
]


def is_complementary_food(product: Dict[str, Any]) -> bool:
    """Filters for complementary foods (6+ months) and flags 0-6m infant formulas."""
    name = (product.get("product_name") or product.get("product_name_en") or "").lower()
    categories = str(product.get("categories_tags", [])).lower()
    generic_name = (product.get("generic_name") or "").lower()
    full_text = f"{name} {generic_name} {categories}"

    # Exclude 0-6m starter infant formulas per FSSAI / LabelFit scope
    if any(k in full_text for k in EXCLUDED_FORMULA_KEYWORDS):
        return False

    # Check if name or category matches complementary food indicators
    return any(k in full_text for k in COMPLEMENTARY_KEYWORDS)


def extract_best_image_url(product: Dict[str, Any], image_type: str = "front") -> Optional[str]:
    """Resolves full-resolution image URL from OFF product record."""
    code = str(product.get("code", "")).strip()
    if not code:
        return None

    # Standard image URL from OFF fields
    field_key = f"image_{image_type}_url"
    url = product.get(field_key)
    if url:
        # Replace thumbnail .400.jpg with .full.jpg or strip resize to get high-res
        full_url = url.replace(".400.jpg", ".full.jpg")
        return full_url

    # Alternate: lookup in raw 'images' dictionary
    images = product.get("images", {})
    if isinstance(images, dict):
        for key in [f"{image_type}_en", image_type, "1", "2", "3", "4"]:
            if key in images and isinstance(images[key], dict):
                # Format OFF barcode path: e.g. 890/105/801/5799
                if len(code) == 13:
                    path_part = f"{code[:3]}/{code[3:6]}/{code[6:9]}/{code[9:]}"
                else:
                    path_part = code
                return f"https://images.openfoodfacts.org/images/products/{path_part}/{key}.jpg"

    return None


def fetch_off_products(limit: int = 50) -> List[Dict[str, Any]]:
    """Queries Open Food Facts Search API across Indian baby food search filters."""
    endpoints = [
        "https://world.openfoodfacts.org/api/v2/search?categories_tags_en=baby-foods&countries_tags_en=india&fields=code,product_name,brands,ingredients_text,images,categories_tags,generic_name,nutriments&page_size=50",
        "https://world.openfoodfacts.org/api/v2/search?categories_tags_en=cereals-for-babies&countries_tags_en=india&fields=code,product_name,brands,ingredients_text,images,categories_tags,generic_name,nutriments&page_size=50",
        "https://world.openfoodfacts.org/api/v2/search?search_terms=cerelac&countries_tags_en=india&fields=code,product_name,brands,ingredients_text,images,categories_tags,generic_name,nutriments&page_size=50",
        "https://world.openfoodfacts.org/api/v2/search?search_terms=slurrp+farm&countries_tags_en=india&fields=code,product_name,brands,ingredients_text,images,categories_tags,generic_name,nutriments&page_size=50",
        "https://world.openfoodfacts.org/api/v2/search?search_terms=baby+cereal&countries_tags_en=india&fields=code,product_name,brands,ingredients_text,images,categories_tags,generic_name,nutriments&page_size=50",
    ]

    seen_barcodes = set()
    collected: List[Dict[str, Any]] = []

    for url in endpoints:
        if len(collected) >= limit:
            break
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for prod in data.get("products", []):
                    code = str(prod.get("code", "")).strip()
                    name = prod.get("product_name") or prod.get("product_name_en")
                    if not code or not name or code in seen_barcodes:
                        continue

                    # Filter for complementary foods (6+ months)
                    if is_complementary_food(prod):
                        seen_barcodes.add(code)
                        collected.append(prod)
                        if len(collected) >= limit:
                            break
        except Exception as err:
            print(f"[Warning] Failed to fetch endpoint: {err}", file=sys.stderr)
        time.sleep(0.5)  # Polite API rate pacing

    return collected


def export_benchmark_csv(products: List[Dict[str, Any]], output_path: str):
    """Exports candidate benchmark rows into docs/benchmark-template.csv schema."""
    fieldnames = [
        "image_id", "sku_id", "brand", "market_city", "package_language_script",
        "photo_condition", "field", "ground_truth", "model_output", "read_status",
        "evidence_located", "unsupported_text", "error_category", "review_seconds", "reviewer_notes"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for idx, prod in enumerate(products):
            code = prod.get("code", f"SKU-{idx+1:03d}")
            sku_id = f"OFF-{code}"
            brand = prod.get("brands") or "Unknown"
            p_name = prod.get("product_name") or prod.get("product_name_en") or ""
            ingredients = prod.get("ingredients_text") or ""

            front_img = extract_best_image_url(prod, "front") or ""
            ingr_img = extract_best_image_url(prod, "ingredients") or front_img

            # Row for productName
            writer.writerow({
                "image_id": f"IMG-{code}-FRONT",
                "sku_id": sku_id,
                "brand": brand,
                "market_city": "India (National Retail)",
                "package_language_script": "English-Latin",
                "photo_condition": "openfoodfacts_packshot",
                "field": "productName",
                "ground_truth": p_name,
                "model_output": "",
                "read_status": "",
                "evidence_located": "",
                "unsupported_text": "",
                "error_category": "",
                "review_seconds": "",
                "reviewer_notes": f"Photo URL: {front_img}"
            })

            # Row for ingredients
            if ingredients:
                writer.writerow({
                    "image_id": f"IMG-{code}-INGR",
                    "sku_id": sku_id,
                    "brand": brand,
                    "market_city": "India (National Retail)",
                    "package_language_script": "English-Latin",
                    "photo_condition": "openfoodfacts_packshot",
                    "field": "ingredients",
                    "ground_truth": ingredients,
                    "model_output": "",
                    "read_status": "",
                    "evidence_located": "",
                    "unsupported_text": "",
                    "error_category": "",
                    "review_seconds": "",
                    "reviewer_notes": f"Photo URL: {ingr_img}"
                })


def download_images(products: List[Dict[str, Any]], dest_dir: str, max_downloads: int = 10):
    """Optionally downloads high-res packaging panels into local test fixtures."""
    os.makedirs(dest_dir, exist_ok=True)
    count = 0

    for prod in products:
        if count >= max_downloads:
            break
        code = prod.get("code")
        front_url = extract_best_image_url(prod, "front")
        ingr_url = extract_best_image_url(prod, "ingredients")

        for img_type, url in [("front", front_url), ("ingredients", ingr_url)]:
            if not url or count >= max_downloads:
                continue
            dest_file = os.path.join(dest_dir, f"{code}_{img_type}.jpg")
            if os.path.exists(dest_file):
                continue
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    with open(dest_file, "wb") as out:
                        out.write(resp.read())
                print(f"[Downloaded] {dest_file} ({os.path.getsize(dest_file)} bytes)")
                count += 1
                time.sleep(0.5)
            except Exception as e:
                print(f"[Warning] Failed to download {url}: {e}", file=sys.stderr)


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_json = os.path.join(repo_root, "docs", "off_india_complementary_manifest.json")
    default_csv = os.path.join(repo_root, "docs", "off_india_benchmark_candidates.csv")

    parser = argparse.ArgumentParser(description="Fetch Indian complementary food packaging from Open Food Facts.")
    parser.add_argument("--limit", type=int, default=50, help="Target number of SKUs (default: 50)")
    parser.add_argument("--output-json", default=default_json,
                        help="Path to save JSON catalog manifest")
    parser.add_argument("--output-csv", default=default_csv,
                        help="Path to export benchmark CSV candidate sheet")
    parser.add_argument("--download-images", type=str, default=None,
                        help="Optional folder to download packshot images")
    parser.add_argument("--download-count", type=int, default=10,
                        help="Max images to download if download-images is set (default: 10)")
    args = parser.parse_args()

    print(f"--> Querying Open Food Facts for Indian complementary food products (target: {args.limit} SKUs)...")
    products = fetch_off_products(limit=args.limit)
    print(f"--> Found {len(products)} relevant Indian complementary food products.")

    # Save JSON manifest
    manifest_records = []
    for p in products:
        manifest_records.append({
            "code": p.get("code"),
            "product_name": p.get("product_name") or p.get("product_name_en"),
            "brand": p.get("brands"),
            "categories": p.get("categories_tags"),
            "ingredients_text": p.get("ingredients_text"),
            "front_image_url": extract_best_image_url(p, "front"),
            "ingredients_image_url": extract_best_image_url(p, "ingredients"),
            "nutrition_image_url": extract_best_image_url(p, "nutrition"),
        })

    os.makedirs(os.path.dirname(args.output_json), exist_ok=True)
    with open(args.output_json, "w", encoding="utf-8") as f:
        json.dump(manifest_records, f, indent=2, ensure_ascii=False)
    print(f"--> Saved JSON manifest: {args.output_json}")

    # Save benchmark CSV candidate sheet
    export_benchmark_csv(products, args.output_csv)
    print(f"--> Exported benchmark candidate sheet: {args.output_csv}")

    # Download images if requested
    if args.download_images:
        print(f"--> Downloading up to {args.download_count} packaging panel images to: {args.download_images}...")
        download_images(products, args.download_images, max_downloads=args.download_count)

    print("--> Complete.")


if __name__ == "__main__":
    main()
