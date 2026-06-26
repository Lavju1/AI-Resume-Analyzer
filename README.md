# AI Resume Analyzer

Production-grade foundation for an AI Resume Analyzer.

Current scope: **Phase 2 application foundation**. The repository now includes a FastAPI application shell with configuration, structured logging, request IDs, CORS, global exception handling, and a health endpoint.

It intentionally does not include business logic, authentication, database models, resume analysis, scoring, or AI features.

## Project Structure

```text
.
|-- .github/workflows/ci.yml
|-- config/
|-- docs/
|-- scripts/
|-- src/ai_resume_analyzer/
|   |-- constants/
|   |-- core/
|   |-- exceptions/
|   |-- middleware/
|   |-- utils/
|   |-- config.py
|   |-- main.py
|   |-- py.typed
|   `-- __init__.py
|-- tests/unit/
|-- .dockerignore
|-- .env.example
|-- .gitattributes
|-- .gitignore
|-- .pre-commit-config.yaml
|-- Dockerfile
|-- docker-compose.yml
|-- pyproject.toml
`-- README.md
```

## Application Foundation

- `config.py` defines Pydantic Settings loaded from environment variables and optional `.env` files.
- `core/logging.py` configures structured JSON logs with request ID correlation.
- `middleware/request_id.py` reads or creates an `X-Request-ID` value and adds it to every HTTP response.
- `exceptions/handlers.py` registers global handlers for HTTP errors, validation errors, and unhandled exceptions.
- `main.py` creates the FastAPI app, registers CORS, middleware, exception handlers, and `/health`.

## Requirements

- Python 3.12+
- Docker and Docker Compose
- Git

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pre-commit install
```

On macOS or Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

## Quality Gates

Run the same checks used by CI:

```bash
ruff check .
black --check .
isort --check-only .
mypy
pytest
```

Apply local pre-commit checks:

```bash
pre-commit run --all-files
```

## Docker

Build the runtime image:

```bash
docker build -t ai-resume-analyzer:foundation .
```

Run the FastAPI foundation container:

```bash
docker compose up --build app
```

Run tests in Docker:

```bash
docker compose --profile test run --rm test
```

## Configuration

Copy `.env.example` to `.env` for local-only overrides:

```bash
cp .env.example .env
```

No secrets are required in Phase 2.

## Phase Boundary

Phase 2 stops at application infrastructure. Future phases can add domain modules, persistence, authentication, API resources, and AI features behind their own scoped implementation plans.
