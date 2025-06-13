# COMMENTS.md

## Architecture Decisions

- Adopted a modular architecture with clear separation of concerns among ingestion, indexing, prompt engine, content
  generation, and UI components to ensure extensibility and maintainability.
- Used design patterns such as Pipeline, Adapter, Strategy, and Factory across modules to support flexible handling of
  resource types and content adaptation strategies.
- Prioritized local processing for all content generation, transcription, and data handling tasks to ensure user privacy
  and data security, aligning with project non-functional requirements.
- Integrated a web-based UI using FastAPI for the backend and React for the frontend, providing a conversational
  interface that integrates dynamically with the `PromptEngine` for adaptive content delivery.
- Enhanced the `PromptEngine` with NLP capabilities using spaCy for deeper semantic analysis of user input, improving
  knowledge gap assessment and topic classification.
- Implemented an expanded fallback mechanism in content retrieval to ensure meaningful responses for general queries and
  specific topics, enhancing user experience.
- Enhanced the feedback mechanism in the web UI to capture user format preferences and improved error handling for
  feedback logging, ensuring robust user input collection for continuous improvement.

## Third-Party Libraries Used

- **pyttsx3**: Local text-to-speech synthesis for audio content generation.
- **moviepy**: Video creation and editing for dynamic content output.
- **spaCy**: Natural language processing for tokenization and semantic analysis in knowledge gap assessment.
- **Vosk**: Offline speech recognition for video transcription, using the 'vosk-model-small-pt-0.3' model for Brazilian
  Portuguese content.
- **PyPDF2, pdfminer.six**: PDF parsing for text extraction from educational resources.
- **nltk**: Text processing for tokenization and basic NLP tasks.
- **Pillow, exifread**: Image metadata extraction for indexing visual content.
- **FastAPI**: Backend framework for serving the web UI and handling API requests for user interaction.
- **React (via frontend integration)**: Frontend framework for creating an intuitive, conversational user interface.

## Improvements for Future Work

- Enhance the Content Generation Module with advanced natural language generation models (e.g., via integration with
  frameworks like LangChain or LlamaIndex) for more nuanced and context-aware content.
- Improve video content generation by incorporating dynamic slides or animations to make visual learning materials more
  engaging.
- Explore alternative or improved speech recognition models for better transcription accuracy, potentially testing other
  Vosk models or OpenAI Whisper if feasible within local processing constraints.
- Optimize performance for large datasets and concurrent users by implementing more efficient indexing solutions like
  Elasticsearch or Pinecone for semantic search.
- Add more comprehensive unit and integration tests to cover edge cases and ensure robustness across all system
  components.
- Implement user session management in the web app to maintain conversation context across multiple interactions,
  improving personalization.

## Unmet Mandatory Requirements

- The web UI (Milestone 5) is fully implemented using FastAPI for the backend and React for the frontend, integrated
  with the Prompt Engine for dynamic content delivery, and operational on both localhost and Docker environments.
  Features like session persistence via localStorage, user preference selection for content format, and an enhanced
  feedback mechanism are now fully integrated, completing this milestone for the current phase.
- Comprehensive end-to-end testing (Milestone 6) is advanced with updated integration tests for both the message and
  feedback API endpoints in 'test_integration.py', with 7 tests now covering core functionality and user interaction;
  additional testing for UI responsiveness and content adaptation accuracy across diverse scenarios is deferred to
  future iterations due to time constraints.
- Final repository management and delivery steps (Milestone 8) remain to be completed as per project instructions for
  forking, pushing, and notifying the recruiter, marking the final project submission phase.

This document will be updated as the project progresses.
