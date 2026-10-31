"""Renumber the sessions of a course: rename files with git mv and map references.

Usage from a course-specific script:
    renum.run(course_dir, moves, lec_map, sem_map, hw_map)
moves: list of (old_rel_path_without_suffix, new_rel_path_without_suffix, kind_new, n_new)
       e.g. ("week-05/lesson-08", "week-05/lesson-05", "lecture", 5)
       every file old + suffix ("", "-book", "-slides") + ".qmd" is moved.
lec_map / sem_map / hw_map: old number -> new number (int) or a string label ("P3").
"""
import os
import re
import subprocess

SUFFIXES = ["", "-book", "-slides"]


def git_mv(src, dst):
    subprocess.run(["git", "mv", src, dst], check=True)


def map_one(n, mp):
    return mp.get(n, n)


def label(word, nums, mp, plural_word):
    """word = 'Lecture' or 'lecture'; nums mapped values; returns text."""
    vals = []
    for v in nums:
        if v not in vals:
            vals.append(v)
    if all(isinstance(v, int) for v in vals):
        if len(vals) == 1:
            return "%s %d" % (word, vals[0])
        return None
    return None


def map_text(s, lec_map, sem_map, hw_map, due_map=None):
    def lec_range(m):
        word, a, dash, b = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        cap = word[0].isupper()
        base = "Lecture" if cap else "lecture"
        if b is None:
            v = map_one(a, lec_map)
            if isinstance(v, int):
                return "%s %d" % (word, v)
            return m.group(0) + "‹?›"
        b = int(b)
        va, vb = map_one(a, lec_map), map_one(b, lec_map)
        if isinstance(va, int) and isinstance(vb, int):
            if va == vb:
                return "%s %d" % (base, va)
            return "%ss %d%s%d" % (base, va, dash, vb)
        return m.group(0) + "‹?›"

    def lec_and(m):
        word, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        cap = word[0].isupper()
        base = "Lecture" if cap else "lecture"
        va, vb = map_one(a, lec_map), map_one(b, lec_map)
        if isinstance(va, int) and isinstance(vb, int):
            if va == vb:
                return "%s %d" % (base, va)
            return "%ss %d and %d" % (base, va, vb)
        return m.group(0) + "‹?›"

    def sem(m):
        word, a = m.group(1), int(m.group(2))
        v = map_one(a, sem_map)
        if isinstance(v, int):
            return "%s %d" % (word, v)
        return "%s %s" % ("Practice" if word[0].isupper() else "practice", v[1:])

    def hw(m):
        word, a = m.group(1), int(m.group(2))
        v = map_one(a, hw_map)
        if v is None:
            return m.group(0) + "‹?›"
        return "%s %d" % (word, v)

    # use placeholders so that nothing is mapped twice
    out = []
    pos = 0
    pat = re.compile(
        r"(?P<and>([Ll]ectures) (\d+) and (\d+))"
        r"|(?P<rng>([Ll]ectures?) (\d+)(?:([–-])(\d+))?)"
        r"|(?P<sem>(Seminar|seminar) (\d+))"
        r"|(?P<hw>(Homework|homework) (\d+))")
    for m in pat.finditer(s):
        out.append(s[pos:m.start()])
        if m.group("and"):
            sub = re.match(r"([Ll]ectures) (\d+) and (\d+)", m.group(0))
            out.append(lec_and(sub))
        elif m.group("rng"):
            sub = re.match(r"([Ll]ectures?) (\d+)(?:([–-])(\d+))?", m.group(0))
            out.append(lec_range(sub))
        elif m.group("sem"):
            sub = re.match(r"(Seminar|seminar) (\d+)", m.group(0))
            out.append(sem(sub))
        else:
            sub = re.match(r"(Homework|homework) (\d+)", m.group(0))
            out.append(hw(sub))
        pos = m.end()
    out.append(s[pos:])
    return "".join(out)


def run(course_dir, moves, lec_map, sem_map, hw_map, skip_text=()):
    os.chdir(course_dir)
    # 1. moves
    for old, new, kind, n in moves:
        for suf in SUFFIXES:
            src = old + suf + ".qmd"
            if os.path.exists(src):
                git_mv(src, new + suf + ".qmd")
    # 2. map references in every .qmd of the course (except skip_text)
    for root, _, files in os.walk("."):
        for f in files:
            if not f.endswith(".qmd"):
                continue
            p = os.path.join(root, f)[2:]
            if p in skip_text:
                continue
            s = open(p, encoding="utf-8").read()
            t = map_text(s, lec_map, sem_map, hw_map)
            if t != s:
                open(p, "w", encoding="utf-8").write(t)
