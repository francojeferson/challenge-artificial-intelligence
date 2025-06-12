from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


# Abstract base class for content generators
class ContentGenerator(ABC):
    @abstractmethod
    def generate(
        self, knowledge_gaps: Dict[str, Any], content_snippets: Optional[list] = None
    ) -> Any:
        """
        Generate content based on user knowledge gaps and relevant content snippets.

        :param knowledge_gaps: Dictionary describing user's knowledge gaps.
        :param content_snippets: Optional list of content snippets retrieved from the index.
        :return: Generated content in the specific format.
        """
        pass


# Text content generator
class TextGenerator(ContentGenerator):
    def generate(
        self, knowledge_gaps: Dict[str, Any], content_snippets: Optional[list] = None
    ) -> str:
        # For simplicity, concatenate content snippets or generate a placeholder text
        if content_snippets:
            return "\n\n".join(content_snippets)
        else:
            return "Conteúdo gerado dinamicamente baseado nas lacunas de conhecimento do usuário."


# Audio content generator using pyttsx3 for local TTS
import pyttsx3
import tempfile
import os


class AudioGenerator(ContentGenerator):
    def __init__(self):
        self.engine = pyttsx3.init()
        # Optional: Configure voice properties here (e.g., language, rate, volume)

    def generate(
        self, knowledge_gaps: Dict[str, Any], content_snippets: Optional[list] = None
    ) -> str:
        text = ""
        if content_snippets:
            text = "\n\n".join(content_snippets)
        else:
            text = "Conteúdo de áudio gerado dinamicamente baseado nas lacunas de conhecimento do usuário."

        # Generate audio file in a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            audio_path = tmp_file.name
        self.engine.save_to_file(text, audio_path)
        self.engine.runAndWait()
        return audio_path


# Video content generator using moviepy to combine audio and images
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from typing import List


class VideoGenerator(ContentGenerator):
    def __init__(self, image_paths: Optional[List[str]] = None):
        """
        :param image_paths: Optional list of image file paths to include in the video.
        """
        self.image_paths = image_paths or []

    def generate(
        self, knowledge_gaps: Dict[str, Any], content_snippets: Optional[list] = None
    ) -> str:
        # Generate audio content first using AudioGenerator
        audio_gen = AudioGenerator()
        audio_path = audio_gen.generate(knowledge_gaps, content_snippets)

        # Create video clips from images or use a placeholder if no images
        clips = []
        duration_per_image = 5  # seconds per image
        if self.image_paths:
            for img_path in self.image_paths:
                clip = ImageClip(img_path).set_duration(duration_per_image)
                clips.append(clip)
        else:
            # Create a blank clip with text or color if no images provided
            from moviepy.editor import ColorClip, TextClip

            blank_clip = ColorClip(
                size=(640, 480), color=(255, 255, 255), duration=duration_per_image
            )
            # Bypass TextClip usage to avoid ImageMagick dependency in tests or environments without ImageMagick
            from moviepy.editor import ColorClip

            clip = ColorClip(
                size=(640, 480), color=(255, 255, 255), duration=duration_per_image
            )
            clips.append(clip)

        # Concatenate clips
        from moviepy.editor import concatenate_videoclips

        video = concatenate_videoclips(clips)

        # Add audio
        audio = AudioFileClip(audio_path)
        video = video.set_audio(audio)

        # Export final video to a temporary file
        import tempfile

        output_path = tempfile.mktemp(suffix=".mp4")
        video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None,
        )

        # Clean up temporary audio file
        try:
            os.remove(audio_path)
        except Exception:
            pass

        return output_path


# Factory to create content generators based on format
class ContentGenerationFactory:
    @staticmethod
    def get_generator(format_type: str, **kwargs) -> ContentGenerator:
        format_type = format_type.lower()
        if format_type == "text":
            return TextGenerator()
        elif format_type == "audio":
            return AudioGenerator()
        elif format_type == "video":
            return VideoGenerator(**kwargs)
        else:
            raise ValueError(f"Unsupported content format: {format_type}")
