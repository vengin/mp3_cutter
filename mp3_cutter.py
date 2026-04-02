import os
import argparse
import subprocess
import math
from pathlib import Path

# Paths to FFmpeg tools provided by user
FFMPEG_PATH = "d:/PF/_Tools/ffmpeg/bin/ffmpeg.exe"
FFPROBE_PATH = "d:/PF/_Tools/ffmpeg/bin/ffprobe.exe"


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


def cut_mp3(file_path, duration, chunk_size):
  """Cuts the MP3 file into smaller chunks."""
  total_chunks = math.ceil(duration / chunk_size)
  pad_length = len(str(total_chunks))
  
  # Create directory with the same name as the file (without extension)
  output_dir = file_path.parent / file_path.stem
  output_dir.mkdir(parents=True, exist_ok=True)
  
  print(f"Cutting '{file_path.name}' into {total_chunks} chunk(s) in directory '{output_dir.name}'")
  
  for i in range(total_chunks):
    start_time = i * chunk_size
    index_str = str(i + 1).zfill(pad_length)
    output_filename = f"{index_str}-{file_path.name}"
    output_path = output_dir / output_filename
    
    cmd = [
      FFMPEG_PATH,
      "-v", "error",
      "-y",  # Overwrite output files without asking
      "-i", str(file_path),
      "-ss", str(start_time),
      "-t", str(chunk_size),
      "-c", "copy",
      str(output_path)
    ]
    
    try:
      subprocess.run(cmd, check=True)
      print(f"  -> Created {output_filename}")
    except subprocess.CalledProcessError as e:
      print(f"  -> Error cutting chunk {i + 1} for {file_path.name}: {e}")


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

  print(f"\nProceeding to cut {len(files_to_cut)} file(s)...")
  for mp3, duration in files_to_cut:
    cut_mp3(mp3, duration, args.chunk_size)


if __name__ == "__main__":
  main()
