#!/bin/bash

YEAR=$1
MONTH=$2
DAY=$3

set -e

python ./download/download.py -d $YEAR-$MONTH-$DAY

python ./utilities/file_merger.py -d $YEAR-$MONTH-$DAY

python ./analysis/analyze_transactions_graph.py -c "config.json" -d $YEAR-$MONTH-$DAY

python ./analysis/analyze_random_graph.py -c "config_random.json" -d $YEAR-$MONTH-$DAY

python ./analysis/printer.py -d $YEAR-$MONTH-$DAY