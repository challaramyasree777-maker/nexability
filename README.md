# NexAbility

Inclusive hiring platform that helps candidates discover relevant jobs, understand job-specific accessibility information, request accommodations, and track employer responses.

## Repository layout

- `frontend/` — intentionally empty placeholder for the frontend application.
- `backend/` — FastAPI application, domain modules, database, agents, and tests.
- `docs/` — architecture decisions, API contracts, and testing guidance.
- `.github/workflows/` — CI workflow definitions.
- `pytest` is configured from `backend/pyproject.toml`; test suites are split by unit, integration, API, contract, and accessibility checks.
- CodeRabbit review guidance lives in `.coderabbit.yaml` at the repository root.

## Backend setup

See [`backend/README.md`](backend/README.md) for local setup instructions. Do not commit `.env`, API keys, database passwords, uploaded resumes, or real candidate information.
