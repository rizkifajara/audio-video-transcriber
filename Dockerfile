# Use Python 3.11 with Ubuntu base for better compatibility with FFmpeg
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for input, output, and models
RUN mkdir -p /app/input /app/output /app/models

# Set permissions
RUN chmod +x /app/*.py

# Default command
CMD ["python", "example_usage.py"] 