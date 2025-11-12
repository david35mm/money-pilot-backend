# Project name
COMPOSE_PROJECT_NAME := moneypilot

# Compose configuration files
COMPOSE_BASE_FILE := docker-compose.yml
COMPOSE_DEV_FILE := docker-compose.dev.yml
COMPOSE_PROD_FILE := docker-compose.prod.yml  # Uncomment when production file is added

# Base docker compose command
COMPOSE_CMD := docker compose -p $(COMPOSE_PROJECT_NAME) -f $(COMPOSE_BASE_FILE)

# .env file (for development use)
ENV_FILE := .env

# Secrets directory and files (for future production use)
SECRETS_DIR := ./secrets
JWT_SECRET_FILE := $(SECRETS_DIR)/jwt_secret.txt
DB_NAME_FILE := $(SECRETS_DIR)/db_name.txt
DB_USER_FILE := $(SECRETS_DIR)/db_user.txt
DB_PASSWORD_FILE := $(SECRETS_DIR)/db_password.txt

# --- Development Tasks ---

.PHONY: dev-up
dev-up: check-env
	@echo "Starting development containers..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) up --build

.PHONY: dev-down
dev-down:
	@echo "Stopping development containers..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) down

.PHONY: dev-logs
dev-logs:
	@echo "Showing development container logs..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) logs -f

.PHONY: dev-exec-backend
dev-exec-backend:
	@echo "Entering backend container shell..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) exec backend sh

.PHONY: dev-exec-db
dev-exec-db:
	@echo "Connecting to PostgreSQL inside db container..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) exec db psql -U postgres -d postgres

# --- Production Tasks ---

.PHONY: prod-up
prod-up: check-secrets-prod
	@echo "Starting production containers..."
	# $(COMPOSE_CMD) -f $(COMPOSE_PROD_FILE) up -d

.PHONY: prod-down
prod-down:
	@echo "Stopping production containers..."
	# $(COMPOSE_CMD) -f $(COMPOSE_PROD_FILE) down

# --- Common Tasks ---

.PHONY: build
build:
	@echo "Building all Docker images..."
	$(COMPOSE_CMD) build

.PHONY: build-backend
build-backend:
	@echo "Building backend image only..."
	$(COMPOSE_CMD) build backend

.PHONY: build-db
build-db:
	@echo "Building database image only..."
	$(COMPOSE_CMD) build db

.PHONY: clean
clean:
	@echo "Stopping and removing containers, networks, and volumes (use with caution)..."
	$(COMPOSE_CMD) down -v --remove-orphans

.PHONY: logs
logs: dev-logs

.PHONY: tests
tests:
	@echo "Running tests inside backend container..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) run --rm backend pytest

.PHONY: shell
shell:
	@echo "Opening backend container shell..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) run --rm backend sh

# --- Environment File Management ---

.PHONY: check-env
check-env:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "No .env file found. Generating default one..."; \
		$(MAKE) generate-env; \
	else \
		echo ".env file already exists."; \
	fi

.PHONY: generate-env
generate-env:
	@echo "Creating .env file with default values..."
	@echo "POSTGRES_DB=moneypilot_db" > $(ENV_FILE)
	@echo "POSTGRES_USER=moneypilot_user" >> $(ENV_FILE)
	@echo "POSTGRES_PASSWORD=$$(openssl rand -hex 16)" >> $(ENV_FILE)
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> $(ENV_FILE)
	@echo "Created .env file with default configuration."

# --- Secrets Management ---

.PHONY: check-secrets-prod
check-secrets-prod:
	@echo "Checking production secrets..."
	@if [ ! -f $(JWT_SECRET_FILE) ] || [ ! -f $(DB_NAME_FILE) ] || [ ! -f $(DB_USER_FILE) ] || [ ! -f $(DB_PASSWORD_FILE) ]; then \
		echo "Error: One or more secret files are missing in $(SECRETS_DIR)."; \
		echo "Run 'make generate-secrets' to create them."; \
		exit 1; \
	fi
	@echo "Production secrets verified."

.PHONY: generate-secrets
generate-secrets:
	@echo "Generating secret files in $(SECRETS_DIR)..."
	@mkdir -p $(SECRETS_DIR)
	@echo "Creating $(JWT_SECRET_FILE)..."
	@openssl rand -hex 32 > $(JWT_SECRET_FILE)
	@echo "Creating $(DB_NAME_FILE)..."
	@echo "moneypilot_db" > $(DB_NAME_FILE)
	@echo "Creating $(DB_USER_FILE)..."
	@echo "moneypilot_user" > $(DB_USER_FILE)
	@echo "Creating $(DB_PASSWORD_FILE)..."
	@openssl rand -hex 16 > $(DB_PASSWORD_FILE)
	@chmod 600 $(SECRETS_DIR)/*
	@echo "Secrets generated in $(SECRETS_DIR). Remember to adjust default values if needed."

.PHONY: help
help:
	@echo "MoneyPilot API Makefile"
	@echo ""
	@echo "Development:"
	@echo "  dev-up              Start development containers (with build)"
	@echo "  dev-down            Stop development containers"
	@echo "  dev-logs            Show logs from development containers"
	@echo "  dev-exec-backend    Open shell in backend container"
	@echo "  dev-exec-db         Connect to PostgreSQL in db container"
	@echo ""
	@echo "Production (conceptual):"
	@echo "  prod-up             Start production containers"
	@echo "  prod-down           Stop production containers"
	@echo ""
	@echo "Common:"
	@echo "  build               Build all Docker images"
	@echo "  build-backend       Build only backend image"
	@echo "  build-db            Build only database image"
	@echo "  clean               Stop and remove all containers, networks, and volumes"
	@echo "  logs                Show container logs (defaults to development)"
	@echo "  tests               Run tests inside backend container"
	@echo "  shell               Open shell in backend container (development)"
	@echo ""
	@echo "Secrets:"
	@echo "  generate-secrets    Generate secret files in $(SECRETS_DIR)"
	@echo "  check-secrets-prod  Verify production secret files"
	@echo ""
	@echo "Other:"
	@echo "  help                Show this help message"