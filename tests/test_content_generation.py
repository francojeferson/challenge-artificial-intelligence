import unittest
from adaptive_learning.content_generation.content_generator import (
    TextGenerator,
    AudioGenerator,
    VideoGenerator,
)
from adaptive_learning.content_generation.content_generation_manager import (
    ContentGenerationManager,
)


class TestContentGeneration(unittest.TestCase):
    def setUp(self):
        self.knowledge_gaps = {"topic": "programação básica"}
        self.content_snippets = [
            "Introdução à programação",
            "Variáveis e tipos de dados",
            "Estruturas de controle",
        ]
        self.manager = ContentGenerationManager()

    def test_text_generation(self):
        text_gen = TextGenerator()
        result = text_gen.generate(self.knowledge_gaps, self.content_snippets)
        self.assertIn("Introdução à programação", result)

    def test_audio_generation(self):
        audio_gen = AudioGenerator()
        audio_path = audio_gen.generate(self.knowledge_gaps, self.content_snippets)
        self.assertTrue(audio_path.endswith(".mp3"))

    def test_video_generation(self):
        video_gen = VideoGenerator()
        video_path = video_gen.generate(self.knowledge_gaps, self.content_snippets)
        self.assertTrue(video_path.endswith(".mp4"))

    def test_manager_text(self):
        result = self.manager.generate_content(
            self.knowledge_gaps, "text", self.content_snippets
        )
        self.assertIn("Variáveis e tipos de dados", result)

    def test_manager_audio(self):
        audio_path = self.manager.generate_content(
            self.knowledge_gaps, "audio", self.content_snippets
        )
        self.assertTrue(audio_path.endswith(".mp3"))

    def test_manager_video(self):
        video_path = self.manager.generate_content(
            self.knowledge_gaps, "video", self.content_snippets
        )
        self.assertTrue(video_path.endswith(".mp4"))


if __name__ == "__main__":
    unittest.main()
