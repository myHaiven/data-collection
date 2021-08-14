#!/bin/bash

# Bash script for running the audio pipeline for a date folder

# To test the files, do `path/to/audio_pipeline.command /path/to/source/date`

# The reddit scraper will download files to current date
# The other scripts will use 2021-07-08 to test source and audio extraction
# robustness

# Use `chmod u+x audio_pipeline.command` if permission denied

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
source /dataprocessing/data-collection/venv/bin/activate

# If using conda, source the conda.sh and then activate your environment like
# so:
# source /home/jackiel/miniconda3/etc/profile.d/conda.sh
# conda activate test-env

PROCESSINGPATH=$(pwd)

# uncomment to run a scrape
#cd ./reddit
# /home/jackiel/data-collection/venv/bin/python reddit_scraper.py
# which python
export PATH=$PATH:/dataprocessing/data-collection/venv/bin/

filepath=$1

cd $filepath

for folder in */
do
  echo "Processing $folder"

  cd $PROCESSINGPATH/segmentation/
  python unprocessed_segmentation.py "$filepath/$folder"

  cd $PROCESSINGPATH/silence-removal/
  python split_silence-removal.py "$filepath/$folder"

  cd $PROCESSINGPATH/segmentation
  python resegment.py "$filepath/$folder"

done
