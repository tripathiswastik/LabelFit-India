# Benchmark status: 10-SKU verified empirical benchmark established

The figures and failure cases previously shown in this file for a 50-SKU dataset remain withdrawn. They were generated from a hand-authored dataset in which the `model_output` values were copied from `ground_truth`.

In accordance with our verification gate, a reproducible **10-SKU evidence-backed benchmark** has been established using real retail packaging photos, dual-adjudicated ground truth by Swastik Tripathi and Saumya Tripathi, and recorded live Gemini model outputs (`gemini-3.6-flash` / `gemini-3.5-flash-lite`).

- **Worksheet:** [docs/benchmark-template.csv](benchmark-template.csv) (60 evaluated fields across 10 retail SKUs)
- **Evaluator Report:** [docs/BENCHMARK_EVALUATION_REPORT.md](BENCHMARK_EVALUATION_REPORT.md)
- **Reproducible Command:** `npm run benchmark:eval` (or `python scripts/evaluate_benchmark.py --csv docs/benchmark-template.csv --export-markdown docs/BENCHMARK_EVALUATION_REPORT.md`)
- **Key Findings:** 100% Exact Field Match on `productName` and `allergenDeclaration`, 90% on `ageMarking` (caloric GDA footnote caught & downgraded), 80% on `ingredients`, 50% on `preparationAndStorage` (marketing text), 30% on `nutritionPanel` (evidence truncation).

Any expansion to a 50-SKU benchmark remains future work pending acquisition of 40 additional authentic complementary infant packaging panels and independent transcriptions.
