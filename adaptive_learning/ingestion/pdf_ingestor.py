"""
PDF Ingestion Module

This module handles the ingestion of PDF resources for the Adaptive Learning System.
It extracts text content from PDFs using PDF parsing libraries for indexing.

Key Responsibilities:
- Read and parse PDF files to extract text content.
- Extract metadata from PDF files for indexing.
- Use PDF parsing libraries (PyPDF2, pdfminer.six) for text extraction.
- Ensure all processing is local and privacy-respecting.

Dependencies:
- PyPDF2: For basic PDF text extraction.
- pdfminer.six: For advanced PDF text extraction with layout preservation.
"""

import os
from typing import Dict, List, Any
import PyPDF2
from pdfminer.high_level import extract_text


def ingest_pdf_file(file_path: str) -> Dict[str, Any]:
    """
    Ingest a single PDF file and extract its content and metadata.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        Dict[str, Any]: Dictionary containing metadata and extracted content.
    """
    file_name = os.path.basename(file_path)
    content = ""
    metadata = {
        "file_name": file_name,
        "file_path": file_path,
        "file_type": ".pdf",
        "size_bytes": os.path.getsize(file_path),
        "last_modified": os.path.getmtime(file_path),
        "page_count": 0,
    }

    try:
        # First attempt with PyPDF2 for basic metadata and text extraction
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            metadata["page_count"] = len(reader.pages)
            if "/Title" in reader.metadata:
                metadata["title"] = reader.metadata.get("/Title", "")
            if "/Author" in reader.metadata:
                metadata["author"] = reader.metadata.get("/Author", "")
            # Extract text from first few pages as a fallback
            content_fallback = ""
            for i in range(min(3, len(reader.pages))):
                content_fallback += reader.pages[i].extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF metadata with PyPDF2 for {file_path}: {e}")
        content_fallback = ""

    try:
        # Use pdfminer.six for more accurate text extraction
        content = extract_text(file_path)
        if not content.strip():
            content = content_fallback  # Fallback to PyPDF2 content if pdfminer fails
    except Exception as e:
        print(f"Error extracting text with pdfminer for {file_path}: {e}")
        content = content_fallback if content_fallback else ""

    if not content:
        print(f"Warning: No content extracted from {file_path}")
        return {}

    return {"metadata": metadata, "content": content, "processed_content": content}


def ingest_pdf_directory(directory_path: str) -> List[Dict[str, Any]]:
    """
    Ingest all PDF files in a directory and its subdirectories.

    Args:
        directory_path (str): Path to the directory containing PDF files.

    Returns:
        List[Dict[str, Any]]: List of dictionaries with metadata and content for each file.
    """
    pdf_data = []
    supported_extension = ".pdf"

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(supported_extension):
                file_path = os.path.join(root, file)
                data = ingest_pdf_file(file_path)
                if data:
                    pdf_data.append(data)

    return pdf_data


if __name__ == "__main__":
    # Example usage for testing
    sample_dir = "../../resources/pdf"
    if os.path.exists(sample_dir):
        pdf_resources = ingest_pdf_directory(sample_dir)
        print(f"Ingested {len(pdf_resources)} PDF resources.")
        for resource in pdf_resources:
            print(
                f"File: {resource['metadata']['file_name']}, Pages: {resource['metadata'].get('page_count', 0)}"
            )
    else:
        print(f"Sample directory {sample_dir} not found.")
