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
    gcc \
    g++ \
    python3-dev \
    ffmpeg \
    libsndfile1 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY adaptive_learning ./adaptive_learning
COPY run.py ./run.py
COPY resources ./resources
COPY index_data ./index_data
COPY vosk-model-small-pt-0.3 ./vosk-model-small-pt-0.3

# Download NLTK data to a specific directory with permissions
RUN mkdir -p /home/appuser/nltk_data && \
    python -m nltk.downloader -d /home/appuser/nltk_data punkt_tab averaged_perceptron_tagger_eng && \
    chown -R appuser:appuser /home/appuser/nltk_data

# Ensure Vosk model permissions
RUN chown -R appuser:appuser /home/appuser/vosk-model-small-pt-0.3

# Set permissions
RUN chown -R appuser:appuser /home/appuser
USER appuser

# Command to run the application
CMD ["python3", "run.py"]
