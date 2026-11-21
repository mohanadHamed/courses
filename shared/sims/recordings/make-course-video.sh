#!/bin/sh
# Make a course video (AUTHORING.md, "Blended courses") from its script and its pictures:
#
#   sh shared/sims/recordings/make-course-video.sh courses/digital-skills/week-01/videos folders
#   sh shared/sims/recordings/make-course-video.sh courses/big-data/week-01/videos lab1-intro <recordings-dir>
#
# The folder holds <name>-script.txt (the words: one caption line per line, a
# blank line between scenes) and <name>.html (the pictures, with video-kit.js).
# It writes <name>.mp4 (1280 x 720, H.264 and AAC), <name>.vtt (the captions:
# the lines of the script at the times of the voice) and <name>.png (the
# poster). The voice reads the script word for word: change the script, then
# run this again. With a recordings dir (the teacher's voice, one file per
# scene: courses/big-data/NOTES.md, "The prep video"), the voice is the
# teacher's; a scene without a recording is spoken by `say` (a draft).
# SCENE_SHOTS=<dir> also saves the end of every scene (scene-01.png …).
# Needs: macOS (say, Swift), Google Chrome and Quarto's Deno.
set -e
cd "$(dirname "$0")/../../.."
DIR="$1"; NAME="$2"; VOICE_DIR="$3"; FPS="${FPS:-30}"
DENO="${DENO:-$(dirname "$(readlink -f "$(command -v quarto)")")/tools/$(uname -m | sed 's/arm64/aarch64/')/deno}"
TMP="${TMPDIR:-/tmp}/course-video-$NAME"
rm -rf "$TMP"; mkdir -p "$TMP/frames"
swift shared/sims/recordings/make-voice.swift "$DIR/$NAME-script.txt" "$TMP/voice-full.m4a" "$DIR/$NAME.vtt" "$TMP/timing.json" ${VOICE_DIR:+"$VOICE_DIR"} 2>/dev/null
# A voice for speech: AAC at 48 kbit/s, one channel (a small file, also from a recording in stereo).
afconvert -f m4af -d aac -b 48000 -c 1 "$TMP/voice-full.m4a" "$TMP/voice.m4a"
"$DENO" run -A shared/sims/recordings/record-video.ts "$DIR/$NAME.html" "$TMP/timing.json" "$TMP/frames" "$FPS" "$DIR/$NAME.png" $POSTER
swift shared/sims/recordings/make-video.swift "$TMP/frames" "$FPS" "$TMP/voice.m4a" "$DIR/$NAME.mp4" "${BITRATE:-260000}" 2>/dev/null
ls -l "$DIR/$NAME.mp4" "$DIR/$NAME.vtt" "$DIR/$NAME.png"
