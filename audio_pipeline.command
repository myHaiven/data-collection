#!/bin/bash

# Bash script for running the audio pipeline for a date folder

# To test the files, do `path/to/audio_pipeline.command /path/to/source/date`

# The reddit scraper will download files to current date
# The other scripts will use 2021-07-08 to test source and audio extraction
# robustness

# Use `chmod u+x audio_pipeline.command` if permission denied

# Change to the directory containing the script
cd "${0%/*}"

PROGNAME=$0

# Error message
usage() {
  cat << EOF >&2
Usage: $PROGNAME [<date>]

<date>: ...

EOF
  exit 1
}
# Check that there are at least 2 arguments
if [ $# -lt 1 ]; then
    echo "Error, you need to supply a date!"
    usage
    exit 1
fi

echo "Running audio pipeline"

# If using Python venv, replace the line below with your venv activation line
source test-env/bin/activate

# If using conda, source the conda.sh and then activate your environment like
# so:
# source /home/jackiel/miniconda3/etc/profile.d/conda.sh
# conda activate test-env

PATH=$1
PROCESSINGPATH=$(pwd)

# uncomment to run a scrape
#cd ./reddit
#python reddit_scraper.py

for folder in $PATH
do
  echo "Processing $folder files"

  python $PROCESSINGPATH/audio_extraction/audio_extraction.py $folder

  python $PROCESSINGPATH/silence-removal/vad.py $folder

  python $PROCESSINGPATH/segmentation/segmentation.py $folder

done

