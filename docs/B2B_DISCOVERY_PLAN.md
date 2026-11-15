# LabelFit India: B2B Label-Digitization Customer Discovery Plan

**Document Reference**: LFI-B2B-DISCOVERY-2026-V1  
**Status**: Qualitative discovery plan & interview hypotheses only.  
**Monetization Boundary**: Zero verified customer interviews, pricing signals, pilots, letters of intent, contracts, or revenues are currently claimed or documented. All monetization remains an unvalidated business hypothesis.  

---

## 1. Executive Context & Objectives

LabelFit India's primary product is a literal packaging transcription and visual verification engine. While consumer caregivers use the interface for package inspection, a secondary hypothesis exists around B2B demand:

> **Core Hypothesis**: Packaged food brands and e-commerce / quick-commerce marketplaces spend significant manual labor auditing, entering, and updating on-pack mandatory declarations (FSSAI licenses, nutritional tables, ingredients, allergens) across thousands of catalog SKUs. A source-linked candidate transcription tool with bounding crop verification could reduce turnaround time and audit friction.

**Objective of Discovery**:
Conduct 5 neutral, qualitative discovery interviews with operations, catalog, and regulatory compliance personnel to evaluate whether this workflow problem represents a genuine, recurring operational bottleneck before investing development resources in enterprise features.

---

## 2. Pre-Registered Decision Criteria (Continue vs. Pivot)

Before conducting interviews, the team pre-registers the following quantitative criteria to decide whether to advance to prototype piloting:

| Metric | Threshold for "Continue" | Signal for "Pivot / Drop" |
|---|---|---|
| **Problem Recurrence** | $\ge 4$ of 5 respondents report manual re-typing or verification takes $>15$ mins per SKU | $\le 2$ report manual transcription as a pain point |
| **Audit Frequency** | Packaging audited at least once per quarter or upon every batch/re-pack | Packaging rarely or never audited after initial onboarding |
| **Willingness to Test** | $\ge 3$ of 5 express interest in a zero-cost, sandboxed pilot with sample SKUs | $\le 1$ expresses interest in reviewing candidate output |
| **Budget Ownership** | Identifies specific department budget (Catalog Ops, Quality Assurance, or Legal) | No identified owner or priority |

*Note: Even if all Continue criteria are met, monetization remains unvalidated until a signed commercial pilot or contract is executed.*

---

## 3. Candidate Interviewee Segments

Interviews will be conducted across 3 target segments:

1. **Quick-Commerce & E-Grocery Catalog Operations**:
   - Roles: Catalog Operations Lead, Quality Assurance Specialist, Vendor Onboarding Lead.
   - Focus: Ingestion of supplier catalog feeds vs physical pack verification; rejection rates due to label discrepancies.
2. **Packaged Food D2C & FMCG Brand Teams**:
   - Roles: Packaging Regulatory Compliance Manager, Brand Catalog Lead.
   - Focus: Brand consistency, label version control across printed batch revisions, speed-to-market.
3. **Packaging Data & Content Aggregators**:
   - Roles: Data Ingestion Specialist, Metadata Operations Manager.
   - Focus: High-volume digital asset and label attribute extraction.

*All prospective companies and individuals are outreach targets only; no formal endorsement, partnership, or engagement exists.*

---

## 4. Neutral 20-Minute Interview Guide

Facilitators must follow neutral inquiry principles (The Mom Test):
- **NEVER** pitch LabelFit or ask *"Would you pay for a tool that does X?"*.
- **NEVER** quote speculative pricing tiers or cost savings.
- Focus exclusively on their past actions, current workflows, and real operational costs.

### Interview Script

#### Part 1: Current Workflow (7 Minutes)
1. *"Walk me through the last time a new food product was added to your catalog or had its packaging updated. Where did the information come from?"*
2. *"Who actually enters the nutritional information, ingredients, and allergen declarations into the database?"*
3. *"Which source does your team treat as the ultimate source of truth: approved packaging artwork (PDF/AI), brand master spreadsheets, or photographs of the physical printed package?"*

#### Part 2: Bottlenecks & Error Costs (7 Minutes)
4. *"Where do errors or delays most commonly happen during this process?"*
5. *"How often do customers, regulators, or internal QA flag a discrepancy between what's printed on the box and what's on the screen?"*
6. *"Roughly how much staff time or contractor cost goes into auditing or fixing label data per month?"*

#### Part 3: Workflow Fit & Pilot Constraints (6 Minutes)
7. *"If an automated tool generated candidate text with cropped photo snippets highlighting each field, where would that fit into your team's workflow?"*
8. *"What security, privacy, data retention, or system integration requirements would your organization require before even considering testing such a tool?"*
9. *"Who in your organization typically owns the budget or evaluation process for catalog tooling?"*

---

## 5. Evidence Logging & Privacy Protocol

1. Record all interview findings in [docs/b2b-discovery-interview-log.csv](file:///D:/ag-ai/LabelFit%20India/docs/b2b-discovery-interview-log.csv).
2. Schema fields:
   - `interview_id`: Unique identifier (e.g. `B2B-INT-001`).
   - `date`: Date of conversation (YYYY-MM-DD).
   - `role`: Job function (e.g. `Catalog Operations Manager`).
   - `organization_category`: Segment (e.g. `Quick-Commerce Marketplace`, `D2C Brand`).
   - `interviewer`: Team member conducting the session.
   - `current_workflow`: Summary of current packaging transcription process.
   - `turnaround_bottlenecks`: Key identified bottlenecks.
   - `transcription_error_frequency`: Reported error rates / frequency.
   - `staff_review_time_cost`: Time/cost spent reviewing label text.
   - `structured_export_fit`: Fit within existing catalog stack.
   - `budget_owner`: Functional owner of catalog/QA tooling.
   - `follow_up_status`: `contacted` / `completed` / `declined`.
   - `notes`: Objective factual observations.
3. **Strict Confidentiality**:
   - Company names, executive identities, and proprietary trade workflows must never be published in public repositories.
   - Only anonymized category findings may be cited in pitch decks or public roadmaps.
