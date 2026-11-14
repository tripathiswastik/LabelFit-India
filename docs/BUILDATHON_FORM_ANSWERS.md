# Startup Buildathon India 2026 - final form answers

Project: **LabelFit India**
Team: **LABEL CHECK**
Team size: **2 members**

## Project Submission

**Provide one sentence summary of your product/project**
LabelFit India turns a photo of a packaged complementary-food label into candidate text fields with source snippets and a read status, so people can check the wording against the package.

**What main problem are you solving?**
Caregivers can struggle to quickly locate age markings, ingredients, allergen statements, nutrition details, and storage wording across dense baby-food labels. Small print and varied layouts make exact wording harder to find; we still need to validate how significant this problem is for caregivers in India.

**Who is a typical user/customer?**
The initial user is a caregiver in India checking packaged complementary foods labelled for babies 6 months and older. Food brands or retailers may be future customers for structured label data, if discovery work validates the need.

**What is your solution?**
A user photographs one package panel. The Gemini API returns candidate text for selected printed fields with a model-provided snippet and read status. The user compares each result with the pack. LabelFit transcribes package wording; it does not interpret health conditions or allergy risk, rate safety, or tell anyone what to feed.

**What is the stage of your product/project?**
Select **Other** and enter: **Early local prototype; idea-stage project. Photo upload and the Gemini request flow are implemented. A live scan has not yet been demonstrated, and there are no accuracy results or traction.**

**What is the potential business model?**
After checking transcription accuracy, usability, and privacy, we plan to test whether food brands or retailers would pay for label digitization and structured exports. This is an early business hypothesis, not current revenue or a validated model.

**Who are your primary competitors and how are you different?**
Open Food Facts offers broad community-contributed product records, while general OCR tools can transcribe text from images. LabelFit is exploring a narrower photo-first workflow for packaged complementary foods labelled 6+ months, showing candidate fields beside snippets from the package. We have not yet measured comparative accuracy or usefulness.

**Primary and secondary target countries**
Primary: India. Secondary: none selected yet.

**Pitch deck**
Upload the attached seven-slide PDF: **LabelFitIndiaBuildathon2026.pdf**. It is under 5 MB.

**How are you planning to use AI?**
Gemini will read a selected package photo and return candidate values for the product name, printed age marking, ingredients, explicit allergen declaration, nutrition panel, and preparation or storage wording. The app shows a model-provided snippet and read status beside each field so the user can check the printed wording. Read status is not a calibrated confidence score.

**Select Google's AI model(s)**
Select **Gemini API**.

**How will you use the selected Google AI model?**
Use Gemini multimodal input and structured output to extract candidate label fields from a package photo. The next evaluation step is to compare results with independently transcribed ground truth for 50 local products, holding out complete products and reporting field-level errors before making accuracy claims.

**Which development platforms will you use?**
Select **Google AI Studio** and **Others**. Google AI Studio is planned for prompt and response-schema iteration. The prototype uses Node.js, HTML, CSS, and JavaScript.

**How will you deploy and scale on Google Cloud?**
Cloud Run is a possible later deployment target after authentication, server-side quotas, billing alerts, and privacy controls are in place. Public analysis is currently disabled on Cloud Run. The initial prototype has no persistent scan history or product catalog.

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
- **Swastik Tripathi** - Founder / Project Lead; leads product and prototype development. LinkedIn: https://www.linkedin.com/in/swastik-tripathi-52333511a/ . GitHub: https://github.com/tripathiswastik/ .
- **Somya Tripathi** - Team Member and IT Operations Engineer at Pitney Bowes, with 4+ years of experience. LinkedIn URL not provided; add it if the form requires it.

**Brief founder/team bio, background, experience, and complementary skills**
Swastik Tripathi is an Oracle Specialist and AI Systems Engineer with 3+ years of enterprise experience in supply-chain planning, Oracle ERP systems, PL/SQL and ETL automation, and applied AI projects. He leads LabelFit India's product and prototype development. Somya Tripathi is an IT Operations Engineer at Pitney Bowes with 4+ years of experience supporting business-critical applications in 24/7 environments. Her work includes AWS, Unix, Wintel, MySQL and MS SQL, production support, vulnerability remediation, deployments, AWS migration, and Sumo Logic monitoring. Somya brings hands-on operations and troubleshooting experience, complementing Swastik's product and prototype work. LABEL CHECK is at an early prototype stage, with no measured product accuracy, customer traction, or revenue yet.

**How long have you been working as a team?**
Select **< 12 months** if that matches when LABEL CHECK formed. Confirm the start date before submitting.

## Evidence limits to keep consistent

The repository's automated tests check software behavior only; they are not Gemini accuracy results. No live Gemini scan, completed 50-SKU benchmark, caregiver usability study, verified customer interview, or traction data is available yet. Do not present planned tests or business hypotheses as completed results.
