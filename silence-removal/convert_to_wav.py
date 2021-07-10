# Script that converts audio files into .wav files

from datetime import datetime
from useful_functions import set_up_logging
from pathlib import Path
from pydub import AudioSegment  # This also requires ffmpeg on the device
import re
import logging

# Function that converts `.aac` or `.mp3` files to `.wav`
def convert_to_wav(audio_file_path):
    """
    Function that converts a `.aac` audio file into a `.wav` audio file.
    
    Arguments:
    audio_file_path | str
    The filename of the `.aac` audio file you want to convert into `.wav`.
    
    Returns:
    new_filename | str
    The filename of the `.wav` file.
    """
    # Set up the logging
    set_up_logging(log_path="logging/convert_to_wav/", log_level=logging.INFO)
    logging.info(f"Audio filename: {audio_file_path.name}")
    # Audio extension that will be converted to `.wav`
    audio_file_extension = audio_file_path.suffix
    audio_extensions = [".aac", ".mp3"]
    if audio_file_extension in audio_extensions:
        # Load the audio file
        sound = AudioSegment.from_file(audio_file_path)
        # Convert filename extension to `.wav`
        new_filename = re.sub(
            pattern=f"{audio_file_extension}$",
            repl=".wav",
            string=str(audio_file_path.name),
        )
        logging.info(f"New audio filename: {new_filename}")
        print(new_filename)
        sound.export(
            Path(Path(audio_file_path).parent, new_filename), format="wav"
        )
    else:
        raise Exception(
            f"The '{audio_file_extension}' " + "extension is not supported!"
        )

    return new_filename
