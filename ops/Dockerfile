FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.7.1

# Configure Poetry: Don't create virtual environment (we're in Docker)
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Copy Poetry files and README (required by pyproject.toml)
COPY pyproject.toml poetry.lock* README.md ./

# Copy application code (needed before poetry install since pyproject.toml references it)
COPY app ./app

# Install dependencies
RUN poetry install --only=main && rm -rf $POETRY_CACHE_DIR

# Expose port
EXPOSE 8000

# Default command (can be overridden in docker-compose)
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
