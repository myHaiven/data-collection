# segmentation.py
# Script that loops through a folder and segments audio into 30 second snippets
# or smaller

# This script has been update to only run one folder at a time
# Uncomment the noted lines to run the script on all folders in a single scrape

from pathlib import Path  # For writing videos into the data folder
from pydub import AudioSegment  # This also requires ffmpeg on the device
import sys
import math

# Uncomment to loop
#date_path = Path(Path.cwd().parent, "data", "reddit", sys.argv[1])
#date_path.glob("[!.]*")
# Comment out to loop
folder_path = sys.argv[1]


# Pydub uses milleseconds as the units; 10 000 is 10 seconds
ten_seconds = 10 * 1000

# Loop through folders in date folder, excluding hidden files
# Uncomment to loop
#for folder in date_path.glob("[!.]*"):
# Tab over to loop
# Uncomment to loop
# file_path = Path(next(Path(folder).glob("*_processed.wav")))
# Comment out to loop
file_path = Path(next(Path(folder_path).glob("*_processed.wav")))
# Import the file
audio_file = AudioSegment.from_file(file_path)
# Determine the number of segments to loop through
number_of_segments = math.floor(audio_file.duration_seconds / 10)
# For each segment of at most 10 seconds, export the segment
for i in range(number_of_segments+1):
    current_segment = audio_file[i * ten_seconds : (i + 1) * ten_seconds]
    current_segment.export(
        Path(file_path.parent, f"{file_path.stem}_{i}.wav"), format="wav"
    )
    print(f"Segmented {file_path.stem}_{i}.wav")

print("Segmentation finished")
