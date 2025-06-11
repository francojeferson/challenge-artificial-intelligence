# COMMENTS.md

## Architecture Overview

The Adaptive Learning System is designed with a modular architecture to ensure extensibility and maintainability,
following a pipeline pattern for data flow through distinct components:

- **Resource Ingestion**: This module uses adapters for each resource type (text, PDF, video, image) to standardize the
  ingestion process. Each adapter handles specific formats and extracts content and metadata, which are then passed to
  the indexing module. Recent updates have enhanced content extraction techniques, such as OCR for scanned PDFs and
  improved metadata extraction for images and videos.
- **Indexing & Search**: The indexing module, recently introduced with index_manager.py, builds an efficient search
  index from ingested resources. It supports both keyword and semantic search to enable relevant resource retrieval,
  forming the foundation for adaptive content delivery.
- **Adaptive Prompt Engine**: (In development) This component will interact with users to assess knowledge gaps and
  learning preferences through a conversational interface, querying the index to retrieve relevant content.
- **Content Generation**: (In development) This module will dynamically create personalized learning content based on
  user needs, adapting format and complexity as required.
- **User Interface**: (In development) The UI will provide an intuitive, conversational experience for users,
  facilitating interaction with the prompt engine and delivery of adaptive content.

Data flows from ingestion to indexing, then to the prompt engine and content generation, and finally to the user
interface, with continuous feedback loops to adapt to user interactions. All processing is local to ensure privacy, and
the system is containerized for isolation and reproducibility.

## Libraries and Dependencies

The following third-party libraries and dependencies are used in the project, as reflected in the updated
requirements.txt:

- **Core Data Processing**:
  - **numpy (>=1.21.0)**: For numerical operations and data handling.
  - **pandas (>=1.3.0)**: For structured data manipulation and analysis.
- **Text Processing**:
  - **nltk (>=3.6.2)**: For natural language processing tasks like tokenization and summarization.
  - **spacy (>=3.1.0)**: For advanced NLP tasks including entity recognition and keyword extraction.
- **PDF Processing**:
  - **PyPDF2 (>=2.0.0)**: For reading PDF metadata and basic text extraction.
  - **pdfminer.six (>=20201018)**: For accurate text extraction from PDFs.
  - **pdf2image (>=1.16.0)**: For converting PDF pages to images for OCR.
  - **pytesseract (>=0.3.8)**: For OCR on scanned PDFs to extract text from images.
- **Video Processing**:
  - **moviepy (>=1.0.3)**: For video manipulation and audio extraction.
  - **whisper (>=20230124)**: For audio transcription from videos using models like 'small' and 'base' for local
    processing.
- **Image Processing**:
  - **Pillow (>=8.3.1)**: For image metadata extraction and manipulation.
  - **exifread (>=2.3.2)**: For detailed EXIF data extraction from images.
- **Indexing and Search**:
  - **faiss-cpu (>=1.7.2)**: For efficient similarity search and indexing of resources.
  - **sentence-transformers (>=2.2.0)**: For generating semantic embeddings to support advanced search capabilities.
- **General Utilities**:
  - **json (>=2.0.9)**, **os (>=0.1.0)**, **tempfile (>=0.1.0)**, **typing (>=3.7.4.3)**, **datetime (>=4.3)**: Standard
    Python libraries for file handling, temporary file management, type hints, and date/time operations.

All dependencies are open-source and compatible with the project's non-functional requirements for local processing and
privacy.

## Design Decisions

- **Modular Architecture**: The system is designed with clear separation of concerns, using adapter patterns for
  ingestion and strategy patterns for future content generation. This ensures extensibility for new resource types and
  learning strategies.
- **Enhanced Ingestion Modules**: Recent updates to ingestion modules prioritize improved content extraction, such as
  OCR fallback for scanned PDFs, timestamped transcription segments for videos, and inferred tags from filenames and
  directories for images. These decisions enhance the richness of metadata and content available for indexing.
- **Local Processing**: All data processing, including transcription and content generation, is performed locally to
  adhere to privacy requirements. Libraries like Whisper are chosen for their ability to run offline.
- **Python 3.8+**: Selected as the primary language for its robust ecosystem of libraries and support for modern
  programming paradigms, aligning with the PRD's technical constraints.
- **Indexing Foundation**: The introduction of index_manager.py focuses on building a simple yet efficient index for
  resource retrieval, setting the stage for semantic search and adaptive content delivery in later phases.
- **Documentation Enforcement**: Documentation is treated as a core workflow, ensuring traceability to PRD success
  criteria and maintaining up-to-date records of architecture and decisions.

## Improvements

- **Ingestion Optimization**: Further optimize ingestion processes for large datasets, potentially integrating parallel
  processing to handle bulk resources efficiently.
- **Advanced Search Capabilities**: Enhance the indexing module with semantic search using embeddings from
  sentence-transformers to improve relevance in resource retrieval.
- **Adaptive Prompt Engine**: Develop the prompt engine with iterative testing to refine user knowledge assessment
  accuracy, incorporating user feedback loops.
- **User Interface Development**: Create a responsive, conversational UI that supports multiple content formats (text,
  video, audio) for a seamless learning experience.
- **Performance Tuning**: Address potential performance bottlenecks with large datasets by exploring more efficient
  indexing solutions or caching strategies.
- **Additional Resource Types**: Plan for extensibility to support new formats like audio-only files or interactive web
  content by adding new ingestion adapters.

## Unmet Requirements

- **Adaptive Prompt Engine**: Not yet implemented. This requires prototyping to assess user knowledge gaps and generate
  dynamic content. Planned for the next development phase with libraries like LangChain or LlamaIndex.
- **Content Generation Module**: Currently unmet. This module will depend on the prompt engine and indexed data to
  create personalized content, adapting to user preferences. Development is scheduled after the prompt engine prototype.
- **User Interface**: Not yet developed. An intuitive, conversational interface is required to deliver adaptive content
  and gather user feedback. This will be addressed after core backend components are complete.
- **Integration & Testing**: Full system integration and testing are pending until all modules (ingestion, indexing,
  prompt engine, content generation, UI) are implemented. This will ensure all components work cohesively to meet PRD
  success criteria.
- **Documentation Finalization**: While initial documentation is in place, finalization (including comprehensive
  architecture details and unmet requirements in COMMENTS.md) will occur after all functional components are complete.

These unmet requirements are tracked with planned mitigation through phased development, focusing first on completing
backend modules before moving to user-facing components and final integration.
