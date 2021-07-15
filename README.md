# data-collection

Data and automated tools for data collection

# Setup

Reference: [Sibling package imports](https://stackoverflow.com/a/50193944)

The scripts `reddit_scraper.py`, `audio_extraction.py`, and `vad.py` require
imports from the folder `useful_functions`. To make this work, first activate
your Python environment. Then change directories into the `data-collection`
folder and run `pip install -e .`. The imports should work afterwards.

# Running the audio pipeline

Use `chmod u+x audio_pipeline.command` if needed to grant permission to run the
shell script. Afterwards, do `./audio_pipeline.command yyyy-mm-dd`, replacing
`yyyy-mm-dd` with the current date.
