#!/usr/bin/env python3
"""Make the homework PDFs by printing the homework web pages with Chrome.

The online activities of a blended course (online-NN.html; older pages:
lesson-NN.html with `online: true`) print the same way: on paper only their
tasks (lesson.css hides the study steps), saved as online-NN.pdf and renamed
<prefix>_onlineN_tasks.pdf by download_names.py.

Homework is a web page with a "Print homework" button (one A4 page, with
answer lines). The "Download PDF" file must look exactly like that printout,
so we do not build it with Typst: we print the finished page itself with
headless Chrome, using the same print styles (lesson.css, @media print).

Project post-render step. Needs Google Chrome or Chromium (preinstalled on
GitHub's ubuntu-latest runners). Without it, the script warns and skips.
"""

import glob
import os
import shutil
import subprocess
import sys
import tempfile

CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]


def find_chrome():
    for c in CANDIDATES:
        if not c:
            continue
        if os.path.isabs(c) and os.path.exists(c):
            return c
        path = shutil.which(c)
        if path:
            return path
    return None


def read_page(html_path):
    try:
        with open(html_path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def is_real_page(html_path):
    """Skip unpublished drafts (Quarto leaves a tiny empty page for them)."""
    text = read_page(html_path)
    return 'class="lesson-hero' in text and "answer-space" in text


def is_online_activity(html_path):
    return "online-activity" in read_page(html_path) and is_real_page(html_path)


def main():
    project_dir = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    out_dir = os.path.join(project_dir, os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
    pages = [p for p in sorted(glob.glob(os.path.join(out_dir, "courses", "*", "week-*", "homework-*.html")))
             if is_real_page(p)]
    for name in ("online-[0-9][0-9].html", "lesson-[0-9][0-9].html"):
        pages += [p for p in sorted(glob.glob(os.path.join(out_dir, "courses", "*", "week-*", name)))
                  if is_online_activity(p)]
    if not pages:
        return
    chrome = find_chrome()
    if not chrome:
        print("homework_pdf: Chrome not found (set CHROME=...); homework PDFs not made", file=sys.stderr)
        return
    profile = tempfile.mkdtemp(prefix="hw-chrome-")
    made = 0
    try:
        for html in pages:
            pdf = html[:-5] + ".pdf"
            cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                   "--user-data-dir=" + profile, "--no-pdf-header-footer",
                   "--virtual-time-budget=5000", "--print-to-pdf=" + pdf,
                   "file://" + os.path.abspath(html)]
            r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            if r.returncode == 0 and os.path.exists(pdf):
                made += 1
            else:
                print("homework_pdf: could not print " + html, file=sys.stderr)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    print("homework_pdf: made %d homework and online-activity PDF(s)" % made)


if __name__ == "__main__":
    main()
