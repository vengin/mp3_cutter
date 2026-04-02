# MP3 Cutter

A script to recursively scan a directory for MP3 files and split them into equally sized chunks if they exceed a certain duration threshold.

## Requirements
- Python 3
- FFmpeg and FFprobe (Paths are configured at the top of `mp3_cutter.py`).

## Usage
Run the script passing the required arguments:
- `--scr-dir`: The root directory to scan for `.mp3` files (includes subfolders).
- `--max-duration`: Maximum duration threshold (in seconds). Only files exceeding this length will be split.
- `--chunk-size`: The duration of each split chunk (in seconds).

### Example
```cmd
python mp3_cutter.py --scr-dir "C:\Music\Podcasts" --max-duration 3600 --chunk-size 600
```

## Details
- Each split chunk will be saved inside a new folder created with the same name as the original MP3 file.
- The chunks are zero-padded numbered chronologically (e.g., `01-original_name.mp3`, `02-original_name.mp3`).
- Cutting is done securely without re-encoding via `ffmpeg -c copy`.
