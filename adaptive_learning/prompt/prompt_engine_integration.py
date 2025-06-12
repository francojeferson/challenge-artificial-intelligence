from typing import Dict, Any, Optional
from adaptive_learning.content_generation.content_generation_manager import (
    ContentGenerationManager,
)


class PromptEngineIntegration:
    def __init__(self):
        self.content_manager = ContentGenerationManager()

    def generate_adaptive_content(
        self,
        knowledge_gaps: Dict[str, Any],
        user_preferences: Dict[str, Any],
        content_snippets: Optional[list] = None,
    ) -> Any:
        """
        Generate adaptive content based on user knowledge gaps and preferences.

        :param knowledge_gaps: Dictionary describing user's knowledge gaps.
        :param user_preferences: Dictionary describing user's content format preferences.
        :param content_snippets: Optional list of content snippets retrieved from the index.
        :return: Generated content in the preferred format.
        """
        preferred_format = user_preferences.get("format", "text")
        additional_params = {}

        # For video format, optionally pass image paths if available in preferences
        if preferred_format == "video":
            additional_params["image_paths"] = user_preferences.get("image_paths", [])

        return self.content_manager.generate_content(
            knowledge_gaps, preferred_format, content_snippets, **additional_params
        )
