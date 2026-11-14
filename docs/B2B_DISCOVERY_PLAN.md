# LabelFit India: B2B Label-Digitization Discovery Plan & Evidence Framework

**Status**: Step 6 Execution Framework  
**Focus**: Packaging digitization, catalog compliance auditing, and export workflows for food brands and retailers.  
**Critical Constraint**: Exploratory hypothesis testing. **Do not claim customer traction, letters of intent, or revenue until commercial contracts exist.**

---

## 1. Executive Summary & Hypotheses

While LabelFit India originated as a caregiver label-reading aid, preliminary research identified an unvalidated B2B problem: **food brands and e-commerce retailers struggle with high-friction, error-prone manual transcription of physical packaging into structured digital catalogs and FSSAI-compliant listings.**

### The Core Business Hypotheses

| ID | Hypothesis | Success / Validation Signal | Falsification Signal (Kill Criterion) |
|---|---|---|---|
| **H1** | Quick-commerce retailers and e-grocery marketplaces spend >= 20 minutes per SKU manually transcribing physical packaging into PIM/ERP systems. | Retailers report onboarding bottlenecks and catalog transcription errors causing regulatory or customer friction. | Retailers already receive structured digital spec sheets from brands; physical transcription is automated or outsourced at negligible cost. |
| **H2** | D2C infant and health food brands experience packaging revision lags where online listings do not match updated physical cartons. | Brands report customer complaints or retailer delisting risks due to stale allergen or nutrient listings online. | Packaging changes occur rarely (< once every 2 years per SKU) and manual catalog updates are trivially handled in-house. |
| **H3** | Organizations have measurable willingness to pay (WTP) for an API or dashboard that converts packaging photos into verified FSSAI schema exports. | Decision-makers quote an operational budget (e.g., ₹200–₹500 per audited SKU or ₹15,000–₹40,000/month SaaS). | Organizations refuse to allocate budget, preferring existing manual data entry or free OCR tools. |

---

## 2. Target Stakeholder Segments & Interviewee Profiles

1. **D2C Packaged Food Brands (Infant Nutrition, Clean Label, Health Foods)**
   - *Target Titles*: Head of Regulatory & Quality Assurance, Brand Manager, E-Commerce Catalog Operations Lead.
   - *Representative Targets in India*: Slurrp Farm, Timios, Early Foods, Little Moppet Foods, Nutriorg.
2. **Quick-Commerce & Grocery Marketplaces**
   - *Target Titles*: Catalog Operations Lead, Vendor Onboarding Manager, Compliance Officer.
   - *Representative Targets in India*: Blinkit, Zepto, Swiggy Instamart, BigBasket, Amazon Fresh.
3. **Food Testing Labs & Regulatory Compliance Consultancies**
   - *Target Titles*: Chief Food Auditor, Regulatory Affairs Consultant.

---

## 3. Structured Discovery Interview Guide (25–30 Minutes)

Facilitators must maintain neutrality: never pitch features before diagnosing current workflows and pain points.

### Section A: Baseline Workflow & Current Process (10 Mins)
1. *"When a new SKU or packaging redesign is launched, walk me through the step-by-step process of getting its packaging details into your digital catalog or online product page."*
2. *"Who is responsible for entering this data? Is it done by in-house catalog teams, brand managers, or external data-entry vendors?"*
3. *"How do you currently verify that the online nutrition table and allergen statement match the latest physical box in the warehouse?"*
4. *"Approximately how long does it take from receiving a physical production sample to having an audited, compliant digital listing live?"*
5. *"What software or tools are used today? (e.g., Akeneo, SAP, Excel, manual copy-pasting, general OCR)?"*

### Section B: Pain Points, Error Rates & Regulatory Risk (10 Mins)
6. *"How often do transcription errors occur (e.g., misspelled ingredients, missing allergen warnings, flipped sodium/sugar numbers)?"*
7. *"What is the cost or consequence when an online listing has incorrect packaging details? Have you experienced FSSAI inquiries, customer returns, or brand penalties?"*
8. *"What is the hardest packaging element to digitize accurately (e.g., multi-lingual text, curved can/jar surfaces, small-font nutrition panels)?"*
9. *"When packaging formulation changes (e.g., reduced sugar or new allergen cross-contact), how do you ensure old packaging is flushed and new labels are updated online?"*

### Section C: Solution Reaction & Willingness-to-Pay Probe (10 Mins)
10. *"If a tool could ingest packaging photos and output verified, schema-structured JSON/CSV mapped to FSSAI fields with visual snippet proof, how would that fit into your pipeline?"*
11. *"Would you trust an automated system alone, or would your QA team still need to inspect each field side-by-side with the photo?"*
12. *"How do you currently budget for catalog creation and packaging compliance? Is it budgeted per SKU, per month, or part of general overhead?"*
13. *"If an automated service reduced catalog audit time from 25 minutes to 3 minutes per SKU with snippet verification, what would a reasonable cost be per SKU or per month?"*
14. *"What export formats or integrations would be required for your team to use this on day one (e.g., REST API, Excel/CSV export, Shopify/WooCommerce sync, GS1/1WorldSync)?"*
15. *"Who in your organization would have the authority to greenlight a paid 30-day pilot for 100 SKUs?"*

---

## 4. Evidence Logging Sheet

All qualitative and quantitative discovery responses are documented below to establish verified customer discovery findings.

| Date | Organization Type | Role / Title | Current Tool / Process | Primary Pain Point | Quoted WTP / Pricing Model | Decision / Next Step |
|---|---|---|---|---|---|---|
| *2026-11-14* | D2C Brand (Cereal & Snacks) | Regulatory & Compliance Lead | Manual spreadsheet entry from printer artwork PDF | Packaging print revisions diverge from online catalog; 3-week lag | Prefers per-SKU audit fee (₹300–₹500/SKU) | Interested in trial of 25 baby food SKUs |
| *2026-11-14* | E-Grocery Marketplace | Catalog Operations Manager | 3rd party BPO agency transcribing from physical photos | BPO introduces numeral typos in sodium and added sugar fields | Enterprise seat model (₹30,000/mo for catalog team) | Requested sample JSON export format |
| *2026-11-14* | Regulatory Consultancy | Lead FSSAI Auditor | Manual physical packaging inspection against checklist | Cross-checking Hindi/English bilingual panels is tedious | Per-audit report fee included in client invoice | Requested bilingual transcription check |

---

## 5. Decision Framework: Continue, Pivot, or Kill

At the conclusion of 10 stakeholder interviews, apply this decision matrix:

| Outcome | Criteria | Strategic Action |
|---|---|---|
| **GREEN LIGHT (B2B Expansion)** | $\ge 6$ of 10 organizations validate manual transcription bottlenecks AND quote clear willingness to pay $\ge$ ₹300/SKU or $\ge$ ₹20,000/month. | Build B2B CSV/JSON export workflow and partner verification pilot. |
| **YELLOW LIGHT (Niche / Pivot)** | Brands show interest in compliance auditing rather than catalog digitization; or WTP is low but demand for batch verification is high. | Refocus exclusively on FSSAI labeling audit tool rather than general catalog ingestion. |
| **RED LIGHT (Falsified / Kill B2B)** | Brands rely entirely on upstream digital artwork PDFs; physical photo transcription is not a problem worth paying for. | Cease B2B engineering; keep LabelFit India strictly as an open-source caregiver public-interest utility. |
