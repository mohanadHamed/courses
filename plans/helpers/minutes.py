#!/usr/bin/env python3
"""Where do the class minutes of a lecture page go? (check_size.py, page_minutes)

    python3 plans/helpers/minutes.py courses/.../lesson-NN.qmd
"""
import re
import sys
sys.path.insert(0, "_extensions/lesson")
import check_size as c

p = sys.argv[1]
body = c.read(p)
st = c.read(p[:-4] + "-sheet.qmd")
for n in "1234":
    t = c.experiment_on_page(st, n)
    if t.strip():
        t = c.IC_BLOCK_RE.sub(" ", t)
        print("experiment", n, "words", c.count_words(t))
for part in re.split(r"^(?=## )", body, flags=re.M):
    if part.startswith("## "):
        e = c.IC_BLOCK_RE.sub(" ", part)
        print(part.splitlines()[0][:44].ljust(46), "words", c.count_words(e) - c.count_words(c.try_it_text(e)),
              "questions", c.count_questions(part), "sims", len(re.findall(r"\{\{< *sim ", part)))
print("total minutes", c.page_minutes(p, body))
