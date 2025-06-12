"""
Text Ingestion Module

This module handles the ingestion of text-based resources (.txt, .json) for the Adaptive Learning System.
It processes the content using natural language processing libraries to extract meaningful data for indexing.

Key Responsibilities:
- Read and parse text files (.txt, .json).
- Extract metadata and content for indexing.
- Use NLP libraries (nltk, spaCy) for text processing.
- Ensure all processing is local and privacy-respecting.

Dependencies:
- nltk: For basic text processing and tokenization.
- spaCy: For advanced NLP tasks like entity recognition.
- json: For handling JSON formatted files.
"""

import os
import json
import nltk
import spacy
from typing import Dict, List, Any

# Download required NLTK data (local processing)
try:
    nltk.download("punkt", quiet=True)
    nltk.download("averaged_perceptron_tagger", quiet=True)
except Exception as e:
    print(
        f"Warning: Could not download NLTK data. Some text processing features may be limited. Error: {e}"
    )
# Check if NLTK data is available, otherwise set a flag to skip NLTK processing
try:
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("taggers/averaged_perceptron_tagger")
    nltk_available = True
except LookupError:
    print(f"Warning: NLTK data not found. Text processing with NLTK will be skipped.")
    nltk_available = False

# Load spaCy model (ensure it is installed locally)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print(
        "Warning: spaCy model 'en_core_web_sm' not found. Please install it using 'python -m spacy download en_core_web_sm'."
    )
    nlp = None


def ingest_text_file(file_path: str) -> Dict[str, Any]:
    """
    Ingest a single text file (.txt or .json) and extract its content and metadata.

    Args:
        file_path (str): Path to the text file.

    Returns:
        Dict[str, Any]: Dictionary containing metadata and processed content.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)
    content = ""
    metadata = {
        "file_name": file_name,
        "file_path": file_path,
        "file_type": file_extension,
        "size_bytes": os.path.getsize(file_path),
        "last_modified": os.path.getmtime(file_path),
        "resource_type": "text",
    }

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            if file_extension == ".json":
                data = json.load(file)
                content = json.dumps(data, ensure_ascii=False)
            else:  # .txt or other text formats
                content = file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        metadata["error"] = str(e)
        return {"metadata": metadata, "content": "", "processed_content": ""}

    # Process text content using NLTK and spaCy if available
    processed_data = process_text_content(content)
    metadata.update(processed_data.get("metadata", {}))

    return {
        "metadata": metadata,
        "content": content,
        "processed_content": processed_data.get("processed_content", content),
    }


def process_text_content(content: str) -> Dict[str, Any]:
    """
    Process text content using NLP tools to extract entities, keywords, and other metadata.

    Args:
        content (str): Raw text content to process.

    Returns:
        Dict[str, Any]: Dictionary with processed content and extracted metadata.
    """
    processed_content = content
    metadata = {}

    # Tokenization with NLTK if available
    if nltk_available:
        try:
            tokens = nltk.word_tokenize(content)
            pos_tags = nltk.pos_tag(tokens)
            metadata["token_count"] = len(tokens)
            metadata["pos_distribution"] = summarize_pos_tags(pos_tags)
        except Exception as e:
            print(f"Error processing text with NLTK: {e}")
            metadata["token_count"] = 0
            metadata["pos_distribution"] = {}
    else:
        metadata["token_count"] = 0
        metadata["pos_distribution"] = {}
        print("Skipping NLTK processing due to missing data.")

    # Entity recognition and keyword extraction with spaCy if available
    if nlp:
        try:
            doc = nlp(
                content[:10000]
            )  # Limit to first 10000 characters for performance
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            metadata["entities"] = entities[:50]  # Limit to first 50 entities

            # Extract keywords based on nouns and proper nouns
            keywords = [
                token.text
                for token in doc
                if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop
            ]
            metadata["keywords"] = list(
                set(keywords[:20])
            )  # Limit to top 20 unique keywords
        except Exception as e:
            print(f"Error processing text with spaCy: {e}")
            metadata["entities"] = []
            metadata["keywords"] = []
    else:
        metadata["entities"] = []
        metadata["keywords"] = []

    # Summarize content for longer texts
    if nltk_available:
        try:
            if len(content) > 500:  # Summarize if content is longer than 500 characters
                sentences = nltk.sent_tokenize(content)
                summary = " ".join(sentences[:3])  # Take first 3 sentences as summary
                metadata["summary"] = summary
            else:
                metadata["summary"] = content
        except Exception as e:
            print(f"Error summarizing content: {e}")
            metadata["summary"] = content[:200] if len(content) > 200 else content
    else:
        metadata["summary"] = content[:200] if len(content) > 200 else content
        print("Skipping content summarization due to missing NLTK data.")

    return {"processed_content": processed_content, "metadata": metadata}


def summarize_pos_tags(pos_tags: List[tuple]) -> Dict[str, int]:
    """
    Summarize the distribution of part-of-speech tags in the text.

    Args:
        pos_tags (List[tuple]): List of (word, pos_tag) tuples from NLTK.

    Returns:
        Dict[str, int]: Dictionary with POS tags as keys and their counts as values.
    """
    pos_distribution = {}
    for _, tag in pos_tags:
        pos_distribution[tag] = pos_distribution.get(tag, 0) + 1
    return pos_distribution


def ingest_text_directory(directory_path: str) -> List[Dict[str, Any]]:
    """
    Ingest all text files in a directory and its subdirectories.

    Args:
        directory_path (str): Path to the directory containing text files.

    Returns:
        List[Dict[str, Any]]: List of dictionaries with metadata and content for each file.
    """
    text_data = []
    supported_extensions = (".txt", ".json")

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(supported_extensions):
                file_path = os.path.join(root, file)
                data = ingest_text_file(file_path)
                if data:
                    text_data.append(data)

    return text_data


if __name__ == "__main__":
    # Example usage for testing
    sample_dir = "../../resources/text"
    if os.path.exists(sample_dir):
        text_resources = ingest_text_directory(sample_dir)
        print(f"Ingested {len(text_resources)} text resources.")
        for resource in text_resources:
            print(
                f"File: {resource['metadata']['file_name']}, Tokens: {resource['metadata'].get('token_count', 0)}"
            )
    else:
        print(f"Sample directory {sample_dir} not found.")
