# German Audio Transcription Tool

Automatically download and transcribe German audio files using OpenAI Whisper for language learning.

## Features

- ✅ **Download audio from videos** - YouTube, Instagram, Facebook, and 1000+ platforms
- ✅ Transcribe German audio files with high accuracy
- ✅ Process single files or batch process entire directories
- ✅ Automatically skip already-transcribed files
- ✅ Support for multiple audio formats (mp3, wav, m4a, flac, ogg, opus, webm)
- ✅ Choose from multiple Whisper models (tiny to large)
- ✅ Save transcripts alongside audio files

## Prerequisites

- Python 3.8 or higher
- FFmpeg (required by Whisper)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

## Installation

1. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Note: First run will download the Whisper model (~140MB for 'base' model).

## Usage

### Download Audio from Videos

Download audio from YouTube, Instagram, Facebook, TikTok, and 1000+ other platforms:

#### ⭐ Auto-Organization (Recommended)

The script automatically detects the platform and creates numbered folders:

```bash
# Download from a single URL (auto-organizes by platform)
python download_audio.py -u "https://www.youtube.com/watch?v=VIDEO_ID" --auto
# Creates: youtube/0001/, youtube/0002/, etc.

# Download multiple URLs (auto-organizes each by platform)
python download_audio.py -f urls.txt --auto
# Creates: instgram/0001/, youtube/0001/, facebook/0001/, etc.
```

#### Manual Organization

Or specify the output directory manually:

```bash
# Download to a specific directory
python download_audio.py -u "https://instagram.com/reel/..." -o instgram/01/

# Download with a custom filename
python download_audio.py -u "https://facebook.com/video/..." -o facebook/ -n "my-video"

# Download multiple URLs to a directory
python download_audio.py -f urls.txt -o downloads/
```

**Supported platforms include:**
- YouTube (videos, shorts, live streams)
- Instagram (reels, IGTV, stories)
- Facebook (videos, watch)
- TikTok
- Twitter/X
- Vimeo
- And 1000+ more platforms

**Creating a URL list file:**

Create a text file (e.g., `urls.txt`) with one URL per line:
```
https://www.youtube.com/watch?v=...
https://www.instagram.com/reel/...
https://www.facebook.com/...
# Lines starting with # are ignored
```

### Transcribe Audio Files

#### Transcribe a Single File

```bash
python transcribe.py -f instgram/01/ReelAudio-8382.mp3
```

This will create `ReelAudio-8382.txt` in the same directory.

#### Batch Process a Directory

```bash
# Process all audio files in instgram/ and subdirectories
python transcribe.py -d instgram/

# Process only the instgram/ directory (not subdirectories)
python transcribe.py -d instgram/ --no-recursive
```

#### Choose a Different Model

Whisper offers different model sizes. Larger models are more accurate but slower:

| Model  | Size  | Speed | Accuracy |
|--------|-------|-------|----------|
| tiny   | 39M   | Fast  | Basic    |
| base   | 74M   | Fast  | Good     |
| small  | 244M  | Med   | Better   |
| medium | 769M  | Slow  | Great    |
| large  | 1550M | Slowest | Best   |

```bash
# Use medium model for better accuracy
python transcribe.py -d instgram/ -m medium

# Use tiny model for faster processing
python transcribe.py -d instgram/ -m tiny
```

#### Re-transcribe Existing Files

By default, files with existing transcripts are skipped. To force re-transcription:

```bash
python transcribe.py -d instgram/ --no-skip
```

## Complete Workflow for Daily Use

### ⭐ Recommended: Auto-Organized Workflow

The easiest way to manage your language learning content:

```bash
# 1. Add URLs to urls.txt throughout the day
echo "https://www.instagram.com/reel/..." >> urls.txt
echo "https://www.youtube.com/watch?v=..." >> urls.txt
echo "https://www.facebook.com/..." >> urls.txt

# 2. Download all at once (auto-organized by platform!)
python download_audio.py -f urls.txt --auto

# 3. Transcribe everything
python transcribe.py -d instgram/ youtube/ facebook/

# 4. Find your organized content:
# instgram/0001/, instgram/0002/, instgram/0003/, ...
# youtube/0001/, youtube/0002/, ...
# facebook/0001/, ...
```

**How auto-organization works:**
- Detects platform from URL (YouTube, Instagram, Facebook, etc.)
- Finds the next available number (checks existing folders: 0001, 0002, ...)
- Creates `platform/####/` and downloads there
- Transcripts are saved alongside audio files

### Manual Workflow

If you prefer to control folders yourself:

```bash
# Download audio
python download_audio.py -u "https://instagram.com/reel/..." -o instgram/05/

# Transcribe immediately
python transcribe.py -d instgram/05/
```

The transcription script automatically skips already-transcribed files, so you can run it anytime new audio files are added!

## Examples

### Complete Workflow Examples

```bash
# Example 1: Download from YouTube and transcribe
python download_audio.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o youtube/
python transcribe.py -d youtube/

# Example 2: Batch download Instagram reels
# Create urls.txt with your Instagram URLs
python download_audio.py -f urls.txt -o instgram/02/
python transcribe.py -d instgram/02/

# Example 3: Download with custom name and transcribe
python download_audio.py -u "https://facebook.com/video/..." -o facebook/ -n "german-lesson-1"
python transcribe.py -f facebook/german-lesson-1.mp3 -m medium
```

### Transcription-Only Examples

```bash
# Transcribe all new Instagram reel audios
python transcribe.py -d instgram/

# Transcribe a specific file with high accuracy
python transcribe.py -f instgram/01/ReelAudio-8382.mp3 -m medium

# Process only today's folder
python transcribe.py -d instgram/02/ --no-recursive

# Re-transcribe everything with a better model
python transcribe.py -d instgram/ -m large --no-skip
```

## Troubleshooting

**Error: "ffmpeg not found"**
- Install FFmpeg (see Prerequisites above)

**Download fails with "Unable to extract"**
- The video might be private, age-restricted, or from an unsupported platform
- Try updating yt-dlp: `pip install --upgrade yt-dlp`
- Check if the URL is accessible in your browser

**Out of memory error (during transcription)**
- Use a smaller model: `-m tiny` or `-m base`
- Process files one at a time using `-f` instead of `-d`

**Transcription not accurate**
- Try a larger model: `-m medium` or `-m large`
- Ensure audio quality is good
- Check that the audio is actually in German

**Download is too slow**
- This depends on your internet connection and the platform's servers
- The tool automatically uses the best available quality for audio

## Project Structure

### With Auto-Organization (Recommended)

```
.
├── instgram/              # Instagram content (auto-organized)
│   ├── 0001/
│   │   ├── audio.mp3
│   │   └── audio.txt     (transcript)
│   ├── 0002/
│   └── 0003/
├── youtube/               # YouTube content (auto-organized)
│   ├── 0001/
│   ├── 0002/
│   └── 0003/
├── facebook/              # Facebook content (auto-organized)
│   └── 0001/
├── urls.txt               # URL list for batch downloads
├── download_audio.py      # Audio downloader script
├── transcribe.py          # Transcription script
└── requirements.txt       # Dependencies
```

### Manual Organization

```
.
├── downloads/             # Manual download directory
│   ├── audio1.mp3
│   ├── audio1.txt
│   └── ...
├── instgram/              # Custom organization
│   └── my-folder/
└── ...
```

## License

MIT License - Feel free to use for your language learning!
