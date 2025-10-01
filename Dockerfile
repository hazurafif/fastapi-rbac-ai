# syntax=docker/dockerfile:1

# 1. Use lightweight Python base image
FROM python:3.12-slim AS base

# 2. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# 3. Install uv (fast Python package manager/runner)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# 4. Set working directory
WORKDIR /app

# 5. Copy dependency files first for better caching
COPY pyproject.toml uv.lock* README.md ./

# 6. Install dependencies
RUN uv pip install --system --no-cache -r <(uv pip compile pyproject.toml)

# 7. Copy the application source
COPY . .

# 8. Expose FastAPI port
EXPOSE 8000

# 9. Run FastAPI with uvicorn (entrypoint is main.py → app)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
