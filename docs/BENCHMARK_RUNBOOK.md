# Benchmark runbook

How to turn package photos into a scored, reproducible result. This file describes tooling only and contains no results. Read `VALIDATION_PLAN.md` first; it defines the sample, ground truth, and stop conditions.

## Before you start

- Node 20+ and Python 3.10+.
- `GEMINI_API_KEY` set in your shell, or in this project's own `.env` file (gitignored).
- **Decide the model once.** Every run records its model, and a run refuses to mix two models. Use `--model` or `GEMINI_MODEL`, and use a new `--run-id` for each model.
- Keep package photos in access-controlled storage **outside the repository**. The tools never copy or store images; they record each image's SHA-256 so a result can be matched to its photo later.
- Never change `ground_truth` after seeing model output, and never copy model output into it.
- Keep a separate development set of SKUs for any prompt or guard changes. Do not tune on the SKUs you evaluate. All photos of one SKU stay in one split.

## 1. Make a manifest

Copy `docs/benchmark-scan-manifest-template.csv` and fill `image_file` with each photo's file name (JPEG, PNG or WebP, under 7 MB, inside your `--images` folder). `image_id` and `sku_id` must match the worksheet.

## 2. Check without spending anything

```
node scripts/scan_benchmark.js --manifest my-manifest.csv --images D:\label-photos --run-id bf-run-1 --dry-run
```

This validates the manifest and every image and makes no API call.

## 3. Scan

```
node scripts/scan_benchmark.js --manifest my-manifest.csv --images D:\label-photos --run-id bf-run-1 --model <model-id>
```

Each image uses the exact call the web app uses. One JSON record per image is written to `benchmark-runs/bf-run-1/` (gitignored): raw model text, parsed and normalized results, model requested and responded, prompt fingerprint, code commit, image SHA-256, time. Failures are recorded, not hidden. Re-run the same command to resume; finished images are skipped and failed ones are retried. Each scan sends the image to Gemini and costs money.

## 4. Copy the run into the worksheet

```
python scripts/apply_scan_run.py --run benchmark-runs/bf-run-1 --worksheet docs/benchmark-50sku-results.csv --dry-run
python scripts/apply_scan_run.py --run benchmark-runs/bf-run-1 --worksheet docs/benchmark-50sku-results.csv
```

Only rows marked `pending_model_scan` are filled. Ground truth is never touched, existing outputs are never overwritten, and failed scans stay pending (they are not counted as misses). The reviewer columns are reset to blank/`unreviewed` because a scan cannot make those judgments.

## 5. Reviewer pass

A person compares each row with the physical pack or photo and fills:

- `evidence_located`: `yes` if the model's snippet can be found on the photographed panel, otherwise `no`.
- `unsupported_text`: `yes` if the output contains wording not visible in the photo, otherwise `no`.
- `error_category`: `none` if the output is correct. Otherwise a short label such as `misread`, `omitted`, `invented`, `number_changed`, `wrong_script`, `truncated`. Pick the labels once and use them consistently.
- `review_seconds`: only if you actually timed a controlled review. Leave blank otherwise.

Rows with these columns blank or `unreviewed` are reported as pending, and the support metrics are withheld until every scored row is reviewed.

## 6. Score

```
python scripts/score_benchmark.py --csv docs/benchmark-50sku-results.csv --out docs/BENCHMARK_50_SKU_INTERVALS.md
```

The report leads with how often a field marked Readable is wrong, with a SKU-clustered interval, then per-field exact match with 95% intervals, number mismatches, and strata. Groups with fewer than 10 rows or 5 SKUs are shown as "too few to report". It warns about single-script samples and brand concentration. The older `scripts/evaluate_benchmark.py` scorecard is unchanged.

## What to commit

Commit the worksheet and the generated report. Do not commit photos. `benchmark-runs/` is gitignored because it holds raw responses; if you want the run reproducible by others, archive it privately with the photos' SHA-256 values, or decide deliberately to commit it (it contains label text only, no personal data).

Do not describe any result as clinical, regulatory, or safety validation, or as representative of all products.
