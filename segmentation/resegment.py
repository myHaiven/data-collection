# segmentation.py
# Script that loops through a folder and segments audio into 30 second snippets
# or smaller


from pathlib import Path  # For writing videos into the data folder
from pydub import AudioSegment  # This also requires ffmpeg on the device
import sys
from os import listdir
from os.path import isfile, join
import re
import math

folder_path = sys.argv[1]
input_filename = folder_path.split('/')[-2]
print(input_filename)

files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
to_join = [AudioSegment.from_file(Path(folder_path,Path(file))) for file in files if re.search("_processed_.*.wav$", file) ]

joined_file = sum(to_join)

# Pydub uses milleseconds as the units; 10 000 is 10 seconds
ten_seconds = 10 * 1000

number_of_segments = math.floor(joined_file.duration_seconds / 10)
# For each segment of at most 10 seconds, export the segment
for i in range(number_of_segments+1):
    current_segment = joined_file[i * ten_seconds : (i + 1) * ten_seconds]
    current_segment.export(
        Path(folder_path, f"{input_filename}_processed_{i}.wav"), format="wav"
    )
    print(f"Segmented {input_filename}_processed_{i}.wav")

print("Segmentation finished")
