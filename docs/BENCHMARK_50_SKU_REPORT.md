# Complementary-food benchmark status

## Current evidence

The founder transcription intake now contains label references for 10 packaged complementary-food products marked for 6+ months. Those references are useful preparation for an evaluation; they are not model results.

The current comparison worksheet has **54 populated field rows**. Only **4 rows** have a recorded Gemini output, all from one Slurrp Farm package panel. The other **50 rows are marked `pending_model_scan`** and are excluded from scoring. The four completed fields are a single-package workflow check, not an accuracy estimate for the product category. Product name and age marking are not represented in those four fields because that photo shows a side panel.

The initial 50-SKU scorecard treated missing model outputs as empty predictions and carried the older mixed-category scope note. Those figures are withdrawn. Run `npm run benchmark:eval:50` to create a separate scorecard from completed pairs; the command leaves this status report intact.

## What remains

- Capture and retain the package image reference, scan date, model ID, prompt/code version, raw response, and normalized output for each SKU.
- Scan the remaining target packages and confirm each recorded reference is paired with the corresponding model result before scoring.
- Keep `pending_model_scan` and `pending_ground_truth` rows visible in progress exports, but exclude them from accuracy denominators.
- Expand toward 50 in-scope products only after the 10-product process is repeatable and representative package sources are documented.

The repository does not contain the original package photos or raw batch JSON, so the current four-field check cannot be independently reproduced from the repository alone. No caregiver usability, customer demand, health, safety, or feeding outcome has been measured.
