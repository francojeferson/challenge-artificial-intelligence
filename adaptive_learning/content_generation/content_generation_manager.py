from typing import Dict, Any, Optional
from adaptive_learning.content_generation.content_generator import (
    ContentGenerationFactory,
)


class ContentGenerationManager:
    def __init__(self):
        # Initialize any required state or configuration here
        pass

    def generate_content(
        self,
        knowledge_gaps: Dict[str, Any],
        preferred_format: str,
        content_snippets: Optional[list] = None,
        **kwargs
    ) -> Any:
        """
        Generate personalized learning content based on user knowledge gaps and preferences.

        :param knowledge_gaps: Dictionary describing user's knowledge gaps.
        :param preferred_format: Desired content format ('text', 'audio', 'video').
        :param content_snippets: Optional list of content snippets retrieved from the index.
        :param kwargs: Additional parameters for content generation (e.g., image paths for video).
        :return: Generated content in the specified format.
        """
        generator = ContentGenerationFactory.get_generator(preferred_format, **kwargs)
        return generator.generate(knowledge_gaps, content_snippets)
