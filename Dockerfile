FROM python:3.12-alpine

WORKDIR /code

# Dependencias del sistema (psycopg2, cryptografía, etc.)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    build-base \
    linux-headers \
    curl \
    bash

# Instalar uv y actualizar pip
RUN pip install --no-cache-dir --upgrade pip uv

# Copiar requirements
COPY requirements.txt requirements-dev.txt ./

# Argumento de entorno (true para dev, false para prod)
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then \
      uv pip install --system -r requirements-dev.txt ; \
    else \
      uv pip install --system -r requirements.txt ; \
    fi

# Crear carpetas necesarias
RUN mkdir -p /code/logs && adduser -D appuser
RUN chown -R appuser:appuser /code

# Copiar código
COPY . .

# Cambiar a usuario no root
USER appuser

EXPOSE 8000

# Cambiamos el host a 0.0.0.0 para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]