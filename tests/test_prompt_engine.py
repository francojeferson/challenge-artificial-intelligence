"""
Unit tests for the PromptEngine class to validate user interaction processing,
knowledge gap assessment, and content adaptation.
"""

import unittest
import logging
import sys
import os

# Configure logging for the test
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to the path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from adaptive_learning.prompt.prompt_engine import PromptEngine
from adaptive_learning.indexing.index_manager import IndexManager


class TestPromptEngine(unittest.TestCase):
    def setUp(self):
        """Set up the PromptEngine instance before each test."""
        self.engine = PromptEngine()
        # Set a dummy IndexManager or None for testing
        index_manager = IndexManager()
        self.engine.set_indexed_data(index_manager)
        logger.info("Test setup complete with PromptEngine initialized.")

    def test_assess_user_knowledge_basic(self):
        """Test knowledge gap assessment for basic programming concepts."""
        user_input = "I don't understand loops."
        gaps = self.engine.assess_user_knowledge(user_input)
        self.assertTrue(
            any(
                "control_structures" in gap or "programming_basics" in gap
                for gap in gaps
            ),
            "Should identify control structures or basics as a knowledge gap.",
        )
        logger.info("Test for basic knowledge gap assessment passed.")

    def test_assess_user_knowledge_advanced(self):
        """Test knowledge gap assessment for advanced topics."""
        user_input = "I want to learn advanced algorithms."
        gaps = self.engine.assess_user_knowledge(user_input)
        self.assertTrue(
            any("advanced_topics" in gap or "algorithms" in gap for gap in gaps),
            "Should identify advanced topics or algorithms as a knowledge gap.",
        )
        logger.info("Test for advanced knowledge gap assessment passed.")

    def test_generate_prompt_basic(self):
        """Test prompt generation for basic knowledge gaps."""
        self.engine.user_context["knowledge_gaps"] = ["programming_basics"]
        prompt = self.engine.generate_prompt()
        self.assertIn(
            "fundamentos de programação",
            prompt,
            "Prompt should mention fundamentals of programming.",
        )
        logger.info("Test for basic prompt generation passed.")

    def test_generate_prompt_general(self):
        """Test prompt generation for general queries."""
        self.engine.user_context["knowledge_gaps"] = ["general_query"]
        prompt = self.engine.generate_prompt()
        self.assertIn(
            "tema de programação",
            prompt,
            "Prompt should ask about general programming topics.",
        )
        logger.info("Test for general prompt generation passed.")

    def test_process_user_interaction(self):
        """Test full user interaction cycle with a specific input."""
        user_input = "I need help with functions."
        response = self.engine.process_user_interaction(user_input)
        self.assertEqual(
            response["status"], "success", "Interaction should process successfully."
        )
        self.assertIn(
            "função", response["prompt"].lower(), "Prompt should mention functions."
        )
        self.assertTrue(
            response["content"], "Should return content or fallback response."
        )
        logger.info("Test for full user interaction passed.")

    def test_update_learning_preference(self):
        """Test updating user learning preference."""
        self.engine.update_learning_preference("video")
        self.assertEqual(
            self.engine.user_context["preferred_format"],
            "video",
            "Preferred format should be updated to video.",
        )
        logger.info("Test for learning preference update passed.")


if __name__ == "__main__":
    unittest.main()
