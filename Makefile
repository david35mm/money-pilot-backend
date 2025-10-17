# Makefile para MoneyPilot Backend
# Define el nombre del proyecto para Docker Compose
COMPOSE_PROJECT_NAME := money-pilot

# Archivos de configuración base y para desarrollo
COMPOSE_BASE_FILE := docker-compose.yml
COMPOSE_DEV_FILE := docker-compose.dev.yml
# COMPOSE_PROD_FILE := docker-compose.prod.yml # Asumiendo que crearás uno separado

# Comando base de docker-compose
COMPOSE_CMD := docker compose -p $(COMPOSE_PROJECT_NAME) -f $(COMPOSE_BASE_FILE)

# --- Variables para secrets ---
# Directorio donde se almacenarán los secrets
SECRETS_DIR := ./secrets
JWT_SECRET_FILE := $(SECRETS_DIR)/jwt_secret.txt
DB_NAME_FILE := $(SECRETS_DIR)/db_name.txt
DB_USER_FILE := $(SECRETS_DIR)/db_user.txt
DB_PASSWORD_FILE := $(SECRETS_DIR)/db_password.txt
# DB_HOST_FILE := $(SECRETS_DIR)/db_host.txt # No es necesario para conexión interna
# DB_PORT_FILE := $(SECRETS_DIR)/db_port.txt # No es necesario para conexión interna (5432)

# --- Tareas de Desarrollo ---

.PHONY: dev-up
dev-up: check-secrets-dev
	@echo "Levantando contenedores para desarrollo..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) up --build

.PHONY: dev-down
dev-down:
	@echo "Deteniendo contenedores de desarrollo..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) down

.PHONY: dev-logs
dev-logs:
	@echo "Mostrando logs de contenedores de desarrollo..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) logs -f

.PHONY: dev-exec-backend
dev-exec-backend:
	@echo "Entrando al contenedor del backend..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) exec backend sh

.PHONY: dev-exec-db
dev-exec-db:
	@echo "Entrando al contenedor de la base de datos..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) exec db psql -U $$(cat $(DB_USER_FILE)) -d $$(cat $(DB_NAME_FILE))

# --- Tareas de Producción (Ejemplo conceptual) ---
# Asumiendo que tienes un docker-compose.prod.yml
# COMPOSE_PROD_FILE := docker-compose.prod.yml
# COMPOSE_CMD_PROD := docker-compose -p $(COMPOSE_PROJECT_NAME) -f $(COMPOSE_BASE_FILE) -f $(COMPOSE_PROD_FILE)

.PHONY: prod-up
prod-up: check-secrets-prod
	@echo "Levantando contenedores para producción (conceptual)..."
	@echo "NOTA: Asegúrate de tener un docker-compose.prod.yml y secrets apropiados."
	# $(COMPOSE_CMD_PROD) up -d

.PHONY: prod-down
prod-down:
	@echo "Deteniendo contenedores de producción (conceptual)..."
	# $(COMPOSE_CMD_PROD) down

# --- Tareas Comunes ---

.PHONY: build
build:
	@echo "Construyendo imágenes..."
	$(COMPOSE_CMD) build

.PHONY: build-backend
build-backend:
	@echo "Construyendo solo la imagen del backend..."
	$(COMPOSE_CMD) build backend

.PHONY: build-db
build-db:
	@echo "Construyendo solo la imagen de la base de datos..."
	$(COMPOSE_CMD) build db

.PHONY: clean
clean:
	@echo "Deteniendo y removiendo contenedores, redes y volúmenes (¡Cuidado!)..."
	$(COMPOSE_CMD) down -v --remove-orphans

.PHONY: logs
logs: dev-logs # Por defecto, muestra logs de desarrollo

.PHONY: tests
tests:
	@echo "Corriendo pruebas dentro del contenedor backend..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) run --rm backend pytest

.PHONY: shell
shell:
	@echo "Entrando a la shell del contenedor backend..."
	$(COMPOSE_CMD) -f $(COMPOSE_DEV_FILE) run --rm backend sh

