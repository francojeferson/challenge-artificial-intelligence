# User Interface Module for Adaptive Learning System

## Overview

This module provides the user interface (UI) for the adaptive learning system, enabling users to interact with the
system through a conversational web interface. The UI is designed to be intuitive, responsive, and adaptive to user
preferences, delivering personalized learning content based on identified knowledge gaps.

## Purpose

The UI module serves as the primary interaction point for users, facilitating:

- Conversational dialogue to assess user knowledge and preferences.
- Delivery of dynamic, format-adapted content (text, video, audio) based on user needs.
- Collection of user feedback to continuously improve the learning experience.
- Session persistence to maintain user context across interactions.

## Architecture

The UI module is built using a modern web stack, ensuring scalability and ease of integration with the backend
components of the adaptive learning system.

### Components

- **Backend (FastAPI)**:

  - Located in `web_app.py`, the FastAPI server handles API requests for user messages and feedback.
  - Integrates with the `PromptEngine` to process user input and generate relevant content.
  - Supports server-side persistence for user preferences in `user_preferences.json`, complementing client-side storage
    for robust session management.
  - Logs feedback to `feedback_log.json` for analysis and system improvement.

- **Frontend (React)**:
  - Located in `frontend/src/App.js`, the React application provides a conversational chat interface.
  - Uses localStorage for client-side persistence of chat history, user ID, and format preferences (text, video, audio).
  - Features a feedback form to capture multi-dimensional user ratings (general, relevance, effectiveness), enhancing
    user input collection.
  - Implements responsive design for accessibility across devices.

### Integration with Other Modules

- **Prompt Engine**: The UI backend (`web_app.py`) communicates with the `PromptEngine` (`prompt_engine.py`) to process
  user interactions and retrieve or generate adaptive content based on indexed data.
- **Content Generation**: Content is dynamically formatted by the `ContentGenerationFactory` based on user preferences,
  which are captured and stored via the UI.
- **Indexing**: Indexed data from the `IndexManager` is accessed through the `PromptEngine` to ensure content relevance,
  with the UI serving as the delivery mechanism.

## Usage

### Running the UI Locally

1. **Prerequisites**:

   - Ensure Python 3.8+ is installed on your system.
   - Install dependencies listed in `requirements.txt` using `pip install -r requirements.txt`.

2. **Start the Backend Server**:

   - Run the FastAPI server with: `uvicorn adaptive_learning.ui.web_app:app --reload`.
   - The server will start on `http://localhost:8000`, serving the React frontend and API endpoints.

3. **Access the Interface**:
   - Open a web browser and navigate to `http://localhost:8000`.
   - Interact with the chat interface to send messages, select content format preferences, and provide feedback.

### Running in Docker

1. **Build and Run**:

   - From the project root, build the Docker image: `docker build -t adaptive-learning-system .`.
   - Run a container: `docker run -d -p 8000:8000 --name adaptive-learning-container adaptive-learning-system`.
   - Access the UI at `http://localhost:8000` in your browser.

2. **Stop the Container**:
   - Stop with `docker stop adaptive-learning-container` and remove with `docker rm adaptive-learning-container`.

## Key Features

- **Conversational Interface**: Users can engage in a dialogue with the system, which assesses knowledge gaps and
  delivers tailored content through a chat-like experience in Brazilian Portuguese.
- **Format Preference Selection**: Users can choose their preferred content format (text, video, audio), with selections
  persisted both client-side (localStorage) and server-side (`user_preferences.json`).
- **Session Persistence**: Maintains user context across sessions using localStorage for chat history and user ID,
  backed by server-side storage for reliability.
- **Enhanced Feedback Mechanism**: Collects detailed user feedback with multi-dimensional ratings (general, relevance,
  effectiveness) to refine content delivery and system performance.
- **Responsive Design**: Ensures accessibility and usability across different devices and screen sizes.

## API Endpoints

- **GET /**: Serves the React frontend application (`index.html`).
- **POST /api/message**: Processes user messages, integrates with the `PromptEngine` to generate responses, and respects
  user format preferences with server-side persistence.
- **POST /api/feedback**: Logs user feedback to `feedback_log.json` and updates user preferences in
  `user_preferences.json` for future interactions.

## Future Improvements

- Implement advanced feedback analysis tools or visualizations to systematically review user ratings and improve content
  relevance.
- Enhance UI with visual cues or animations for a more engaging user experience, particularly for video content
  delivery.
- Explore real-time content adaptation indicators to show users how the system is tailoring content to their needs
  during interactions.
- Optimize server-side storage for scalability, potentially integrating a lightweight database for handling larger user
  bases or more complex session data.

## Troubleshooting

- **Server Not Starting**: Ensure all dependencies are installed (`pip install -r requirements.txt`) and that port 8000
  is not in use. Check terminal logs for specific errors.
- **UI Not Loading**: Verify that the React build files are present in `frontend/build`. If missing, rebuild the
  frontend or ensure the correct path in `web_app.py`.
- **Content Not Adapting**: Confirm that the `PromptEngine` and `ContentGenerationFactory` are correctly integrated and
  that user preferences are being passed to the backend.
- **Feedback Not Saving**: Check write permissions for `feedback_log.json` and `user_preferences.json` in the project
  directory.

This README provides a comprehensive guide to the UI module, ensuring users and developers can effectively interact with
and maintain the adaptive learning system.
