# Benchmark Audit Report

```

================================================================================
  LABELFIT INDIA - EXPLORATORY 10-PACKAGE BENCHMARK
================================================================================
Total Evaluated Fields: 54
Unique Retail SKUs:     10
Unique Label Panels:    10
--------------------------------------------------------------------------------

[1] FIELD-BY-FIELD TEXT COMPARISON:
Field                    | Exact Match  | CER    | Snippet %  | Flagged %  | Clear CER>.15
--------------------------------------------------------------------------------
ingredients              | 11.1% (1/9)  | 0.889  | 11.1%      | 0.0%       | 0
allergenDeclaration      | 11.1% (1/9)  | 0.889  | 11.1%      | 0.0%       | 0
nutritionPanel           | 11.1% (1/9)  | 0.889  | 11.1%      | 0.0%       | 0
preparationAndStorage    | 10.0% (1/10) | 0.900  | 10.0%      | 0.0%       | 0
productName              | 0.0% (0/9)   | 1.000  | 0.0%       | 0.0%       | 0
ageMarking               | 0.0% (0/8)   | 1.000  | 0.0%       | 0.0%       | 0

[2] STRATA BREAKDOWN BY SCRIPT:
Script / Language        | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
English-Latin            | 54       | 7.4           % | 0.926

[3] STRATA BREAKDOWN BY PHOTO CONDITION:
Condition                | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
pouch_panel              | 54       | 7.4           % | 0.926

================================================================================
Note: Exploratory comparison of recorded Gemini output with founder-entered package text.
      Sample: 10 mixed-category products; only one complementary-food package.
      Snippet% means a snippet was present, not verified against the image.
      Flagged% reflects worksheet labels, not an independent token audit.
      Clear CER>.15 is a heuristic mismatch count, not human error adjudication.
      Review time is not measured. Not an infant-food accuracy or clinical study.
================================================================================
```
