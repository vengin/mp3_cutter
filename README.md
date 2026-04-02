# Audio Cutter

A script to recursively scan a directory for audio files (mp3, m4b, m4a, wav, flac, ogg, aac) and split them into equally sized chunks or by a CUE sheet if present.

## Features
- **Smart Detection**: Automatically detects companion `.cue` files (e.g., `audiobook.cue` for `audiobook.m4b`).
- **Precision Cutting**: If a `.cue` file is found, the script uses it for exact track/chapter splitting.
- **Fixed-Size Splitting**: If no cuesheet is found, files exceeding `AUDIO_MAX_DURATION_SZ` are split into `AUDIO_CUT_CHUNK_SZ` parts.
- **Git Aware**: Designed to be tracked and versioned.

## Requirements
- Python 3
- FFmpeg and FFprobe (Paths are configured at the top of `mp3_cutter.py`).

## Configuration
All parameters are configurable at the top of `mp3_cutter.py`:
- `SRC_DIR`: The root directory to scan for audio files (includes subfolders).
- `AUDIO_MAX_DURATION_SZ`: Maximum duration threshold (in seconds). Only files exceeding this length without a cuesheet will be split.
- `AUDIO_CUT_CHUNK_SZ`: The duration of each split chunk (in seconds) for files without a cuesheet.
- `SKIP_EXISTING`: If True, gracefully skip re-cutting files that already contain a populated folder.
- `AUDIO_EXTENSIONS`: A set of file extensions that the script will process.

## Usage
Simply run the script with no arguments:
```cmd
python mp3_cutter.py
```

## Details
- Each split chunk will be saved inside a new folder created with the same name as the original audio file.
- **Filename Format (Fixed Size)**: `{index_str} {original_filename}`.
- **Filename Format (CUE based)**: `{index_str} {original_filename} {track_title}`.
- Cutting is done securely without re-encoding via `ffmpeg -c copy`.
