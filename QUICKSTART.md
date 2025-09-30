# Quick Start Guide

Get started with EchoWrite in 3 simple steps!

## 🚀 Setup (One Time Only)

```bash
# 1. Install FFmpeg (if not already installed)
sudo apt install ffmpeg  # Ubuntu/Debian
# brew install ffmpeg    # macOS
# sudo pacman -S ffmpeg  # Arch

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 📥 Download & 📝 Transcribe

### ⭐ Recommended: Auto-Organization

The easiest way! Just add URLs and let the script organize everything:

```bash
# Download from a single URL (auto-organizes by platform)
python download_audio.py -u "YOUR_VIDEO_URL" --auto

# Or batch download from urls.txt
python download_audio.py -f urls.txt --auto

# Transcribe everything
python transcribe.py -d instgram/ youtube/ facebook/
```

The script will:
- Detect the platform (YouTube, Instagram, Facebook, etc.)
- Create numbered folders automatically: `youtube/0001/`, `instgram/0002/`, etc.
- Download the audio there
- Ready for transcription!

### Manual Organization

If you prefer to specify folders yourself:

```bash
# Download to specific folder
python download_audio.py -u "YOUR_VIDEO_URL" -o instgram/05/

# Transcribe it
python transcribe.py -d instgram/05/
```

## 🎯 Real-World Example

### Complete Daily Workflow

```bash
# 1. Add URLs to urls.txt throughout the day
echo "https://www.instagram.com/reel/ABC123/" >> urls.txt
echo "https://www.youtube.com/watch?v=XYZ789" >> urls.txt

# 2. Download all at once (auto-organized!)
python download_audio.py -f urls.txt --auto
# Creates: instgram/0003/, youtube/0002/, etc.

# 3. Transcribe everything
python transcribe.py -d instgram/ -d youtube/

# 4. Find your transcripts organized by platform!
ls instgram/*/  # All Instagram transcripts
ls youtube/*/   # All YouTube transcripts
```

Result:
```
instgram/
├── 0001/ ✓ audio.mp3 + transcript.txt
├── 0002/ ✓ audio.mp3 + transcript.txt
└── 0003/ ✓ audio.mp3 + transcript.txt (new!)

youtube/
├── 0001/ ✓ audio.mp3 + transcript.txt
└── 0002/ ✓ audio.mp3 + transcript.txt (new!)
```

## ⚙️ Common Options

### Download Options
- `-u URL` - Single video URL
- `-f FILE` - File with multiple URLs
- `--auto` - **Auto-organize by platform** (Recommended! 🌟)
- `-o DIR` - Manual output directory (ignored if `--auto` is used)
- `-n NAME` - Custom filename (without extension)

### Transcription Options
- `-f FILE` - Single audio file
- `-d DIR` - Process entire directory
- `-m MODEL` - Model size: `tiny`, `base`, `small`, `medium`, `large`
  - `tiny` = Fast but basic
  - `base` = Good balance (default)
  - `medium` = Slower but more accurate
  - `large` = Best quality, slowest
- `--no-skip` - Re-transcribe files with existing transcripts
- `--no-recursive` - Don't search subdirectories

## 🔥 Pro Tips

1. **Use auto-organization** - It's magical! 🪄
   ```bash
   # Just use --auto and forget about folder management
   python download_audio.py -f urls.txt --auto
   ```

2. **Batch everything:** Keep adding to `urls.txt` throughout the day
   ```bash
   echo "https://youtube.com/..." >> urls.txt
   echo "https://instagram.com/..." >> urls.txt
   # Then download all at once
   python download_audio.py -f urls.txt --auto
   ```

3. **Skip already done:** The transcriber automatically skips files with existing transcripts!
   ```bash
   # Run this anytime - it only processes new files
   python transcribe.py -d instgram/ youtube/
   ```

4. **Folder organization:**
   - Auto-mode creates: `platform/0001/`, `platform/0002/`, etc.
   - Each project gets its own numbered folder
   - Transcripts are saved alongside audio files

## 📦 Supported Platforms

✅ YouTube (videos, shorts, live streams)  
✅ Instagram (reels, IGTV, stories)  
✅ Facebook (videos, watch)  
✅ TikTok  
✅ Twitter/X  
✅ Vimeo  
✅ Twitch  
✅ Reddit  
✅ And 1000+ more!

## 💡 Need Help?

Check out the full [README.md](README.md) for detailed documentation and troubleshooting.
