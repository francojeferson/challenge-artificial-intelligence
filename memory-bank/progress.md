# Progress for Adaptive Learning System

## What Works

- Resource ingestion and indexing across all types: text, PDF, image, and video, with a total of 15 resources
  successfully indexed in the latest run.
- Video transcription operational with the 'vosk-model-small-pt-0.3' model for Brazilian Portuguese content, confirmed
  by the latest run of 'run.py' in both local and Docker environments, loading the model from
  './vosk-model-small-pt-0.3'.
- Error handling for text processing to skip NLTK operations if required data is missing, ensuring ingestion continues.
- Audio conversion fallbacks in video ingestion using 'moviepy' when 'ffmpeg' is not directly available.
- Metadata extraction and storage even when content extraction fails, ensuring all resources are accounted for in the
  index.
- Updated Docker configuration to support containerized deployment, with resolved dependency issues for building the
  image, including copying the Vosk model and downloading NLTK data ('punkt_tab' and 'averaged_perceptron_tagger_eng')
  during the build process.
- Successful Docker image build and container run, confirming the application runs as expected in a containerized
  environment with all necessary resources available.
- Adaptive Prompt Engine Prototype (Milestone 3) implemented and integrated, enabling interactive user dialogue to
  assess knowledge gaps and deliver personalized content via 'prompt_engine.py' and an updated 'run.py'.
- Localized user interaction to Brazilian Portuguese (PT-BR), with prompts, responses, and interface text in
  'prompt_engine.py' and 'run.py' updated for a consistent language experience.
- Implemented a retry mechanism for temporary file deletion in 'video_ingestor.py', reducing the risk of disk space
  issues by attempting deletion multiple times before logging a warning.
- Confirmed the installation of the spaCy model 'en_core_web_sm', ensuring readiness for enhanced text processing
  without additional setup.
- Developed a web-based user interface using FastAPI and React, providing a conversational chat interface for adaptive
  learning.
- Integrated the React frontend build process into the Dockerfile, ensuring the web UI is built and served correctly in
  both local and containerized environments.
- Enhanced backend adaptive content generation logic to dynamically serve content from indexed resources in the
  'resources/' directory based on user input keywords.
- Updated project documentation with detailed setup and run instructions for both local and Docker environments,
  including frontend build and backend startup.

## What's Left to Build

- Conduct thorough testing of the system in both local and Docker environments to ensure smooth operation.
- Gather user feedback on the web UI usability and adaptive content relevance.
- Proceed with further enhancements to content generation and user interaction based on feedback.
- Finalize COMMENTS.md with architecture decisions, libraries used, improvements, and unmet requirements.
- Prepare repository for delivery as per project instructions.

## Current Status

- The system is fully operational for ingesting and indexing resources of all supported types, both locally and in a
  Docker container.
- Video transcription is active with the lightweight model 'vosk-model-small-pt-0.3' for Brazilian Portuguese.
- Adaptive Prompt Engine Prototype and web UI are implemented and integrated.
- Dockerfile updated to build and serve the React frontend with the FastAPI backend.
- Documentation updated to reflect local and Docker usage.

## Known Issues

- Temporary file deletion warnings during video ingestion due to file access conflicts are mitigated but may still
  appear.
- Alternative Vosk model fails to load due to CARPA file issues; current model is used.
- Some npm package deprecation warnings during frontend build; no critical impact.

## Evolution of Project Decisions

- Prioritized local, privacy-respecting processing with open-source tools.
- Shifted from CLI to web-based UI for better user experience.
- Integrated frontend build into Docker for consistent deployment.
- Adopted modular design and clear separation of concerns.
- Emphasized detailed documentation and iterative development.
