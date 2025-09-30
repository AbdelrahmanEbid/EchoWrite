#!/usr/bin/env python3
"""
German Audio Transcription Tool
Transcribes German audio files using OpenAI Whisper
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional
import whisper
from tqdm import tqdm


# Supported audio file extensions
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.opus', '.webm'}


class AudioTranscriber:
    """Handles audio transcription using Whisper"""
    
    def __init__(self, model_name: str = "base", language: str = "de"):
        """
        Initialize the transcriber
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
            language: Language code (de for German)
        """
        if not model_name:
            raise ValueError("Model name cannot be empty")
        if not language:
            raise ValueError("Language cannot be empty")
            
        print(f"Loading Whisper model '{model_name}'...")
        self.model = whisper.load_model(model_name)
        self.language = language
        print("Model loaded successfully!")
    
    def transcribe_file(self, audio_path: Path, output_path: Optional[Path] = None) -> str:
        """
        Transcribe a single audio file
        
        Args:
            audio_path: Path to audio file
            output_path: Optional path for transcript file
            
        Returns:
            Transcript text
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        if not audio_path.is_file():
            raise ValueError(f"Path is not a file: {audio_path}")
            
        print(f"\nTranscribing: {audio_path.name}")
        
        # Transcribe with language specified for better accuracy
        result = self.model.transcribe(
            str(audio_path),
            language=self.language,
            verbose=False
        )
        
        transcript = result["text"].strip()
        
        # Determine output path
        if output_path is None:
            output_path = audio_path.with_suffix('.txt')
        
        # Save transcript
        output_path.write_text(transcript, encoding='utf-8')
        print(f"✓ Transcript saved: {output_path.name}")
        
        return transcript


def find_audio_files(directory: Path, recursive: bool = True) -> List[Path]:
    """
    Find all audio files in a directory
    
    Args:
        directory: Directory to search
        recursive: Search subdirectories
        
    Returns:
        List of audio file paths
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    if not directory.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    audio_files = []
    
    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"
    
    for path in directory.glob(pattern):
        if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
            audio_files.append(path)
    
    return sorted(audio_files)


def process_batch(
    directory: Path,
    model_name: str = "base",
    skip_existing: bool = True,
    recursive: bool = True
):
    """
    Process all audio files in a directory
    
    Args:
        directory: Directory containing audio files
        model_name: Whisper model to use
        skip_existing: Skip files that already have transcripts
        recursive: Process subdirectories
    """
    if not directory:
        raise ValueError("Directory cannot be None")
    
    # Find audio files
    print(f"Searching for audio files in: {directory}")
    audio_files = find_audio_files(directory, recursive=recursive)
    
    if not audio_files:
        print("No audio files found.")
        return
    
    print(f"Found {len(audio_files)} audio file(s)")
    
    # Filter out already transcribed files
    files_to_process = []
    for audio_file in audio_files:
        transcript_file = audio_file.with_suffix('.txt')
        if skip_existing and transcript_file.exists():
            print(f"⊘ Skipping (already transcribed): {audio_file.name}")
        else:
            files_to_process.append(audio_file)
    
    if not files_to_process:
        print("\nAll files already transcribed!")
        return
    
    print(f"\nProcessing {len(files_to_process)} file(s)...\n")
    
    # Initialize transcriber
    transcriber = AudioTranscriber(model_name=model_name, language="de")
    
    # Process files
    for i, audio_file in enumerate(files_to_process, 1):
        print(f"\n[{i}/{len(files_to_process)}]")
        try:
            transcriber.transcribe_file(audio_file)
        except Exception as e:
            print(f"✗ Error transcribing {audio_file.name}: {e}")
            continue
    
    print(f"\n{'='*60}")
    print(f"Batch processing complete!")
    print(f"Processed: {len(files_to_process)} file(s)")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Transcribe German audio files using OpenAI Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transcribe a single file
  python transcribe.py -f instgram/01/ReelAudio-8382.mp3
  
  # Batch process all audio files in a directory
  python transcribe.py -d instgram/
  
  # Use a larger model for better accuracy
  python transcribe.py -d instgram/ -m medium
  
  # Force re-transcribe all files (skip nothing)
  python transcribe.py -d instgram/ --no-skip
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-f', '--file',
        type=str,
        help='Path to a single audio file'
    )
    input_group.add_argument(
        '-d', '--directory',
        type=str,
        help='Directory containing audio files'
    )
    
    # Model options
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Whisper model size (default: base). Larger = more accurate but slower'
    )
    
    # Processing options
    parser.add_argument(
        '--no-skip',
        action='store_true',
        help='Re-transcribe files even if transcript already exists'
    )
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Don\'t search subdirectories (only for directory mode)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.file:
            # Single file mode
            audio_path = Path(args.file)
            transcriber = AudioTranscriber(model_name=args.model, language="de")
            transcriber.transcribe_file(audio_path)
            
        elif args.directory:
            # Batch mode
            directory = Path(args.directory)
            process_batch(
                directory=directory,
                model_name=args.model,
                skip_existing=not args.no_skip,
                recursive=not args.no_recursive
            )
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
