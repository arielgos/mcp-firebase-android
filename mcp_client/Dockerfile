FROM python:3.14.0

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src ./app

# Application ports
ENV PORT=9000
EXPOSE 9000

# Start the application
# uvicorn app.webservice:app --reload --host 0.0.0.0 --port 9000
CMD ["tail", "-f", "/dev/null"]

# Start the application uvicorn app.main:mcp --host 0.0.0.0 --port 8000
#CMD ["uvicorn", "app.webservice:app", "--host", "0.0.0.0", "--port", "9000"]