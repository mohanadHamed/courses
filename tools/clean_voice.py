"""The teacher's recording of a prep video, cleaned before the video is made
(courses/big-data/NOTES.md, "The prep video").

  python3 tools/clean_voice.py find <recording> [--lang ar-SA]
      Hears the recording on this Mac (macOS speech recognition, on-device,
      tools/transcribe_voice.swift) and prints its words with their times,
      then the places where words are said twice in a row: a sentence read
      wrong and read again. macOS asks once to allow speech recognition.

  python3 tools/clean_voice.py cut <recording> <out.wav> 60.95-64.30 [...]
      Writes the recording without the given parts (seconds), for example the
      first, wrong reading of a sentence: cut from the start of the wrong
      reading to the start of the right one.

The long pauses are shortened later, inside each scene, by
shared/sims/recordings/make-voice.swift (MAX_PAUSE). Only the tools of macOS
(afconvert, swiftc, the Speech framework) and Python's standard library.
"""
import json, math, os, re, struct, subprocess, sys, tempfile, wave

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.expanduser("~/Library/Application Support/courses-voice/Transcribe.app")
PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleIdentifier</key><string>local.courses.transcribe</string>
<key>CFBundleName</key><string>Transcribe</string>
<key>CFBundleExecutable</key><string>transcribe</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>LSUIElement</key><true/>
<key>NSSpeechRecognitionUsageDescription</key><string>To write the words of a recording of the teacher, on this Mac only.</string>
</dict></plist>
"""


def to_wav(src, dst):
    """Any audio file -> 16-bit WAV, one channel."""
    subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", "-c", "1", src, dst], check=True)


def read_wav(path):
    w = wave.open(path)
    rate, n = w.getframerate(), w.getnframes()
    return rate, w.readframes(n)


def loudness(raw, rate):
    """dB every 10 ms, and the threshold of speech."""
    data = struct.unpack("<%dh" % (len(raw) // 2), raw)
    win = rate // 100
    db = [20 * math.log10(math.sqrt(sum(x * x for x in data[i:i + win]) / win) / 32768 + 1e-9)
          for i in range(0, len(data) - win, win)]
    s = sorted(db)
    floor, peak = s[int(len(s) * 0.1)], s[int(len(s) * 0.98)]
    return db, max(floor + 6, floor + 0.3 * (peak - floor))


def build_app():
    src = os.path.join(HERE, "transcribe_voice.swift")
    exe = os.path.join(APP, "Contents", "MacOS", "transcribe")
    if os.path.exists(exe) and os.path.getmtime(exe) > os.path.getmtime(src):
        return
    os.makedirs(os.path.dirname(exe), exist_ok=True)
    open(os.path.join(APP, "Contents", "Info.plist"), "w").write(PLIST)
    subprocess.run(["swiftc", "-O", "-o", exe, src], check=True, stderr=subprocess.DEVNULL)
    subprocess.run(["codesign", "-s", "-", "--force", APP], check=True, stderr=subprocess.DEVNULL)


def find(rec):
    tmp = tempfile.mkdtemp(prefix="voice-")
    wav = os.path.join(tmp, "all.wav")
    to_wav(rec, wav)
    rate, raw = read_wav(wav)
    db, thr = loudness(raw, rate)
    loud = [d > thr for d in db]
    gaps, k = [], 0
    while k < len(loud):
        if not loud[k]:
            e = k
            while e < len(loud) and not loud[e]:
                e += 1
            if e - k >= 50:
                gaps.append((k + e) // 2)
            k = e
        else:
            k += 1
    # Parts of about 40 seconds, cut in the middle of a pause.
    cuts, t = [0], 4000
    while t < len(loud) - 1500:
        c = min((g for g in gaps if g > cuts[-1] + 1500), key=lambda g: abs(g - t), default=None)
        if c is None:
            break
        cuts.append(c)
        t = c + 4000
    cuts.append(len(loud))
    parts = os.path.join(tmp, "parts")
    os.makedirs(parts)
    win = rate // 100
    for i in range(len(cuts) - 1):
        o = wave.open(os.path.join(parts, "part-%02d.wav" % i), "wb")
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(rate)
        o.writeframes(raw[cuts[i] * win * 2:cuts[i + 1] * win * 2]); o.close()
    build_app()
    out = os.path.join(tmp, "words.json")
    for _ in range(2):   # the recognizer sometimes stops early: try once more
        subprocess.run(["open", "-W", APP, "--args", parts, out], check=True)
        if os.path.exists(out):
            break
    if not os.path.exists(out):
        sys.exit("No words: is speech recognition allowed? (" + out[:-5] + ".log)")
    words = []
    for part, off in zip(json.load(open(out)), cuts):
        words += [(off / 100 + w["t"], off / 100 + w["t"] + w["d"], w["w"].strip("‏‫‬")) for w in part["words"]]
    line, last = [], -9
    for a, b, w in words:
        if a - last > 1.2 and line:
            print(" ".join(line)); line = []
        if not line:
            line.append("[%.1f]" % a)
        line.append(w); last = b
    print(" ".join(line))
    # Words said twice in a row: the same 1-4 words again within a few seconds.
    norm = lambda w: re.sub(r"[ً-ْـ.,،؟?]", "", w)
    print("\nSaid twice (check each against the script: some words are twice on purpose;"
          " then cut from the first reading to the second):")
    i = 0
    while i < len(words):
        for n in (4, 3, 2, 1):
            a, b = words[i:i + n], words[i + n:i + 2 * n]
            same = sum(norm(x[2]) == norm(y[2]) for x, y in zip(a, b))
            # n words again (or all but one of 3-4 words: the recognizer may hear one differently)
            if len(b) == n and (same == n or (n >= 3 and same >= n - 1)) and b[0][0] - a[0][0] < 8:
                print("  %.2f-%.2f  %s  (again at %.2f)" % (a[0][0], b[0][0], " ".join(x[2] for x in a), b[0][0]))
                i += n
                break
        else:
            i += 1


def cut(rec, out, ranges):
    tmp = tempfile.mkdtemp(prefix="voice-")
    wav = os.path.join(tmp, "all.wav")
    to_wav(rec, wav)
    rate, raw = read_wav(wav)
    spans = sorted(tuple(float(x) for x in r.split("-")) for r in ranges)
    keep, pos = [], 0
    for a, b in spans:
        keep.append(raw[pos * 2:int(a * rate) * 2])
        pos = int(b * rate)
    keep.append(raw[pos * 2:])
    o = wave.open(out, "wb")
    o.setnchannels(1); o.setsampwidth(2); o.setframerate(rate)
    o.writeframes(b"".join(keep)); o.close()
    gone = sum(b - a for a, b in spans)
    print("cut %d parts, %.1f seconds: %s" % (len(spans), gone, out))


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "find":
        find(sys.argv[2])
    elif len(sys.argv) >= 5 and sys.argv[1] == "cut":
        cut(sys.argv[2], sys.argv[3], sys.argv[4:])
    else:
        sys.exit(__doc__)
