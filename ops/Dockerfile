FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==1.6.1

# Copy poetry files first (for better caching)
COPY pyproject.toml poetry.lock* ./

# Configure poetry and install dependencies
RUN poetry install --only=main && rm -rf $POETRY_CACHE_DIR
# RUN poetry config virtualenvs.create false \
#     && poetry config virtualenvs.in-project false \
#     && poetry install

# Copy application code
COPY . .

# Create non-root user and set permissions
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]