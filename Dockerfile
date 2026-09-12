# Use a lightweight official Python runtime
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies and supervisor for multi-process management
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code, model artifacts, api, and app directory
COPY source/ ./source/
COPY api/ ./api/
COPY models/ ./models/
COPY app/ ./app/
COPY tests/ ./tests/

# Copy supervisor configuration file to container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose Render's required web port (10000 for Streamlit) 
# and FastAPI's internal port (8000)
EXPOSE 10000 8000

# Run supervisor to manage both FastAPI and Streamlit processes
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]