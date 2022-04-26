#!/bin/bash

PIDS=$(pgrep -f leo1311_main.py)
echo "$PIDS"
kill -9 "$PIDS"

PIDS=$(pgrep -f leo1311_main.py)

if [ -n "$PIDS" ]
then
	echo "Fail"
	exit 1
fi
echo "Stopped"

