# MoneyPilot Backend

FastAPI-based financial API for managing users, profiles, and transactions.

## Overview

MoneyPilot Backend is a financial management API built with FastAPI, PostgreSQL, and JWT authentication. It provides endpoints for user registration, profile management, and financial transaction tracking.

## How to Run (with Docker)

Using the provided Makefile commands:

```bash
make build       # Build Docker containers
make dev-up      # Start development containers
make dev-down    # Stop containers
make logs        # View logs
```

The API will be accessible at `http://localhost:11011` in development mode.

## How to Run (without Docker)

For local development without Docker:

```bash
uv sync
uv run uvicorn api.main:app --reload
```

## API Access

- API endpoint: `http://localhost:11011`
- Interactive docs: `http://localhost:11011/docs`
- Alternative docs: `http://localhost:11011/redoc`

## Frontend Development Note

When running locally, ensure your frontend API base URL matches the backend port and uses HTTP instead of HTTPS.
