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
            try:
                os.remove(audio_path)
            except Exception as delete_error:
                print(
                    f"Warning: Could not delete temporary file {audio_path}: {delete_error}"
                )
        metadata["error"] = "Failed to extract audio from video"
        return {"metadata": metadata, "content": "", "processed_content": ""}

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
            wf.close()
            converted_audio_path = convert_audio_format(audio_path)
            if converted_audio_path:
                if audio_path and os.path.exists(audio_path):
                    try:
                        os.remove(audio_path)
                    except Exception as delete_error:
                        print(
                            f"Warning: Could not delete temporary file {audio_path}: {delete_error}"
                        )
                audio_path = converted_audio_path
                wf = wave.open(audio_path, "rb")
            else:
                wf.close()
                raise ValueError(
                    "Audio conversion failed, format not supported for Vosk"
                )

        # Initialize Vosk model (check for model in a default or user-specified path)
        model_path = os.environ.get(
            "VOSK_MODEL_PATH", "./vosk-model-small-pt-0.3"
        )  # Default to a lightweight Portuguese model in the workspace root
        if not os.path.exists(model_path):
            print(
                f"Error: Vosk model not found at {model_path}. For this Adaptive Learning System with Brazilian Portuguese content, I recommend 'vosk-model-pt-fb-v0.1.1-20220516_2113' for higher accuracy or 'vosk-model-small-pt-0.3' for lower resource usage. Ensure the model folder is in the workspace root or set the correct path in video_ingestor.py or as an environment variable 'VOSK_MODEL_PATH'. Download from https://alphacephei.com/vosk/models if needed."
            )
            raise FileNotFoundError(
                f"Vosk model not found at {model_path}. Please update model_path in video_ingestor.py or set the environment variable 'VOSK_MODEL_PATH' with the correct path to a Vosk model."
            )

        # Test loading the alternative model for higher accuracy
        try:
            alt_model_path = "./vosk-model-pt-fb-v0.1.1-20220516_2113"
            if os.path.exists(alt_model_path):
                print(
                    f"Attempting to load alternative model from {alt_model_path} for testing..."
                )
                alt_model = vosk.Model(alt_model_path)
                print(f"Successfully loaded alternative model from {alt_model_path}.")
                model = alt_model
            else:
                print(
                    f"Alternative model path {alt_model_path} not found, using default model."
                )
                model = vosk.Model(model_path)
        except Exception as alt_error:
            print(f"Error loading alternative model from {alt_model_path}: {alt_error}")
            print(f"Falling back to default model at {model_path}.")
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
            try:
                os.remove(audio_path)
            except Exception as delete_error:
                print(
                    f"Warning: Could not delete temporary file {audio_path}: {delete_error}"
                )

    if not content:
        print(f"Warning: No transcription extracted from {file_path}")
        metadata["error"] = "No transcription extracted from video"
        return {"metadata": metadata, "content": "", "processed_content": ""}

    return {"metadata": metadata, "content": content, "processed_content": content}


def convert_audio_format(input_path: str) -> str:
    """
    Convert audio file to mono, 16-bit, 16000 Hz WAV format for Vosk compatibility.
    Attempts to use ffmpeg directly, falls back to moviepy if ffmpeg is not available.

    Args:
        input_path (str): Path to the input audio file.

    Returns:
        str: Path to the converted audio file, or empty string if conversion fails.
    """
    import subprocess
    import tempfile
    from moviepy.editor import AudioFileClip

    # First attempt with ffmpeg if available
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_path = temp_file.name

        command = [
            "ffmpeg",
            "-i",
            input_path,
            "-ac",
            "1",  # Mono
            "-ar",
            "16000",  # Sample rate 16000 Hz
            "-acodec",
            "pcm_s16le",  # 16-bit PCM
            "-y",  # Overwrite output if exists
            output_path,
        ]
        subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        if os.path.exists(output_path):
            return output_path
        else:
            print("Error: Converted audio file not created with ffmpeg.")
    except subprocess.CalledProcessError as e:
        print(f"Error converting audio format with ffmpeg: {e.stderr.decode()}")
    except FileNotFoundError:
        print(
            "Error: ffmpeg not found on system. Falling back to moviepy for conversion."
        )
    except Exception as e:
        print(f"Error converting audio format with ffmpeg: {e}")

    # Fallback to moviepy if ffmpeg direct call fails
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_path = temp_file.name

        audio = AudioFileClip(input_path)
        audio.write_audiofile(
            output_path,
            codec="pcm_s16le",
            fps=16000,
            nbytes=2,  # 16-bit
            verbose=False,
            logger=None,
        )
        audio.close()
        if os.path.exists(output_path):
            return output_path
        else:
            print("Error: Converted audio file not created with moviepy.")
            return ""
    except Exception as e:
        print(f"Error converting audio format with moviepy: {e}")
        return ""


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
