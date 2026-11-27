#!/bin/sh
# The screens of the Big Data Lab 2 worksheet: each one is the BigQuery Lab
# simulator itself (courses/big-data/week-02/sims/bq-lab2.html?shot=<name>),
# with its orange numbers, taken with headless Chrome. The worksheet is done
# on this simulator (no Google account), so its pictures match it exactly.
#
#   python3 -m http.server 8765 --bind 127.0.0.1 &     # from the project root (or BASE=<url of _site>)
#   sh tools/bq_sim_shots.sh                           # every screen
#   sh tools/bq_sim_shots.sh count                     # one screen
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE="${BASE:-http://127.0.0.1:8765}/courses/big-data/week-02/sims/bq-lab2.html"
OUT="courses/big-data/week-02/images"
# name:height (the width is 1000)
SHOTS="menu-ds:330 dataset:600 menu-tbl:330 upload:600 picker:600 table:600 schema:470 details:430 preview:470 where:600"
PROFILE=$(mktemp -d)
for s in $SHOTS; do
  name=${s%%:*}; h=${s##*:}
  [ -n "$1" ] && [ "$1" != "$name" ] && continue
  "$CHROME" --headless=new --user-data-dir="$PROFILE" --hide-scrollbars --force-device-scale-factor=1.5 \
    --window-size=1000,"$h" --virtual-time-budget=8000 --screenshot="$OUT/bq2-$name.png" "$BASE?shot=$name" 2>/dev/null
  echo "$OUT/bq2-$name.png"
done
rm -rf "$PROFILE"
