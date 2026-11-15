# Benchmark Audit Report

```

================================================================================
  LABELFIT INDIA - EXPLORATORY PACKAGE-LABEL COMPARISON
================================================================================
Total Evaluated Fields: 12
Pending Rows Not Scored: 42
Unique Retail SKUs:     3
Unique Label Panels:    0
--------------------------------------------------------------------------------

[1] FIELD-BY-FIELD TEXT COMPARISON:
Field                    | Exact Match  | CER    | Snippet %  | Flagged %  | Clear CER>.15
--------------------------------------------------------------------------------
ingredients              | 50.0% (1/2)  | 0.500  | 50.0%      | 0.0%       | 0
allergenDeclaration      | 50.0% (1/2)  | 0.500  | 50.0%      | 0.0%       | 0
nutritionPanel           | 50.0% (1/2)  | 0.500  | 50.0%      | 0.0%       | 0
preparationAndStorage    | 33.3% (1/3)  | 0.484  | 66.7%      | 0.0%       | 1
productName              | 0.0% (0/2)   | 0.837  | 50.0%      | 0.0%       | 1
ageMarking               | 0.0% (0/1)   | 0.714  | 100.0%     | 0.0%       | 1

[2] STRATA BREAKDOWN BY SCRIPT:
Script / Language        | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
English-Latin            | 12       | 33.3          % | 0.570

[3] STRATA BREAKDOWN BY PHOTO CONDITION:
Condition                | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
pouch_panel              | 12       | 33.3          % | 0.570

================================================================================
Note: Exploratory comparison of recorded Gemini output with package reference text.
      Pending ground-truth or model-scan rows are excluded from all scores.
      Snippet% means a snippet was present, not verified against the image.
      Flagged% reflects worksheet labels, not an independent token audit.
      Clear CER>.15 is a heuristic mismatch count, not human error adjudication.
      Review time is not measured. These scores are not clinical or safety validation.
================================================================================
```
