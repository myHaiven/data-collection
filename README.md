# data-collection

Data and automated tools for data collection

# Setup

The scripts `reddit_scraper.py`, `audio_extraction.py`, and `vad.py` require
imports from the folder `useful_functions`. Here are the steps to make the
imports work:

- Activate the Python environment
- Change directories into the `data-collection` folder
- Run `pip install -e .`

The imports should work afterwards.

## Changes for testing `reddit_scraper.py`

If you are only testing `reddit_scraper.py`, you can change the last line from
`test_functions(download_quantity=50)` to `test_functions(download_quantity=3)`
to speed up the process.

# Running the audio pipeline

Use `chmod u+x audio_pipeline.command` if needed to grant permission to run the
shell script. Afterwards, do `./audio_pipeline.command yyyy-mm-dd`, replacing
`yyyy-mm-dd` with the current date.

# References

- [Sibling package imports](https://stackoverflow.com/a/50193944)
