#!/usr/bin/env python3
"""
Audio Downloader for Video Platforms
Downloads audio from YouTube, Instagram, Facebook, and other platforms
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import Optional
import yt_dlp


def detect_platform(url: str) -> str:
    """
    Detect the platform from a URL
    
    Args:
        url: Video URL
        
    Returns:
        Platform name (youtube, instgram, facebook, tiktok, etc.)
    """
    url_lower = url.lower()
    
    # Map common domains to folder names
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'youtube'
    elif 'instagram.com' in url_lower:
        return 'instgram'  # Keep your original spelling
    elif 'facebook.com' in url_lower or 'fb.watch' in url_lower:
        return 'facebook'
    elif 'tiktok.com' in url_lower:
        return 'tiktok'
    elif 'twitter.com' in url_lower or 'x.com' in url_lower:
        return 'twitter'
    elif 'vimeo.com' in url_lower:
        return 'vimeo'
    elif 'twitch.tv' in url_lower:
        return 'twitch'
    elif 'reddit.com' in url_lower:
        return 'reddit'
    else:
        return 'other'


def get_next_numbered_folder(platform: str, base_path: Path = Path(".")) -> Path:
    """
    Get the next available numbered folder for a platform
    
    Args:
        platform: Platform name (youtube, instgram, facebook, etc.)
        base_path: Base directory to search in
        
    Returns:
        Path to the next numbered folder (e.g., instgram/0003/)
    """
    platform_dir = base_path / platform
    
    # Find existing numbered folders
    existing_numbers = []
    if platform_dir.exists():
        for folder in platform_dir.iterdir():
            if folder.is_dir():
                # Match folders like 0001, 0002, 01, 02, etc.
                match = re.match(r'^(\d+)$', folder.name)
                if match:
                    existing_numbers.append(int(match.group(1)))
    
    # Get next number
    if existing_numbers:
        next_number = max(existing_numbers) + 1
    else:
        next_number = 1
    
    # Format with leading zeros (4 digits: 0001, 0002, etc.)
    next_folder = platform_dir / f"{next_number:04d}"
    
    return next_folder


class AudioDownloader:
    """Handles audio downloading from video platforms"""
    
    def __init__(self, output_dir: Path = Path("downloads"), auto_organize: bool = False):
        """
        Initialize the downloader
        
        Args:
            output_dir: Directory to save downloaded audio files
            auto_organize: Automatically organize by platform and number
        """
        self.output_dir = output_dir
        self.auto_organize = auto_organize
        
        if not auto_organize:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def download(self, url: str, filename: Optional[str] = None) -> Optional[Path]:
        """
        Download audio from a video URL
        
        Args:
            url: Video URL (YouTube, Instagram, Facebook, etc.)
            filename: Optional custom filename (without extension)
            
        Returns:
            Path to downloaded audio file, or None if failed
        """
        try:
            # Auto-organize if enabled
            if self.auto_organize:
                platform = detect_platform(url)
                actual_output_dir = get_next_numbered_folder(platform)
                actual_output_dir.mkdir(parents=True, exist_ok=True)
                print(f"📊 Detected platform: {platform}")
                print(f"📁 Auto-organizing to: {actual_output_dir}/")
            else:
                actual_output_dir = self.output_dir
            
            # Configure yt-dlp options
            if filename:
                output_template = str(actual_output_dir / f"{filename}.%(ext)s")
            else:
                output_template = str(actual_output_dir / "%(title)s.%(ext)s")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'extract_flat': False,
            }
            
            print(f"\n📥 Downloading audio from: {url}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first to get the final filename
                info = ydl.extract_info(url, download=True)
                
                if info:
                    # Get the actual filename that was saved
                    if filename:
                        final_path = actual_output_dir / f"{filename}.mp3"
                    else:
                        title = info.get('title', 'audio')
                        # Clean filename
                        title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_', '⧸')).strip()
                        final_path = actual_output_dir / f"{title}.mp3"
                    
                    print(f"✓ Download complete: {final_path}")
                    return final_path
                    
        except Exception as e:
            print(f"✗ Error downloading audio: {e}", file=sys.stderr)
            return None
    
    def download_batch(self, urls: list[str]) -> list[Path]:
        """
        Download audio from multiple URLs
        
        Args:
            urls: List of video URLs
            
        Returns:
            List of paths to successfully downloaded audio files
        """
        downloaded_files = []
        
        print(f"\n{'='*60}")
        print(f"Batch download: {len(urls)} URL(s)")
        print(f"{'='*60}")
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}]")
            result = self.download(url)
            if result:
                downloaded_files.append(result)
        
        print(f"\n{'='*60}")
        print(f"Batch download complete!")
        print(f"Successfully downloaded: {len(downloaded_files)}/{len(urls)} file(s)")
        print(f"{'='*60}")
        
        return downloaded_files


def read_urls_from_file(file_path: Path) -> list[str]:
    """
    Read URLs from a text file (one URL per line)
    
    Args:
        file_path: Path to file containing URLs
        
    Returns:
        List of URLs
    """
    if not file_path.exists():
        raise FileNotFoundError(f"URL file not found: {file_path}")
    
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                urls.append(line)
    
    return urls


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Download audio from video platforms (YouTube, Instagram, Facebook, etc.)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-organize by platform (recommended)
  python download_audio.py -u "https://www.youtube.com/watch?v=..." --auto
  python download_audio.py -f urls.txt --auto
  
  # Download to a specific directory
  python download_audio.py -u "https://instagram.com/reel/..." -o instgram/01/
  
  # Download with a custom filename
  python download_audio.py -u "https://facebook.com/video/..." -o facebook/ -n "my-video"
  
  # URLs file format (urls.txt):
  # https://www.youtube.com/watch?v=...
  # https://www.instagram.com/reel/...
  # https://www.facebook.com/...
  
Auto-organization creates folders like:
  youtube/0001/, youtube/0002/, ...
  instgram/0001/, instgram/0002/, ...
  facebook/0001/, facebook/0002/, ...
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-u', '--url',
        type=str,
        help='Video URL to download audio from'
    )
    input_group.add_argument(
        '-f', '--file',
        type=str,
        help='Text file containing URLs (one per line)'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='downloads',
        help='Output directory for downloaded audio files (default: downloads/). Ignored if --auto is used.'
    )
    parser.add_argument(
        '-n', '--name',
        type=str,
        help='Custom filename for the audio (without extension, single URL only)'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Auto-organize downloads by platform (youtube/0001/, instgram/0002/, etc.)'
    )
    
    args = parser.parse_args()
    
    try:
        # Determine output directory
        if args.auto:
            # Auto-organize mode - output_dir is ignored
            output_dir = Path(".")  # Use current directory as base
            auto_organize = True
            print("🤖 Auto-organization enabled")
        else:
            output_dir = Path(args.output)
            auto_organize = False
        
        downloader = AudioDownloader(output_dir=output_dir, auto_organize=auto_organize)
        
        if args.url:
            # Single URL mode
            if args.name:
                downloader.download(args.url, filename=args.name)
            else:
                downloader.download(args.url)
                
        elif args.file:
            # Batch mode from file
            if args.name:
                print("Warning: --name option is ignored in batch mode", file=sys.stderr)
            
            urls = read_urls_from_file(Path(args.file))
            if not urls:
                print("No URLs found in file.", file=sys.stderr)
                sys.exit(1)
                
            downloader.download_batch(urls)
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()