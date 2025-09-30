## 1. Purpose

This project automates the process of **transcribing German audio files** to help with language learning.

It:

* Accepts a **pre-downloaded audio file** (e.g., `.wav`, `.mp3`) from a designated folder.
* Generates an **accurate German transcript** using **OpenAI Whisper**.
* Outputs the transcript in text file

---

## 2. Scope

The application will:

1. Take an **audio file** stored in a specific directory (e.g., `project_root/audio/`).
2. Transcribe the **spoken German** using **Whisper**.
3. Produce:
    - a file with the transcript 

Out of scope for MVP:

* Video downloading or audio extraction from video.
* Vocabulary translation or dictionary lookups.
* GUI front-end (CLI only for MVP).