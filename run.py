"""
run.py

Entry point script for the Adaptive Learning System.
This script imports and runs the main function from the adaptive_learning package.
"""

from adaptive_learning import AdaptiveLearningSystem


def main():
    """
    Main function to initialize and run the Adaptive Learning System.
    """
    system = AdaptiveLearningSystem()
    system.process_resources()

    # Test search functionality
    test_query = "learning"
    search_results = system.search_resources(test_query)
    for i, result in enumerate(search_results, 1):
        print(f"\nResult {i}:")
        print(f"  Filepath: {result.get('filepath')}")
        print(f"  Type: {result.get('type')}")
        text_snippet = result.get("text", result.get("transcript", ""))[:200]
        if text_snippet:
            print(f"  Text Snippet: {text_snippet}...")


if __name__ == "__main__":
    main()
