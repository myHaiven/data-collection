#!/bin/bash

# Bash script for running the audio pipeline for a date folder

# Use `chmod u+x FILENAME` if permission denied

# Change to the directory containing the script
cd "${0%/*}"

PROGNAME=$0

# Error message
usage() {
  cat << EOF >&2
Usage: $PROGNAME [<source_path>] [<date_path>]

<source_path>: ...

<date_path>: ...

EOF
  exit 1
}
# Check that there are at least 2 arguments
if [ $# -lt 2 ]; then
    echo "Error, you need to supply a date path and a source path!"
    usage
    exit 1
fi

echo "Running audio pipeline"

source ~/Documents/Coding/anaconda3/etc/profile.d/conda.sh
conda activate audio_pipeline

SOURCE_NAME=$1
DATE=$2

cd ./reddit
python reddit_scraper.py

cd ../audio_extraction
python audio_extraction.py $DATE

cd ../silence-removal
python vad.py $DATE

cd ../segmentation
python segmentation.py $DATE

