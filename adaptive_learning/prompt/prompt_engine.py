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
from ..content_generation.content_generator import ContentGenerator

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
        self.content_generator: Optional[ContentGenerator] = None
        logger.info("PromptEngine initialized with empty user context.")

    def set_indexed_data(self, index_manager: Any) -> None:
        """
        Set the IndexManager instance for content retrieval and initialize ContentGenerator.

        Args:
            index_manager (Any): An instance of IndexManager to query indexed resources.
        """
        self.indexed_data = index_manager
        # Do not instantiate ContentGenerator here; it should be set externally
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

        # Maintain existing knowledge gaps if input doesn't clearly indicate a new topic
        current_gaps = self.user_context.get("knowledge_gaps", [])
        knowledge_gaps = current_gaps.copy()  # Preserve context by default

        user_input_lower = user_input.lower()
        # Expanded logic for knowledge assessment to handle varied inputs
        # In a full implementation, this would use advanced NLP techniques locally
        basic_indicators = [
            "não entendo",
            "dificuldade",
            "ajuda",
            "preciso de ajuda",
            "não sei",
            "confuso",
            "dúvida",
            "explicar",
            "o que é",
            "como funciona",
        ]
        advanced_indicators = [
            "avançado",
            "complexo",
            "mais difícil",
            "profundo",
            "detalhe",
            "específico",
            "avançar",
            "próximo nível",
        ]

        if any(term in user_input_lower for term in basic_indicators):
            if "programming_basics" not in knowledge_gaps:
                knowledge_gaps.append("programming_basics")
            logger.info("Identified potential knowledge gap in programming basics.")
        elif any(term in user_input_lower for term in advanced_indicators):
            if "advanced_topics" not in knowledge_gaps:
                knowledge_gaps.append("advanced_topics")
            logger.info("Identified interest in advanced topics.")
        else:
            # Extract potential topics from input to maintain conversation flow
            programming_topics = [
                "loop",
                "laço",
                "função",
                "function",
                "variável",
                "variable",
                "condicional",
                "if",
                "else",
                "while",
                "for",
                "array",
                "lista",
                "objeto",
                "classe",
                "class",
                "método",
                "method",
                "algoritmo",
                "programação",
                "coding",
                "código",
                "code",
            ]
            for topic in programming_topics:
                if topic in user_input_lower:
                    if topic not in knowledge_gaps:
                        knowledge_gaps.append(topic)
                    logger.info(f"Identified specific topic: {topic}")
                    break
            # If no specific topic or indicator, retain current gaps to avoid resetting
            if not knowledge_gaps and current_gaps:
                logger.info(
                    "No new knowledge gaps identified; retaining current context."
                )
            elif not knowledge_gaps:
                knowledge_gaps.append("general_query")
                logger.info(
                    "No specific knowledge gap identified; treating as general query."
                )

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
        if not gaps or "general_query" in gaps:
            prompt = "Oi! Sobre qual tema de programação você gostaria de conversar ou tem dúvidas? Estou aqui pra te ajudar!"
        else:
            topic = gaps[-1]  # Focus on the most recent gap
            topic_translated = topic.replace("_", " ")
            if topic == "programming_basics":
                topic_translated = "fundamentos de programação"
            elif topic == "advanced_topics":
                topic_translated = "tópicos mais avançados"
            elif topic == "general_query":
                topic_translated = "esse tema"
            else:
                topic_translated = topic  # Use the specific topic identified
            # Vary the prompt based on conversation history to avoid repetition
            history = self.user_context.get("conversation_history", [])
            if len(history) > 2 and "Prompt" in history[-2]:
                prompt = f"Entendi, ainda sobre {topic_translated}, tem algo mais específico que tá te preocupando ou outra dúvida relacionada?"
            else:
                prompt = f"Ei, parece que você tá precisando de uma mãozinha com {topic_translated}. O que tá pegando? Me explica um pouco mais pra eu te ajudar da melhor forma!"

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
            content = resource.get("content", None)
            if content is None or content == "Content not available.":
                logger.warning(f"Content is empty or unavailable for topic: {topic}")
                return None
            return {
                "title": resource["metadata"].get("file_name", "Untitled"),
                "type": resource["metadata"].get("file_type", "text").lstrip("."),
                "content": content,
            }

        logger.warning(f"No content found for topic: {topic}")
        return None

    def adapt_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt the retrieved content to the user's preferred format and complexity level using ContentGenerator.

        Args:
            content (Dict[str, Any]): The raw content to adapt.

        Returns:
            Dict[str, Any]: The adapted content tailored to user preferences.
        """
        if self.content_generator is None:
            logger.warning("No ContentGenerator available for content adaptation.")
            return content

        topic = content.get("title", "unknown topic")
        # Use the correct method name 'generate' instead of 'generate_content'
        adapted_content = self.content_generator.generate(
            self.user_context.get("knowledge_gaps", {}), [content.get("content", "")]
        )
        if adapted_content is None:
            logger.warning(f"Failed to generate adapted content for topic: {topic}")
            return content

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
                    else "Hmm, ainda não achei um conteúdo que se encaixe perfeitamente. Que tal a gente continuar conversando pra eu entender melhor o que você precisa?"
                ),
                "status": "success",
            }
            logger.info("User interaction processed successfully.")
            return response

        except Exception as e:
            logger.error(f"Error processing user interaction: {str(e)}")
            return {
                "prompt": "Ops, tô com um pouco de dificuldade pra entender o que você precisa. Pode explicar de novo ou dar mais detalhes sobre o que tá te confundindo?",
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
