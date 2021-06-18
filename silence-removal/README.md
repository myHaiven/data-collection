# Adaptive voice activity detection
Python script that cuts out silent audio sounds. [Original `vad.py`](https://github.com/mauriciovander/silence-removal) written by [mauriciovander](https://github.com/mauriciovander/)

## Table of contents
- [Adaptive voice activity detection](#adaptive-voice-activity-detection)
  - [Table of contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
    - [Directories](#directories)
  - [Usage](#usage)
  - [Details](#details)
  - [References:](#references)

--

## Prerequisites
The system must have [ffmpeg](https://ffmpeg.org/download.html) installed. On MacOS, this can be installed with [brew](https://formulae.brew.sh/formula/ffmpeg) via `brew install ffmpeg`.

### Directories
`vad.py` will generate a logging folder in its directory and generates the output to its directory as well. `useful_functions.py` and `convert_to_wav.py` should be in the same directory as `vad.py`.

## Usage
Examples of using the silence removal script `vad.py`:
```{python}
python vad.py './data/0no4f8nb0d351.aac' '0no4f8nb0d351_(processed)'
python vad.py './data/clip_(stereo).mp3' 'clip_(stereo)_(processed)'
python vad.py './data/taps_(mono).wav' 'taps_(mono)_(processed)'
```

## Details
<details><summary>Array formats for different audio channel types</summary>
For mono audio, the data is formatted as a single array of amplitude values. 
```{python}
[123, 123, 112]
```
For stereo audio, the data is formatted as an array of arrays, with the inner array listing the values for left and right amplitude values.
```{python}
[[123, 111], [123, 121], [221, 121]]
```
</details>

<details><summary>Log file contents</summary>
At the info level, the log file for `vad.py` shows the system arguments, audio file's filename and extension, the new audio filename, a preview of the amplitude data, and a confirmation of whether or not the audio is mono or stereo.  

At the debug level, it shows the first frame of amplitude measurements.

The `convert_to_wav` log file shows the before and after filenames.
</details>

<details><summary>Log file location</summary>
`vad.py` log files are located at `/silence-removal/logging/vad`. 
</details>

<details><summary>Log file naming and overwriting</summary>
The log file filenames are based on the current time and are unique to the minute. If a log is created and a file with the same name already exists, the new log will just be appended to the existing file.  
</details>


<details><summary>Logging levels</summary>
Logging levels can be adjusted in these lines of code for `vad.py`, `useful_functions.py`, and `.convert_to_wav.py`:
```
set_up_logging(log_path = "logging/vad2/",
               log_level = logging.INFO)
```
</details>

<details><summary>Modification to the algorithm for stereo audio</summary>
For the algorithm, it uses a threshold to check stuff. We should use the maximum of both sides of the stereo for the `np.mean` function so that it checks if any of the channels are above the threshold. I chose to go with maximum because we care when both sides are silent.
</details>

<details><summary>Numbers in the arrays generated by `scipy`</summary>
According to [derobert](https://stackoverflow.com/a/732830), the numbers from `scipy.io.wavfile.read` are amplitude measurements. I'm guessing that the start of the array are the amplitude measurements of the beginning of the audio and vice versa for the end of the array.
</details>

<details><summary>Silence removal threshold</summary>
The threshold for silence removal can be adjusted on this line of code: `if self.vad(_frame = window, threshold = 0.01):`. Higher numbers mean that more frames are counted as "silent" and therefore more audio segments are removed. Smaller numbers mean that less frames are considered "silent" and therefore more audio is preserved.
</details>

## References:
* [Original `vad.py`](https://github.com/mauriciovander/silence-removal) written by [mauriciovander](https://github.com/mauriciovander/)
* [derobert on how audio is represented in numbers](https://stackoverflow.com/a/732830)