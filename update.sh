#!/bin/sh
# Pull fresh scores from Messages, rebuild data.js, and open the leaderboard.
# The terminal running this needs Full Disk Access to read ~/Library/Messages/chat.db.
set -e
cd "$(dirname "$0")"

./krillion.sh                       # writes ~/Desktop/krillion.csv
cp ~/Desktop/krillion.csv ./krillion.csv
python3 build.py
open index.html
