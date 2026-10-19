#!/usr/bin/env python3
"""Give the files that students download meaningful, unique names.

Quarto names each output after its source file (lesson-05-book.pdf), so every
course has the same names. After the render, this step renames them in _site:

    lesson-05-book.pdf    -> math_lecture5.pdf
    lesson-05-slides.pptx -> math_lecture5_slides.pptx
    homework-03.pdf       -> math_week3_homework.pdf

The prefix is `course.file-prefix` in courses/<slug>/_metadata.yml (else the
slug with "_" for "-"). banner.lua and the schedule shortcode link the same
names, so a file keeps its name whether it is downloaded or opened and saved.

Project post-render step: after pptx_finish.py and homework_pdf.py, before
build_stamp.py. Only the Python standard library is used.
"""

import glob
import os
import re

RULES = [
    (re.compile(r"^lesson-(\d+)-book\.pdf$"), "{prefix}_lecture{n}.pdf"),
    (re.compile(r"^lesson-(\d+)-slides\.pptx$"), "{prefix}_lecture{n}_slides.pptx"),
    (re.compile(r"^homework-(\d+)\.pdf$"), "{prefix}_week{n}_homework.pdf"),
]


def file_prefix(project_dir, slug):
    try:
        with open(os.path.join(project_dir, "courses", slug, "_metadata.yml"), encoding="utf-8") as f:
            m = re.search(r'^\s+file-prefix:\s*"([^"]+)"', f.read(), re.M)
            if m:
                return m.group(1)
    except OSError:
        pass
    return slug.replace("-", "_")


def new_name(filename, prefix):
    for pattern, template in RULES:
        m = pattern.match(filename)
        if m:
            return template.format(prefix=prefix, n=int(m.group(1)))
    return None


def main():
    project_dir = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    out_dir = os.path.join(project_dir, os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
    renamed = 0
    for course_dir in sorted(glob.glob(os.path.join(out_dir, "courses", "*"))):
        if not os.path.isdir(course_dir):
            continue
        prefix = file_prefix(project_dir, os.path.basename(course_dir))
        for path in sorted(glob.glob(os.path.join(course_dir, "week-*", "*"))):
            name = new_name(os.path.basename(path), prefix)
            if name:
                os.replace(path, os.path.join(os.path.dirname(path), name))
                renamed += 1
    print("download_names: renamed %d file(s)" % renamed)


if __name__ == "__main__":
    main()
