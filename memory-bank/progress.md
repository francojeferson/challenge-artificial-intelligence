# Progress for Adaptive Learning System

## What Works

- Resource ingestion and indexing across all types: text, PDF, image, and video, with a total of 15 resources
  successfully indexed.
- Video transcription now operational with the 'vosk-model-small-pt-0.3' model for Brazilian Portuguese content,
  confirmed by the latest run of 'run.py' which loaded the model from './vosk-model-small-pt-0.3'.
- Error handling for text processing to skip NLTK operations if required data is missing, ensuring ingestion continues.
- Audio conversion fallbacks in video ingestion using 'moviepy' when 'ffmpeg' is not directly available.
- Metadata extraction and storage even when content extraction fails, ensuring all resources are accounted for in the
  index.
- Updated Docker configuration to support containerized deployment, with resolved dependency issues for building the
  image.

## What's Left to Build

- Investigation into the failure of the alternative model 'vosk-model-pt-fb-v0.1.1-20220516_2113' and potential testing
  of other models or configurations if transcription accuracy with the current model does not meet expectations.
- Resolution of non-critical warnings related to temporary file deletion during video processing to prevent potential
  disk space issues over time.
- Final testing of Docker image build and deployment to confirm all dependencies are correctly installed and the
  application runs as expected in a containerized environment.
- Further user-driven enhancements or feature additions based on feedback or evolving project requirements.

## Current Status

- The system is fully operational for ingesting and indexing resources of all supported types.
- Video transcription is active with the lightweight model 'vosk-model-small-pt-0.3' for Brazilian Portuguese, after an
  unsuccessful attempt to use 'vosk-model-pt-fb-v0.1.1-20220516_2113' which failed due to a model loading error.
- Docker setup has been updated to resolve build errors, with system dependencies and version specifications adjusted
  for compatibility.
- Minor warnings exist regarding temporary file access during video processing, but they do not impact core
  functionality.

## Known Issues

- Temporary file deletion warnings during video ingestion due to file access conflicts (e.g., "The process cannot access
  the file because it is being used by another process"). These are non-critical but should be monitored.
- NLTK processing errors due to missing data ('averaged_perceptron_tagger_eng'), though these are handled gracefully and
  do not prevent text ingestion.
- Failure to load the alternative Vosk model 'vosk-model-pt-fb-v0.1.1-20220516_2113' due to an error with the CARPA
  model file, necessitating a revert to 'vosk-model-small-pt-0.3'.

## Evolution of Project Decisions

- Initial setup focused on general resource ingestion without language-specific considerations for video content.
- User feedback revealed the need for Brazilian Portuguese transcription, leading to iterative updates of Vosk model
  recommendations from English to Portuguese models.
- Attempted to use 'vosk-model-pt-fb-v0.1.1-20220516_2113' for higher accuracy, but reverted to
  'vosk-model-small-pt-0.3' after the alternative model failed to load due to internal file structure issues.
- Finalized on 'vosk-model-small-pt-0.3' as the default after user confirmation of its presence in the workspace, with a
  path update to './vosk-model-small-pt-0.3' to ensure accessibility.
- Decision to prioritize local processing with Vosk for privacy, avoiding cloud-based transcription services.
- Adapted error handling and fallback mechanisms over time to ensure robustness across different system configurations
  (e.g., absence of 'ffmpeg').
- Iteratively updated Docker configuration and dependency specifications ('requirements.txt') to resolve build errors,
  adding necessary system libraries ('portaudio19-dev') and adjusting version ranges for compatibility with Python 3.8.
