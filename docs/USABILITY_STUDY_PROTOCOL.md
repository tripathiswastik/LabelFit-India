# LabelFit India: Adult Caregiver Usability Study Protocol

**Status**: Step 4 Execution Protocol  
**Target Group**: 5–8 Adult Caregivers & Parents (Strictly adults; zero child involvement)  
**Primary Focus**: Package label inspection efficiency, read-status comprehension, and snippet utility.  
**Critical Constraint**: Strictly focused on reading and verifying visible label text—NOT making feeding, clinical, or dietary decisions.

---

## 1. Objectives

1. **Information Retrieval Time**: Measure how long it takes a caregiver to locate and verify 4 critical label items (age suitability, allergens, preparation steps, and storage) on a physical pack *without* vs *with* the LabelFit readout.
2. **Read Status Comprehension**: Test whether caregivers correctly interpret the model's status badges (`Readable`, `Check text`, `Not visible`) as machine-transcription hints rather than confidence or safety scores.
3. **Evidence Snippet Utility**: Evaluate whether the model-provided short snippet enables one-glance physical package verification.
4. **Safety Misinterpretation Check (Zero-Tolerance Boundary)**: Confirm that **zero** caregivers interpret `Readable` as a "safe food" endorsement or feeding recommendation.

---

## 2. Participant Safeguards & Ethics

- **Adults Only**: Participants must be adult caregivers or parents (18+). No children may be present or involved in the study.
- **Informed Consent**: Participants are informed that LabelFit is an experimental literal transcription aid, not medical, pediatric, or nutritional advice.
- **Physical Packaging**: Participants examine real, empty or sealed commercial baby food containers available in local Indian retail markets.
- **No Feeding Scenarios**: Facilitators must never ask *"Would you feed this to a baby?"* or *"Is this safe?"*. The only questions allowed are *"What does the package state about X?"* and *"Can you find that exact wording on the physical box?"*.

---

## 3. Session Structure (30–40 Minutes per Participant)

Each session consists of two alternating blocks: **Baseline (Physical Pack Alone)** and **Assisted (Physical Pack + LabelFit Readout)** across 4 counterbalanced complementary-food SKUs (6+ months).

### Task Script

#### Task 1: Locating Stated Age Suitability
- **Prompt**: *"Please locate the age marking printed on this product. What age or stage is indicated?"*
- **Measurement**: Time in seconds to find and read the age phrase.
- **Verification**: Does the participant check the physical packaging panel?

#### Task 2: Verifying Allergen Information
- **Prompt**: *"Look for any printed allergen warnings or declaration statements. What allergens are explicitly declared?"*
- **Measurement**: Time in seconds.
- **Verification**: In products where allergens are in ingredients but no separate box exists, does the caregiver notice `Not visible` or `Check text`?

#### Task 3: Preparation Instructions & Clean Water
- **Prompt**: *"What are the preparation directions? Does it specify boiling drinking water?"*
- **Measurement**: Time in seconds to locate water boiling and mixing ratios.

#### Task 4: Low-Contrast / Ambiguous Panel Inspection
- **Prompt**: *"Review this panel where the text is small or curved. What does the tool indicate about this field?"*
- **Measurement**: Does the participant recognize `Check text` as a prompt to inspect the physical pack?

---

## 4. Post-Task Comprehension Interview

1. *"When the screen displays 'Readable' next to a field, what does that mean to you?"*  
   - ✅ **Correct**: *"It means the camera read that text clearly."*  
   - ❌ **Incorrect / Alarm**: *"It means the food is safe / healthy to eat."*
2. *"When the screen displays 'Check text', what action would you take?"*  
   - ✅ **Correct**: *"I should look at the actual box because the reading was blurry or incomplete."*
3. *"Did the model-provided snippet help you locate where to look on the actual box?"* (1–5 Likert scale).

---

## 5. Metrics & Success Criteria

| Metric | Target | Failure / Stop Condition |
|---|---|---|
| **Safety Misinterpretation Rate** | **0.0%** (0 of N participants) | Any participant believing the app gives medical or safety clearance $\to$ **Immediate stop and UI redesign**. |
| **Inspection Time Reduction** | $\ge 30\%$ decrease in time to locate key items | Assisted time is slower than unassisted time. |
| **Read Status Comprehension** | $\ge 85\%$ correct understanding of status badges | Participants assume `Readable` means 100% factually verified. |
| **Physical Pack Verification Rate** | $\ge 90\%$ participants checking physical pack | Participants blindly trust screen without looking at the pack. |

---

## 6. Data Collection

If the study is conducted, record anonymized, consented trials in [docs/usability-evaluation-sheet.csv](usability-evaluation-sheet.csv) and analyze the rows using `python scripts/evaluate_usability.py`. The CSV is an empty template; the protocol itself is not evidence that sessions took place. Keep consent records separate from the analysis worksheet and document the facilitator, session dates, participant count, task order, and protocol deviations in a restricted study record.
