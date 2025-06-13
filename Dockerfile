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
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install uvicorn fastapi && python -m spacy download en_core_web_sm

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

# Install Node.js and npm for building React frontend
USER root
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install pyttsx3 dependencies and pyttsx3 itself
RUN apt-get update && apt-get install -y espeak libespeak1 libespeak-dev && \
    pip install pyttsx3

# Build React frontend
COPY adaptive_learning/ui/frontend ./adaptive_learning/ui/frontend
WORKDIR /home/appuser/adaptive_learning/ui/frontend
RUN npm install && npm run build

# Change back to app root
WORKDIR /home/appuser
USER appuser

# Command to run the FastAPI web app serving the React frontend
CMD ["uvicorn", "adaptive_learning.ui.web_app:app", "--host", "0.0.0.0", "--port", "8000"]