# --- Tareas de Secrets ---

.PHONY: check-secrets-dev
check-secrets-dev:
	@echo "Verificando secrets para desarrollo..."
	@if [ ! -f $(JWT_SECRET_FILE) ] || [ ! -f $(DB_NAME_FILE) ] || [ ! -f $(DB_USER_FILE) ] || [ ! -f $(DB_PASSWORD_FILE) ]; then \
		echo "Error: Uno o más archivos de secrets no existen en $(SECRETS_DIR)."; \
		echo "Corre 'make generate-secrets' para crearlos."; \
		exit 1; \
	fi
	@echo "Secrets para desarrollo verificados."

.PHONY: check-secrets-prod
check-secrets-prod:
	@echo "Verificando secrets para producción..."
	@if [ ! -f $(JWT_SECRET_FILE) ] || [ ! -f $(DB_NAME_FILE) ] || [ ! -f $(DB_USER_FILE) ] || [ ! -f $(DB_PASSWORD_FILE) ]; then \
		echo "Error: Uno o más archivos de secrets no existen en $(SECRETS_DIR)."; \
		echo "Corre 'make generate-secrets' para crearlos."; \
		exit 1; \
	fi
	@echo "Secrets para producción verificados (conceptual)."

.PHONY: generate-secrets
generate-secrets:
	@echo "Generando secrets en $(SECRETS_DIR)..."
	@mkdir -p $(SECRETS_DIR)
	@echo "Generando $(JWT_SECRET_FILE)..."
	@openssl rand -hex 32 > $(JWT_SECRET_FILE)
	@echo "Generando $(DB_NAME_FILE)..."
	@echo "money_pilot_db" > $(DB_NAME_FILE) # Cambia si lo deseas
	@echo "Generando $(DB_USER_FILE)..."
	@echo "money_pilot_user" > $(DB_USER_FILE) # Cambia si lo deseas
	@echo "Generando $(DB_PASSWORD_FILE)..."
	@openssl rand -hex 16 > $(DB_PASSWORD_FILE)
	@chmod 600 $(SECRETS_DIR)/*
	@echo "Secrets generados en $(SECRETS_DIR). ¡Recuerda cambiar los valores por defecto si es necesario!"

.PHONY: help
help:
	@echo "Makefile para MoneyPilot Backend"
	@echo ""
	@echo "Desarrollo:"
	@echo "  dev-up              Levanta contenedores para desarrollo (build incluido)"
	@echo "  dev-down            Detiene contenedores de desarrollo"
	@echo "  dev-logs            Muestra logs de contenedores de desarrollo"
	@echo "  dev-exec-backend    Ejecuta shell en el contenedor backend de desarrollo"
	@echo "  dev-exec-db         Ejecuta psql en el contenedor db de desarrollo"
	@echo ""
	@echo "Producción (conceptual):"
	@echo "  prod-up             Levanta contenedores para producción"
	@echo "  prod-down           Detiene contenedores de producción"
	@echo ""
	@echo "Comunes:"
	@echo "  build               Construye todas las imágenes"
	@echo "  build-backend       Construye solo la imagen del backend"
	@echo "  build-db            Construye solo la imagen de la base de datos"
	@echo "  clean               Detiene y remueve contenedores, redes y volúmenes (¡Cuidado!)"
	@echo "  logs                Muestra logs (por defecto desarrollo)"
	@echo "  tests               Corre las pruebas dentro del contenedor backend"
	@echo "  shell               Ejecuta shell en el contenedor backend (desarrollo)"
	@echo ""
	@echo "Secrets:"
	@echo "  generate-secrets    Genera archivos de secrets en $(SECRETS_DIR)"
	@echo "  check-secrets-dev   Verifica que los secrets para desarrollo existan"
	@echo "  check-secrets-prod  Verifica que los secrets para producción existan"
	@echo ""
	@echo "Otros:"
	@echo "  help                Muestra este mensaje"