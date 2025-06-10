# Tech Context

## Technologies Used / Recommended

- **Text & PDF Processing**
  - Python: spaCy, PyPDF2, pdfminer.six, textract
  - Node.js: pdf-parse, natural
- **Video Transcription**
  - Speech-to-text: OpenAI Whisper, Google Speech-to-Text API, Vosk
- **Image Metadata Extraction**
  - Python: Pillow, ExifTool
  - Node.js: sharp, exiftool-vendored
- **Search & Indexing**
  - ElasticSearch, Whoosh, or vector databases (e.g., FAISS, Pinecone)
- **Prompt/Dialogue Engine**
  - Python: LangChain, OpenAI API, LlamaIndex
  - Node.js: LangChain.js, LlamaIndex.js
- **General**
  - Modular, extensible codebase
  - Local processing preferred for privacy

## Development Setup

- Python 3.10+ or Node.js 18+
- Virtual environment or containerization recommended
- Requirements.txt or package.json for dependency management

## Technical Constraints

- All data processing must be local (no external data sharing)
- Code must be well-organized, documented, and maintainable
- Efficient handling of large and diverse datasets

## Tool Usage Patterns

- Use adapters for each resource type to standardize ingestion and indexing
- Employ semantic and keyword search for flexible retrieval
- Integrate prompt engine with indexed data for dynamic content generation

## Dependencies

- List all third-party libraries in COMMENTS.md
- Ensure all dependencies are open-source and compatible with project requirements
