# NexAbility Backend

## Structure

The backend is a modular FastAPI application (not a microservices deployment). Modules are separated by responsibility so five layer owners can work in parallel without creating duplicate business logic.

- `api/v1/endpoints/`: HTTP routes only; validate inputs and call services.
- `core/`: settings, security, logging and shared configuration.
- `db/`: SQLAlchemy base, session and database initialization.
- `models/`: SQLAlchemy persistence models.
- `schemas/`: Pydantic request/response contracts.
- `repositories/`: database queries and persistence operations.
- `services/`: deterministic business logic and integrations, grouped by domain.
- `agents/`: coordinator, specialist-agent definitions and controlled tools. Agents call services; they do not access the database directly.
- `workers/`: optional background jobs (only add a queue if the use case needs it).
- `tests/`: pytest suites.
- `alembic/`: database migrations.

## Local setup

Use Python 3.11+.

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

For Windows, create `.env` by copying `.env.example` manually if `cp` is unavailable.

## Test and quality commands

Run these from `backend/`:

```bash
pytest
pytest tests/unit -q
pytest tests/api -q
pytest tests/integration -q
pytest tests/contract -q
pytest tests/accessibility -q
ruff check app tests
ruff format --check app tests
```

The accessibility tests include automated checks and browser-level assertions, but they do not replace manual keyboard and screen-reader testing.
