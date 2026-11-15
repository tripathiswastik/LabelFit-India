# Benchmark Audit Report

```

================================================================================
  LABELFIT INDIA - EXPLORATORY PACKAGE-LABEL COMPARISON
================================================================================
Total Evaluated Fields: 4
Pending Rows Not Scored: 50
Unique Retail SKUs:     1
Unique Label Panels:    1
--------------------------------------------------------------------------------

[1] FIELD-BY-FIELD TEXT COMPARISON:
Field                    | Exact Match  | CER    | Snippet %  | Flagged %  | Clear CER>.15
--------------------------------------------------------------------------------
ingredients              | 100.0% (1/1) | 0.000  | 100.0%     | 0.0%       | 0
allergenDeclaration      | 100.0% (1/1) | 0.000  | 100.0%     | 0.0%       | 0
nutritionPanel           | 100.0% (1/1) | 0.000  | 100.0%     | 0.0%       | 0
preparationAndStorage    | 100.0% (1/1) | 0.000  | 100.0%     | 0.0%       | 0

[2] STRATA BREAKDOWN BY SCRIPT:
Script / Language        | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
English-Latin            | 4        | 100.0         % | 0.000

[3] STRATA BREAKDOWN BY PHOTO CONDITION:
Condition                | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
pouch_panel              | 4        | 100.0         % | 0.000

================================================================================
Note: Exploratory comparison of recorded Gemini output with package reference text.
      Pending ground-truth or model-scan rows are excluded from all scores.
      Snippet% means a snippet was present, not verified against the image.
      Flagged% reflects worksheet labels, not an independent token audit.
      Clear CER>.15 is a heuristic mismatch count, not human error adjudication.
      Review time is not measured. These scores are not clinical or safety validation.
================================================================================
```
