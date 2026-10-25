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
vector-lab|courses/game-math/week-02/sims/vector-lab.html|9|courses/game-math/week-02/sims/vector-lab.gif
fair-speed|courses/game-math/week-02/sims/fair-speed.html|8|courses/game-math/week-02/sims/fair-speed.gif
raft-rush|courses/game-math/week-02/sims/raft-rush.html|10|courses/game-math/week-02/sims/raft-rush.gif
dot-lab|courses/game-math/week-02/sims/dot-lab.html|8|courses/game-math/week-02/sims/dot-lab.gif
shadow-cat|courses/game-math/week-02/sims/shadow-cat.html|8|courses/game-math/week-02/sims/shadow-cat.gif
turret-turn|courses/game-math/week-03/sims/turret-turn.html|9|courses/game-math/week-03/sims/turret-turn.gif
normal-lab|courses/game-math/week-03/sims/normal-lab.html|10|courses/game-math/week-03/sims/normal-lab.gif|window
projection-lab|courses/game-math/week-03/sims/projection-lab.html|9|courses/game-math/week-03/sims/projection-lab.gif
asteroid-beam|courses/game-math/week-03/sims/asteroid-beam.html|8|courses/game-math/week-03/sims/asteroid-beam.gif
unit-circle-lab|courses/game-math/week-04/sims/unit-circle-lab.html|9|courses/game-math/week-04/sims/unit-circle-lab.gif
drone-drop|courses/game-math/week-04/sims/drone-drop.html|8|courses/game-math/week-04/sims/drone-drop.gif
turn-lab|courses/game-math/week-04/sims/turn-lab.html|9|courses/game-math/week-04/sims/turn-lab.gif
wave-lab|courses/game-math/week-04/sims/wave-lab.html|9|courses/game-math/week-04/sims/wave-lab.gif
sky-lift|courses/game-math/week-04/sims/sky-lift.html|8|courses/game-math/week-04/sims/sky-lift.gif
gem-grid|courses/game-math/week-05/sims/gem-grid.html|9|courses/game-math/week-05/sims/gem-grid.gif
matrix-lab|courses/game-math/week-05/sims/matrix-lab.html|9|courses/game-math/week-05/sims/matrix-lab.gif
multiply-lab|courses/game-math/week-05/sims/multiply-lab.html|9|courses/game-math/week-05/sims/multiply-lab.gif
crystal-spells|courses/game-math/week-05/sims/crystal-spells.html|10|courses/game-math/week-05/sims/crystal-spells.gif
one-frame|courses/computing-systems/week-01/sims/one-frame.html|8|courses/computing-systems/week-01/sims/one-frame.gif
one-frame-slow|courses/computing-systems/week-01/sims/one-frame.html|9|courses/computing-systems/week-01/sims/one-frame-slow.gif
lag-lab|courses/computing-systems/week-01/sims/lag-lab.html|9|courses/computing-systems/week-01/sims/lag-lab.gif
data-trip|courses/computing-systems/week-02/sims/data-trip.html|9|courses/computing-systems/week-02/sims/data-trip.gif
pocket-pets|courses/computing-systems/week-02/sims/pocket-pets.html|10|courses/computing-systems/week-02/sims/pocket-pets.gif
parts-finder|courses/computing-systems/week-02/sims/parts-finder.html|9|courses/computing-systems/week-02/sims/parts-finder.gif
test-lab|courses/computing-systems/week-02/sims/test-lab.html|9|courses/computing-systems/week-02/sims/test-lab.gif
input-lab|courses/computing-systems/week-03/sims/input-lab.html|8|courses/computing-systems/week-03/sims/input-lab.gif
paint-race|courses/computing-systems/week-03/sims/paint-race.html|7|courses/computing-systems/week-03/sims/paint-race.gif
settings-tuner|courses/computing-systems/week-03/sims/settings-tuner.html|8|courses/computing-systems/week-03/sims/settings-tuner.gif
spec-check|courses/computing-systems/week-03/sims/spec-check.html|8|courses/computing-systems/week-03/sims/spec-check.gif
spec-match|courses/computing-systems/week-03/sims/spec-match.html|8|courses/computing-systems/week-03/sims/spec-match.gif
soc-explorer|courses/computing-systems/week-04/sims/soc-explorer.html|9|courses/computing-systems/week-04/sims/soc-explorer.gif
tilt-lab|courses/computing-systems/week-04/sims/tilt-lab.html|9|courses/computing-systems/week-04/sims/tilt-lab.gif
battery-lab|courses/computing-systems/week-04/sims/battery-lab.html|9|courses/computing-systems/week-04/sims/battery-lab.gif
marble-peak|courses/computing-systems/week-04/sims/marble-peak.html|9|courses/computing-systems/week-04/sims/marble-peak.gif
sheet-filter|courses/computing-systems/week-04/sims/sheet-filter.html|10|courses/computing-systems/week-04/sims/sheet-filter.gif
phone-picker|courses/computing-systems/week-04/sims/phone-picker.html|9|courses/computing-systems/week-04/sims/phone-picker.gif
scheduler-lab|courses/computing-systems/week-05/sims/scheduler-lab.html|8|courses/computing-systems/week-05/sims/scheduler-lab.gif
ram-rush|courses/computing-systems/week-05/sims/ram-rush.html|9|courses/computing-systems/week-05/sims/ram-rush.gif
settings-explorer|courses/computing-systems/week-05/sims/settings-explorer.html|9|courses/computing-systems/week-05/sims/settings-explorer.gif
help-ticket|courses/computing-systems/week-05/sims/help-ticket.html|8|courses/computing-systems/week-05/sims/help-ticket.gif
lantern-keeper|courses/digital-media/week-01/sims/lantern-keeper.html|10|courses/digital-media/week-01/sims/lantern-keeper.gif
ember-trail|courses/digital-media/week-01/sims/ember-trail.html|10|courses/digital-media/week-01/sims/ember-trail.gif
juice-it|courses/digital-media/week-01/sims/juice-it.html|8|courses/digital-media/week-01/sims/juice-it.gif
sound-stage|courses/digital-media/week-01/sims/sound-stage.html|8|courses/digital-media/week-01/sims/sound-stage.gif
story-sorter|courses/digital-media/week-02/sims/story-sorter.html|9|courses/digital-media/week-02/sims/story-sorter.gif
curve-builder|courses/digital-media/week-02/sims/curve-builder.html|8|courses/digital-media/week-02/sims/curve-builder.gif
stage-order|courses/digital-media/week-02/sims/stage-order.html|10|courses/digital-media/week-02/sims/stage-order.gif
branch-builder|courses/digital-media/week-03/sims/branch-builder.html|8|courses/digital-media/week-03/sims/branch-builder.gif
silent-station|courses/digital-media/week-03/sims/silent-station.html|10|courses/digital-media/week-03/sims/silent-station.gif
premise-doctor|courses/digital-media/week-03/sims/premise-doctor.html|7|courses/digital-media/week-03/sims/premise-doctor.gif
pitch-room|courses/digital-media/week-03/sims/pitch-room.html|8|courses/digital-media/week-03/sims/pitch-room.gif
script-formatter|courses/digital-media/week-04/sims/script-formatter.html|9|courses/digital-media/week-04/sims/script-formatter.gif
dialogue-doctor|courses/digital-media/week-04/sims/dialogue-doctor.html|9|courses/digital-media/week-04/sims/dialogue-doctor.gif
rooftop-rescue|courses/digital-media/week-04/sims/rooftop-rescue.html|11|courses/digital-media/week-04/sims/rooftop-rescue.gif
voice-match|courses/digital-media/week-04/sims/voice-match.html|8|courses/digital-media/week-04/sims/voice-match.gif
scene-cutter|courses/digital-media/week-04/sims/scene-cutter.html|10|courses/digital-media/week-04/sims/scene-cutter.gif
frame-lab|courses/digital-media/week-05/sims/frame-lab.html|9|courses/digital-media/week-05/sims/frame-lab.gif
shot-caller|courses/digital-media/week-05/sims/shot-caller.html|9|courses/digital-media/week-05/sims/shot-caller.gif
board-builder|courses/digital-media/week-05/sims/board-builder.html|10|courses/digital-media/week-05/sims/board-builder.gif
board-fixer|courses/digital-media/week-05/sims/board-fixer.html|9|courses/digital-media/week-05/sims/board-fixer.gif
path-finder|courses/digital-skills/week-01/sims/path-finder.html|9|courses/digital-skills/week-01/sims/path-finder.gif
digcomp-check|courses/digital-skills/week-01/sims/digcomp-check.html|7|courses/digital-skills/week-01/sims/digcomp-check.gif
hiring-desk|courses/digital-skills/week-01/sims/hiring-desk.html|10|courses/digital-skills/week-01/sims/hiring-desk.gif
time-saver|courses/digital-skills/week-01/sims/time-saver.html|10|courses/digital-skills/week-01/sims/time-saver.gif
app-launcher|courses/digital-skills/week-01/sims/app-launcher.html|10|courses/digital-skills/week-01/sims/app-launcher.gif
ai-chat|courses/digital-skills/week-01/sims/ai-chat.html|10|courses/digital-skills/week-01/sims/ai-chat.gif
office-day|courses/digital-skills/week-01/sims/office-day.html|9|courses/digital-skills/week-01/sims/office-day.gif
next-word|courses/digital-skills/week-02/sims/next-word.html|10|courses/digital-skills/week-02/sims/next-word.gif
weak-spots|courses/digital-skills/week-02/sims/weak-spots.html|10|courses/digital-skills/week-02/sims/weak-spots.gif
right-tool|courses/digital-skills/week-02/sims/right-tool.html|10|courses/digital-skills/week-02/sims/right-tool.gif
newsletter|courses/digital-skills/week-02/sims/newsletter.html|10|courses/digital-skills/week-02/sims/newsletter.gif
window-tour|courses/digital-skills/week-03/sims/window-tour.html|9|courses/digital-skills/week-03/sims/window-tour.gif
ribbon-finder|courses/digital-skills/week-03/sims/ribbon-finder.html|9|courses/digital-skills/week-03/sims/ribbon-finder.gif
save-lab|courses/digital-skills/week-03/sims/save-lab.html|10|courses/digital-skills/week-03/sims/save-lab.gif
help-desk|courses/digital-skills/week-03/sims/help-desk.html|9|courses/digital-skills/week-03/sims/help-desk.gif
pdf-export|courses/digital-skills/week-03/sims/pdf-export.html|10|courses/digital-skills/week-03/sims/pdf-export.gif
paste-lab|courses/digital-skills/week-03/sims/paste-lab.html|9|courses/digital-skills/week-03/sims/paste-lab.gif
share-settings|courses/digital-skills/week-03/sims/share-settings.html|9|courses/digital-skills/week-03/sims/share-settings.gif
format-lab|courses/digital-skills/week-04/sims/format-lab.html|9|courses/digital-skills/week-04/sims/format-lab.gif
style-lab|courses/digital-skills/week-04/sims/style-lab.html|9|courses/digital-skills/week-04/sims/style-lab.gif
list-table-lab|courses/digital-skills/week-04/sims/list-table-lab.html|8|courses/digital-skills/week-04/sims/list-table-lab.gif
notice-maker|courses/digital-skills/week-04/sims/notice-maker.html|10|courses/digital-skills/week-04/sims/notice-maker.gif
page-setup-lab|courses/digital-skills/week-04/sims/page-setup-lab.html|9|courses/digital-skills/week-04/sims/page-setup-lab.gif
header-footer-lab|courses/digital-skills/week-04/sims/header-footer-lab.html|8|courses/digital-skills/week-04/sims/header-footer-lab.gif
toc-builder|courses/digital-skills/week-04/sims/toc-builder.html|9|courses/digital-skills/week-04/sims/toc-builder.gif
word-ai-lab|courses/digital-skills/week-05/sims/word-ai-lab.html|10|courses/digital-skills/week-05/sims/word-ai-lab.gif
tone-lab|courses/digital-skills/week-05/sims/tone-lab.html|9|courses/digital-skills/week-05/sims/tone-lab.gif
morning-desk|courses/digital-skills/week-05/sims/morning-desk.html|8|courses/digital-skills/week-05/sims/morning-desk.gif
"
echo "$LIST" | while IFS='|' read -r name page secs gif mode; do
  [ -z "$name" ] && continue
  if [ $# -gt 0 ] && ! echo " $* " | grep -q " $name "; then continue; fi
  rm -rf "$TMP/$name"
  HEADLESS=$([ "$mode" = window ] && echo 0 || echo 1) "$DENO" run -A shared/sims/recordings/record.ts "$BASE/$page" "$TMP/$name" \
    "shared/sims/recordings/scenarios/$name.js" "$secs" 600
  swift shared/sims/recordings/make-gif.swift "$TMP/$name" "$gif" 560
done
