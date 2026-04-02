import os
import subprocess
import math
from pathlib import Path
import msvcrt


# Parameters
SRC_DIR             = "d:/work/python/!tools/mp3_cutter/src1" # Directory to scan for audio files (including subfolders)
AUDIO_MAX_DURATION_SZ = 60*60  # seconds (1 hour)
AUDIO_CUT_CHUNK_SZ    = 45*60  # seconds (30 minutes)
SKIP_EXISTING       = True   # If True, skips files that already have a generated sub-folder
AUDIO_EXTENSIONS    = {".mp3", ".m4b", ".m4a", ".wav", ".flac", ".ogg", ".aac"}

# Paths to FFmpeg tools provided by user
FFMPEG_PATH  = "d:/PF/_Tools/ffmpeg/bin/ffmpeg.exe"
FFPROBE_PATH = "d:/PF/_Tools/ffmpeg/bin/ffprobe.exe"


def find_audio_files(src_dir):
  """Scans the directory and subdirectories for supported audio files."""
  audio_files = []
  directory = Path(src_dir)
  for path in directory.rglob("*"):
    if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS:
      # Filter out cut output files by checking if they are inside an output folder
      potential_original = path.parent.parent / (path.parent.name + path.suffix)
      if potential_original.is_file():
        continue
      audio_files.append(path)
  return audio_files


def get_duration(file_path):
  """Uses ffprobe to obtain the duration of an audio file in seconds."""
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


def cut_audio(file_path, duration, chunk_size):
  """Cuts the audio file into smaller chunks."""
  total_chunks = math.ceil(duration / chunk_size)
  pad_length = len(str(total_chunks))

  # Create directory with the same name as the file (without extension)
  output_dir = file_path.parent / file_path.stem
  output_dir.mkdir(parents=True, exist_ok=True)

  print(f"Cutting '{file_path.name}' into {total_chunks} chunk(s) in directory '{output_dir.name}'")

  for i in range(total_chunks):
    start_time = i * chunk_size
    index_str = str(i + 1).zfill(pad_length)
    output_filename = f"{index_str} {file_path.name}"
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
      print(f"  -> {output_filename}")
    except subprocess.CalledProcessError as e:
      print(f"  -> Error cutting chunk {i + 1} for {file_path.name}: {e}")


def main():
  if not os.path.isdir(SRC_DIR):
    print(f"Error: Directory '{SRC_DIR}' does not exist.")
    return

  audio_files = find_audio_files(SRC_DIR)
  print(f"Found {len(audio_files)} audio file(s) in '{SRC_DIR}'.")

  files_to_cut = []
  for audio in audio_files:
    duration = get_duration(audio)
    if duration > AUDIO_MAX_DURATION_SZ:
      output_dir = audio.parent / audio.stem
      if SKIP_EXISTING and output_dir.is_dir():
        print(f"File '{audio.name}' skip: folder already exists")
      else:
        print(f"File '{audio.name}' duration: {duration:.2f}s (EXCEEDS {AUDIO_MAX_DURATION_SZ}s - will be cut)")
        files_to_cut.append((audio, duration))
    else:
      print(f"File '{audio.name}' duration: {duration:.2f}s (OK)")

  print(f"\nProceeding to cut {len(files_to_cut)} file(s)...")
  for audio, duration in files_to_cut:
    cut_audio(audio, duration, AUDIO_CUT_CHUNK_SZ)

  #input("\nPress Enter to exit...")
  print("Press any key to exit...")
  msvcrt.getch()

if __name__ == "__main__":
  main()
