# LabelFit India: Adult Caregiver Usability Study Runbook

**Document Reference**: LFI-USAB-RUNBOOK-2026-V1  
**Target Audience**: Usability Facilitators & Research Observers  
**Participant Cohort**: $N=5$ Adult Caregivers (Parents/Guardians aged 18+; zero child involvement)  
**Target SKUs**: 5 Complementary infant foods (6+ months): `SKU-BF-001` through `SKU-BF-005`  
**Data Destination**: [docs/usability-evaluation-sheet.csv](file:///D:/ag-ai/LabelFit%20India/docs/usability-evaluation-sheet.csv)  

---

## 1. Pre-Session Checklist (Mise en Place)

Prior to the arrival of each participant:
- [ ] **Physical Packages**: Ensure all 5 physical retail cartons/pouches are clean, authentic, sealed or safely empty, and placed on the table.
- [ ] **Consent Forms**: Have printed copies of [docs/CAREGIVER_CONSENT_FORM.md](file:///D:/ag-ai/LabelFit%20India/docs/CAREGIVER_CONSENT_FORM.md) ready.
- [ ] **Prototype Device**: Local prototype running on `http://127.0.0.1:4173/` (offline/local mode; Cloud Run live analysis disabled).
- [ ] **Measurement Tools**: Standard digital stopwatch / timer ready for latency logging.
- [ ] **Safety Rule Invariant**: Facilitators must **never** ask:
  - ❌ *"Would you feed this to your child?"*
  - ❌ *"Does this product look safe?"*
  - ✅ Permitted question: *"What does the packaging state about X, and can you point to that text on the box?"*

---

## 2. Facilitator Briefing Script (Word-for-Word)

> *"Thank you for taking the time to participate today. We are evaluating a digital tool called LabelFit India.*
> 
> *LabelFit is an experimental reader designed to help people locate and read printed information on food packaging—such as ingredient lists, allergen statements, age recommendations, and preparation instructions.*
> 
> *It is **strictly a literal reading aid**. It does **not** give nutritional, paediatric, or health advice. It does not judge whether a food is good, healthy, or safe. When the tool shows a 'Readable' badge, it only means the camera was able to read the printed letters clearly.*
> 
> *Today, we want to see how easy or hard it is to find specific information on real packages, both with and without the tool. We will also ask for your feedback on how clear the screen hints are. You may take a break or stop at any time."*

---

## 3. Standardized Task Protocols

Each participant completes 4 standardized evaluation tasks across counterbalanced SKUs:

### Task 1: Locating Stated Age Suitability (`age_marking`)
- **SKU**: `SKU-BF-002` (Manna First Foods) or `SKU-BF-003` (Timios)
- **Facilitator Prompt**: *"Please find the age recommendation printed on this package. What age range or stage is indicated?"*
- **Measurement**:
  - Start stopwatch when prompt ends.
  - Stop stopwatch when participant speaks the stated age (e.g., *"Stage 1: From 6 to 24 Months"* or *"6+ Months"*).
  - Record whether the participant verified the text on the physical carton.

### Task 2: Verifying Allergen Declaration (`allergen_declaration`)
- **SKU**: `SKU-BF-001` (Slurrp Farm) or `SKU-BF-004` (Early Foods)
- **Facilitator Prompt**: *"Look for any printed allergen warning or declaration statement. Does this package declare containing milk, wheat, or nuts?"*
- **Measurement**:
  - Time to locate the allergen statement.
  - Record whether participant located the dedicated allergen box or had to scan the whole ingredient table.

### Task 3: Preparation Instructions & Clean Water (`preparation_clean_water`)
- **SKU**: `SKU-BF-005` (Little Moppet) or `SKU-BF-002` (Manna)
- **Facilitator Prompt**: *"What are the preparation directions? Does it specify using boiled drinking water and what is the liquid ratio?"*
- **Measurement**:
  - Time to locate the preparation steps and clean water warning.

### Task 4: Low-Contrast / Ambiguous Panel Inspection (`ambiguous_panel`)
- **SKU**: Pouch crimp, curved corner, or small font panel displaying `Check text`.
- **Facilitator Prompt**: *"Look at this field where the tool displays 'Check text'. What does that badge mean to you, and what would you do next?"*
- **Measurement**:
  - Record whether participant correctly states they should inspect the physical box (`relied_on_physical_pack = yes`).

---

## 4. Post-Task Comprehension & Safety Interview

Ask the following questions verbatim:

1. **Badge Comprehension**:
   - *"When the screen displays 'Readable' in green next to an ingredient list, what does that mean?"*
   - ✅ **Correct**: *"The camera read the printed letters clearly."*
   - ❌ **Safety Violation**: *"The food is safe or approved for my baby."* $\to$ **CRITICAL ALARM: Note violation immediately.**

2. **Check Text Action**:
   - *"When the screen displays 'Check text' in amber, what action should you take?"*
   - ✅ **Correct**: *"Check the actual physical packaging because the photo or reading might be blurry or incomplete."*

3. **Snippet Utility**:
   - *"Did the short quote on the screen help you quickly find the exact spot on the box?"*
   - Rate 1 (Not helpful) to 5 (Extremely helpful).

---

## 5. Safety Stop Condition & Circuit Breakers

> [!CAUTION]
> **ZERO TOLERANCE FOR SAFETY MISINTERPRETATION:**
> If any participant states or implies that a `Readable` badge serves as a safety endorsement, clinical approval, or feeding recommendation:
> 1. Pause the trial immediately.
> 2. Re-explain that LabelFit is solely an OCR reading aid.
> 3. Record `misinterpreted_as_safety_score = yes` in the log sheet.
> 4. Trigger an immediate UI review to make the transcription-only disclaimer even more prominent.

---

## 6. Data Logging Procedure

Record each trial row directly into `docs/usability-evaluation-sheet.csv` using this schema:
```csv
session_id,caregiver_id,sku_id,task_type,time_without_tool_sec,time_with_tool_sec,accuracy_check,understood_read_status,relied_on_physical_pack,misinterpreted_as_safety_score,feedback_notes
```

Run evaluation script upon completing session entries:
```bash
python scripts/evaluate_usability.py --export-markdown docs/USABILITY_EVALUATION_REPORT.md
```
