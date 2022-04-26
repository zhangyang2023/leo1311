#!/bin/bash

# conda env list
# conda activate leo1311
# conda deactivate

dt=$(date +%Y%m%d)
nohup python -u leo1311_main.py > log/log."$dt" 2>&1 &

PIDS=$(pgrep -f leo1311_main.py)
echo "$PIDS"

if [ -n "$PIDS" ]
then
	echo "OK"
fi

# http://localhost:8008/algo-server