#############################
# STAGE 1: Build Dependencies
#############################
FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT="/venv" 

WORKDIR /app

RUN apk add --no-cache build-base libpq-dev libffi-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
RUN uv sync --frozen --no-dev

#############################
# STAGE 2: Runtime
#############################
FROM python:3.12-alpine AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH" \
    VIRTUAL_ENV="/venv"
    

WORKDIR /app

RUN apk add --no-cache libpq

RUN addgroup -S appuser && adduser -S -G appuser appuser

COPY --from=builder --chown=appuser:appuser /app /app
COPY --from=builder --chown=appuser:appuser /venv /venv 

USER appuser

EXPOSE 8000