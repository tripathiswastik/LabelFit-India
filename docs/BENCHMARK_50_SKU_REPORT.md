# Benchmark status: exploratory 10-package audit

The figures and failure cases previously shown for a 50-SKU dataset remain withdrawn. They came from a hand-authored dataset in which `model_output` values were copied from `ground_truth`.

The current CSV contains 60 field comparisons across 10 distinct packages and records Gemini outputs against founder-entered package text. The sample covers mixed grocery categories and only one complementary-food package, so it is not a benchmark of LabelFit's intended baby-food category. It is a small engineering check, not an accuracy guarantee or representative evaluation.

- **Results CSV:** [docs/benchmark-10sku-results.csv](benchmark-10sku-results.csv) (60 fields, 10 package SKUs)
- **Blank worksheet:** [docs/benchmark-template.csv](benchmark-template.csv)
- **Evaluator report:** [docs/BENCHMARK_EVALUATION_REPORT.md](BENCHMARK_EVALUATION_REPORT.md)
- **Recalculate from committed results CSV:** `npm run benchmark:eval`
- **Reported exact field matches:** product name 10/10; allergen declaration 10/10; printed age marking 9/10; ingredients 8/10; preparation/storage 5/10; nutrition panel 3/10.
- **Metric limits:** snippet presence does not verify a snippet against the photo; worksheet flags are not a full unsupported-text audit; clear-read mismatch counts use a CER heuristic; review time was not measured.
- **Reproduction limit:** the CSV can be scored from the repository, but original package photos and raw batch results used to build it are not committed, so the data-generation step is not independently reproducible from this repository alone.

The next evaluation should collect at least 10 in-scope packaged complementary-food products labelled 6+ months, retain permission/source records, and capture two dated founder transcriptions before inspecting model outputs. Expand toward 50 only after the sample and adjudication process is repeatable. Keep formula for 0–6 months and foods for special medical purposes out of scope.
