# German Audio Transcription Tool

Automatically transcribe German audio files using OpenAI Whisper for language learning.

## Features

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

### Transcribe a Single File

```bash
python transcribe.py -f instgram/01/ReelAudio-8382.mp3
```

This will create `ReelAudio-8382.txt` in the same directory.

### Batch Process a Directory

```bash
# Process all audio files in instgram/ and subdirectories
python transcribe.py -d instgram/

# Process only the instgram/ directory (not subdirectories)
python transcribe.py -d instgram/ --no-recursive
```

### Choose a Different Model

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

### Re-transcribe Existing Files

By default, files with existing transcripts are skipped. To force re-transcription:

```bash
python transcribe.py -d instgram/ --no-skip
```

## Workflow for Daily Use

1. **Download new audio files** to the appropriate folder (e.g., `instgram/02/`)
2. **Run batch transcription:**
   ```bash
   python transcribe.py -d instgram/
   ```
3. **Find your transcripts** - they'll be saved as `.txt` files next to the audio files

The script automatically skips already-transcribed files, so you can run it anytime new audio files are added!

## Examples

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

**Out of memory error**
- Use a smaller model: `-m tiny` or `-m base`
- Process files one at a time using `-f` instead of `-d`

**Transcription not accurate**
- Try a larger model: `-m medium` or `-m large`
- Ensure audio quality is good
- Check that the audio is actually in German

## Project Structure

```
.
├── instgram/
│   ├── 01/
│   │   ├── ReelAudio-8382.mp3
│   │   └── ReelAudio-8382.txt  (generated)
│   └── 02/
│       └── ...
├── transcribe.py
├── requirements.txt
└── README.md
```

## License

MIT License - Feel free to use for your language learning!
