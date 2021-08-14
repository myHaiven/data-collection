# reddit_scraper.py

from datetime import datetime
import praw
import requests
import re
from pathlib import Path  # For writing videos into the data folder
import logging

from useful_functions.useful_functions import set_up_logging

# Requirements

# This file should be named `reddit_scraper.py`; the path to the script is
# hard coded at
# ```{python}
# script_name = "reddit_scraper.py"
# path1 = Path("./", script_name)
# ```

# Make sure the praw.ini file is in the correct directory

# Also, make sure there is a folder called "data" in the same directory that
# contains this script so that download_media() works. The path to data folder
# is hard coded at `data_path = Path("../data").resolve()` in the
# `download_media()` function

# Set up the logging
set_up_logging(log_path="logging/reddit_scraper/", log_level=logging.INFO)


def convert_streamable(url):
    """
    Convert streamable url from reddit to actual video url
    
    Arguments:
    url | string | the streamable link that reddit gives you
    
    Returns:
    video_url | string | the link to the actual video
    """

    # Replace streamable.com with api.streamable.com/videos to get the api link
    api_url = re.sub(
        string=url,
        pattern="streamable\.com/",
        repl="api.streamable.com/videos/",
    )
    # The api link gets us a json file, we use json() to decode it
    json1 = requests.get(api_url).json()
    # Access the video url in the json file
    video_url = json1["files"]["mp4"]["url"]

    return video_url


def convert_reddit(video_url):
    """
    Convert v.redd.it video url into audio url
    
    Arguments:
    video_url | string | the fallback video url from reddit's secure media
    
    Returns:
    audio_url | string | the audio url inferred from the fallback video url;
    this can be obtained in the DASHPlaylist.mpd file, search for the base url 
    and audio sections
    """
    audio_url = ""

    # If there is a .mp4 extension in the url, replace with "DASH_audio.mp4"
    if bool(re.search(string=video_url, pattern="\/DASH_\d{2,4}\.mp4")):
        audio_url = re.sub(
            string=video_url,
            pattern="\/DASH_\d{2,4}\.mp4",
            repl="/DASH_audio.mp4",
        )

    # Else if there is no .mp4 extension in the url, just replace with "audio"
    elif bool(re.search(string=video_url, pattern="\/DASH_(\d{2,4})\?")):
        audio_url = re.sub(
            string=video_url, pattern="\/DASH_(\d{2,4})\?", repl="/audio?"
        )
    # Else notify user that no match was detected
    else:
        print("error, no match detected")
        logging.info(f"No match detected with video url: f{video_url}")

    return audio_url


def audio_url_from_submission(submission):
    """
    Get the audio file urls from the given submission
    
    Arguments:
    submission | praw.models.reddit.submission.Submission | the elements in the 
    listing generator you get these when you iterate through a listing 
    generator Ex. `for i in reddit.subreddit("PublicFreakout").top(limit = 3):`
    
    Returns:
    audio_url | string array | array that contains the links to the relevant 
    files if the link is streamable, it will be a list of size 1 linking to the 
    video because the video contains audio if the link is reddit, it will be a 
    list of size 2 with the first element linking to the video graphics and the 
    second element linking to the audio
    
    Example conversions:
    https://streamable.com/u2jzoo into https://api.streamable.com/videos/u2jzoo,
    then retrieve url from json
    
    For reddit, get subreddit post, find the fall back video url
    and the audio url by replacing parts
    Example: 
    https://v.redd.it/9v2san14was51/DASH_720.mp4?source=fallback to
    https://v.redd.it/9v2san14was51/DASH_audio.mp4?source=fallback
    
    https://v.redd.it/w56rwny74y351/DASH_360?source=fallback to
    https://v.redd.it/w56rwny74y351/audio?source=fallback
    """

    # Initialize the string array
    url_array = []
    # I'm using an array because Streamable gives us audio + video in one file
    # but Reddit has two links, one for video (graphics) only and one for audio
    # only

    # Check if it's streamable or reddit
    # If streamable
    if submission.domain == "streamable.com":
        # Convert the streamable url to the actual video url
        video_url = convert_streamable(submission.url)
        # Append the url to the array
        url_array.append(video_url)

    # If reddit
    elif submission.domain == "v.redd.it":
        try:
            # Get the url from secure_media instead
            video_url = submission.secure_media["reddit_video"]["fallback_url"]
        except:
            # Try causes an error if it's a crosspost. We have to access
            # crosspost_parent_list,
            # 0, secure_media, etc.
            # Example:
            # https://www.reddit.com/r/PublicFreakout/comments/hafl7q/cop_chokes_and_punches_teenage_girl_in_the_head.json
            video_url = submission.crosspost_parent_list[0]["secure_media"][
                "reddit_video"
            ]["fallback_url"]

        ### # Append the video url to the list
        ### url_array.append(video_url)
        # Get the audio
        audio_url = convert_reddit(video_url)
        url_array.append(audio_url)

    else:
        print(f"This script does not support {submission.domain}")
        logging.info(f"Unable to handle submission domain: {submission.domain}")

    return url_array


