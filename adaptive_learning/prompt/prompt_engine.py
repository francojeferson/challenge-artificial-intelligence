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
        Assess user knowledge gaps based on their input through dialogue with enhanced topic classification.
        Utilizes NLP techniques with spaCy for deeper semantic analysis if available.

        Args:
            user_input (str): The user's response or query.

        Returns:
            List[str]: A list of identified knowledge gaps or topics to address, prioritized by relevance.
        """
        # Log user input for tracking
        self.user_context["conversation_history"].append(user_input)
        logger.info(f"User input received: {user_input}")

        # Maintain existing knowledge gaps if input doesn't clearly indicate a new topic
        current_gaps = self.user_context.get("knowledge_gaps", [])
        knowledge_gaps = current_gaps.copy()  # Preserve context by default

        user_input_lower = user_input.lower()
        # Check for affirmative responses to continue previous topic
        affirmative_responses = [
            "sim",
            "yes",
            "claro",
            "ok",
            "certo",
            "entendi",
            "continuar",
            "mais",
        ]
        if (
            any(resp in user_input_lower for resp in affirmative_responses)
            and current_gaps
            and current_gaps[-1] != "general_query"
        ):
            logger.info(
                "User provided affirmative response; retaining current knowledge gaps."
            )
            return current_gaps

        # Expanded logic for knowledge assessment to handle varied inputs with categorized indicators
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
            "básico",
            "começar",
            "iniciante",
            "aprendendo",
            "novo nisso",
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
            "expert",
            "dominar",
            "aprofundar",
        ]
        debugging_indicators = [
            "erro",
            "bug",
            "problema",
            "não funciona",
            "travou",
            "falha",
            "crash",
            "depurar",
            "debug",
            "corrigir",
            "resolver",
        ]
        project_indicators = [
            "projeto",
            "aplicação",
            "app",
            "desenvolver",
            "criar",
            "construir",
            "implementar",
            "sistema",
            "software",
            "programa",
        ]

        # Initialize a dictionary to score potential topics based on indicators
        topic_scores: Dict[str, int] = {
            "programming_basics": 0,
            "advanced_topics": 0,
            "debugging": 0,
            "project_development": 0,
        }

        # Score based on indicator matches
        if any(term in user_input_lower for term in basic_indicators):
            topic_scores["programming_basics"] += 2
            logger.info("Identified potential knowledge gap in programming basics.")
        if any(term in user_input_lower for term in advanced_indicators):
            topic_scores["advanced_topics"] += 2
            logger.info("Identified interest in advanced topics.")
        if any(term in user_input_lower for term in debugging_indicators):
            topic_scores["debugging"] += 2
            logger.info("Identified potential debugging or error resolution need.")
        if any(term in user_input_lower for term in project_indicators):
            topic_scores["project_development"] += 2
            logger.info("Identified interest in project or application development.")

        # Expanded list of specific programming topics with categorization
        programming_topics = {
            "control_structures": [
                "loop",
                "loops",
                "laço",
                "while",
                "for",
                "if",
                "else",
                "condicional",
                "switch",
                "case",
                "repetição",
            ],
            "functions": [
                "função",
                "function",
                "método",
                "method",
                "procedimento",
                "chamar",
                "retornar",
                "return",
            ],
            "variables": [
                "variável",
                "variable",
                "valor",
                "atribuir",
                "declarar",
                "constante",
                "const",
                "let",
                "var",
            ],
            "data_structures": [
                "array",
                "lista",
                "objeto",
                "dicionário",
                "dictionary",
                "tupla",
                "tuple",
                "set",
                "estrutura",
                "dados",
            ],
            "oop": [
                "classe",
                "class",
                "objeto",
                "herança",
                "inheritance",
                "polimorfismo",
                "encapsulamento",
                "instância",
            ],
            "algorithms": [
                "algoritmo",
                "algorithm",
                "ordenar",
                "sort",
                "buscar",
                "search",
                "recursão",
                "recursion",
                "complexidade",
            ],
            "coding": [
                "programação",
                "coding",
                "código",
                "code",
                "escrever código",
                "programar",
                "desenvolvimento",
            ],
            "html": [
                "html",
                "html5",
                "web",
                "página",
                "site",
                "estrutura web",
                "markup",
                "tags",
                "hipertexto",
            ],
        }

        # Score specific topics
        for category, terms in programming_topics.items():
            if any(term in user_input_lower for term in terms):
                if category not in topic_scores:
                    topic_scores[category] = 0
                topic_scores[category] += 3  # Higher weight for specific topics
                logger.info(f"Identified specific topic category: {category}")

        # Direct topic match for single-word inputs or clear topic references
        for category in programming_topics.keys():
            if user_input_lower.strip() == category.lower():
                if category not in topic_scores:
                    topic_scores[category] = 0
                topic_scores[category] += 5  # Highest weight for direct match
                logger.info(f"Direct topic match identified: {category}")

        # Attempt to use spaCy for deeper NLP analysis if available
        try:
            import spacy

            nlp = spacy.load("en_core_web_sm")
            doc = nlp(user_input)
            # Analyze for specific entities or concepts that might indicate a topic
            for token in doc:
                if (
                    token.pos_ in ["NOUN", "PROPN"]
                    and token.text.lower() in user_input_lower
                ):
                    for category, terms in programming_topics.items():
                        if token.text.lower() in terms:
                            if category not in topic_scores:
                                topic_scores[category] = 0
                            topic_scores[
                                category
                            ] += 4  # Even higher weight for NLP-detected terms
                            logger.info(
                                f"NLP identified specific topic via token: {category}"
                            )
            # Check for dependency patterns indicating questions or confusion
            for token in doc:
                if token.dep_ == "ROOT" and token.text.lower() in [
                    "understand",
                    "know",
                    "get",
                    "learn",
                    "explain",
                ]:
                    topic_scores["programming_basics"] += 1
                    logger.info(
                        "NLP identified potential confusion or learning intent."
                    )
        except ImportError:
            logger.warning(
                "spaCy not available for NLP analysis; relying on keyword matching."
            )
        except Exception as e:
            logger.warning(
                f"spaCy processing failed: {str(e)}; falling back to keyword analysis."
            )

        # Determine the most relevant topics based on scores
        prioritized_gaps = []
        for topic, score in topic_scores.items():
            if score > 0:
                prioritized_gaps.append((topic, score))

        # Sort by score in descending order to prioritize highly relevant topics
        prioritized_gaps.sort(key=lambda x: x[1], reverse=True)
        new_gaps = [gap[0] for gap in prioritized_gaps]

        if new_gaps:
            knowledge_gaps = new_gaps
            logger.info(f"Prioritized knowledge gaps based on input: {knowledge_gaps}")
        else:
            # If no specific topic or indicator, retain current gaps to avoid resetting
            if current_gaps:
                logger.info(
                    "No new knowledge gaps identified; retaining current context."
                )
            else:
                knowledge_gaps = ["general_query"]
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
            elif topic == "functions":
                topic_translated = "função"
            elif topic == "control_structures":
                topic_translated = "estruturas de controle"
            elif topic == "variables":
                topic_translated = "variáveis"
            elif topic == "data_structures":
                topic_translated = "estruturas de dados"
            elif topic == "oop":
                topic_translated = "programação orientada a objetos"
            elif topic == "algorithms":
                topic_translated = "algoritmos"
            elif topic == "coding":
                topic_translated = "programação"
            elif topic == "debugging":
                topic_translated = "depuração"
            elif topic == "project_development":
                topic_translated = "desenvolvimento de projetos"
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
        Includes expanded fallback mechanisms for general queries and specific topics to ensure meaningful responses.

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
                results = self.indexed_data.search_by_similarity(
                    topic, k=5
                )  # Increased to get more potential matches
                logger.info(
                    f"Performed semantic search for topic: {topic}, found {len(results)} results."
                )
        except Exception as e:
            logger.warning(f"Semantic search failed for {topic}: {str(e)}")

        if not results:
            results = self.indexed_data.search_by_keyword(topic)
            logger.info(
                f"Performed keyword search for topic: {topic}, found {len(results)} results."
            )

        if results:
            # Return the first matching result with valid content
            for resource in results:
                content = resource.get("content", None)
                if content and content != "Content not available.":
                    logger.info(f"Retrieved content for topic: {topic}")
                    return {
                        "title": resource["metadata"].get("file_name", "Untitled"),
                        "type": resource["metadata"]
                        .get("file_type", "text")
                        .lstrip("."),
                        "content": content,
                    }
            logger.warning(f"Content is empty or unavailable for topic: {topic}")
            # If no valid content found in results, proceed to fallback

        # Expanded fallback mechanism for both general queries and specific topics
        fallback_topics = []
        if topic == "general_query":
            fallback_topics = [
                "programming_basics",
                "fundamentals",
                "introduction",
                "basics",
                "coding",
                "programação",
                "html",
                "web",
            ]
            logger.info("Using fallback for general query.")
        else:
            # For specific topics, try related broader terms and synonyms as fallback
            fallback_mapping = {
                "control_structures": [
                    "programming_basics",
                    "coding",
                    "loops",
                    "if",
                    "while",
                    "for",
                ],
                "functions": ["programming_basics", "coding", "método", "function"],
                "variables": ["programming_basics", "coding", "valor", "variable"],
                "data_structures": [
                    "programming_basics",
                    "advanced_topics",
                    "array",
                    "lista",
                    "objeto",
                ],
                "oop": [
                    "advanced_topics",
                    "programming_basics",
                    "classe",
                    "objeto",
                    "herança",
                ],
                "algorithms": [
                    "advanced_topics",
                    "programming_basics",
                    "algoritmo",
                    "ordenar",
                    "buscar",
                ],
                "debugging": [
                    "programming_basics",
                    "coding",
                    "erro",
                    "bug",
                    "problema",
                ],
                "project_development": [
                    "coding",
                    "programming_basics",
                    "projeto",
                    "aplicação",
                    "app",
                ],
                "advanced_topics": [
                    "coding",
                    "programming_basics",
                    "complexo",
                    "avançado",
                ],
                "programming_basics": [
                    "coding",
                    "introduction",
                    "básico",
                    "fundamentos",
                    "programação",
                ],
                "coding": ["programming_basics", "introduction", "código", "programar"],
                "html": ["web", "programming_basics", "página", "site", "estrutura"],
                "loops": [
                    "control_structures",
                    "programming_basics",
                    "laço",
                    "repetição",
                    "while",
                    "for",
                ],
            }
            fallback_topics = fallback_mapping.get(
                topic.lower(),
                [
                    "programming_basics",
                    "coding",
                    "introduction",
                    "básico",
                    "fundamentos",
                ],
            )
            logger.info(
                f"Using fallback for specific topic: {topic} with terms: {fallback_topics}"
            )

        # Iterate through fallback topics to find any relevant content
        for fallback in fallback_topics:
            results = self.indexed_data.search_by_keyword(fallback)
            logger.info(
                f"Fallback search for '{fallback}' returned {len(results)} results."
            )
            if results:
                for resource in results:
                    content = resource.get("content", None)
                    if content and content != "Content not available.":
                        logger.info(f"Retrieved fallback content using: {fallback}")
                        return {
                            "title": resource["metadata"].get("file_name", "Untitled"),
                            "type": resource["metadata"]
                            .get("file_type", "text")
                            .lstrip("."),
                            "content": content,
                        }
        logger.warning(
            f"No fallback content found for topic: {topic} after trying all fallbacks."
        )
        return None

    def adapt_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt the retrieved content to the user's preferred format and complexity level.
        Summarizes content using local NLP tools for concise, human-friendly responses.

        Args:
            content (Dict[str, Any]): The raw content to adapt.

        Returns:
            Dict[str, Any]: The adapted content tailored to user preferences.
        """
        topic = content.get("title", "unknown topic")
        raw_content = content.get("content", "")
        logger.info(f"Adapting content for topic: {topic}")

        # Attempt to summarize content using local NLP processing with spaCy
        summary = self._summarize_content(raw_content, topic)
        if summary:
            content["content"] = summary
        else:
            # Fallback to a concise message if summarization fails
            content["content"] = (
                f"Este material aborda {topic}. É um conteúdo rico que pode ajudar no seu aprendizado. Quer saber algo específico sobre isso?"
            )

        return content

    def _summarize_content(self, raw_content: str, topic: str) -> Optional[str]:
        """
        Summarize raw content using local NLP tools like spaCy to extract key insights.
        Ensures responses are concise (max 50 words) and focus on wisdom.

        Args:
            raw_content (str): The raw content to summarize.
            topic (str): The topic of the content.

        Returns:
            Optional[str]: A summarized paragraph if successful, otherwise None.
        """
        try:
            import spacy
            import json

            # Check if content is JSON format (common in exercise data)
            try:
                data = json.loads(raw_content)
                # Extract meaningful fields if available
                name = data.get("name", "")
                title = data.get("title", "")
                desc = data.get("description", "")
                key_info = name or title or desc
                if key_info:
                    summary = f"Este recurso sobre {topic} aborda '{key_info}'. É um material útil para aprender. Quer saber mais detalhes?"
                    logger.info(f"Extracted summary from JSON content for {topic}.")
                    return summary
            except json.JSONDecodeError:
                pass  # Not JSON, proceed with text summarization

            nlp = spacy.load("en_core_web_sm")
            doc = nlp(raw_content[:1000])  # Limit to first 1000 chars for performance

            # Extract key sentences or phrases based on importance (e.g., first few sentences)
            sentences = [
                sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10
            ]
            if sentences:
                # Take the first meaningful sentence or key idea, limit to ~50 words
                key_idea = sentences[0].split()[:30]  # Approx 30 words
                key_idea_text = " ".join(key_idea)
                summary = f"Este conteúdo sobre {topic} destaca que {key_idea_text}... Quer aprofundar nisso?"
                logger.info(f"Successfully summarized content for {topic} using spaCy.")
                return summary

            logger.warning(f"No meaningful sentences extracted for {topic}.")
            return None
        except ImportError:
            logger.warning("spaCy not available for summarization; using fallback.")
            return None
        except Exception as e:
            logger.error(f"Error summarizing content for {topic}: {str(e)}")
            return None

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
            if gaps and gaps[-1] != "general_query":
                content_data = self.retrieve_content(gaps[-1])
                if content_data:
                    content = self.adapt_content(content_data)

            response = {
                "prompt": prompt,
                "content": (
                    content
                    if content
                    else {
                        "title": "Introdução à Programação",
                        "type": "text",
                        "content": "Não encontrei conteúdo específico agora. Programação é fascinante! Posso te guiar em fundamentos como variáveis e loops, ou em temas avançados. O que você quer aprender?",
                    }
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
