# data-collection

Data and automated tools for data collection

# Requirements

- The device must have [`ffmpeg`](https://ffmpeg.org/download.html) installed
- There must be a `praw.ini` file in the `reddit` folder
- The `useful_functions` setup must be done (see the setup section below)

# Example `praw.ini` file

```{praw.ini}
[bot1]
client_id=TYPE_YOUR_CLIENT_ID_HERE
client_secret=TYPE_YOUR_CLIENT_SECRET_HERE
password=TYPE_YOUR_PASSWORD_HERE
username=TYPE_YOUR_USERNAME_HERE
user_agent=bot1
```

Details can be found in the
[PRAW documentation](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html).

# Setup

## Setting up the Python environment

If using Python venv, you can use the code below to set up the code:

```{bash}
python3 -m pip install -r requirements.txt
```

If using Conda, you can use:

```{bash}
conda create --name <env> --file requirements.txt
conda activate <env>
conda install pip
```

The scripts `reddit_scraper.py`, `audio_extraction.py`, and `vad.py` require
imports from the folder `useful_functions`. Here are the steps to make the
imports work:

- Activate the Python environment
- Change directories into the `data-collection` folder
- Run `pip install -e .`

The imports should work afterwards.

The `pip install -e.` line

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
