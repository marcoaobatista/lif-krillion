#!/bin/zsh
# Daily refresh, run by the launchd job com.marco.krillion-leaderboard
# (~/Library/LaunchAgents/com.marco.krillion-leaderboard.plist).
# Pulls scores from Messages, rebuilds data.js, and pushes to GitHub if anything changed.
# Log: ~/Library/Logs/krillion-leaderboard.log
set -e
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
cd "$(dirname "$0")"

echo "--- $(date '+%Y-%m-%d %H:%M:%S') ---"
./krillion.sh                       # writes ~/Desktop/krillion.csv
cp ~/Desktop/krillion.csv ./krillion.csv
/usr/bin/python3 build.py           # leaves data.js alone if no new scores

if git diff --quiet -- data.js; then
  echo "Nothing to publish"
else
  git add data.js
  git commit -q -m "Scores through $(date '+%b %-d')"
  git push -q origin main
  echo "Published"
fi
