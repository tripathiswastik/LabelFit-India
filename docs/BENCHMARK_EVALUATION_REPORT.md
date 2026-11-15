# Benchmark Audit Report

```

================================================================================
  LABELFIT INDIA - 10-SKU EVIDENCE-BACKED BENCHMARK AUDIT REPORT
================================================================================
Total Evaluated Fields: 60
Unique Retail SKUs:     10
Unique Label Panels:    10
--------------------------------------------------------------------------------

[1] FIELD-BY-FIELD ACCURACY & EVIDENCE AUDIT:
Field                    | Exact Match  | CER    | Evidence%  | Unsupp%  | False Clear
--------------------------------------------------------------------------------
productName              | 100.0% (10/10) | 0.000  | 90.0%      | 0.0%     | 0          
ageMarking               | 90.0% (9/10) | 0.100  | 10.0%      | 10.0%    | 0          
ingredients              | 80.0% (8/10) | 0.061  | 90.0%      | 0.0%     | 2          
allergenDeclaration      | 100.0% (10/10) | 0.000  | 80.0%      | 0.0%     | 0          
nutritionPanel           | 30.0% (3/10) | 0.426  | 90.0%      | 0.0%     | 0          
preparationAndStorage    | 50.0% (5/10) | 0.321  | 90.0%      | 0.0%     | 2          

[2] STRATA BREAKDOWN BY SCRIPT:
Script / Language        | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
English-Latin            | 48       | 72.9          % | 0.169   
Bilingual-Devanagari-Latin | 12       | 83.3          % | 0.079   

[3] STRATA BREAKDOWN BY PHOTO CONDITION:
Condition                | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
pouch_vertical_panel     | 6        | 100.0         % | 0.000   
pouch_flat_back          | 24       | 62.5          % | 0.214   
pouch_front_back         | 6        | 66.7          % | 0.175   
pouch_vertical           | 6        | 83.3          % | 0.018   
tin_cylindrical          | 6        | 83.3          % | 0.141   
jar_cylindrical          | 12       | 83.3          % | 0.161   

================================================================================
Note: Empirical 10-SKU retail package benchmark (60 evaluated fields).
      Evaluates recorded Gemini model outputs against physical packaging ground truth
      independently transcribed & adjudicated by Swastik Tripathi & Saumya Tripathi.
      Not a clinical study, certified accuracy guarantee, or feeding recommendation.
================================================================================

```
