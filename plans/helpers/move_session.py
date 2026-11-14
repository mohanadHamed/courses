#!/usr/bin/env python3
"""Move a session file to another week folder, with what it uses.

    python3 plans/helpers/move_session.py SRC.qmd DST.qmd [--copy]

The session (lesson-NN*.qmd, online-NN.qmd …) is moved with `git mv` (or
copied with --copy). Every file that it references with a path inside its
own folder (sims/…, images/…, files/… and the start files of its front
matter) is copied to the new folder, with the companions of a simulator
(.png, .svg, .gif, and the .js/.css files that its HTML loads). The old
files stay: the hidden face-to-face version links them.
"""
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def copy(src_dir, dst_dir, rel):
    s, d = os.path.join(src_dir, rel), os.path.join(dst_dir, rel)
    if not os.path.exists(s) or os.path.abspath(s) == os.path.abspath(d):
        return
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if not os.path.exists(d):
        shutil.copy2(s, d)
        print("  copied", os.path.relpath(d, ROOT))
    if rel.endswith(".html"):
        html = open(s, encoding="utf-8").read()
        for dep in re.findall(r'(?:src|href)="([^"/:][^":]*\.(?:js|css))"', html):
            if not dep.startswith(".."):
                copy(src_dir, dst_dir, os.path.join(os.path.dirname(rel), dep))
        base = rel[:-5]
        for ext in (".png", ".svg", ".gif"):
            copy(src_dir, dst_dir, base + ext)
    if rel.endswith(".png"):
        copy(src_dir, dst_dir, rel[:-4] + ".svg")


def main():
    src, dst = sys.argv[1], sys.argv[2]
    src_dir, dst_dir = os.path.dirname(os.path.abspath(src)), os.path.dirname(os.path.abspath(dst))
    text = open(src, encoding="utf-8").read()
    refs = set(re.findall(r'(?<![\w./])((?:sims|images|files|videos)/[\w./-]+\.\w+)', text))
    for m in re.findall(r"^\s*- name: (\S+)", text, re.M):
        refs.add("files/" + m)
    os.makedirs(dst_dir, exist_ok=True)
    for r in sorted(refs):
        copy(src_dir, dst_dir, r)
    if "--copy" in sys.argv:
        shutil.copy2(src, dst)
    else:
        subprocess.run(["git", "mv", src, dst], check=True)
    print("%s %s -> %s" % ("copied" if "--copy" in sys.argv else "moved", os.path.relpath(src, ROOT), os.path.relpath(dst, ROOT)))


if __name__ == "__main__":
    main()
