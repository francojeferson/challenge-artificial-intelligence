# Tech Context

## Technologies Used / Recommended

- **Primary Stack**
  - Python 3.8+ (required)
  - Containerization for isolation and reproducibility (e.g., Docker)
- **Text & PDF Processing**
  - PyPDF2, pdfminer.six, nltk, spaCy, textract
- **Video Transcription**
  - OpenAI Whisper (Python), Google Speech-to-Text API (Python client), Vosk (Python, using 'vosk-model-small-pt-0.3'
    for Brazilian Portuguese content)
- **Image Metadata Extraction**
  - Pillow, exifread
- **Search & Indexing**
  - Elasticsearch (Python client), Pinecone (Python client), other Python-based vector DBs
- **Prompt/Dialogue Engine**
  - LangChain, LlamaIndex, OpenAI API (Python integration)
- **General**
  - Modular, extensible codebase
  - All processing is local and privacy-respecting

## Development Setup

- Python 3.8+ (primary)
- Containerization required for isolation and reproducibility (e.g., Docker)
- Docker setup includes system dependencies: build-essential, gcc, g++, python3-dev, ffmpeg, libsndfile1,
  portaudio19-dev
- requirements.txt or poetry for dependency management

## Technical Constraints

- All data processing must be local (no external data sharing)
- Code must be well-organized, documented, and maintainable
- Efficient handling of large and diverse datasets
- Codebase must be modular, extensible, and maintainable
- Use only open-source, compatible dependencies

## Tool Usage Patterns

- Use adapters for each resource type to standardize ingestion and indexing
- Employ semantic and keyword search for flexible retrieval
- Integrate prompt engine with indexed data for dynamic content generation

## Dependencies

- List all third-party libraries in COMMENTS.md
- Ensure all dependencies are open-source and compatible with project requirements

## Documentation Requirements

- Maintain up-to-date documentation (including COMMENTS.md) covering:
  - Architecture
  - Libraries and dependencies
  - Design decisions
  - Improvements and unmet requirements
- Documentation must be traceable to PRD success criteria and non-functional requirements