# Function for downloading video or audio files from subreddit urls
def download_media(url):
    """
    Download a file from a url
    
    Arguments:
    url | string | the link that you want to download from
    audio | boolean | True will set the extension to .aac, False will set the 
    extension to .mp4

    Returns:
    local_filename | string | name of the downloaded file
    """

    # Check the root website
    root_url = url.split("/")[2]
    logging.info(f"Processing video from : {url}")

    source = ""
    current_date = datetime.now().strftime("%Y-%m-%d")
    base_filename = ""

    # If this is reddit
    if re.search(string=root_url, pattern="^v\.redd\.it"):
        source = "reddit"
        # If the url is an audio url
        if re.search(string=url, pattern="/.*audio"):
            file_suffix = "_raw.aac"
        else:
            file_suffix = ".mp4"
        # Use the second last part of the url within the slashes, it
        # should be unique
        base_filename = url.split("/")[-2]
        local_filename = f"{base_filename}{file_suffix}"

    # If this is streamable, chop off the stuff after .mp4
    elif re.match(string=root_url, pattern="^.*streamable.com"):
        source = "streamable"
        filename_part = re.sub(
            string=url.split("/")[-1], pattern="(?<=\.mp4).*", repl=""
        )
        base_filename = url.split("/")[-1]
        local_filename = f"{filename_part}.mp4"

    else:
        # Create file name with the last part of the url within the slashes
        base_filename = url.split("/")[-1]
        local_filename = url.split("/")[-1]
        logging.info(f"{local_filename} not from reddit or streamable")

    # Name of script
    script_name = "reddit_scraper.py"
    path1 = Path(Path.cwd() / script_name)

    # Create a path for the data folder
    data_path = Path("../data").resolve()
    # If the data folder doesn't exist
    if not data_path.is_dir():
        # Create the data folder
        data_path.mkdir()

    # Check that the script is a file
    if path1.is_file():
        # This is the absolute path we want our file to be written in
        path2 = Path(
            path1.resolve().parent.parent,
            "data",
            source,
            current_date,
            base_filename,
        )
        if not path2.is_dir():
            path2.mkdir(parents=True)
        # This is the file with the path that open will write to
        path3 = Path(path2, local_filename)

    # Using with to automatically close the connection when we are done with it
    with requests.get(url, stream=True) as req:
        # Raise an http error if there is one
        if not req.ok:
            logging.info(req)
            logging.info(
                f"No file will be downloaded, removing empty directory: {path2}"
            )
            # Remove empty directory because we don't expect to have a file
            path2.rmdir()
        else:
            # Write the file in binary
            with open(path3, "wb") as video_file:
                for chunk in req.iter_content(chunk_size=4000):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    video_file.write(chunk)

    return local_filename


def test_functions(download_quantity=2):
    # Connect to Reddit's API
    reddit = praw.Reddit("bot1", user_agent="bot1")
    # Check that the praw.ini file worked
    logging.info(reddit.user.me())
    # Link to json file with streamable and reddit links as of Oct. 13, 2020
    # https://www.reddit.com/r/PublicFreakout/top/.json?t=year

    # Select the public freakout subreddit
    sr1 = reddit.subreddit("PublicFreakout")
    # Select the top 10 (it is selecting top 10 of the year by default)
    top1 = sr1.top(time_filter="year", limit=download_quantity)
    # Initialize arrays
    urls = []
    # Place the relevant info into the array from the selected top 3
    for i in top1:
        logging.info(len(urls))
        try:
            urls.append(audio_url_from_submission(i))
        except:
            logging.info(
                f"Exception: {urls.append(audio_url_from_submission(i))}"
            )
    print("urls appended, starting downloads")
    # Download the videos
    for i in range(len(urls)):
        for j in range(len(urls[i])):
            try:
                download_media(urls[i][j])
            except Exception as exception:
                # Getting this HTTP error
                # 403 Client Error: Forbidden for url:
                # https://v.redd.it/716d4vdxcqu41/audio?source=fallback
                # Also, some of the posts are not videos. When printing the #
                # length of the url, sometimes it says "errorgfycat.com" or
                # "errori.redd.it" for example.
                logging.info(f"Error with post number {str(i)}")
                logging.info(f"Exception: {exception}")
    print("reddit_scraper.py finished")


# Take daily top 50 links from the public freakout subreddit and attempt to
# download

# Only execute this if run as a script
if __name__ == "__main__":
    test_functions(download_quantity=2)
