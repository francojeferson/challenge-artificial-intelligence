"""
run.py

Entry point script for the Adaptive Learning System.
This script integrates ingestion modules to process resources and builds an index for search functionality.
"""

import os
import sys
from adaptive_learning.ingestion.text_ingestor import ingest_text_directory
from adaptive_learning.ingestion.pdf_ingestor import ingest_pdf_directory
from adaptive_learning.ingestion.video_ingestor import ingest_video_directory
from adaptive_learning.ingestion.image_ingestor import ingest_image_directory
from adaptive_learning.indexing.index_manager import (
    build_index_from_resources,
    IndexManager,
)


def main():
    """
    Main function to ingest resources and build an index for the Adaptive Learning System.
    """
    resources_dir = "resources"
    all_resources = []

    print("Starting resource ingestion process...")

    # Ingest all types of resources from their respective directories
    text_dir = os.path.join(resources_dir, "text")
    if os.path.exists(text_dir) and len(os.listdir(text_dir)) > 0:
        text_data = ingest_text_directory(text_dir)
    else:
        # Check root resources directory for text files
        text_data = []
        for file in os.listdir(resources_dir):
            if file.endswith((".txt", ".json")):
                file_path = os.path.join(resources_dir, file)
                if os.path.isfile(file_path):
                    from adaptive_learning.ingestion.text_ingestor import (
                        ingest_text_file,
                    )

                    text_data.append(ingest_text_file(file_path))
    all_resources.extend(text_data)
    print(f"Ingested {len(text_data)} text resources.")

    pdf_dir = os.path.join(resources_dir, "pdf")
    if os.path.exists(pdf_dir) and len(os.listdir(pdf_dir)) > 0:
        pdf_data = ingest_pdf_directory(pdf_dir)
    else:
        # Check root resources directory for PDF files
        pdf_data = []
        for file in os.listdir(resources_dir):
            if file.endswith(".pdf"):
                file_path = os.path.join(resources_dir, file)
                if os.path.isfile(file_path):
                    from adaptive_learning.ingestion.pdf_ingestor import ingest_pdf_file

                    pdf_data.append(ingest_pdf_file(file_path))
    all_resources.extend(pdf_data)
    print(f"Ingested {len(pdf_data)} PDF resources.")

    video_dir = os.path.join(resources_dir, "video")
    if os.path.exists(video_dir) and len(os.listdir(video_dir)) > 0:
        video_data = ingest_video_directory(video_dir)
    else:
        # Check root resources directory for video files
        video_data = []
        for file in os.listdir(resources_dir):
            if file.endswith((".mp4", ".avi", ".mkv")):
                file_path = os.path.join(resources_dir, file)
                if os.path.isfile(file_path):
                    from adaptive_learning.ingestion.video_ingestor import (
                        ingest_video_file,
                    )

                    video_data.append(ingest_video_file(file_path))
    all_resources.extend(video_data)
    print(f"Ingested {len(video_data)} video resources.")

    image_dir = os.path.join(resources_dir, "image")
    if os.path.exists(image_dir) and len(os.listdir(image_dir)) > 0:
        image_data = ingest_image_directory(image_dir)
    else:
        # Check root resources directory for image files
        image_data = []
        for file in os.listdir(resources_dir):
            if file.endswith((".jpg", ".jpeg", ".png", ".bmp")):
                file_path = os.path.join(resources_dir, file)
                if os.path.isfile(file_path):
                    from adaptive_learning.ingestion.image_ingestor import (
                        ingest_image_file,
                    )

                    image_data.append(ingest_image_file(file_path))
    all_resources.extend(image_data)
    print(f"Ingested {len(image_data)} image resources.")

    # Build and save the index
    indexer = build_index_from_resources(all_resources, "index_data/simple_index.json")
    print(f"Total resources indexed: {len(indexer.get_all_resources())}")

    # Test search functionality
    test_keyword = "programming"
    search_results = indexer.search_by_keyword(test_keyword)
    print(f"\nSearch results for '{test_keyword}': {len(search_results)} matches.")
    for i, result in enumerate(search_results, 1):
        print(f"Result {i}:")
        print(f"  File: {result['metadata'].get('file_name', 'unknown')}")
        print(f"  Type: {result['metadata'].get('file_type', 'unknown')}")
        content_snippet = result.get("content", "")[:200]
        if content_snippet:
            print(f"  Content Snippet: {content_snippet}...")

    print("\nResource ingestion and indexing completed successfully.")

    # Initialize PromptEngine for user interaction
    from adaptive_learning.prompt.prompt_engine import PromptEngine

    engine = PromptEngine()
    engine.set_indexed_data(indexer)

    print("\nIniciando sessão interativa de aprendizado...")
    print("Você pode digitar 'sair' a qualquer momento para encerrar a sessão.")

    while True:
        user_input = input(
            "\nSobre o que você gostaria de aprender ou precisa de ajuda? "
        )
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando sessão interativa. Até logo!")
            break

        # Process user input through the prompt engine
        response = engine.process_user_interaction(user_input)
        print(f"\nPergunta: {response['prompt']}")
        if response["content"] and isinstance(response["content"], dict):
            print(f"Conteúdo: {response['content'].get('title', 'Sem título')}")
            print(f"Tipo: {response['content'].get('type', 'texto')}")
            content_snippet = response["content"].get(
                "content", "Conteúdo não disponível."
            )[:200]
            if content_snippet:
                print(f"Trecho do Conteúdo: {content_snippet}...")
            if "note" in response["content"]:
                print(f"Nota: {response['content']['note']}")
        else:
            print(f"Resposta: {response['content']}")


if __name__ == "__main__":
    main()
