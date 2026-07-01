# AI Resume Analyzer

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=111111)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

A full-stack AI-powered Resume Analyzer that helps users upload resumes, receive
ATS scores, AI-powered resume feedback, and job matching analysis using Google
Gemini.

## Features

- Secure JWT Authentication
- Resume Upload (PDF & DOCX)
- Resume Parsing
- ATS Scoring
- AI Resume Analysis
- Job Matching
- Responsive Dashboard
- Modern UI

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Axios

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic

### Database
- PostgreSQL (Neon)

### AI
- Google Gemini AI

### Deployment
- Docker
- Render
- Vercel

## Project Structure

```text
AI-Resume-Analyzer/
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- alembic/
|   |-- versions/
|   |-- env.py
|   `-- script.py.mako
|-- docs/
|   `-- images/
|-- frontend/
|   |-- public/
|   |-- src/
|   |   |-- api/
|   |   |-- components/
|   |   |-- hooks/
|   |   |-- layouts/
|   |   |-- pages/
|   |   |-- routes/
|   |   |-- services/
|   |   |-- types/
|   |   `-- utils/
|   |-- package.json
|   `-- vite.config.ts
|-- src/
|   `-- ai_resume_analyzer/
|       |-- ai/
|       |-- api/
|       |-- auth/
|       |-- database/
|       |-- extractors/
|       |-- feedback/
|       |-- job_matching/
|       |-- parsers/
|       |-- repositories/
|       |-- schemas/
|       |-- scoring/
|       |-- services/
|       |-- config.py
|       `-- main.py
|-- tests/
|   `-- unit/
|-- uploads/
|   `-- resumes/
|-- .env.example
|-- Dockerfile
|-- docker-compose.yml
|-- pyproject.toml
`-- README.md
```

## Screenshots

![Login](docs/images/login.png)

![Dashboard](docs/images/dashboard.png)

![Resume Upload](docs/images/resume-upload.png)

![ATS Analysis](docs/images/ats-analysis.png)

![Job Matching](docs/images/job-matching.png)

## Installation

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 15+
- Docker and Docker Compose
- Google Gemini API key

### Backend Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
copy .env.example .env
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
```

Update `.env` with your local database URL, JWT secret, and Gemini API key.
Then run migrations and start the API:

```bash
alembic upgrade head
python -m uvicorn ai_resume_analyzer.main:app --reload
```

The backend runs at:

```text
http://localhost:8000
```

### Frontend Setup

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

On macOS or Linux:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

### Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE ai_resume_analyzer;
```

Or start a local PostgreSQL container:

```bash
docker run --name ai-resume-analyzer-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ai_resume_analyzer \
  -p 5432:5432 \
  -d postgres:15
```

Use this connection string in `.env`:

```text
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_resume_analyzer
```

Apply migrations:

```bash
alembic upgrade head
```

## Environment Variables

### Backend

| Variable | Description | Example |
| --- | --- | --- |
| `APP_NAME` | FastAPI application name | `ai-resume-analyzer` |
| `APP_ENV` | Application environment | `development` |
| `DEBUG` | Enables debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `DATABASE_URL` | PostgreSQL async connection URL | `postgresql+asyncpg://postgres:postgres@localhost:5432/ai_resume_analyzer` |
| `DATABASE_ECHO` | Enables SQLAlchemy query logging | `false` |
| `JWT_SECRET_KEY` | Secret key used to sign JWTs | `change-me-in-production` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |
| `UPLOAD_DIRECTORY` | Resume file storage directory | `uploads/resumes` |
| `MAX_UPLOAD_SIZE_MB` | Maximum upload size | `10` |
| `ALLOWED_FILE_TYPES` | Accepted resume MIME types | `["application/pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document"]` |
| `REQUEST_ID_HEADER` | Request correlation header | `X-Request-ID` |
| `CORS_ALLOW_ORIGINS` | Allowed frontend origins | `["http://localhost:5173"]` |
| `CORS_ALLOW_CREDENTIALS` | Enables credentialed CORS requests | `false` |
| `CORS_ALLOW_METHODS` | Allowed HTTP methods | `["GET","POST","PUT","PATCH","DELETE","OPTIONS"]` |
| `CORS_ALLOW_HEADERS` | Allowed request headers | `["*"]` |
| `GEMINI_API_KEY` | Google Gemini API key | `your-api-key` |
| `GEMINI_MODEL` | Gemini model name | `gemini-1.5-flash` |

### Frontend

| Variable | Description | Example |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Authenticate and receive a JWT |
| `GET` | `/auth/me` | Return the current authenticated user |
| `POST` | `/resumes/upload` | Upload a PDF or DOCX resume and receive parsed analysis |
| `GET` | `/resumes` | List uploaded resumes for the authenticated user |
| `GET` | `/resumes/{resume_id}` | Get resume metadata |
| `DELETE` | `/resumes/{resume_id}` | Delete a resume |
| `POST` | `/resumes/job-match` | Compare an uploaded resume against a job description |

## Development Commands

### Backend

```bash
python -m black .
python -m isort .
python -m ruff check .
python -m mypy src
python -m pytest
```

### Frontend

```bash
cd frontend
npm run build
```

### Docker

```bash
docker compose up --build app
```

Run the backend test image:

```bash
docker compose --profile test run --rm test
```

## Future Roadmap

- Semantic Job Matching
- Resume Tailoring
- Cover Letter Generator
- Interview Question Generator
- pgvector Integration
- Deployment

## 🌐 Live Demo

- **Frontend:** https://ai-resume-analyzer-chi-rouge.vercel.app
- **Backend API (Swagger):** https://ai-resume-analyzer-ayti.onrender.com/docs

## Author

**Lavnish Jain**

GitHub: [https://github.com/Lavju1](https://github.com/Lavju1)

LinkedIn: [https://www.linkedin.com/in/lavnish-jain-443934243/](https://www.linkedin.com/in/lavnish-jain-443934243/)
