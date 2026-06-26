# AI Resume Analyzer

Production-grade foundation for an AI Resume Analyzer.

Current scope: **Phase 1 only**. This repository contains project scaffolding, packaging, quality tooling, Docker support, CI, and documentation. It intentionally does not include business logic, APIs, authentication, or AI features.

## Project Structure

```text
.
├── .github/workflows/ci.yml
├── config/
├── docs/
├── scripts/
├── src/ai_resume_analyzer/
├── tests/unit/
├── .dockerignore
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

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

Run the foundation container:

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

No secrets are required in Phase 1.

## Phase Boundary

Phase 1 stops at foundation setup. Future phases can add application modules, APIs, authentication, persistence, and AI features behind their own scoped implementation plans.
