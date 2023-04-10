#!/bin/bash

YEAR=$1
MONTH=$2
DAY=$3

set -e   # set behaviour: exit the script if any command fails

echo "Downloading transactions of the day $YEAR/$MONTH/$DAY"

if test -d "data/Cosmos-$YEAR-$MONTH-$DAY"; then
    echo "Found pre-existing folder. Continue..."
else
    echo "Folder Cosmos-$YEAR-$MONTH-$DAY created."
    mkdir data/Cosmos-$YEAR-$MONTH-$DAY
fi

# python download/download.py -d 2023-04-01
python download/download.py -d "$YEAR-$MONTH-$DAY"

exit(0)
