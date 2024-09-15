From python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy our app into the container
COPY . /app

# Install the application dependancies
WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the server
CMD ["/app/.venv/bin/fastapi", "run", "/app/main.py", "--port", "80", "--host", "0.0.0.0"]

