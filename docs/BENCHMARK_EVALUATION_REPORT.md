# Benchmark Audit Report

```

================================================================================
  LABELFIT INDIA - BENCHMARK EVALUATION AUDIT REPORT
================================================================================
Total Rows:     300
Unique SKUs:    50
Unique Images:  100
--------------------------------------------------------------------------------

[1] FIELD-BY-FIELD ACCURACY & EVIDENCE AUDIT:
Field                    | Exact Match  | CER    | Evidence%  | Unsupp%  | False Clear
--------------------------------------------------------------------------------
productName              | 100.0% (50/50) | 0.000  | 100.0%     | 0.0%     | 0          
ageMarking               | 100.0% (50/50) | 0.000  | 100.0%     | 0.0%     | 0          
ingredients              | 90.0% (45/50) | 0.012  | 100.0%     | 0.0%     | 0          
allergenDeclaration      | 94.0% (47/50) | 0.060  | 94.0%      | 6.0%     | 3          
nutritionPanel           | 88.0% (44/50) | 0.001  | 88.0%      | 12.0%    | 6          
preparationAndStorage    | 98.0% (49/50) | 0.000  | 100.0%     | 0.0%     | 0          

[2] STRATA BREAKDOWN BY SCRIPT:
Script / Language        | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
English-Latin            | 252      | 95.2          % | 0.014   
Bilingual (English + Hindi) | 12       | 100.0         % | 0.000   
Bilingual (English + Tamil) | 12       | 100.0         % | 0.000   
Hindi-Devanagari         | 6        | 83.3          % | 0.002   
Tamil-Tamil              | 6        | 83.3          % | 0.002   
Marathi-Devanagari       | 12       | 91.7          % | 0.001   

[3] STRATA BREAKDOWN BY PHOTO CONDITION:
Condition                | Samples  | Exact Match %  | Mean CER
------------------------------------------------------------
standard_indoor          | 126      | 96.8          % | 0.008   
slight_angle             | 36       | 100.0         % | 0.000   
glare_glossy_pouch       | 66       | 90.9          % | 0.009   
creased_foil             | 24       | 95.8          % | 0.042   
low_light                | 36       | 94.4          % | 0.028   
curved_tin               | 12       | 83.3          % | 0.002   

================================================================================
Note: Small exploratory check (target 50 SKUs). Not a clinical or nationwide claim.
================================================================================

```
