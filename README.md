# CLOUD-03: CI/CD Pipeline with GitHub Actions

[![CI](https://github.com/CarlosRolo/cloud-cicd-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/CarlosRolo/cloud-cicd-pipeline/actions/workflows/ci.yml)
[![CD](https://github.com/CarlosRolo/cloud-cicd-pipeline/actions/workflows/cd.yml/badge.svg)](https://github.com/CarlosRolo/cloud-cicd-pipeline/actions/workflows/cd.yml)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)](https://github.com/CarlosRolo/cloud-cicd-pipeline/actions)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-multi--stage-2496ED)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Production-grade CI/CD pipeline for a FastAPI microservice. Every pull request triggers automated lint and tests; every merge to main builds a Docker image and deploys automatically to Render with Telegram notifications.

**Live API:** https://cloud-cicd-pipeline.onrender.com

---

## Pipeline Architecture

```
Developer → GitHub PR → CI (lint + tests) → merge to main
                                                    ↓
                                          CD (Docker build + deploy)
                                                    ↓
                                          Render.com (live API)
                                                    ↓
                                          Telegram notification
```

---

## Workflows

| Workflow | Trigger | Jobs |
|----------|---------|------|
| **CI** | Pull Request / push to main | ruff lint → black check → pytest (98% coverage) |
| **CD** | Push to main | Render deploy hook → health check |
| **Notify** | CI or CD completed | Telegram message with status + commit |
| **Blue-Green** | Manual (workflow_dispatch) | Build image → tag :blue or :green → push GHCR → deploy |

---

## Stack

| Tool | Purpose |
|------|---------|
| FastAPI 0.111 | REST API with automatic OpenAPI docs |
| pytest + httpx | Unit and integration tests |
| ruff + black | Linting and formatting |
| Docker multi-stage | Optimized production image |
| GitHub Actions | CI/CD automation |
| GHCR | Docker image registry |
| Render.com | Free cloud hosting |
| Telegram Bot API | Pipeline notifications |

---

## Project Structure

```
cloud-cicd-pipeline/
├── .github/
│   └── workflows/
│       ├── ci.yml           # Lint + tests on every PR
│       ├── cd.yml           # Deploy to Render on merge to main
│       ├── notify.yml       # Telegram notifications
│       └── blue-green.yml   # Manual blue/green deploy
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py        # GET /health, GET /
│   │   └── items.py         # CRUD /items
│   └── models/
│       ├── __init__.py
│       └── schemas.py       # Pydantic models
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   └── test_items.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── Makefile
└── README.md
```

---

## Quick Start

```bash
git clone https://github.com/CarlosRolo/cloud-cicd-pipeline.git
cd cloud-cicd-pipeline
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
make run
```

API available at `http://localhost:8000` - interactive docs at `http://localhost:8000/docs`

---

## Running Tests

```bash
make test
```

Output:

```
tests/test_health.py::test_root                PASSED
tests/test_health.py::test_health_check        PASSED
tests/test_items.py::test_list_items           PASSED
tests/test_items.py::test_get_item             PASSED
tests/test_items.py::test_get_item_not_found   PASSED
tests/test_items.py::test_create_item          PASSED
tests/test_items.py::test_delete_item          PASSED

7 passed — coverage: 98%
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root - service info |
| GET | `/health` | Health check - returns status, version, environment |
| GET | `/items/` | List all items |
| GET | `/items/{id}` | Get item by ID |
| POST | `/items/` | Create a new item |
| DELETE | `/items/{id}` | Delete item by ID |

### Example request

```bash
curl https://cloud-cicd-pipeline.onrender.com/health
```

```json
{
  "status": "ok",
  "version": "1.0.0",
  "environment": "production"
}
```

---

## CI/CD Flow

### On Pull Request

1. GitHub Actions triggers **CI** workflow
2. `ruff check` lints the code
3. `black --check` verifies formatting
4. `pytest` runs all tests with coverage report
5. PR is blocked from merging if any step fails

### On Push to Main

1. GitHub Actions triggers **CD** workflow
2. Render deploy hook is called via HTTP POST
3. Render pulls the latest code and rebuilds the Docker image
4. Health check confirms the API is live
5. **Notify** workflow fires a Telegram message with the result

---

## Blue-Green Deploy

Manual blue/green deploy via:

**GitHub → Actions → Blue-Green Deploy → Run workflow → select slot**

| Slot | Image tag | Use |
|------|-----------|-----|
| `blue` | `:blue` | Current stable production |
| `green` | `:green` | New version under validation |

Images are pushed to GHCR:

```
ghcr.io/carlosrolo/cloud-cicd-pipeline:blue
ghcr.io/carlosrolo/cloud-cicd-pipeline:green
ghcr.io/carlosrolo/cloud-cicd-pipeline:latest
```

To promote green → blue: re-run the workflow selecting `blue` slot after validating green.

---

## Docker

### Build locally

```bash
docker build -t cloud-cicd-pipeline .
docker run -p 8000:8000 cloud-cicd-pipeline
```

### With Docker Compose

```bash
docker compose up --build
```

---

## Required Secrets

Configure these in **GitHub → Settings → Secrets and variables → Actions**:

| Secret | Description |
|--------|-------------|
| `RENDER_DEPLOY_HOOK` | Render deploy hook URL (Settings → Deploy Hook) |
| `TELEGRAM_BOT_TOKEN` | Token from @BotFather |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |

---

## Environment Variables

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Runtime environment label |

---

## Makefile Commands

```bash
make install      # Install all dependencies
make test         # Run tests with coverage
make lint         # Run ruff linter
make format       # Run black formatter
make run          # Start development server
make docker-build # Build Docker image locally
```

---

## Author

**Carlos David Rodriguez Lopez**  
Telematic Engineer - ESPOCH  
Riobamba, Chimborazo, Ecuador  
Manta, Manabí, Ecuador  
GitHub: [github.com/CarlosRolo](https://github.com/CarlosRolo)  
LinkedIn: [linkedin.com/in/carlosdrodriguezl](https://linkedin.com/in/carlosdrodriguezl)

---

## License

MIT License - see [LICENSE](LICENSE)
