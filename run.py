"""
run.py

Entry point script for the Adaptive Learning System.
This script integrates ingestion modules to process resources, builds an index for search functionality,
and provides options for command-line or web-based user interaction.
"""

import os
import sys
import logging
from adaptive_learning.ingestion.text_ingestor import ingest_text_directory
from adaptive_learning.ingestion.pdf_ingestor import ingest_pdf_directory
from adaptive_learning.ingestion.video_ingestor import ingest_video_directory
from adaptive_learning.ingestion.image_ingestor import ingest_image_directory
from adaptive_learning.indexing.index_manager import (
    build_index_from_resources,
    IndexManager,
)

# Configure logging for the main script
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to ingest resources, build an index for the Adaptive Learning System,
    and start user interaction either via CLI or web UI.
    """
    resources_dir = "resources"
    all_resources = []

    logger.info("Starting resource ingestion process...")

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
    logger.info(f"Ingested {len(text_data)} text resources.")

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
    logger.info(f"Ingested {len(pdf_data)} PDF resources.")

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
    logger.info(f"Ingested {len(video_data)} video resources.")

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
    logger.info(f"Ingested {len(image_data)} image resources.")

    # Build and save the index with error handling
    try:
        indexer = build_index_from_resources(
            all_resources, "index_data/simple_index.json"
        )
        logger.info(f"Total resources indexed: {len(indexer.get_all_resources())}")
    except Exception as e:
        logger.error(f"Error building index: {str(e)}")
        sys.exit(1)

    # Test search functionality
    test_keyword = "programming"
    try:
        search_results = indexer.search_by_keyword(test_keyword)
        logger.info(
            f"Search results for '{test_keyword}': {len(search_results)} matches."
        )
        for i, result in enumerate(search_results, 1):
            logger.info(f"Result {i}:")
            logger.info(f"  File: {result['metadata'].get('file_name', 'unknown')}")
            logger.info(f"  Type: {result['metadata'].get('file_type', 'unknown')}")
            content_snippet = result.get("content", "")[:200]
            if content_snippet:
                logger.info(f"  Content Snippet: {content_snippet}...")
    except Exception as e:
        logger.error(f"Error testing search functionality: {str(e)}")

    logger.info("Resource ingestion and indexing completed successfully.")

    # Initialize PromptEngine for user interaction
    from adaptive_learning.prompt.prompt_engine import PromptEngine
    from adaptive_learning.content_generation.content_generator import (
        ContentGenerationFactory,
    )

    engine = PromptEngine()
    # Use ContentGenerationFactory to get a TextGenerator instance as default
    content_generator = ContentGenerationFactory.get_generator("text")
    engine.content_generator = content_generator
    engine.set_indexed_data(indexer)

    # Provide option for CLI interaction or starting the web UI
    import argparse

    parser = argparse.ArgumentParser(description="Run the Adaptive Learning System")
    parser.add_argument(
        "--web",
        action="store_true",
        help="Start the web UI server instead of CLI interaction",
    )
    args = parser.parse_args()

    if args.web:
        logger.info("Starting web UI server with FastAPI...")
        try:
            import uvicorn
            from adaptive_learning.ui.web_app import app

            logger.info("Web UI server starting at http://127.0.0.1:8000/")
            uvicorn.run(app, host="127.0.0.1", port=8000)
        except ImportError:
            logger.error(
                "Uvicorn not installed. Please install it with 'pip install uvicorn' to run the web UI."
            )
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error starting web UI server: {str(e)}")
            sys.exit(1)
    else:
        logger.info("Iniciando sessão interativa de aprendizado via CLI...")
        logger.info(
            "Você pode digitar 'sair' a qualquer momento para encerrar a sessão."
        )

        while True:
            user_input = input(
                "\nSobre o que você gostaria de aprender ou precisa de ajuda? "
            )
            if user_input.lower() in ["sair", "exit", "quit"]:
                logger.info("Encerrando sessão interativa. Até logo!")
                break

            try:
                # Process user input through the prompt engine
                response = engine.process_user_interaction(user_input)
                print(f"\nPergunta: {response['prompt']}")
                if response["content"] and isinstance(response["content"], dict):
                    print(f"Conteúdo: {response['content'].get('title', 'Sem título')}")
                    print(f"Formato: {response['content'].get('format', 'texto')}")
                    print(
                        f"Fonte: {response['content'].get('source', 'Fonte desconhecida')}"
                    )
                    content_text = response["content"].get(
                        "content", "Conteúdo não disponível."
                    )
                    if content_text:
                        print(f"Conteúdo Gerado: {content_text}")
                    if "note" in response["content"]:
                        print(f"Nota: {response['content']['note']}")
                else:
                    print(f"Resposta: {response['content']}")
            except Exception as e:
                logger.error(f"Error processing user input: {str(e)}")
                print("Ops, algo deu errado. Por favor, tente novamente.")


if __name__ == "__main__":
    main()
