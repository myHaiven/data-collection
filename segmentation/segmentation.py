# segmentation.py

from pathlib import Path  # For writing videos into the data folder
from pydub import AudioSegment  # This also requires ffmpeg on the device
import sys

date_path = Path(Path.cwd().parent, "data", "reddit", sys.argv[1])

# Pydub uses milleseconds as the units; 10 000 is 10 seconds
ten_seconds = 10 * 1000

date_path.glob("[!.]*")

# Loop through folders in date folder, excluding hidden files
for folder in date_path.glob("[!.]*"):
    file_path = Path(next(Path(folder).glob("*_processed.wav")))
    # Import the file
    audio_file = AudioSegment.from_file(file_path)
    # Determine the number of segments to loop through
    number_of_segments = round(audio_file.duration_seconds / 10)
    # For each segment of at most 10 seconds, export the segment
    for i in range(number_of_segments):
        current_segment = audio_file[i * ten_seconds : (i + 1) * ten_seconds]
        current_segment.export(
            Path(file_path.parent, f"{file_path.stem}_{i}.wav"), format="wav"
        )
        print(f"{file_path.stem}_{i}.wav")
