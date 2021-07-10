# Audio extraction

from pathlib import Path
from useful_functions import set_up_logging
import ffmpeg
import logging
import re


def extract_audio_from_video(
    video_path="data",
    video_extensions=[".mp4", ".mov"],
    log_level=logging.WARNING,
):
    """
    Function that goes into the directory and extracts audio from all `.mp4`
    files and outputs it into a folder called 'extracted_audio'
    
    Arguments:
    video_path | pathlib.PosixPath
    Path to the directory that contains all of the video files.
    
    Optional Arguments:
    to_folder | pathlib.PosixPath
    Path to the directory where you want to store the extracted audio. By default,
    it will be extracted into a folder in video_path's parent directory as 'extracted_audio'
    
    video_extensions | list
    A list of strings that contains the extensions you want ffmpeg to extract
    audio from. The default includes `.mp4` files and `.mov` files.
    
    log_level | int
    A integer representing the logging level. See
    https://docs.python.org/3/howto/logging.html#when-to-use-logging for 
    descriptions of the various levels
    
    Returns:
    It returns a string that tells you how many audio files were extracted.
    """

    # Make the data folder if it doesn't already exist
    Path(video_path).mkdir(exist_ok = True)
    
    # Make the extracted_audio folder if it doesn't already exist
    Path(to_folder).mkdir(exist_ok = True)
    
    set_up_logging(log_path = "logging/", log_level = log_level)
    
    # Create a counter for the number of audio files processed
    audio_file_counter = 0

    # Go through all files in `video_path`
    for child in video_path.iterdir():
        # Debugging: show the file name
        logging.debug(f"Detected file: {child.name}")
        # Store the extension of the file name
        file_extension = Path(child.name).suffix
        # If the file's extension is in `video_extensions`
        if file_extension in video_extensions:
            # Do an ffmpeg probe on the currently selected file
            current_probe = ffmpeg.probe(child)
            # If the number of streams is more than 1
            # (as a proxy for if the file could have audio)
            if len(current_probe["streams"]) > 1:
                # Check if `codec_type` is audio
                for stream in current_probe["streams"]:
                    # Debugging: print the codec type
                    logging.debug(f'Codec type: {stream["codec_type"]}')
                    # If the codec type is audio
                    if stream["codec_type"] == "audio":
                        # Debugging: print the video file's path
                        logging.debug(f"Audio codec detected: {child}")
                        # Store the video file path
                        new_child = str(child)
                        # Replace the extension with .mp3
                        new_child = re.sub(
                            pattern=f"{file_extension}$",
                            repl=".mp3",
                            string=new_child,
                        )

                        # Information about the ffmpeg command:
                        ## ffmpeg -i input.mp4 -vn -q:a 0 -map a audio.mp3
                        ## '-i' is the input, '-vn' excludes video,
                        ## '-q:a' is the mp3 encoding,
                        ## '0' is the best quality mp3 encoding,
                        ## '-map a' only grabs audio

                        # Using ffmpeg to transform the video file into a .mp3 file
                        try:
                            error_message = ffmpeg.input(str(child)) \
                            .output(filename = str(audio_file_path),
                                   **{'qscale:a': 0,
                                      'map': 'a'}) \
                            .overwrite_output() \
                            .run()
                            
                            # Create a variable to store the audio file's path
                            audio_file_path = Path(to_folder).joinpath(
                                Path(new_child).name
                            )
                            # Debugging: print the audio file's path
                            logging.debug('Audio file extracted to: ' +
                                          f'{audio_file_path}')
                        # Print the error message if the try doesn't work
                        except ffmpeg.Error as error_message:
                            print("ffmpeg stderr:", error_message.stderr())
                            raise error_message

                        audio_file_counter += 1
    # Return a print message that states how many audio files were extracted
    if audio_file_counter == 1:
        file_word = "file"
    else:
        file_word = "files"
    # Print how many audio files were extracted
    return str(audio_file_counter) + " audio " + file_word + " extracted!"


def test_audio_extraction():    
    # Testing function
    # Make the path to the data folder that contains the video files
    v_path_1 = Path.cwd().joinpath('data')
    # Make a directory that you want the extracted audio to go into
    a_path_1 = Path.cwd().joinpath('extracted_audio')
    # Show where the video files are coming from
    print("Video path: ", v_path_1)
    # Test the function
    extract_audio_from_video(video_path = v_path_1, to_folder = a_path_1,
                             log_level = logging.DEBUG)

test_audio_extraction()