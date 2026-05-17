# GitHub Copilot Instructions for AI-Time-Machines

## Repository Overview

AI-Time-Machines is a full-stack AI platform for time-series agent creation and management. It is composed of three services:

- **Frontend** (`frontend/`) — React + TailwindCSS SPA served on port 3000
- **Backend** (`backend/`) — Node.js + Express REST API served on port 5000
- **Python ML Service** (`python-service/`) — Flask + TensorFlow forecasting service served on port 8000

All three services connect to a **PostgreSQL** database. The root `src/` directory contains standalone integration helpers (ChatGPT, OpenClaw) that can be used independently or within the full-stack app.

## Architecture & Key Files

```
AI-Time-Machines/
├── .github/
│   ├── copilot-instructions.md   # This file
│   ├── workflows/
│   │   ├── ci.yml                # Main CI/CD pipeline
│   │   ├── integrations.yml      # Platform integrations + security checks
│   │   ├── release.yml           # Release automation
│   │   ├── dependency-updates.yml
│   │   ├── reusable-ci.yml       # Reusable workflow for sibling repositories
│   │   └── cross-repo-sync.yml   # Cross-repository standards sync
├── backend/src/
│   ├── server.js                 # Express app entry point
│   ├── routes/                   # API route definitions
│   ├── controllers/              # Request handlers
│   ├── models/                   # Sequelize ORM models
│   ├── middleware/               # auth.js, rateLimiter.js, validate.js
│   └── config/                   # database.js
├── frontend/src/
│   ├── App.js                    # Root component + router
│   ├── contexts/                 # AuthContext
│   ├── pages/                    # Route-level page components
│   ├── components/               # Reusable UI components
│   └── services/                 # API service layer (axios)
├── python-service/
│   ├── app.py                    # Flask entry point
│   ├── models/                   # LSTM, GRU, ARIMA, Prophet, Transformer
│   └── requirements.txt
├── src/
│   ├── chatgpt.js                # OpenAI ChatGPT wrapper
│   └── openclaw.js               # OpenClaw analytics client
├── config/services.example.json  # Secrets / env vars documentation
├── .env.example                  # Environment variable template
└── docker-compose.yml            # Multi-service orchestration
```

## Development Setup

### Prerequisites
- Node.js ≥ 18, Python ≥ 3.11, PostgreSQL ≥ 15, Docker + Docker Compose

### Start Everything (Docker — recommended)
```bash
cp .env.example .env   # fill in JWT_SECRET and DB_PASSWORD at minimum
docker-compose up -d
```

### Start Locally
```bash
# Install all dependencies
npm run install:all

# Run all services concurrently
npm run dev
```

### Run Tests
```bash
npm test               # root-level Jest tests (src/)
cd backend && npm test # backend unit/integration tests (requires Postgres)
cd frontend && npm test -- --watchAll=false
```

### Lint
```bash
npm run lint           # ESLint over src/ and backend/
```

## Code Conventions

### JavaScript / Node.js (backend + src/)
- **CommonJS** (`require` / `module.exports`) — do not use ES Modules
- `async/await` for all asynchronous code; never use raw `.then()` chains in new code
- Use `express-validator` for all input validation in route handlers
- Apply `auth` middleware before route logic; apply `apiLimiter` after `auth`
- All Sequelize model definitions use `define()` with explicit `tableName`
- Environment variables are accessed via `process.env.*`; use `dotenv` at entry points only
- Error responses follow the pattern `res.status(NNN).json({ error: 'message' })`

### React (frontend/)
- Functional components with hooks only — no class components
- State management via React Context (`src/contexts/`) for global state, `useState`/`useReducer` locally
- TailwindCSS utility classes for all styling — no inline `style` props
- API calls are centralized in `src/services/` — components should never call `fetch`/`axios` directly
- Protected routes use the `PrivateRoute` pattern from `AuthContext`

### Python (python-service/)
- PEP 8 style; type hints on all public functions
- Flask blueprints for route grouping
- Model classes stored under `python-service/models/`
- Return JSON responses with consistent `{ "status": "success"|"error", "data": ... }` envelope

### Environment Variables
- Never hardcode secrets; always read from `process.env` / `os.environ`
- Document every new variable in both `.env.example` and `config/services.example.json`
- Secrets for GitHub Actions go in **repository secrets** (Settings → Secrets and variables → Actions)

### Commits & PRs
- Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`
- All PRs must reference an issue (`Fixes #N`)
- Fill in the PR template fully before requesting review

## Testing Guidelines

- Backend: Jest + Supertest for API endpoint tests; use the `test` database (`ai_time_machines_test`)
- Frontend: React Testing Library; mock API service calls
- Python: `pytest` under `python-service/tests/`
- Coverage target: aim for ≥ 70% on new code

## Security Rules

- Rate-limit all public endpoints with `apiLimiter` (100 req / 15 min by default)
- Stricter `createLimiter` (10 req / min) for POST create operations
- All write endpoints require JWT authentication via the `auth` middleware
- Webhook receivers (`POST /api/integrations/webhooks/:platform`) intentionally omit auth — do not add auth to these
- Sanitize and validate all user-provided input before database writes
- XML output must use `xmlEscape()` to prevent injection

## Cross-Repository Integration

This repository is part of a family of repositories owned by **lippytm**. Shared tooling is provided via reusable workflows:

- **`reusable-ci.yml`** — call from any sibling repo to run standard security, linting, and test checks
- **`cross-repo-sync.yml`** — dispatched automatically to propagate workflow and configuration updates across repos

### How to Use the Reusable CI Workflow in a Sibling Repo

```yaml
# .github/workflows/ci.yml  (in a sibling repository)
jobs:
  shared-ci:
    uses: lippytm/AI-Time-Machines/.github/workflows/reusable-ci.yml@main
    secrets: inherit
```

### Required Secrets (cross-repo operations)

| Secret | Purpose |
|--------|---------|
| `GITHUB_PAT` | Personal Access Token with `repo` and `workflow` scopes — needed for `cross-repo-sync.yml` to dispatch events to sibling repos |
| `OPENAI_API_KEY` | Optional — enables OpenAI connectivity tests |

Configure these in **Settings → Secrets and variables → Actions** for each repository that needs them.
