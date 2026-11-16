#!/usr/bin/env python3
"""Turn krillion.csv (the output of krillion.sh) into data.js for index.html.

Usage: python3 build.py [path/to/krillion.csv]
"""
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "krillion.csv"

rows, seen, replaced = [], set(), 0
with open(src, encoding="utf-8-sig", newline="") as f:
    for rec in csv.reader(f):
        if len(rec) < 5 or rec[0] == "sent":  # skip blanks and the header row
            continue
        sent, player, game, score, results = rec[:5]
        results = results.replace(" ", "").replace("️", "")
        if not results or not score.strip().lstrip("-").isdigit():
            continue
        # A player's first post for a game is the one that counts.
        key = (player, int(game))
        if key in seen:
            replaced += 1
            continue
        seen.add(key)
        # Only the game's own output is kept: game number, score, emoji line.
        # Anything else typed in the message (full_text) is ignored.
        rows.append({
            "sent": sent,
            "player": player,
            "game": int(game),
            "score": int(score),
            "results": list(results),
        })

data = {
    "built": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "repeatPostsIgnored": replaced,
    "rows": rows,
}
out = HERE / "data.js"
PREFIX = "window.KRILLION = "
if out.exists():
    # Leave the file untouched when the scores are the same, so the daily job
    # only publishes when there is something new.
    try:
        old = json.loads(out.read_text(encoding="utf-8").strip()[len(PREFIX):].rstrip(";"))
        if old.get("rows") == rows:
            print(f"No new scores ({len(rows)} already in {out.name})")
            sys.exit(0)
    except ValueError:
        pass
out.write_text("window.KRILLION = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
print(f"Wrote {out.name}: {len(rows)} scores, {replaced} repeat posts ignored")
