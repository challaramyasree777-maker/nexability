# NexAbility layer ownership

- **L1 Accessible Experience:** all frontend pages and WCAG 2.2 AA behaviour, including screen-reader and keyboard support for blind/low-vision, deaf/hard-of-hearing, motor, cognitive/learning and speech-related needs.
- **L2 Core Platform:** FastAPI route integration, auth/roles, database, applications, accommodation state machine, claims, feedback, notifications and seed data.
- **L3 Intelligence:** résumé/job parsing, normalization, embeddings, ranking, per-need accessibility statuses, explanations and evaluation.
- **L4 Agent Orchestration:** one coordinator plus Candidate Intelligence, Job Matching & Accessibility, and Accommodation & Interview specialists; controlled tools and approval gates.
- **L5 Interview, Integration & Delivery:** video SDK, scheduling coordination, mock SuccessFactors payload, CI/deployment, end-to-end tests and demo.

Rules:
1. Agents never access the database directly; they call permission-checked tools.
2. Unknown accessibility information is not Confirmed.
3. Accommodation requests are submitted only after explicit candidate approval.
4. Every feature owner tests the feature against the shared contract.
