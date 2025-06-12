from adaptive_learning.ingestion import *
from adaptive_learning.indexing import *
from adaptive_learning.prompt import *
from adaptive_learning.content_generation import *
from adaptive_learning.ui.ui_manager import UIManager


class IntegrationManager:
    def __init__(self):
        self.ui_manager = UIManager()
        # Initialize other components as needed, e.g., ingestion, indexing, prompt engine

    def run(self):
        # Start the user interaction loop
        self.ui_manager.start_interaction()

        # Additional integration logic can be added here for ingestion, indexing, etc.


if __name__ == "__main__":
    manager = IntegrationManager()
    manager.run()
