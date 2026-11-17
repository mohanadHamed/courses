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

The PDF is a form to fill in (the teacher's request of 2026-11-08: students
type their answers in the downloaded PDF instead of printing it). On paper
every {{< answer-space lines=N >}} and the Name and Student number line hold
an empty link to https://answer.field/<name> (shortcodes.lua, banner.lua,
lesson.css); Chrome prints each link as a link rectangle, and make_fillable()
turns each rectangle into a text field of the same size (multiline from two
lines). A box for a drawing stays a box. A multiple-choice question
({.pick}, interact.lua) prints a circle for each option with a link to
https://answer.field/pick-N?opt=A: the circles of one question become one
radio-button field ("Question N"), so the student taps one option in the PDF
and writes nothing.

Project post-render step. Needs Google Chrome or Chromium (preinstalled on
GitHub's ubuntu-latest runners) and the Python package pypdf for the form
fields (`pip install pypdf`). Without Chrome the script warns and skips;
without pypdf the PDFs are made without fields.
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


FIELD_URL = "https://answer.field/"
FIELD_NAMES = {"name": "Name", "student-number": "Student number"}


def make_fillable(pdf_path):
    """Turn the answer links of a printed page into text fields (see above).
    Returns the number of fields, or None without pypdf."""
    try:
        from pypdf import PdfWriter
        from pypdf.generic import (ArrayObject, BooleanObject, DictionaryObject, FloatObject,
                                   NameObject, NumberObject, DecodedStreamObject, TextStringObject)
    except ImportError:
        return None
    writer = PdfWriter(clone_from=pdf_path)
    root = getattr(writer, "root_object", None) or writer._root_object
    font = writer._add_object(DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
        NameObject("/Encoding"): NameObject("/WinAnsiEncoding"),
    }))
    dingbats = writer._add_object(DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/ZapfDingbats"),
    }))
    fields = ArrayObject()
    radios = {}    # "pick-3" -> its radio-button field (a {.pick} question)

    def dot_streams(w, h):
        """The look of one radio button: "on" is a dark dot in the printed
        circle, "off" is empty (the printed circle stays visible)."""
        r = min(w, h) * 0.3
        cx, cy, k = w / 2, h / 2, 0.5523 * r
        circle = ("0.13 g %.2f %.2f m %.2f %.2f %.2f %.2f %.2f %.2f c %.2f %.2f %.2f %.2f %.2f %.2f c "
                  "%.2f %.2f %.2f %.2f %.2f %.2f c %.2f %.2f %.2f %.2f %.2f %.2f c f"
                  % (cx + r, cy,
                     cx + r, cy + k, cx + k, cy + r, cx, cy + r,
                     cx - k, cy + r, cx - r, cy + k, cx - r, cy,
                     cx - r, cy - k, cx - k, cy - r, cx, cy - r,
                     cx + k, cy - r, cx + r, cy - k, cx + r, cy))
        out = []
        for content in (circle, ""):
            s = DecodedStreamObject()
            s.set_data(content.encode("ascii"))
            s.update({NameObject("/Type"): NameObject("/XObject"), NameObject("/Subtype"): NameObject("/Form"),
                      NameObject("/BBox"): ArrayObject([FloatObject(0), FloatObject(0), FloatObject(w), FloatObject(h)])})
            out.append(writer._add_object(s))
        return out

    for page in writer.pages:
        if "/Annots" not in page:
            continue
        kept = ArrayObject()
        for ref in page["/Annots"].get_object():
            annot = ref.get_object()
            action = annot.get("/A")
            uri = str(action.get_object().get("/URI", "")) if action is not None else ""
            if annot.get("/Subtype") != "/Link" or not uri.startswith(FIELD_URL):
                kept.append(ref)
                continue
            key, _, query = uri[len(FIELD_URL):].partition("?")
            if key.startswith("pick-") and "opt=" in query:
                # One option of a multiple-choice question: a radio button.
                opt = query.split("opt=")[1].split("&")[0]
                if key not in radios:
                    name = "Question " + key[len("pick-"):]
                    radios[key] = writer._add_object(DictionaryObject({
                        NameObject("/FT"): NameObject("/Btn"),
                        NameObject("/Ff"): NumberObject(49152),   # radio, no toggle to off
                        NameObject("/T"): TextStringObject(name),
                        NameObject("/TU"): TextStringObject(name),
                        NameObject("/V"): NameObject("/Off"),
                        NameObject("/Kids"): ArrayObject(),
                    }))
                    fields.append(radios[key])
                rect = [float(v) for v in annot["/Rect"]]
                on, off = dot_streams(abs(rect[2] - rect[0]), abs(rect[3] - rect[1]))
                widget = writer._add_object(DictionaryObject({
                    NameObject("/Type"): NameObject("/Annot"),
                    NameObject("/Subtype"): NameObject("/Widget"),
                    NameObject("/Parent"): radios[key],
                    NameObject("/Rect"): ArrayObject([FloatObject(v) for v in rect]),
                    NameObject("/F"): NumberObject(4),
                    NameObject("/P"): page.indirect_reference,
                    NameObject("/AS"): NameObject("/Off"),
                    NameObject("/AP"): DictionaryObject({NameObject("/N"): DictionaryObject({
                        NameObject("/" + opt): on, NameObject("/Off"): off})}),
                    NameObject("/MK"): DictionaryObject({NameObject("/CA"): TextStringObject("l")}),
                    NameObject("/DA"): TextStringObject("/ZaDb 0 Tf 0.13 g"),
                }))
                radios[key].get_object()["/Kids"].append(widget)
                kept.append(widget)
                continue
            lines = int(query.split("lines=")[1]) if "lines=" in query else 1
            name = FIELD_NAMES.get(key, "Answer " + key)
            widget = DictionaryObject({
                NameObject("/Type"): NameObject("/Annot"),
                NameObject("/Subtype"): NameObject("/Widget"),
                NameObject("/FT"): NameObject("/Tx"),
                NameObject("/T"): TextStringObject(name),
                NameObject("/TU"): TextStringObject(name),
                NameObject("/Rect"): ArrayObject([FloatObject(float(v)) for v in annot["/Rect"]]),
                NameObject("/F"): NumberObject(4),                       # printed
                NameObject("/Ff"): NumberObject(4096 if lines > 1 else 0),  # multiline
                NameObject("/DA"): TextStringObject("/Helv 11 Tf 0 g"),
                # A thin blue frame: the printed answer lines stay visible inside it.
                NameObject("/MK"): DictionaryObject({
                    NameObject("/BC"): ArrayObject([FloatObject(0.45), FloatObject(0.62), FloatObject(0.95)])}),
                NameObject("/BS"): DictionaryObject({
                    NameObject("/W"): NumberObject(1), NameObject("/S"): NameObject("/S")}),
            })
            field = writer._add_object(widget)
            kept.append(field)
            fields.append(field)
        page[NameObject("/Annots")] = kept
    if fields:
        root[NameObject("/AcroForm")] = DictionaryObject({
            NameObject("/Fields"): fields,
            NameObject("/NeedAppearances"): BooleanObject(True),
            NameObject("/DA"): TextStringObject("/Helv 11 Tf 0 g"),
            NameObject("/DR"): DictionaryObject({
                NameObject("/Font"): DictionaryObject({NameObject("/Helv"): font, NameObject("/ZaDb"): dingbats})}),
        })
        with open(pdf_path, "wb") as f:
            writer.write(f)
    return len(fields)


def is_real_page(html_path):
    """Skip unpublished drafts (Quarto leaves a tiny empty page for them)."""
    text = read_page(html_path)
    return 'class="lesson-hero' in text and ("answer-space" in text or 'class="pick"' in text)


def is_online_activity(html_path):
    return "online-activity" in read_page(html_path) and is_real_page(html_path)


def main():
    # HOMEWORK_PDF=off skips the printing, for a quick render of many pages
    # one by one; then run this script once (python3 _extensions/lesson/homework_pdf.py).
    if os.environ.get("HOMEWORK_PDF", "").lower() == "off":
        return
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
    made = fields = 0
    no_forms = False
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
                n = make_fillable(pdf)
                if n is None and not no_forms:
                    no_forms = True
                    print("homework_pdf: pypdf not installed (pip install pypdf); the PDFs have no form fields",
                          file=sys.stderr)
                elif n:
                    fields += n
            else:
                print("homework_pdf: could not print " + html, file=sys.stderr)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    print("homework_pdf: made %d homework and online-activity PDF(s), %d form field(s) to fill in" % (made, fields))


if __name__ == "__main__":
    main()
