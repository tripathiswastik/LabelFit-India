#!/usr/bin/env python3
"""Create a blank benchmark worksheet; never generate benchmark results."""

import csv
from pathlib import Path


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


def build_benchmark_csv(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        csv.writer(csv_file).writerow(FIELDNAMES)


if __name__ == "__main__":
    template_path = Path(__file__).resolve().parents[1] / "docs" / "benchmark-template.csv"
    build_benchmark_csv(template_path)
    print(f"Created blank benchmark worksheet: {template_path}")
    print("No package data, ground truth, or model outputs were generated.")
