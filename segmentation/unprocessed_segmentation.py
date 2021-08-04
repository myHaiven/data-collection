import logging
import sys
from pathlib import Path
from os import listdir
from os.path import isfile, join

from useful_functions.useful_functions import set_up_logging
from useful_functions.convert_to_wav import convert_to_wav

# Set up the logging
set_up_logging(log_path="logging/vad/", log_level=logging.INFO)
# Show system arguments
logging.info(f"System arguments: {sys.argv}")
from pathlib import Path  # For writing videos into the data folder
from pydub import AudioSegment  # This also requires ffmpeg on the device
import sys
import math


# in the case where you are not loping the date_folder is just a audio file folder
def get_file(date_folder):
    """
    Function that removes silences from all audio files in a folder.
    File structure is
    ```
    | data
    | |-- reddit
    |     |-- date_folder
    |         |-- filename_folder
    |             |-- audio_files
    ```
    
    Arguments:
        date_folder | pathlib.PosixPath
        Path to the date folder that contains the filename folders that contain
        the audio files that you want to remove silences from.
    """
    date_folder_path = Path(date_folder)
    # comment out to loop
    file_folder = date_folder_path
    input_filename = ''
    # Uncommnet to loop
    #for file_folder in date_folder_path.glob("[!.]*"):
        # Loop through raw files in the filename folders, excluding hidden
        # files
    # tab over to loop
    files = [f for f in listdir(file_folder) if isfile(join(file_folder, f))]
    if len(files) == 1:
        input_filename = Path(file_folder,Path(files[0]))
        if "_raw." in files[0]:
            audio_file_extension = Path(input_filename).suffix
            logging.info(f"Audio file extension: {audio_file_extension}")
            # If the file isn't a .wav file, convert it into a .wav file
            if audio_file_extension != ".wav":
                print("creating .wav")
                convert_to_wav(input_filename)
                # replace filename extension with .wav
                input_filename = Path(file_folder,Path(f"{input_filename.stem}.wav"))
        else:
            print(f"This folder does not contain a file with the correct format, skipping {file_folder}")
            # Uncomment below to allow loop to continue if looping
            #continue
            # Comment out the following to loop
            exit(1)
    elif not len(files):
        print(f"This folder does not contain any files, skipping {file_folder}")
        # Uncomment below to allow loop to continue if looping
        #continue
        # Comment out the following to loop
        exit(1)
    else:
        if any("processed.wav" in filename for filename in files):
            print(f"It appears this file has already been processed, skipping {file_folder}")
            # Uncomment below to allow loop to continue if looping
            #continue
            # Comment out the following to loop
            exit(1)
        raw_files = [file for file in files if "_raw." in file]
        input_filename = [file for file in raw_files if ".wav" in file]
        if not len(input_filename) and len(raw_files) == 1 :
            input_filename = Path(file_folder,Path(raw_files[0]))
            audio_file_extension = Path(input_filename).suffix
            logging.info(f"Audio file extension: {audio_file_extension}")
            # If the file isn't a .wav file, convert it into a .wav file
            if audio_file_extension != ".wav":
                print("creating .wav")
                convert_to_wav(input_filename)
                # replace filename extension with .wav
                input_filename = Path(file_folder,Path(f"{input_filename.stem}.wav"))
        elif not len(input_filename):
            print(f"This folder does not contain a file with the correct format or too many raw files, skipping {file_folder}")
            # Uncomment below to allow loop to continue if looping
            #continue
            # Comment out the following to loop
            exit(1)
        elif len(input_filename) == 1:
            print(".wav file already exists")
            input_filename = Path(file_folder, Path(input_filename[0]))
        else:
            print(f"Warning: There may be extra files inside of {file_folder}, check for extra files")
            # Uncomment below to allow loop to continue if looping
            #continue
            # Comment out the following to loop
            exit(1)
    return input_filename

folder_path = sys.argv[1]

input_filename = get_file(folder_path)
# Pydub uses milleseconds as the units; 10 000 is 10 seconds
thirty_seconds = 10 * 1000

# Import the file
audio_file = AudioSegment.from_file(input_filename)
# Determine the number of segments to loop through
number_of_segments = math.floor(audio_file.duration_seconds / 10)
# For each segment of at most 30 seconds, export the segment
for i in range(number_of_segments+1):
    current_segment = audio_file[i * thirty_seconds : (i + 1) * thirty_seconds]
    current_segment.export(
        Path(input_filename.parent, f"{input_filename.stem}_{i}.wav"), format="wav"
    )
    print(f"Segmented {input_filename.stem}_{i}.wav")

print("Segmentation finished")
