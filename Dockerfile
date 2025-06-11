# Dockerfile for Adaptive Learning System

FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user for security
RUN useradd -m appuser
WORKDIR /home/appuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY adaptive_learning ./adaptive_learning

# Set permissions
RUN chown -R appuser:appuser /home/appuser
USER appuser

CMD ["python3"]
