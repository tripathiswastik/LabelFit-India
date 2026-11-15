# Startup Buildathon India 2026 — form answers

Project: **LabelFit India**


Team: **LABEL CHECK**


Team size: **2 members**

## Project Submission

**Provide one sentence summary of your product/project**


LabelFit India turns a package-panel photo into candidate label text with image snippets and a read status, helping people check the wording against the package.

**What main problem are you solving?**


Caregivers can find it difficult to locate exact age markings, ingredients, allergen statements, nutrition details, and storage wording across small-print package panels. We are testing whether a photo-based review flow makes that wording easier to find for packaged complementary foods in India.

**Who is a typical user/customer?**


The first intended user is a caregiver in India checking a packaged complementary food labelled for babies 6 months and older. Food brands or retailers may be future customers for structured label data if discovery work validates a need.

**What is your solution?**


A user photographs one package panel. Gemini returns candidate text for selected printed fields with a snippet from the image and a read status. The user checks the wording against the package. LabelFit transcribes package information; it does not interpret health conditions or allergy risk, rate safety, or tell anyone what to feed.

**What is the stage of your product/project?**


Select **Other** and enter: **Working local prototype; the website is deployed on Cloud Run, with Gemini analysis disabled there. Founder-entered label references cover 10 target products; Gemini output is recorded for 12 fields from 3 SKUs, which is not an accuracy estimate. The 20 usability rows in the repository are illustrative protocol data, not caregiver study results. Pre-commercial exploratory stage; no revenue or traction.**

**What is the potential business model?**


After improving and evaluating the transcription workflow, we plan to interview food brands and retailers about whether structured label exports would help their catalog operations. This is a business hypothesis; there is no revenue or validated willingness to pay.

**Who are your primary competitors and how are you different?**


Open Food Facts provides community-contributed product records, while general OCR tools extract text from images. LabelFit is designed specifically around packaged complementary foods and pairs candidate fields with image snippets for people to review against the pack.

**Primary and secondary target countries**


Primary: India. Secondary: none selected yet.

**Pitch deck**


Upload the revised seven-slide PDF: **LABEL_CHECK_Startup_Buildathon_2026.pdf**. It is below 5 MB.

**How are you planning to use AI?**


Gemini will read a selected package photo and return candidate values for the product name, printed age marking, ingredients, explicit allergen declaration, nutrition panel, and preparation or storage wording. The app shows an image snippet and read status beside each field so the user can check the wording. Read status is not a calibrated confidence score.

**Select Google's AI model(s)**


Select **Gemini API**.

**How will you use the selected Google AI model?**


The local prototype uses the Gemini API with Gemini 3.8 Flash as the default model to extract six candidate label fields from one package-panel photo. The Node.js server validates and normalizes the response; the review page shows candidate wording, a model-provided photo snippet, and a read status such as Readable, Check text, or Not visible. When online analysis is enabled after access, quota, spend, and privacy controls are ready, this is the experience we intend users to see: candidate text alongside its photo evidence, for them to compare with the package. The Cloud Run website is live through GitHub Actions, but Gemini analysis is disabled in that deployment today. Next, we plan to pair scans with the 10 prepared product references, expand toward 50 products, and then run a consented caregiver usability study. These are future milestones, not measured results.

**Which development platforms will you use?**


Select **Google AI Studio** and **Others**. Google AI Studio is planned for prompt and response-schema iteration; the current prototype uses the Gemini API. The website is deployed to Google Cloud Run by a GitHub Actions workflow. The app uses Node.js, HTML, CSS, and JavaScript.

**How will you deploy and scale on Google Cloud?**


The website is deployed on Cloud Run from GitHub Actions. The public site serves the interface, but Gemini analysis is disabled. Before enabling analysis, we plan to add authenticated access, durable quotas and spend controls, and complete a privacy review. The near-term product target is a paired benchmark on packaged complementary foods, expanding toward 50 products; after that, we will evaluate the review flow with consented adult caregivers. No accuracy or user-benefit target is claimed yet.

**How did you hear about the Buildathon?**


**Hack2Skill event announcement.** Change this if the actual source was different.

## Startup / Project Details

**Are you planning to build a venture?**


Yes. We plan to explore a venture if the workflow proves useful and can be operated responsibly.

**How many members are working together?**


Two.

**Intended Industry/Vertical**


Choose **FoodTech** or **Food & Beverage** if listed. If the form uses technology sectors, choose **AI / Consumer Technology**.

**Founders/founding members, roles, and LinkedIn URLs**

- **Swastik Tripathi** — Founder / Project Lead; leads product and prototype development. LinkedIn: https://www.linkedin.com/in/swastik-tripathi-52333511a/ . GitHub: https://github.com/tripathiswastik/ .
- **Saumya Tripathi** — Team Member and IT Operations Engineer at Pitney Bowes, with 4+ years of experience. LinkedIn URL was not provided; add it if the form requires it.

**Brief founder/team bio, background, experience, and complementary skills**


Swastik Tripathi is an Oracle Specialist and AI Systems Engineer with 3+ years of enterprise experience in supply-chain planning, Oracle ERP systems, PL/SQL and ETL automation, and applied AI projects. He leads LabelFit India's product and prototype development. Saumya Tripathi is an IT Operations Engineer at Pitney Bowes with 4+ years of experience supporting business-critical applications in 24/7 environments. Her work includes AWS, Unix, Wintel, MySQL and MS SQL, production support, vulnerability remediation, deployments, AWS migration, and Sumo Logic monitoring. Saumya brings hands-on operations and troubleshooting experience, complementing Swastik's product and prototype work. The team has a working local prototype and a Cloud Run website with analysis disabled; benchmark coverage and caregiver usability remain to be evaluated. There is no commercial traction or revenue.

**How long have you been working as a team?**


Select **< 12 months** if that matches when LABEL CHECK formed. Confirm the start date before submitting.

## Evidence limits to keep consistent

The project maintains strict evidence boundaries: founder-entered text references are prepared for 10 target products, while the current comparison records Gemini output for 6 fields from 2 SKUs. The usability sheet contains 20 illustrative protocol rows; no live caregiver sessions are documented. These materials do not establish model accuracy across Indian retail packaging, user benefit, clinical outcomes, product safety, or willingness to pay. The next technical target is to pair model scans with product references and expand the benchmark toward 50 SKUs; a caregiver study would require real, consented adult participants and separate reporting.
