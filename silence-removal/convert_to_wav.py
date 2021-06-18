# Script that converts audio files into .wav files

from datetime import datetime
from useful_functions import set_up_logging
from pathlib import Path
from pydub import AudioSegment # This also requires ffmpeg on the device
import re
import logging

# Function that converts `.aac` or `.mp3` files to `.wav`
def convert_to_wav(audio_filename):
    """
    Function that converts a `.aac` audio file into a `.wav` audio file.
    
    Arguments:
    audio_filename | str
    The filename of the `.aac` audio file you want to convert into `.wav`.
    
    Returns:
    new_filename | str
    The filename of the `.wav` file.
    """
    # Set up the logging
    set_up_logging(log_path = "logging/convert_to_wav/",
                   log_level = logging.INFO)
    logging.info(f"Audio filename: {audio_filename}")
    # Audio extension that will be converted to `.wav`
    audio_extensions = [".aac", ".mp3"]
    audio_file_extension = re.search(pattern = "\.\w+$",
                                     string = audio_filename).group(0)
    
    if audio_file_extension in audio_extensions:
        # Load the audio file
        sound = AudioSegment.from_file(audio_filename)
        # Convert filename extension from `.aac` to `.wav`
        new_filename = re.sub(pattern = f"\.{audio_file_extension}$",
                              repl = ".wav",
                              string = audio_filename)
        logging.info(f"New audio filename: {new_filename}")
        sound.export(new_filename, format = "wav")
    else:
        raise Exception(f"The '{audio_file_extension}' " +
                        "extension is not supported!")
    
    return new_filename
