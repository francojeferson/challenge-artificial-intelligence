"""
Video Ingestion Module

This module handles the ingestion of video resources for the Adaptive Learning System.
It extracts audio transcripts and metadata from video files for indexing.

Key Responsibilities:
- Extract audio from video files and transcribe it to text.
- Extract metadata from video files for indexing.
- Use speech-to-text libraries (whisper) for transcription.
- Ensure all processing is local and privacy-respecting.

Dependencies:
- whisper: For local speech-to-text transcription of video audio.
- moviepy: For extracting audio from video files.
"""

import os
from typing import Dict, List, Any
import whisper
from moviepy.editor import VideoFileClip
import tempfile


def ingest_video_file(file_path: str) -> Dict[str, Any]:
    """
    Ingest a single video file and extract its audio transcript and metadata.

    Args:
        file_path (str): Path to the video file.

    Returns:
        Dict[str, Any]: Dictionary containing metadata and transcribed content.
    """
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_path)[1].lower()
    metadata = {
        "file_name": file_name,
        "file_path": file_path,
        "file_type": file_extension,
        "size_bytes": os.path.getsize(file_path),
        "last_modified": os.path.getmtime(file_path),
        "duration_seconds": 0,
    }

    # Extract audio from video
    audio_path = None
    try:
        video = VideoFileClip(file_path)
        metadata["duration_seconds"] = video.duration
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            audio_path = temp_audio.name
            video.audio.write_audiofile(
                audio_path, codec="pcm_s16le", verbose=False, logger=None
            )
        video.close()
    except Exception as e:
        print(f"Error extracting audio from video {file_path}: {e}")
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        return {}

    # Transcribe audio using Whisper
    content = ""
    try:
        model = whisper.load_model("base")  # Use 'base' model for local processing
        result = model.transcribe(audio_path, fp16=False)
        content = result["text"]
        metadata["language"] = result.get("language", "unknown")
    except Exception as e:
        print(f"Error transcribing audio from {file_path}: {e}")
    finally:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

    if not content:
        print(f"Warning: No transcription extracted from {file_path}")
        return {}

    return {"metadata": metadata, "content": content, "processed_content": content}


def ingest_video_directory(directory_path: str) -> List[Dict[str, Any]]:
    """
    Ingest all video files in a directory and its subdirectories.

    Args:
        directory_path (str): Path to the directory containing video files.

    Returns:
        List[Dict[str, Any]]: List of dictionaries with metadata and content for each file.
    """
    video_data = []
    supported_extensions = (".mp4", ".avi", ".mkv", ".mov")

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(supported_extensions):
                file_path = os.path.join(root, file)
                data = ingest_video_file(file_path)
                if data:
                    video_data.append(data)

    return video_data


if __name__ == "__main__":
    # Example usage for testing
    sample_dir = "../../resources/video"
    if os.path.exists(sample_dir):
        video_resources = ingest_video_directory(sample_dir)
        print(f"Ingested {len(video_resources)} video resources.")
        for resource in video_resources:
            print(
                f"File: {resource['metadata']['file_name']}, Duration: {resource['metadata'].get('duration_seconds', 0)}s"
            )
    else:
        print(f"Sample directory {sample_dir} not found.")
