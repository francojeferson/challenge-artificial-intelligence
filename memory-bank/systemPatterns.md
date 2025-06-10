# System Patterns

## System Architecture

- **Data Ingestion**

  - Text: Direct parsing and indexing of .txt and .json files.
  - PDF: Text extraction using OCR or PDF parsers.
  - Video: Audio transcription (speech-to-text) and metadata extraction.
  - Image: Metadata and tag extraction.

- **Indexing & Search**

  - All resources indexed for keyword and semantic search.
  - Support for efficient retrieval by type, topic, and relevance.

- **Adaptive Prompt Engine**

  - Interactive dialogue system to assess user knowledge and preferences.
  - Identifies knowledge gaps and learning styles.
  - Generates dynamic, short-form content in multiple formats (text, video, audio).

- **Content Generation**

  - Uses indexed data to create personalized learning content.
  - Adapts content format and complexity to user needs.

- **Modularity**
  - Clear separation of concerns: ingestion, indexing, retrieval, prompt logic, and content generation.
  - Extensible to support new resource types or learning strategies.

## Design Patterns

- **Pipeline Pattern** for data ingestion and processing.
- **Adapter Pattern** for handling different resource types (text, PDF, video, image).
- **Strategy Pattern** for selecting content generation and adaptation strategies.
- **Factory Pattern** for prompt and content generation modules.
- **Separation of Concerns** throughout all components.

## Component Relationships

- Ingestion feeds into indexing.
- Indexing supports search and retrieval.
- Prompt engine interacts with user, queries index, and triggers content generation.
- Content generation delivers output to user interface.

## Critical Implementation Paths

- Accurate extraction and indexing of all resource types.
- Fast, relevant search and retrieval.
- Robust, adaptive prompt logic for user assessment and content delivery.
