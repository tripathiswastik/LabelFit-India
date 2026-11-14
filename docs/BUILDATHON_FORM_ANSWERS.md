# Startup Buildathon India 2026 - form answer draft

## Project Submission

**Project/team name**  
LABEL CHECK

**One-sentence project summary**  
LabelFit India turns a photo of a packaged complementary-food label into candidate text fields with source snippets and visible read status, so a person can check the wording against the pack.

**Main problem**  
Caregivers can struggle to quickly locate age markings, ingredients, allergen statements, nutrition details, and storage wording across dense baby-food labels. Small print and varied layouts make the exact wording harder to find; the scale of this problem in India still needs validation.

**Typical user/customer**  
The initial user is a caregiver in India checking packaged complementary foods labelled for babies 6 months and older. Retailers or food brands are possible future customers for structured label data, subject to validation.

**Solution**  
A user photographs one label panel. The configured Gemini API returns candidate text for selected fields, paired with a model-provided snippet and read status. The user checks the result against the package. The prototype reports printed wording; it does not interpret health conditions or allergies, rate safety, or direct feeding decisions.

**Product stage**  
Select **Other** and enter: **Early local prototype; idea-stage project. The photo-upload and Gemini request flow are implemented, but a live scan has not yet been demonstrated. No benchmark or traction yet.**

**Potential business model**  
After field-level accuracy, usability, and privacy checks, test whether food brands or retailers will pay for label digitization and structured exports. This is a hypothesis, not current revenue or a validated plan.

**Competitors and difference**  
Open Food Facts provides broad community-contributed product records, and general OCR tools can transcribe text. LabelFit is exploring a narrower photo-first workflow for packaged complementary foods labelled 6+ months, pairing candidate fields with snippets and read status. Comparative accuracy and usefulness have not yet been measured.

**Primary and secondary target countries**  
Primary: India. Secondary: none selected yet.

**AI use**  
Gemini processes a selected package photo and returns candidate label fields in a structured response. The interface presents each candidate with its snippet and read status so the wording can be checked against the physical package. These statuses are model outputs, not calibrated confidence scores.

**Google AI model(s)**  
Gemini API.

**How Gemini will be used**  
Use Gemini multimodal input to extract candidate product name, printed age marking, ingredients, explicit allergen declaration, nutrition information, and preparation or storage wording. Evaluate exact field matches, unsupported text, and uncertainty handling on an independently transcribed 50-SKU set, held out by product, before making accuracy claims.

**Development platform**  
Google AI Studio for prompt and response-schema iteration; other development tools for the web prototype.

**Google Cloud plan**  
Cloud Run is a possible later deployment target after authentication, server-side quotas, billing alerts, and privacy controls are in place. Public analysis is currently disabled on Cloud Run. No database or persistent scan history is planned for the initial prototype.

**How did you hear about the Buildathon?**  
Enter the actual source through which the team heard about it; do not guess.

## Startup / Project Details

**Are you planning to build a venture?**  Yes. The team intends to explore building a venture if the transcription workflow proves useful and can be operated responsibly.

**Team name**  LABEL CHECK.

**Team size**  Two members.

**Members, roles, and LinkedIn profiles**  
- **Swastik Tripathi** - Founder / Project Lead; product and prototype development. LinkedIn: https://www.linkedin.com/in/swastik-tripathi-52333511a/ . GitHub: https://github.com/tripathiswastik/ .
- **Saumya Tripathi** - Team Member; working professional with nearly 5 years of experience. Specific functional title, field of experience, and LinkedIn profile have not been provided; confirm these before submitting if the form requires them.

**Brief team bio and complementary skills**  
LABEL CHECK is a two-member team building LabelFit India, an early-stage label-transcription prototype. Swastik Tripathi leads the product and prototype work. Saumya Tripathi is a working professional with nearly five years of experience and has joined the project team. The team has no measured product accuracy, customer traction, or revenue to report. Add Saumya's professional field and specific role if the application requires them.

**How long have you been working together?**  Select **< 12 months** if the team formed within the past year; confirm the start date before submission.

## Pitch and evidence status

The deck should identify LABEL CHECK as the team and LabelFit India as the product. No live Gemini scan result, completed 50-SKU benchmark, caregiver usability study, verified customer interview, or traction data is available yet. Present repository tests as software checks only; they are not AI accuracy results. For a live demonstration, first complete a local smoke test with a synthetic package-label image.
