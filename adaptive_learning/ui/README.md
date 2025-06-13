# Adaptive Learning Web UI

This directory contains the React frontend for the Adaptive Learning System.

## Setup and Build

1. Navigate to this directory:

```bash
cd adaptive_learning/ui/frontend
```

2. Install dependencies:

```bash
npm install
```

3. Build the React app:

```bash
npm run build
```

This will create a production build in the `build/` directory.

## Running the Web UI

The FastAPI backend (`adaptive_learning/ui/web_app.py`) serves the built React app, now fully integrated with features
like session persistence, user preference selection for content format, and feedback mechanisms.

### Locally

1. Ensure the React app is built:

```bash
cd adaptive_learning/ui/frontend
npm install
npm run build
cd ../../..
```

2. Run the FastAPI backend:

```bash
uvicorn adaptive_learning.ui.web_app:app --reload
```

3. Open your browser and navigate to `http://localhost:8000` to access the web UI with all integrated features.

### Using Docker

1. Build the Docker image:

```bash
docker build -t adaptive-learning-system .
```

2. Run the Docker container:

```bash
docker run -it --rm -p 8000:8000 adaptive-learning-system
```

3. Open your browser and navigate to `http://localhost:8000` to access the web UI.

## Running the CLI Ingestion and Interactive Session

Alternatively, you can run the CLI-based ingestion and interactive learning session using `run.py`:

### Locally

```bash
python run.py
```

### Using Docker

```bash
docker run -it --rm adaptive-learning-system python run.py
```

## Notes

- The backend API endpoint `/api/message` handles user messages and returns adaptive content responses.
- The frontend communicates with the backend to provide a conversational interface.
