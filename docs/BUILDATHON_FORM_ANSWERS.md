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


Select **Other** and enter: **Working local prototype with live Gemini scans and a small 10-package, 60-field engineering check. The sample covers mixed grocery categories and includes only one complementary-food package, so infant-food accuracy is not yet established. No caregiver study or commercial traction is claimed.**

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


We use Gemini multimodal input and structured output to extract candidate label fields from package photos. Our early 10-package comparison covers mixed grocery products and includes only one complementary-food package; it exposed weak transcription of dense nutrition and preparation/storage text. Next we will evaluate a focused sample of 6+ month complementary-food labels before making claims about that category.

**Which development platforms will you use?**


Select **Google AI Studio** and **Others**. Google AI Studio is planned for prompt and response-schema iteration. The prototype uses Node.js, HTML, CSS, and JavaScript.

**How will you deploy and scale on Google Cloud?**


Cloud Run is a possible later deployment target after authentication, server-side quotas, billing alerts, and privacy controls are in place. Public analysis is currently disabled on Cloud Run. The local prototype has no persistent scan history or product catalog.

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


Swastik Tripathi is an Oracle Specialist and AI Systems Engineer with 3+ years of enterprise experience in supply-chain planning, Oracle ERP systems, PL/SQL and ETL automation, and applied AI projects. He leads LabelFit India's product and prototype development. Saumya Tripathi is an IT Operations Engineer at Pitney Bowes with 4+ years of experience supporting business-critical applications in 24/7 environments. Her work includes AWS, Unix, Wintel, MySQL and MS SQL, production support, vulnerability remediation, deployments, AWS migration, and Sumo Logic monitoring. Saumya brings hands-on operations and troubleshooting experience, complementing Swastik's product and prototype work. The team is at an early prototype stage, with no caregiver study, commercial traction, or revenue claimed.

**How long have you been working as a team?**


Select **< 12 months** if that matches when LABEL CHECK formed. Confirm the start date before submitting.

## Evidence limits to keep consistent

The current 10-package benchmark includes nine general grocery products and one complementary-food product; it does not establish performance on baby-food labels. It reports package-text comparison only, not caregiver usability, health outcomes, product suitability, willingness to pay, or business traction. Automated tests check software behavior and are not model-accuracy results.
