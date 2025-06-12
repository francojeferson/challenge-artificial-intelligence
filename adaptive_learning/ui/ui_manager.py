from typing import Dict, Any, Optional
from adaptive_learning.prompt.prompt_engine_integration import PromptEngineIntegration


class UIManager:
    def __init__(self):
        self.prompt_integration = PromptEngineIntegration()

    def start_interaction(self):
        print("Bem-vindo ao Sistema de Aprendizagem Adaptativa!")
        user_preferences = self.get_user_preferences()
        while True:
            user_input = input(
                "Por favor, informe sua dúvida ou área de dificuldade (ou 'sair' para encerrar): "
            )
            if user_input.lower() == "sair":
                print("Obrigado por usar o sistema. Até logo!")
                break

            knowledge_gaps = self.assess_knowledge_gaps(user_input)
            content_snippets = self.retrieve_relevant_content(knowledge_gaps)
            generated_content = self.prompt_integration.generate_adaptive_content(
                knowledge_gaps, user_preferences, content_snippets
            )
            self.deliver_content(generated_content, user_preferences)

    def get_user_preferences(self) -> Dict[str, Any]:
        print("Selecione o formato de conteúdo preferido:")
        print("1. Texto")
        print("2. Áudio")
        print("3. Vídeo")
        choice = input("Digite o número correspondente ao formato: ")
        format_map = {"1": "text", "2": "audio", "3": "video"}
        preferred_format = format_map.get(choice, "text")
        return {"format": preferred_format}

    def assess_knowledge_gaps(self, user_input: str) -> Dict[str, Any]:
        # Placeholder: In a real system, analyze user input to identify knowledge gaps
        return {"topic": user_input}

    def retrieve_relevant_content(
        self, knowledge_gaps: Dict[str, Any]
    ) -> Optional[list]:
        # Placeholder: Query the indexing system to retrieve relevant content snippets
        # For now, return a dummy list
        return [f"Conteúdo relevante para o tópico: {knowledge_gaps.get('topic', '')}"]

    def deliver_content(self, content: Any, user_preferences: Dict[str, Any]):
        preferred_format = user_preferences.get("format", "text")
        if preferred_format == "text":
            print("\nConteúdo gerado:\n")
            print(content)
        elif preferred_format == "audio":
            print(f"\nÁudio gerado no arquivo: {content}")
            # Optionally, play the audio file using a suitable library
        elif preferred_format == "video":
            print(f"\nVídeo gerado no arquivo: {content}")
            # Optionally, play the video file using a suitable library
