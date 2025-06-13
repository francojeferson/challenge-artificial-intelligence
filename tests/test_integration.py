import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from adaptive_learning.integration.integration_manager import IntegrationManager
from adaptive_learning.ui.web_app import app


class TestIntegrationManager(unittest.TestCase):
    @patch("adaptive_learning.ui.ui_manager.UIManager.start_interaction")
    def test_run_starts_ui_interaction(self, mock_start_interaction):
        manager = IntegrationManager()
        manager.run()
        mock_start_interaction.assert_called_once()


class TestWebAppIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch(
        "adaptive_learning.prompt.prompt_engine.PromptEngine.process_user_interaction"
    )
    def test_api_message_endpoint_basic_response(self, mock_process_interaction):
        # Mock the PromptEngine's response for a basic user input
        mock_response = {
            "prompt": "Oi! Sobre qual tema de programação você gostaria de conversar?",
            "content": {
                "title": "Introdução à Programação",
                "type": "text",
                "content": "Programação é uma habilidade incrível que envolve resolver problemas com código.",
            },
            "status": "success",
        }
        mock_process_interaction.return_value = mock_response

        # Send a request to the API endpoint
        response = self.client.post(
            "/api/message", json={"message": "Não entendo loops"}
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("response", response_data)
        self.assertIn("prompt", response_data)
        self.assertEqual(response_data["prompt"], mock_response["prompt"])
        self.assertIn("Introdução à Programação", response_data["response"])
        self.assertIn(
            "Programação é uma habilidade incrível", response_data["response"]
        )

    @patch(
        "adaptive_learning.prompt.prompt_engine.PromptEngine.process_user_interaction"
    )
    def test_api_message_endpoint_no_content_fallback(self, mock_process_interaction):
        # Mock the PromptEngine's response when no content is found
        mock_response = {
            "prompt": "Ei, parece que você tá precisando de uma mãozinha com loops. O que tá pegando?",
            "content": None,
            "status": "success",
        }
        mock_process_interaction.return_value = mock_response

        # Send a request to the API endpoint
        response = self.client.post(
            "/api/message", json={"message": "Não entendo loops"}
        )

        # Assert the response status code and fallback message
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("response", response_data)
        self.assertIn("prompt", response_data)
        self.assertEqual(response_data["prompt"], mock_response["prompt"])
        self.assertIn(
            "Desculpe, não consegui encontrar conteúdo relevante",
            response_data["response"],
        )

    @patch(
        "adaptive_learning.prompt.prompt_engine.PromptEngine.process_user_interaction"
    )
    def test_api_message_endpoint_error_handling(self, mock_process_interaction):
        # Simulate an exception in PromptEngine processing
        mock_process_interaction.side_effect = Exception("Processing error")

        # Send a request to the API endpoint
        response = self.client.post("/api/message", json={"message": "Test error"})

        # Assert the response status code and error message
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("response", response_data)
        self.assertIn(
            "Ops, algo deu errado ao processar sua mensagem",
            response_data["response"],
        )

    @patch(
        "adaptive_learning.prompt.prompt_engine.PromptEngine.process_user_interaction"
    )
    def test_api_message_endpoint_general_query_fallback(
        self, mock_process_interaction
    ):
        # Mock the PromptEngine's response for a general query with default fallback content
        mock_response = {
            "prompt": "Oi! Sobre qual tema de programação você gostaria de conversar ou tem dúvidas?",
            "content": {
                "title": "Introdução à Programação",
                "type": "text",
                "content": "Parece que não encontrei um conteúdo específico no momento. Vamos falar mais sobre o que você está buscando?",
            },
            "status": "success",
        }
        mock_process_interaction.return_value = mock_response

        # Send a request to the API endpoint with a general query
        response = self.client.post(
            "/api/message", json={"message": "Quero aprender programação"}
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("response", response_data)
        self.assertIn("prompt", response_data)
        self.assertEqual(response_data["prompt"], mock_response["prompt"])
        self.assertIn("Introdução à Programação", response_data["response"])
        self.assertIn(
            "Parece que não encontrei um conteúdo específico", response_data["response"]
        )

    @patch(
        "adaptive_learning.prompt.prompt_engine.PromptEngine.process_user_interaction"
    )
    def test_api_message_endpoint_content_format_preference(
        self, mock_process_interaction
    ):
        # Mock the PromptEngine's response based on preferred content format
        mock_response = {
            "prompt": "Entendi que você prefere conteúdo em vídeo. Vamos falar sobre loops?",
            "content": {
                "title": "Tutorial de Loops em Vídeo",
                "type": "video",
                "content": "Aqui está um vídeo explicando loops em programação.",
            },
            "status": "success",
        }
        mock_process_interaction.return_value = mock_response

        # Send a request to the API endpoint with a specific format preference
        response = self.client.post(
            "/api/message", json={"message": "Não entendo loops", "format": "video"}
        )

        # Assert the response status code and content respects the format preference
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("response", response_data)
        self.assertIn("prompt", response_data)
        self.assertEqual(response_data["prompt"], mock_response["prompt"])
        self.assertIn("Tutorial de Loops em Vídeo", response_data["response"])
        self.assertIn("vídeo explicando loops", response_data["response"])


if __name__ == "__main__":
    unittest.main()
