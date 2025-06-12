"""
Adaptive Prompt Engine for the Adaptive Learning System.

This module implements an interactive dialogue system to assess user knowledge gaps
and learning preferences. It generates dynamic prompts to identify user needs and
integrates with indexed educational resources to deliver personalized content.

The PromptEngine class serves as the core component for user interaction, maintaining
conversation context and adapting responses based on user feedback.
"""

from typing import Dict, List, Optional, Any
import logging

# Configure logging for the prompt engine
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptEngine:
    """
    A class to manage interactive user dialogue, assess knowledge gaps, and adapt content
    delivery based on user preferences and progress.

    Attributes:
        user_context (Dict[str, Any]): Stores user-specific data such as knowledge level,
            learning preferences, and conversation history.
        indexed_data (Optional[Dict]): Placeholder for indexed educational resources to
            retrieve relevant content (to be integrated with indexing module).
    """

    def __init__(self) -> None:
        """
        Initialize the PromptEngine with an empty user context and placeholder for indexed data.
        """
        self.user_context: Dict[str, Any] = {
            "knowledge_gaps": [],
            "preferred_format": "text",  # Default to text format
            "conversation_history": [],
            "progress": {},
        }
        self.indexed_data: Optional[Dict] = None
        logger.info("PromptEngine initialized with empty user context.")

    def set_indexed_data(self, index_manager: Any) -> None:
        """
        Set the IndexManager instance for content retrieval.

        Args:
            index_manager (Any): An instance of IndexManager to query indexed resources.
        """
        self.indexed_data = index_manager
        logger.info("IndexManager set for PromptEngine.")

    def assess_user_knowledge(self, user_input: str) -> List[str]:
        """
        Assess user knowledge gaps based on their input through dialogue.

        Args:
            user_input (str): The user's response or query.

        Returns:
            List[str]: A list of identified knowledge gaps or topics to address.
        """
        # Log user input for tracking
        self.user_context["conversation_history"].append(user_input)
        logger.info(f"User input received: {user_input}")

        # Placeholder logic for knowledge assessment
        # In a full implementation, this would use NLP techniques (e.g., LangChain, LlamaIndex)
        # to analyze user input for gaps in understanding.
        knowledge_gaps = []
        user_input_lower = user_input.lower()
        if any(
            term in user_input_lower
            for term in ["não entendo", "dificuldade", "ajuda", "preciso de ajuda"]
        ):
            knowledge_gaps.append("programming_basics")
            logger.info("Identified potential knowledge gap in programming basics.")
        elif any(
            term in user_input_lower
            for term in ["avançado", "complexo", "mais difícil"]
        ):
            knowledge_gaps.append("advanced_topics")
            logger.info("Identified interest in advanced topics.")

        self.user_context["knowledge_gaps"] = knowledge_gaps
        return knowledge_gaps

    def update_learning_preference(self, format_preference: str) -> None:
        """
        Update the user's preferred content format (text, video, audio).

        Args:
            format_preference (str): The user's preferred format for content delivery.
        """
        valid_formats = ["text", "video", "audio"]
        if format_preference.lower() in valid_formats:
            self.user_context["preferred_format"] = format_preference.lower()
            logger.info(
                f"Updated user learning preference to {format_preference.lower()}."
            )
        else:
            logger.warning(f"Invalid format {format_preference}; defaulting to text.")
            self.user_context["preferred_format"] = "text"

    def generate_prompt(self) -> str:
        """
        Generate a dynamic prompt based on the user's context and knowledge gaps.

        Returns:
            str: A tailored prompt or question to guide the user in Brazilian Portuguese.
        """
        gaps = self.user_context.get("knowledge_gaps", [])
        if not gaps:
            prompt = "Me conte sobre um conceito de programação com o qual você está tendo dificuldade ou gostaria de aprender mais."
        else:
            topic = gaps[-1]  # Focus on the most recent gap
            topic_translated = topic.replace("_", " ")
            if topic == "programming_basics":
                topic_translated = "fundamentos de programação"
            elif topic == "advanced_topics":
                topic_translated = "tópicos avançados"
            prompt = f"Notei que você pode precisar de ajuda com {topic_translated}. Pode me contar mais sobre o que acha desafiador?"

        logger.info(f"Generated prompt: {prompt}")
        self.user_context["conversation_history"].append(f"Prompt: {prompt}")
        return prompt

    def retrieve_content(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve relevant content from indexed data based on the topic or knowledge gap.

        Args:
            topic (str): The topic or knowledge gap to address.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing content details if available,
                otherwise None.
        """
        if self.indexed_data is None:
            logger.warning("No IndexManager available for content retrieval.")
            return None

        # Use IndexManager to search for relevant content
        # First try semantic search if available, otherwise fall back to keyword search
        results = []
        try:
            if hasattr(self.indexed_data, "search_by_similarity"):
                results = self.indexed_data.search_by_similarity(topic, k=1)
                logger.info(f"Performed semantic search for topic: {topic}")
        except Exception as e:
            logger.warning(f"Semantic search failed for {topic}: {str(e)}")

        if not results:
            results = self.indexed_data.search_by_keyword(topic)
            logger.info(f"Performed keyword search for topic: {topic}")

        if results:
            # Return the first matching result
            resource = results[0]
            logger.info(f"Retrieved content for topic: {topic}")
            return {
                "title": resource["metadata"].get("file_name", "Untitled"),
                "type": resource["metadata"].get("file_type", "text").lstrip("."),
                "content": resource.get("content", "Content not available."),
            }

        logger.warning(f"No content found for topic: {topic}")
        return None

    def adapt_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt the retrieved content to the user's preferred format and complexity level.

        Args:
            content (Dict[str, Any]): The raw content to adapt.

        Returns:
            Dict[str, Any]: The adapted content tailored to user preferences.
        """
        preferred_format = self.user_context.get("preferred_format", "text")
        adapted_content = content.copy()

        # Placeholder logic for content adaptation
        # In a full implementation, this would convert content between formats if needed.
        if adapted_content["type"] != preferred_format:
            logger.info(
                f"Adapting content from {adapted_content['type']} to {preferred_format}."
            )
            format_translation = {"text": "texto", "video": "vídeo", "audio": "áudio"}
            preferred_format_pt = format_translation.get(
                preferred_format, preferred_format
            )
            adapted_content["note"] = (
                f"Este conteúdo foi adaptado para o formato {preferred_format_pt} conforme sua preferência."
            )

        return adapted_content

    def process_user_interaction(self, user_input: str) -> Dict[str, Any]:
        """
        Process a full user interaction cycle: assess knowledge, generate prompt, and adapt content.

        Args:
            user_input (str): The user's input or response.

        Returns:
            Dict[str, Any]: A response dictionary containing the prompt and adapted content if available.
        """
        try:
            # Assess knowledge gaps based on input
            gaps = self.assess_user_knowledge(user_input)

            # Generate a relevant prompt
            prompt = self.generate_prompt()

            # Retrieve and adapt content if a specific gap is identified
            content = None
            if gaps:
                content_data = self.retrieve_content(gaps[-1])
                if content_data:
                    content = self.adapt_content(content_data)

            response = {
                "prompt": prompt,
                "content": (
                    content
                    if content
                    else "Ainda não encontrei conteúdo relevante. Vamos continuar conversando."
                ),
                "status": "success",
            }
            logger.info("User interaction processed successfully.")
            return response

        except Exception as e:
            logger.error(f"Error processing user interaction: {str(e)}")
            return {
                "prompt": "Estou tendo dificuldade para processar sua solicitação. Pode esclarecer o que precisa de ajuda?",
                "content": None,
                "status": "error",
                "error_message": str(e),
            }


if __name__ == "__main__":
    # Example usage of the PromptEngine
    from ..indexing.index_manager import IndexManager

    engine = PromptEngine()

    # Use real IndexManager for testing
    index_manager = IndexManager()
    engine.set_indexed_data(index_manager)

    # Simulate user interaction
    user_input = "I don't understand loops."
    engine.update_learning_preference("video")
    response = engine.process_user_interaction(user_input)
    print(f"Prompt: {response['prompt']}")
    if response["content"]:
        print(f"Content: {response['content']}")
