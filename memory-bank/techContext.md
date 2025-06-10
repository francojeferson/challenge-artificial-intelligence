# Tech Context

## Technologies Used / Recommended

- **Primary Stack**
  - Node.js 18+ (required)
  - Containerization for isolation and reproducibility (e.g., Docker)
- **Text & PDF Processing**
  - Node.js: pdf-parse, natural
  - Python (optional): spaCy, PyPDF2, pdfminer.six, textract
- **Video Transcription**
  - Node.js wrappers: OpenAI Whisper, Google Speech-to-Text API, Vosk
- **Image Metadata Extraction**
  - Node.js: sharp, exiftool-vendored
  - Python (optional): Pillow, ExifTool
- **Search & Indexing**
  - ElasticSearch (Node.js client), Pinecone (Node.js client), other JavaScript-based vector DBs
- **Prompt/Dialogue Engine**
  - LangChain.js, LlamaIndex.js, OpenAI API (Node.js integration)
- **General**
  - Modular, extensible codebase
  - All processing is local and privacy-respecting

## Development Setup

- Node.js 18+ (primary)
- Containerization required for isolation and reproducibility (e.g., Docker)
- package.json for dependency management
- Python 3.10+ (optional, for some resource adapters)

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
