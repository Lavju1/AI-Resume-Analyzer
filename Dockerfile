# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN groupadd --system app \
    && useradd --system --gid app --create-home app

FROM base AS builder

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --upgrade pip \
    && pip install .

FROM builder AS development

RUN pip install ".[dev]"

COPY tests ./tests

CMD ["pytest"]

FROM base AS runtime

ENV PATH="/opt/venv/bin:${PATH}"

COPY --from=builder /opt/venv /opt/venv

USER app

CMD ["python", "-c", "import ai_resume_analyzer; print('AI Resume Analyzer foundation image is ready.')"]
