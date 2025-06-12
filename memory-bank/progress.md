# Progress for Adaptive Learning System

## What Works

- Resource ingestion and indexing across all types: text, PDF, image, and video, with a total of 20 resources
  successfully indexed in the latest Docker container run.
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

## What's Left to Build

- Implementation of a robust solution for temporary file deletion warnings during video processing to prevent potential
  disk space issues over time, possibly through delayed deletion, retry mechanisms, or alternative file management
  strategies.
- Assessment of transcription accuracy for the current model 'vosk-model-small-pt-0.3' based on user feedback, with
  potential exploration of other Vosk models or configurations if accuracy is deemed insufficient.
- Resolution of the warning about the missing spaCy model 'en_core_web_sm' by updating the Dockerfile or requirements to
  include it, if deemed necessary for enhanced text processing.
- Development of the Content Generation Module (Milestone 4) to create dynamic, short-form content in multiple formats
  (text, video, audio) based on user preferences and indexed resources.
- Implementation of the User Interface (Milestone 5) for a more intuitive, conversational experience beyond the current
  command-line interaction.
- Integration and comprehensive testing of all system components (Milestone 6) to ensure seamless operation and
  alignment with PRD success criteria.
- Finalization of documentation (Milestone 7) and repository management for delivery (Milestone 8) as per project
  requirements.
- Further user-driven enhancements or feature additions based on feedback or evolving project requirements.

## Current Status

- The system is fully operational for ingesting and indexing resources of all supported types, both locally and in a
  Docker container.
- Video transcription is active with the lightweight model 'vosk-model-small-pt-0.3' for Brazilian Portuguese, after an
  unsuccessful attempt to use 'vosk-model-pt-fb-v0.1.1-20220516_2113' which failed due to a model loading error.
- Investigation confirmed that the alternative model 'vosk-model-pt-fb-v0.1.1-20220516_2113' fails to load with the
  error "ConstArpaLm <LmStates> section reading failed", indicating an issue with the CARPA model file.
- Docker setup has been updated to resolve build errors, with system dependencies, Vosk model, and NLTK data included,
  ensuring compatibility and functionality in isolated environments.
- Minor warnings exist regarding temporary file access during video processing, which do not impact core functionality
  but require further resolution.
- A warning about the missing spaCy model 'en_core_web_sm' persists, which may affect advanced text processing but does
  not prevent core operations.
- Adaptive Prompt Engine Prototype (Milestone 3) is complete, with user interaction now localized to Brazilian
  Portuguese, supporting PT-BR prompts, responses, and interface text for a culturally relevant experience.

## Known Issues

- Temporary file deletion warnings during video ingestion due to file access conflicts (e.g., "The process cannot access
  the file because it is being used by another process"). These are non-critical but should be addressed to prevent
  potential disk space issues.
- NLTK processing errors due to missing data ('averaged_perceptron_tagger_eng') are now resolved in the Docker
  environment by including the data during build, though this was an issue in earlier container runs.
- Failure to load the alternative Vosk model 'vosk-model-pt-fb-v0.1.1-20220516_2113' due to an error with the CARPA
  model file ("ConstArpaLm <LmStates> section reading failed"), necessitating continued use of
  'vosk-model-small-pt-0.3'.
- Warning about missing spaCy model 'en_core_web_sm', which does not prevent core functionality but may limit advanced
  text processing capabilities.

## Evolution of Project Decisions

- Initial setup focused on general resource ingestion without language-specific considerations for video content.
- User feedback revealed the need for Brazilian Portuguese transcription, leading to iterative updates of Vosk model
  recommendations from English to Portuguese models.
- Attempted to use 'vosk-model-pt-fb-v0.1.1-20220516_2113' for higher accuracy, but reverted to
  'vosk-model-small-pt-0.3' after the alternative model failed to load due to internal file structure issues.
- Finalized on 'vosk-model-small-pt-0.3' as the default after user confirmation of its presence in the workspace, with a
  path update to './vosk-model-small-pt-0.3' to ensure accessibility.
- Recent investigation confirmed the specific error with the alternative model as a CARPA file reading issue, deciding
  to stick with the current model unless transcription accuracy feedback necessitates further exploration.
- Decision to prioritize local processing with Vosk for privacy, avoiding cloud-based transcription services.
- Adapted error handling and fallback mechanisms over time to ensure robustness across different system configurations
  (e.g., absence of 'ffmpeg').
- Iteratively updated Docker configuration and dependency specifications ('requirements.txt') to resolve build errors,
  adding necessary system libraries ('portaudio19-dev') and adjusting version ranges for compatibility with Python 3.8.
- Enhanced error logging in 'video_ingestor.py' to diagnose model loading and temporary file issues, with ongoing
  efforts to address persistent file deletion warnings on Windows systems.
- Updated Dockerfile to include Vosk model and NLTK data, ensuring the containerized application runs with all required
  resources, confirmed by a successful container run that ingested and indexed all resources without critical errors.
- Developed and integrated the Adaptive Prompt Engine Prototype (Milestone 3), focusing on interactive user dialogue and
  content delivery, with a subsequent update to localize all user interaction to Brazilian Portuguese based on user
  request.
