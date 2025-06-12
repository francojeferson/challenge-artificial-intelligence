# Active Context for Adaptive Learning System

## Current Work Focus

- Developed and integrated the Adaptive Prompt Engine Prototype (Milestone 3) into the system, enabling interactive user
  dialogue to assess knowledge gaps and deliver personalized content.
- Localized the prompt engine and user interface in 'run.py' to support Brazilian Portuguese (PT-BR) interaction,
  aligning with user requirements for language-specific engagement.
- Resolved syntax errors and formatting issues in 'prompt_engine.py' to ensure the codebase is functional and ready for
  testing.
- Implemented a retry mechanism for temporary file deletion in 'video_ingestor.py' to address warnings during video
  processing, reducing the risk of disk space issues.
- Confirmed the installation of the spaCy model 'en_core_web_sm' for enhanced text processing, resolving any previous
  warnings about its absence.
- Developed a web-based user interface using FastAPI and React, providing a conversational chat interface for adaptive
  learning.
- Integrated the React frontend build process into the Dockerfile, ensuring the web UI is built and served correctly in
  both local and containerized environments.
- Enhanced backend adaptive content generation logic to dynamically serve content from indexed resources in the
  'resources/' directory based on user input keywords.
- Updated project documentation with detailed setup and run instructions for both local and Docker environments,
  including frontend build and backend startup.
- Fixed abstract class instantiation error by using ContentGenerationFactory to instantiate concrete content generators.
- Corrected method call in PromptEngine to use 'generate' instead of 'generate_content' for content adaptation.
- Improved content retrieval to handle empty or unavailable content gracefully.
- Verified smooth operation of run.py and web UI both locally and in Docker.
- Identified opportunity to improve knowledge gap classification and general query handling for better user experience.

## Recent Changes

- Created 'adaptive_learning/ui/web_app.py' implementing FastAPI backend serving the React frontend and handling
  adaptive content API requests.
- Scaffolded React frontend in 'adaptive_learning/ui/frontend' with chat interface components and build scripts.
- Updated Dockerfile to install Node.js, build React frontend, and serve it via FastAPI backend.
- Updated 'adaptive_learning/ui/README.md' with comprehensive instructions for running the system locally and in Docker.
- Updated run.py to instantiate appropriate content generator and integrate with PromptEngine correctly.
- Updated PromptEngine to fix content adaptation and retrieval logic.
- Updated Dockerfile to install pyttsx3 and its dependencies to fix module errors in Docker.
- Added fallback handling for empty content in PromptEngine.
- Updated Memory Bank files to reflect current project state and technical decisions.

## Next Steps

- Enhance knowledge gap assessment to better classify user inputs into specific topics.
- Improve content retrieval and indexing to provide meaningful responses for general queries.
- Add default fallback content for general queries to improve user experience.
- Conduct further testing and gather user feedback on the improved system.
- Continue updating Memory Bank and documentation as development progresses.

## Active Decisions and Considerations

- Prioritized a web-based UI using FastAPI and React for accessibility and modern user experience.
- Ensured all processing remains local and privacy-respecting, including video transcription and content generation.
- Adopted modular design patterns and clear separation of concerns for maintainability and extensibility.
- Integrated frontend build into Docker to streamline deployment and consistency across environments.
- Maintained detailed documentation and logging to support development and review.
- Recognized the need for improved knowledge gap classification and general query handling for better content relevance.

## Important Patterns and Preferences

- Modular architecture with distinct ingestion, indexing, prompt engine, content generation, and UI components.
- Use of keyword-based adaptive content generation as a starting point, with plans for more advanced NLP integration.
- Localization to Brazilian Portuguese for all user-facing text and interaction.
- Emphasis on iterative development with continuous feedback loops.

## Learnings and Project Insights

- Integrating React frontend build into Docker requires Node.js installation and careful file copying.
- Serving a React SPA via FastAPI is effective for combining backend logic and frontend UI in a single container.
- Keyword matching provides a simple but effective initial adaptive content approach, with room for future NLP
  enhancements.
- Detailed documentation and clear setup instructions are critical for smooth developer and user experience.
- Handling empty or unavailable content gracefully improves system robustness.
- Proper instantiation of concrete content generators is essential to avoid abstract class errors.
- System runs smoothly on both localhost and Docker with appropriate dependency management.
