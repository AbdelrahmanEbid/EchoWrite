# Changelog

## [2.0.0] - 2025-09-30

### 🎉 Major New Feature: Audio Downloader

Added ability to download audio from videos on YouTube, Instagram, Facebook, and 1000+ other platforms!

### ✨ New Features

- **`download_audio.py`** - New script to download audio from video URLs
  - Supports single URL download
  - Batch download from URL list file
  - Custom output directory
  - Custom filename support
  - Automatic MP3 conversion
  - Works with YouTube, Instagram, Facebook, TikTok, Twitter, Vimeo, and many more

### 📦 New Dependencies

- `yt-dlp>=2024.0.0` - Industry-standard video downloader supporting 1000+ platforms

### 📚 Documentation Updates

- Updated `README.md` with download instructions and complete workflow examples
- Updated `about.md` to reflect new capabilities
- Added `QUICKSTART.md` for easy getting started
- Added `urls.txt` template for batch downloads

### 🔄 Workflow Enhancement

New recommended workflow:
1. Download audio: `python download_audio.py -u "URL" -o folder/`
2. Transcribe: `python transcribe.py -d folder/`
3. Get your transcript alongside the audio file!

---

## [1.0.0] - Initial Release

### Features

- German audio transcription using OpenAI Whisper
- Single file and batch directory processing
- Multiple Whisper models (tiny to large)
- Automatic skip of already-transcribed files
- Support for multiple audio formats
