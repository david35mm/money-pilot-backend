FROM python:3.12-alpine

WORKDIR /code

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    linux-headers \
    curl \
    bash

COPY requirements*.txt ./

ARG INSTALL_DEV=false
RUN pip install --no-cache-dir --upgrade pip uv && \
    if [ "$INSTALL_DEV" = "true" ]; then \
      uv pip install --system -r requirements-dev.txt ; \
    else \
      uv pip install --system -r requirements.txt ; \
    fi

RUN adduser -D appuser && \
    mkdir -p /code/logs && \
    chown -R appuser:appuser /code

COPY . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]