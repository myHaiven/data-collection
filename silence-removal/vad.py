# Silence removal

import logging
import numpy as np
import scipy.io.wavfile as wf
import re
import sys
from pathlib import Path

from useful_functions.useful_functions import set_up_logging
from useful_functions.convert_to_wav import convert_to_wav

# Set up the logging
set_up_logging(log_path="logging/vad/", log_level=logging.INFO)
# Show system arguments
logging.info(f"System arguments: {sys.argv}")


class VoiceActivityDetection:
    def __init__(self):
        self.__step = 160
        self.__buffer_size = 160
        self.__buffer = np.zeros(shape=(0, 2), dtype=np.int16)
        self.__out_buffer = np.zeros(shape=(0, 2), dtype=np.int16)
        self.__n = 0
        self.__VADthd = 0.0  # Period used to convert to floating point number
        self.__VADn = 0.0
        self.__silence_counter = 0
        self.__channels = 0  # Number of audio channels

    # Voice Activity Detection
    # Adaptive threshold
    def vad(self, _frame, threshold=0.1):
        # Each _frame consists of 160 non-overlapping amplitude measurements

        # Check that the threshold is between 0 and 1
        if threshold < 0:
            raise Exception(f"Error, threshold: {threshold} is lower than 0.")
        elif threshold > 1:
            raise Exception(f"Error, threshold: {threshold} is larger than 1.")

        frame = np.array(_frame) ** 2.0
        max_frame = np.zeros(len(frame))
        for index, array in enumerate(frame):
            max_frame[index] = np.max(array)
        result = True
        threshold = 0.02
        thd = np.min(frame) + np.ptp(frame) * threshold
        # This is the previous frame's thd
        self.__VADthd = (self.__VADn * self.__VADthd + thd) / float(
            self.__VADn + 1.0
        )
        self.__VADn += 1.0

        # Take the mean of the maximum amplitudes across any channel
        if np.mean(max_frame) <= self.__VADthd:
            self.__silence_counter += 1
        else:
            self.__silence_counter = 0

        if self.__silence_counter > 60:
            result = False
        return result

    # Push new audio samples into the buffer.
    def add_samples(self, data):
        self.__buffer = np.append(self.__buffer, data, axis=0)
        result = len(self.__buffer) >= self.__buffer_size
        return result

    # Pull a portion of the buffer to process (pulled samples are deleted
    # after being processed)
    def get_frame(self):
        window = self.__buffer[: self.__buffer_size]
        self.__buffer = self.__buffer[self.__step :]
        return window

    # Adds new audio samples to the internal buffer and processes them
    def process(self, data):
        logging.debug(f"First frame of audio data:\n{data[ :160]}")
        # Detects mono or stereo audio
        self.__channels = self.get_audio_channels(data=data)
        if self.__channels == 1:
            logging.info("This is mono audio")
            # Reshape data so that it works with np.append(axis = 0)
            # and other functions that only work with 2d arrays
            data = data.reshape(len(data), 1)
            self.__buffer = np.zeros(shape=(0, 1), dtype=np.int16)
            self.__out_buffer = np.zeros(shape=(0, 1), dtype=np.int16)

        elif self.__channels == 2:
            logging.info("This is stereo audio")

        if self.add_samples(data):
            while len(self.__buffer) >= self.__buffer_size:
                # Framing
                window = self.get_frame()
                # Add window if threshold is met
                if self.vad(_frame=window, threshold=0.01):  # speech frame
                    self.__out_buffer = np.append(
                        self.__out_buffer, window, axis=0
                    )

    def get_voice_samples(self):
        # If mono audio, undo the earlier reshaping
        if self.__channels == 1:
            self.__out_buffer = self.__out_buffer.reshape(
                len(self.__out_buffer)
            )
            # Check that the resulting shape is 1d instead of 2d
            logging.debug(self.__out_buffer.shape)
        return self.__out_buffer

    def get_audio_channels(self, data):
        """
        Function that takes audio data and returns the number of audio   channels as an integer.
        
        Arguments:
        data | numpy.ndarray
        Audio data from
        `scipy.io.wavfile.read(filename = 'your_file_name')[1]`.
        
        Returns:
        int
        1 for mono audio, 2 for stereo audio
        """
        # Mono audio is just an array
        if len(data.shape) == 1:
            return 1
        # However stereo audio is an array of arrays where each inner array
        # is the audio of both sides at that particular time point
        elif data.shape[1] == 2:
            return 2
        else:
            raise Exception("Error, data is neither mono or stereo!")


def remove_silences(date_folder):
    """
    Function that removes silences from all audio files in a folder.
    File structure is
    ```
    | data
    | |-- reddit
    |     |-- date_folder
    |         |-- filename_folder
    |             |-- audio_file
    ```
    
    Arguments:
        date_folder | pathlib.PosixPath
        Path to the date folder that contains the filename folders that contain
        the audio files that you want to remove silences from.
    """

    # Loop through the source folders (Reddit, Streamable)
    for source in Path(Path.cwd().parent, "data").glob("[!.]*"):
        date_folder_path = Path(source, date_folder)
        for file_folder in date_folder_path.glob("[!.]*"):
            # Loop through raw files in the filename folders, excluding hidden
            # files
            for file in file_folder.glob("[!.]*_raw.???"):
                print(f"Path: {Path(file)}")
                input_filename = file
                new_filename = input_filename
                audio_file_extension = Path(input_filename).suffix
                logging.info(f"Audio file extension: {audio_file_extension}")
                # If the file isn't a .wav file, convert it into a .wav file
                if audio_file_extension != ".wav":
                    convert_to_wav(input_filename)
                    # replace filename extension with .wav
                    new_filename = f"{input_filename.stem}.wav"
                # Use the .wav file
                try:
                    wav = wf.read(str(Path(Path(file_folder), new_filename)))
                except (ValueError):
                    raise Exception(f"{new_filename} failed.")
                sample_rate = wav[0]
                audio_data = wav[1]
                logging.info(f"Audio data: {audio_data}")

                vad = VoiceActivityDetection()
                # Remove the silences
                vad.process(audio_data)
                # Get the processed audio
                voice_samples = vad.get_voice_samples()
                output_name = re.sub(
                    pattern=f"_raw\..*",
                    repl="_processed.wav",
                    string=Path(new_filename).name,
                )
                output_path = Path(Path(file).parent, output_name)
                # Write the processed audio into a new `.wav` file
                wf.write(f"{output_path}", sample_rate, voice_samples)
                print("done silence removal")


try:
    remove_silences(date_folder=sys.argv[1])
except (IndexError):
    raise Exception(
        f"Error, you must supply a date like the example below:\n"
        + "python vad.py 2021-07-14"
    )

