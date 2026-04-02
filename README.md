# MP3 Cutter

A script to recursively scan a directory for MP3 files and split them into equally sized chunks if they exceed a certain duration threshold.

## Requirements
- Python 3
- FFmpeg and FFprobe (Paths are configured at the top of `mp3_cutter.py`).

## Configuration
All parameters are configurable at the top of `mp3_cutter.py`:
- `SRC_DIR`: The root directory to scan for `.mp3` files (includes subfolders).
- `MP3_MAX_DURATION_SZ`: Maximum duration threshold (in seconds). Only files exceeding this length will be split.
- `MP3_CUT_CHUNK_SZ`: The duration of each split chunk (in seconds).
- `SKIP_EXISTING`: If True, gracefully skip re-cutting files that already contain a populated folder.

## Usage
Simply run the script with no arguments:
```cmd
python mp3_cutter.py
```

## Details
- Each split chunk will be saved inside a new folder created with the same name as the original MP3 file.
- The chunks are zero-padded numbered chronologically (e.g., `01-original_name.mp3`, `02-original_name.mp3`).
- Cutting is done securely without re-encoding via `ffmpeg -c copy`.
