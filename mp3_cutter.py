import os
import argparse
import subprocess
from pathlib import Path

# Paths to FFmpeg tools provided by user
FFMPEG_PATH = r"d:\PF\_Tools\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"d:\PF\_Tools\ffmpeg\bin\ffprobe.exe"


def setup_args():
  parser = argparse.ArgumentParser(description="MP3 Cutter Script")
  parser.add_argument(
    "--scr-dir", 
    type=str, 
    required=True, 
    help="Directory to scan for MP3 files (including subfolders)."
  )
  parser.add_argument(
    "--max-duration", 
    type=float, 
    required=True, 
    help="Maximum duration threshold in seconds (MP3_MAX_DURATION_SZ)."
  )
  parser.add_argument(
    "--chunk-size", 
    type=float, 
    required=True, 
    help="Chunk size for cutting in seconds (MP3_CUT_CHUNK_SZ)."
  )
  return parser.parse_args()


def find_mp3_files(scr_dir):
  """Scans the directory and subdirectories for .mp3 files."""
  mp3_files = []
  directory = Path(scr_dir)
  for path in directory.rglob("*.mp3"):
    if path.is_file():
      mp3_files.append(path)
  return mp3_files


def get_duration(file_path):
  """Uses ffprobe to obtain the duration of an MP3 file in seconds."""
  cmd = [
    FFPROBE_PATH,
    "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    str(file_path)
  ]
  try:
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    duration = float(result.stdout.strip())
    return duration
  except (subprocess.CalledProcessError, ValueError) as e:
    print(f"Error getting duration for {file_path}: {e}")
    return 0.0


def main():
  args = setup_args()
  
  if not os.path.isdir(args.scr_dir):
    print(f"Error: Directory '{args.scr_dir}' does not exist.")
    return

  mp3_files = find_mp3_files(args.scr_dir)
  print(f"Found {len(mp3_files)} MP3 file(s) in '{args.scr_dir}'.")

  files_to_cut = []
  for mp3 in mp3_files:
    duration = get_duration(mp3)
    if duration > args.max_duration:
      print(f"File '{mp3.name}' duration: {duration:.2f}s (EXCEEDS {args.max_duration}s - will be cut)")
      files_to_cut.append((mp3, duration))
    else:
      print(f"File '{mp3.name}' duration: {duration:.2f}s (OK)")


if __name__ == "__main__":
  main()
