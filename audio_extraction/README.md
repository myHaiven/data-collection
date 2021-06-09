# Audio extraction
Python script that extracts audio from video files.

# Table of contents
- [Audio extraction](#audio-extraction)
- [Table of contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
    - [Directories](#directories)
  - [Usage](#usage)
  - [Details](#details)

## Prerequisites
The system must have [ffmpeg](https://ffmpeg.org/download.html) installed. On MacOS, this can be installed with [brew](https://formulae.brew.sh/formula/ffmpeg) via `brew install ffmpeg`.

The video files should be in a folder named "data". The "data" folder should be in the same directory that contains `audio_extraction.py`.

### Directories
By default, `audio_extraction.py` reads video files from the "data" folder. This can be changed by changing the `video_path` argument in the `extract_audio_from_video` call. `audio_extraction.py` will generate a logging folder in its directory and generates the extracted audio to the "extracted audio" folder.

## Usage
Extract audio from the "data" folder:
`python audio_extraction.py`

## Details
<details><summary>Logging levels</summary>
The logging level details can be found at https://docs.python.org/3/howto/logging.html#when-to-use-logging .
</details>
