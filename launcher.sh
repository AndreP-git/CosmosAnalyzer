#python ./analysis/analyze_transactions_graph.py -c "config.json" -d 2023-04-01

#!/bin/bash

YEAR=$1
MONTH=$2
DAY=$3

set -e

bash download/download.sh $YEAR $MONTH $DAY

python ./utilities/file_merger.py -d $YEAR-$MONTH-$DAY

python ./analysis/analyze_transactions_graph.py -c "config.json" -d $YEAR-$MONTH-$DAY

python analysis/analyze_random_graph.py -c "config_random.json" -d $YEAR-$MONTH-$DAY