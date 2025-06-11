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
import vosk
import wave
import json
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
        "resolution": "",
        "fps": 0,
        "resource_type": "video",
    }

    # Extract audio and metadata from video
    audio_path = None
    try:
        video = VideoFileClip(file_path)
        metadata["duration_seconds"] = video.duration
        metadata["resolution"] = f"{video.w}x{video.h}"
        metadata["fps"] = video.fps
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

    # Transcribe audio using Vosk
    content = ""
    try:
        # Ensure the audio is in WAV format with correct parameters for Vosk
        wf = wave.open(audio_path, "rb")
        if (
            wf.getnchannels() != 1
            or wf.getsampwidth() != 2
            or wf.getframerate() not in [16000, 44100]
        ):
            print(f"Audio format not supported for {file_path}. Converting...")
            # Conversion logic could be added here if needed
            raise ValueError("Audio must be mono, 16-bit, and 16000 or 44100 Hz")

        # Initialize Vosk model (assuming a model is available in the specified path)
        model_path = "model"  # Replace with actual path to Vosk model
        if not os.path.exists(model_path):
            print(
                f"Error: Vosk model not found at {model_path}. Please download a Vosk model from https://alphacephei.com/vosk/models and update the model_path in video_ingestor.py."
            )
            raise FileNotFoundError(
                f"Vosk model not found at {model_path}. Please update model_path in video_ingestor.py with the correct path to a Vosk model."
            )

        model = vosk.Model(model_path)
        rec = vosk.KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        # Process audio
        segments = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "result" in result:
                    for word in result["result"]:
                        start = word.get("start", 0)
                        end = word.get("end", 0)
                        text = word.get("word", "")
                        segments.append(f"[{start:.1f}s - {end:.1f}s]: {text}")
                content += result.get("text", "") + " "
            else:
                partial = json.loads(rec.PartialResult())
                content += partial.get("partial", "") + " "

        if segments:
            content = "\n".join(segments)
        metadata["language"] = (
            "unknown"  # Vosk does not provide language detection by default
        )
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
