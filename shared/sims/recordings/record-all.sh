#!/bin/sh
# Record every simulator and mini-game that has a scenario, as an animated GIF
# next to it (sims/<name>.gif). The slides show the GIF next to the QR code.
#
#   sh shared/sims/recordings/record-all.sh [name ...]
#
# Needs: a local web server for the repository on port 4323
# (python3 -m http.server 4323), Google Chrome, Quarto's Deno, and Swift (Xcode).
set -e
cd "$(dirname "$0")/../../.."
DENO="${DENO:-$(dirname "$(command -v quarto)")/tools/$(uname -m | sed 's/arm64/aarch64/')/deno}"
TMP="${TMPDIR:-/tmp}/sim-recordings"
BASE="http://localhost:4323"

# name | page of the simulator | seconds | gif | window (3D scenes need a real window)
LIST="
harbor-guard|courses/game-math/week-01/sims/harbor-guard.html|9|courses/game-math/week-01/sims/harbor-guard.gif
comet-courier|courses/game-math/week-01/sims/comet-courier.html|11|courses/game-math/week-01/sims/comet-courier.gif
grid-strike|courses/game-math/week-01/sims/grid-strike.html|8|courses/game-math/week-01/sims/grid-strike.gif
vector-dash|courses/game-math/week-01/sims/vector-dash.html|10|courses/game-math/week-01/sims/vector-dash.gif
position-3d|courses/game-math/week-01/sims/position-3d.html|7|courses/game-math/week-01/sims/position-3d.gif|window
one-frame|courses/computing-systems/week-01/sims/one-frame.html|8|courses/computing-systems/week-01/sims/one-frame.gif
one-frame-slow|courses/computing-systems/week-01/sims/one-frame.html|9|courses/computing-systems/week-01/sims/one-frame-slow.gif
lag-lab|courses/computing-systems/week-01/sims/lag-lab.html|9|courses/computing-systems/week-01/sims/lag-lab.gif
data-trip|courses/computing-systems/week-02/sims/data-trip.html|9|courses/computing-systems/week-02/sims/data-trip.gif
pocket-pets|courses/computing-systems/week-02/sims/pocket-pets.html|10|courses/computing-systems/week-02/sims/pocket-pets.gif
lantern-keeper|courses/digital-media/week-01/sims/lantern-keeper.html|10|courses/digital-media/week-01/sims/lantern-keeper.gif
ember-trail|courses/digital-media/week-01/sims/ember-trail.html|10|courses/digital-media/week-01/sims/ember-trail.gif
juice-it|courses/digital-media/week-01/sims/juice-it.html|8|courses/digital-media/week-01/sims/juice-it.gif
sound-stage|courses/digital-media/week-01/sims/sound-stage.html|8|courses/digital-media/week-01/sims/sound-stage.gif
path-finder|courses/digital-skills/week-01/sims/path-finder.html|9|courses/digital-skills/week-01/sims/path-finder.gif
digcomp-check|courses/digital-skills/week-01/sims/digcomp-check.html|7|courses/digital-skills/week-01/sims/digcomp-check.gif
hiring-desk|courses/digital-skills/week-01/sims/hiring-desk.html|10|courses/digital-skills/week-01/sims/hiring-desk.gif
"
echo "$LIST" | while IFS='|' read -r name page secs gif mode; do
  [ -z "$name" ] && continue
  if [ $# -gt 0 ] && ! echo " $* " | grep -q " $name "; then continue; fi
  rm -rf "$TMP/$name"
  HEADLESS=$([ "$mode" = window ] && echo 0 || echo 1) "$DENO" run -A shared/sims/recordings/record.ts "$BASE/$page" "$TMP/$name" \
    "shared/sims/recordings/scenarios/$name.js" "$secs" 600
  swift shared/sims/recordings/make-gif.swift "$TMP/$name" "$gif" 560
done
