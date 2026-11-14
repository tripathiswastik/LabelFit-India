# LabelFit India: Privacy, data handling, and regulatory review checklist

**Status: Preliminary engineering notes only. This document is not a legal opinion, privacy audit, security certification, or regulatory approval. No external legal, privacy, or domain review is recorded.**

## Current prototype behavior to verify

- The local web app asks the user to confirm that the selected image contains package information only before analysis.
- The server forwards an accepted image to the configured Gemini endpoint and does not intentionally write uploaded images to an application file or database.
- The request sets `store: false`; this must not be described as zero retention or as overriding the provider's terms and logging.
- Cloud Run analysis is disabled in the current deployment configuration. This is a code-level deployment guard, not a complete production access, cost, or abuse-control system.
- The app has no child profile or persistent scan history.

These are implementation observations, not proof of compliance. Provider behavior depends on the actual account, endpoint, region, and current contract. Verify the deployed configuration and current provider terms before sending any real user's data.

## Before any external pilot

- Obtain qualified India privacy counsel's advice on the applicable DPDP Act and Rules, commencement dates, notice and consent, data-subject requests, security safeguards, processor terms, and any child-directed use.
- Obtain current FSSAI regulatory review for the exact product category and intended use. LabelFit only transcribes candidate package text and must not claim that a label or food is compliant.
- Review the data flow, logs, backups, telemetry, provider retention, access controls, incident response, deletion path, and data location with the service owner.
- Require authentication, durable rate and spend controls, billing alerts, and a documented operational owner before enabling public model calls.
- Keep any future participant or customer research separate from production data; obtain informed consent and store records securely.
- Recheck current official laws, rules, notifications, and provider terms at the time of review. Record reviewer, sources, date, scope, and unresolved questions.

## Product boundaries

The prototype is limited to candidate transcription of visible wording on packaged complementary foods labelled 6+ months. It does not assess product safety, health effects, allergy risk, regulatory compliance, or suitability for an individual child, and it does not provide feeding instructions. Infant formula and foods for special medical purposes are outside the prototype scope.

## Review record

No legal or compliance sign-off is recorded. All proposed pilot and deployment gates remain open until a named qualified reviewer documents the review and its scope.
