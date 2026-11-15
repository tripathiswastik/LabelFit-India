# Complementary-food benchmark status

## Current evidence

The founder transcription intake now contains label references for 10 packaged complementary-food products marked for 6+ months. Those references are useful preparation for an evaluation; they are not model results.

The current comparison worksheet has **54 populated field rows**. Currently, **6 rows** across 2 Slurrp Farm package panels (`SKU-BF-001` side panel, `SKU-BF-009` back panel) have recorded Gemini outputs. The other **48 rows are marked `pending_model_scan`** and are excluded from scoring. The completed fields represent a workflow check across available panels, not an accuracy estimate for the entire product category. Product name is represented from the back panel; age marking remains not visible on these two panels.

The initial 50-SKU scorecard treated missing model outputs as empty predictions and carried the older mixed-category scope note. Those figures are withdrawn. Run `npm run benchmark:eval:50` to create a separate scorecard from completed pairs; the command leaves this status report intact.

## What remains

- Capture and retain the package image reference, scan date, model ID, prompt/code version, raw response, and normalized output for each SKU.
- Scan the remaining target packages and confirm each recorded reference is paired with the corresponding model result before scoring.
- Keep `pending_model_scan` and `pending_ground_truth` rows visible in progress exports, but exclude them from accuracy denominators.
- Expand toward 50 in-scope products only after the 10-product process is repeatable and representative package sources are documented.

The repository retains full audit records (model ID, prompt fingerprint, raw and normalized JSON, image SHA-256) for completed scans under `benchmark-runs/`. No caregiver usability, customer demand, health, safety, or feeding outcome has been measured.
