#!/usr/bin/env python3
"""Draw the screens of the Windows apps for the lab worksheets of Digital Skills.

Since 2026-11-20 the course has a computer lab (Windows and Microsoft
Office), and the lecture is the "lab model" (NOTES.md): about 15 minutes on
the interactive page, then each student follows the printed worksheet in the
real app. A student who reads the worksheet alone must see where each button
is: one picture for each step, drawn close to Word for Windows (Microsoft 365
and Office 2021, the classic ribbon), without logos. A numbered orange circle
marks what to click, in the order of the step's sub-steps.

Every screen is a function below, listed in SCREENS. Run from the project root:

    python3 tools/lab_screens.py            # every SVG and its PNG
    python3 tools/lab_screens.py --svg      # the SVGs only
    python3 tools/lab_screens.py lab-table  # only the screens whose name has "lab-table"

The PNG is exported like the posters (shared/sims/README.md): quarto typst
compile at 200 ppi. Without Helvetica or Arial, a copy of the SVG in
Liberation Sans (the widths of Arial) is exported; the SVG stays unchanged.
"""

import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phone_screens import (Svg, FONT, INK, GREY, LINE, BG, MARK, MARK_INK, MARK_SOFT,  # noqa: E402
                           icon_search, icon_folder, icon_doc)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "courses/digital-skills/week-04/images/"

W = 900                       # the width of every picture
WORD = "#185abd"              # Word blue
WORD_SOFT = "#dbe7f8"
TITLE_BG = "#f3f3f3"
RIBBON_BG = "#f9f9f9"
CANVAS = "#e6e6e6"            # the grey around the page
BTN = "#ffffff"
EDGE = "#c8c8c8"
SEL = "#c7dcf7"               # selected text
RED = "#d13438"

TABS = ("File", "Home", "Insert", "Draw", "Design", "Layout", "References", "Mailings", "Review", "View", "Help")


# ---------- The window --------------------------------------------------------

def frame(s, h):
    s.rect(0, 0, W, h, fill=BG, rx=18)
    s.rect(14, 14, W - 28, h - 28, fill="#ffffff", stroke="#b9bdc2", sw=1.5, rx=10)


def title_bar(s, name="Document1 - Word"):
    s.rect(15, 15, W - 30, 34, fill=TITLE_BG, rx=9)
    s.rect(15, 35, W - 30, 14, fill=TITLE_BG)
    s.text(30, 37, "AutoSave", 11.5, 400, GREY)
    s.rect(84, 26, 30, 15, fill="#ffffff", stroke="#8a8a8a", sw=1.2, rx=7.5)
    s.circle(92, 33.5, 4, fill="#5f5f5f")
    s.text(120, 37, "Off", 11.5, 400, GREY)
    # Save (a disk), Undo
    s.rect(150, 25, 15, 15, stroke=INK, sw=1.3, rx=2)
    s.rect(154, 25, 7, 5, fill=INK)
    s.path("M182 30 a6 6 0 1 1 -1 7", stroke=INK, sw=1.4)
    s.poly([(178, 27), (183, 31), (177, 33)], fill=INK)
    s.text(205, 37, name, 12.5, 400, INK)
    s.rect(400, 22, 230, 22, fill="#ffffff", stroke="#c9c9c9", sw=1, rx=5)
    icon_search(s, 414, 33, GREY)
    s.text(428, 37.5, "Search", 11.5, 400, GREY)
    # Window buttons: minimize, maximize, close (two diagonal strokes, never upright)
    s.line(W - 118, 33, W - 106, 33, INK, 1.3)
    s.rect(W - 80, 27, 11, 11, stroke=INK, sw=1.3)
    s.line(W - 46, 27, W - 36, 39, INK, 1.3)
    s.line(W - 46, 39, W - 36, 27, INK, 1.3)


def tab_row(s, active="Home"):
    s.rect(15, 49, W - 30, 30, fill=TITLE_BG)
    x, pos = 30, {}
    for t in TABS:
        w = 7.4 * len(t) + 4
        if t == "File":
            s.text(x, 69, t, 13, 400, INK)
        else:
            s.text(x, 69, t, 13, 700 if t == active else 400, WORD if t == active else INK)
        if t == active:
            s.rect(x - 2, 74, w, 3, fill=WORD, rx=1.5)
        pos[t] = (x - 6, 52, w + 12, 26)
        x += w + 16
    return pos


def ribbon_box(s):
    s.rect(15, 79, W - 30, 104, fill=RIBBON_BG)
    s.line(15, 183, W - 15, 183, "#d6d6d6", 1)


def group(s, x1, x2, label):
    s.text((x1 + x2) / 2, 177, label, 10.5, 400, GREY, "middle")
    s.line(x2, 86, x2, 176, "#dadada", 1)


def small_btn(s, x, y, w, h, label=None, size=12, weight=400, color=INK, fill=BTN, stroke=None):
    s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1, rx=3)
    if label:
        s.text(x + w / 2, y + h / 2 + size * 0.36, label, size, weight, color, "middle")


def dropdown(s, x, y, w, text, h=22):
    s.rect(x, y, w, h, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=2)
    s.text(x + 6, y + h / 2 + 4.3, text, 12, 400, INK)
    s.poly([(x + w - 13, y + h / 2 - 2), (x + w - 5, y + h / 2 - 2), (x + w - 9, y + h / 2 + 3)], fill=INK)


def align_icon(s, x, y, kind, c=INK):
    """Four lines: left, center, right or justify."""
    widths = {"left": (16, 11, 16, 9), "center": (16, 10, 16, 10), "right": (16, 11, 16, 9), "justify": (16, 16, 16, 16)}
    for i, lw in enumerate(widths[kind]):
        if kind == "left" or kind == "justify":
            x1 = x
        elif kind == "center":
            x1 = x + (16 - lw) / 2
        else:
            x1 = x + 16 - lw
        s.line(x1, y + i * 4, x1 + lw, y + i * 4, c, 1.6)


def list_icon(s, x, y, numbered=False):
    for i in range(3):
        yy = y + i * 5.5
        if numbered:
            s.text(x, yy + 2.5, str(i + 1), 6.5, 700, INK)
        else:
            s.circle(x + 1.5, yy, 1.6, fill=INK)
        s.line(x + 6, yy, x + 17, yy, INK, 1.4)


def home_ribbon(s, active_style=None):
    """The Home tab, classic ribbon. Returns where the buttons are."""
    ribbon_box(s)
    p = {}
    # Clipboard
    s.rect(34, 92, 30, 36, fill="#ffffff", stroke="#7a7a7a", sw=1.3, rx=3)
    s.rect(41, 88, 16, 8, fill="#7a7a7a", rx=2)
    s.rect(42, 104, 26, 30, fill="#ffffff", stroke=WORD, sw=1.3, rx=2)
    s.text(46, 156, "Paste", 11.5, 400, INK)
    group(s, 20, 96, "Clipboard")
    # Font
    dropdown(s, 104, 92, 128, "Calibri (Body)")
    dropdown(s, 236, 92, 44, "11")
    small_btn(s, 286, 92, 22, 22, "A", 13, 400)
    s.poly([(301, 96), (305, 96), (303, 93)], fill=INK)
    small_btn(s, 310, 92, 22, 22, "A", 10.5, 400)
    p["bold"] = (104, 124, 24, 24)
    small_btn(s, 104, 124, 24, 24, "B", 14, 800)
    small_btn(s, 130, 124, 24, 24, None)
    s.text(142, 141, "I", 14, 400, INK, "middle")
    s.raw('<text x="142" y="141" font-size="14" font-style="italic" fill="%s" text-anchor="middle"></text>' % INK)
    small_btn(s, 156, 124, 24, 24, "U", 13.5, 400)
    s.line(162, 144, 174, 144, INK, 1.2)
    small_btn(s, 182, 124, 24, 24, "ab", 11, 400)
    s.line(184, 137, 204, 137, INK, 1)
    small_btn(s, 210, 124, 24, 24, "x", 12, 400)
    s.text(229, 145, "2", 8, 400, INK)
    small_btn(s, 238, 124, 24, 24, "x", 12, 400)
    s.text(253, 133, "2", 8, 400, INK)
    # Highlight and font colour: a letter with a colour bar, and a small arrow
    s.rect(270, 124, 32, 24, fill=BTN, rx=3)
    s.path("M276 140 L284 128 L289 132 L281 143 Z", stroke=INK, sw=1.2)
    s.rect(274, 143, 16, 4, fill="#ffe066")
    s.poly([(294, 134), (300, 134), (297, 138)], fill=INK)
    p["color"] = (304, 124, 32, 24)
    s.rect(304, 124, 32, 24, fill=BTN, rx=3)
    s.text(316, 139, "A", 14, 700, INK, "middle")
    s.rect(308, 142, 16, 4, fill=RED)
    s.poly([(327, 134), (333, 134), (330, 138)], fill=INK)
    group(s, 96, 342, "Font")
    # Paragraph
    for i, numbered in enumerate((False, True, False)):
        list_icon(s, 352 + i * 30, 96, numbered)
        s.poly([(373 + i * 30, 101), (378 + i * 30, 101), (375.5 + i * 30, 104)], fill=INK)
    s.text(462, 107, "¶", 15, 400, INK)
    s.text(440, 107, "A", 11, 400, INK)
    s.text(448, 107, "Z", 8, 400, INK)
    for i, kind in enumerate(("left", "center", "right", "justify")):
        x = 352 + i * 28
        p[kind] = (x - 4, 124, 24, 24)
        s.rect(x - 4, 124, 24, 24, fill=BTN, rx=3)
        align_icon(s, x, 130, kind)
    s.rect(466, 124, 30, 24, fill=BTN, rx=3)
    for i in range(3):
        s.line(476, 130 + i * 5, 490, 130 + i * 5, INK, 1.4)
    s.poly([(470, 131), (473, 127), (476, 131)], fill=INK)
    s.poly([(470, 141), (473, 145), (476, 141)], fill=INK)
    group(s, 342, 506, "Paragraph")
    # Styles gallery
    styles = [("Normal", "AaBbCcDd", 11, 400, INK), ("No Spacing", "AaBbCcDd", 11, 400, INK),
              ("Heading 1", "AaBbCc", 13, 400, WORD), ("Heading 2", "AaBbCcD", 11.5, 400, WORD),
              ("Title", "AaB", 21, 300, INK)]
    for i, (name, sample, size, weight, color) in enumerate(styles):
        x = 512 + i * 61
        box = (x, 90, 58, 62)
        p[name] = box
        on = name == active_style
        s.rect(x, 90, 58, 62, fill=WORD_SOFT if on else "#ffffff", stroke=WORD if on else "#e0e0e0", sw=1.2, rx=3)
        s.text(x + 29, 120, sample, size, weight, color, "middle")
        s.text(x + 29, 144, name, 10, 400, INK, "middle")
    s.rect(818, 90, 13, 62, fill="#ffffff", stroke="#e0e0e0", sw=1)
    s.poly([(821, 118), (828, 118), (824.5, 122)], fill=INK)
    group(s, 506, 838, "Styles")
    s.text(846, 108, "Find", 11.5, 400, INK)
    s.text(846, 128, "Replace", 11.5, 400, INK)
    s.text(846, 148, "Select", 11.5, 400, INK)
    s.text(862, 177, "Editing", 10.5, 400, GREY, "middle")
    return p


def big_btn(s, x, w, label, icon=None, label2=None):
    s.rect(x, 88, w, 78, fill=BTN, rx=4)
    if icon:
        icon(s, x + w / 2, 112)
    s.text(x + w / 2, 150, label, 11.5, 400, INK, "middle")
    if label2:
        s.text(x + w / 2, 163, label2, 11.5, 400, INK, "middle")


def ic_table(s, cx, cy):
    s.rect(cx - 15, cy - 13, 30, 26, fill="#ffffff", stroke=WORD, sw=1.4, rx=1)
    s.rect(cx - 15, cy - 13, 30, 7, fill=WORD)
    for r in range(2):            # the cells, as small boxes (no crossing lines)
        for c in range(3):
            s.rect(cx - 13 + c * 9.3, cy - 4 + r * 8.3, 7.4, 6.4, fill="#e8f0fb")


def ic_picture(s, cx, cy):
    s.rect(cx - 14, cy - 11, 28, 22, fill="#ffffff", stroke="#5c5c5c", sw=1.3, rx=2)
    s.circle(cx + 6, cy - 4, 3, fill="#f2b705")
    s.path("M%g %g l8 -9 l6 6 l4 -4 l8 8 z" % (cx - 13, cy + 10), fill="#4caf50")


def ic_shapes(s, cx, cy):
    s.circle(cx - 6, cy - 4, 8, stroke="#5c5c5c", sw=1.3, fill="#ffffff")
    s.rect(cx - 2, cy - 2, 16, 14, fill=WORD_SOFT, stroke=WORD, sw=1.3)


def ic_page(s, cx, cy, lines=True):
    s.rect(cx - 11, cy - 14, 22, 28, fill="#ffffff", stroke="#5c5c5c", sw=1.3, rx=1)
    if lines:
        for i in range(4):
            s.line(cx - 6, cy - 7 + i * 5, cx + 6, cy - 7 + i * 5, "#9a9a9a", 1.2)


def insert_ribbon(s):
    ribbon_box(s)
    p = {}
    for i, t in enumerate(("Cover Page", "Blank Page", "Page Break")):
        s.rect(26, 92 + i * 24, 12, 15, fill="#ffffff", stroke="#5c5c5c", sw=1.1)
        s.text(44, 104 + i * 24, t, 11.5, 400, INK)
    group(s, 20, 120, "Pages")
    p["table"] = (128, 88, 60, 80)
    big_btn(s, 128, 60, "Table", ic_table)
    s.poly([(153, 158), (163, 158), (158, 163)], fill=INK)
    group(s, 120, 196, "Tables")
    big_btn(s, 204, 62, "Pictures", ic_picture)
    big_btn(s, 270, 58, "Shapes", ic_shapes)
    for i, t in enumerate(("Icons", "3D Models", "SmartArt")):
        s.text(340, 104 + i * 24, t, 11.5, 400, INK)
    for i, t in enumerate(("Chart", "Screenshot")):
        s.text(418, 104 + i * 24, t, 11.5, 400, INK)
    group(s, 196, 494, "Illustrations")
    for i, t in enumerate(("Header", "Footer", "Page Number")):
        s.text(506, 104 + i * 24, t, 11.5, 400, INK)
    group(s, 494, 600, "Header & Footer")
    big_btn(s, 610, 56, "Text", ic_page, "Box")
    for i, t in enumerate(("Quick Parts", "WordArt", "Drop Cap")):
        s.text(676, 104 + i * 24, t, 11.5, 400, INK)
    group(s, 600, 770, "Text")
    s.text(784, 104, "Equation", 11.5, 400, INK)
    s.text(784, 128, "Symbol", 11.5, 400, INK)
    s.text(828, 177, "Symbols", 10.5, 400, GREY, "middle")
    return p


def checkbox(s, x, y, on, label):
    s.rect(x, y, 13, 13, fill=WORD if on else "#ffffff", stroke=WORD if on else "#6b6b6b", sw=1.2, rx=2)
    if on:
        s.path("M%g %g l3.5 3.5 l6 -7" % (x + 2.5, y + 7), stroke="#ffffff", sw=1.8)
    s.text(x + 20, y + 11, label, 11.5, 400, INK)


def view_ribbon(s, nav_on=False):
    ribbon_box(s)
    p = {}
    for i, (t, on) in enumerate((("Read", False), ("Print", True), ("Web", False))):
        x = 24 + i * 56
        s.rect(x, 88, 52, 78, fill=WORD_SOFT if on else BTN, rx=4)
        ic_page(s, x + 26, 112)
        s.text(x + 26, 150, t, 11.5, 400, INK, "middle")
        s.text(x + 26, 163, "Mode" if t == "Read" else "Layout", 11.5, 400, INK, "middle")
    group(s, 20, 196, "Views")
    big_btn(s, 204, 56, "Focus", lambda s_, x, y: s_.rect(x - 12, y - 10, 24, 20, stroke="#5c5c5c", sw=1.3, rx=2))
    big_btn(s, 264, 70, "Immersive", ic_page, "Reader")
    group(s, 196, 340, "Immersive")
    checkbox(s, 352, 96, False, "Ruler")
    checkbox(s, 352, 120, False, "Gridlines")
    p["nav"] = (346, 140, 128, 22)
    checkbox(s, 352, 144, nav_on, "Navigation Pane")
    group(s, 340, 480, "Show")
    big_btn(s, 490, 52, "Zoom", lambda s_, x, y: icon_search(s_, x, y, INK))
    big_btn(s, 546, 52, "100%", ic_page)
    for i, t in enumerate(("One Page", "Multiple Pages", "Page Width")):
        s.text(606, 104 + i * 24, t, 11.5, 400, INK)
    group(s, 480, 712, "Zoom")
    big_btn(s, 722, 64, "New", ic_page, "Window")
    s.text(800, 104, "Arrange All", 11.5, 400, INK)
    s.text(800, 128, "Split", 11.5, 400, INK)
    s.text(838, 177, "Window", 10.5, 400, GREY, "middle")
    return p


def status_bar(s, h, words="18 words"):
    s.rect(15, h - 40, W - 30, 25, fill=TITLE_BG)
    s.rect(15, h - 25, W - 30, 10, fill=TITLE_BG, rx=9)
    s.text(30, h - 23, "Page 1 of 1", 11, 400, GREY)
    s.text(110, h - 23, words, 11, 400, GREY)
    s.text(190, h - 23, "English (United States)", 11, 400, GREY)
    s.text(W - 120, h - 23, "100%", 11, 400, GREY)
    s.line(W - 88, h - 27, W - 30, h - 27, "#9a9a9a", 1.5)
    s.rect(W - 62, h - 32, 4, 10, fill="#5f5f5f")


# ---------- The page and its text ---------------------------------------------

_FONTS = {}


def width(text, size, weight=400):
    """The width of a text in the picture: measured with Liberation Sans (the widths of
    Arial and Helvetica) when Pillow has it, else estimated."""
    try:
        from PIL import ImageFont
        bold = weight >= 600
        key = (bold, size)
        if key not in _FONTS:
            name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
            _FONTS[key] = ImageFont.truetype("/usr/share/fonts/truetype/liberation/" + name, int(size * 10))
        return _FONTS[key].getlength(text) / 10
    except Exception:
        return len(text) * size * 0.55

# The notice of the worksheet. Each paragraph: (style, text). The style gives
# the look: "plain" (typed, no style yet), Title, Heading 1, Normal.
TYPED = [("plain", "Book Fair"), ("plain", "When and where"),
         ("plain", "Sunday to Tuesday, 10:00 to 15:00, in the college library."),
         ("plain", "Entry is free."), ("plain", "Prices")]

LOOK = {
    "plain": (13.5, 400, INK, 6),
    "Normal": (13.5, 400, INK, 6),
    "Title": (30, 300, INK, 12),
    "Heading 1": (19, 400, WORD, 12),
}


def page(s, x, y, w, h, paras, sel=None, center=(), bold_word=None, red_word=None, caret=None, table=None,
         table_at=None, squiggle=None):
    """A white page with its paragraphs. Returns the box of each paragraph and word marks."""
    s.rect(x, y, w, h, fill="#ffffff", stroke="#d0d0d0", sw=1)
    boxes, cy = [], y + 46
    left = x + 56
    for i, (style, text) in enumerate(paras):
        size, weight, color, gap = LOOK[style]
        if style == "Heading 1":
            cy += 8
        tx = left
        anchor = "start"
        if i in center:
            tx, anchor = x + w / 2, "middle"
        tw = width(text, size, weight)
        bx = tx if anchor == "start" else tx - tw / 2
        if sel == i:
            s.rect(bx - 2, cy - size * 0.95, tw + 4, size * 1.3, fill=SEL)
        if bold_word and bold_word[0] == i:
            # one word in bold (and maybe in colour), the rest plain
            pre, word, post = text.partition(bold_word[1])
            s.raw('<text x="%g" y="%g" font-size="%g" fill="%s" text-anchor="%s">%s<tspan font-weight="800" fill="%s">%s</tspan>%s</text>'
                  % (tx, cy, size, color, anchor, pre, bold_word[2], word, post))
        elif red_word and red_word[0] == i:
            pre, word, post = text.partition(red_word[1])
            ws = bx + width(pre, size)
            s.rect(ws - 1, cy - size * 0.95, width(word, size) + 2, size * 1.3, fill=SEL)
            s.text(tx, cy, text, size, weight, color, anchor)
        else:
            s.text(tx, cy, text, size, weight, color, anchor)
        if squiggle and squiggle[0] == i:
            pre, word, _ = text.partition(squiggle[1])
            ws = bx + width(pre, size)
            we = ws + width(word, size)
            d = "M%g %g" % (ws, cy + 4)
            xx, up = ws, True
            while xx < we:
                xx += 3
                d += " L%g %g" % (xx, cy + (2 if up else 5))
                up = not up
            s.path(d, stroke=RED, sw=1.2)
            boxes.append(("word", ws, cy - size, we - ws, size * 1.4))
        boxes.append((bx, cy - size, tw, size * 1.4))
        if caret is not None and caret == i:
            s.line(bx + tw + 3, cy - size, bx + tw + 3, cy + 3, INK, 1.4)
        cy += size + gap + 6
        if table_at is not None and table_at == i and table:
            cy = draw_table(s, left, cy - 4, table) + 24
    return [b for b in boxes if b[0] != "word"], [b for b in boxes if b[0] == "word"]


PRICES = [["Book", "Price (JD)"], ["Novel", "3"], ["Dictionary", "5"], ["Notebook", "1"]]


def draw_table(s, x, y, rows, cw=150, rh=24):
    for r, row in enumerate(rows):
        for c in range(len(row)):
            s.rect(x + c * cw, y + r * rh, cw, rh, fill="#ffffff", stroke="#5c5c5c", sw=1)
            if row[c]:
                s.text(x + c * cw + 7, y + r * rh + 16.5, row[c], 12.5, 700 if r == 0 else 400, INK)
    return y + len(rows) * rh


def word_window(s, h, tab, name="Document1 - Word", **kw):
    frame(s, h)
    title_bar(s, name)
    tabs = tab_row(s, tab)
    if tab == "Home":
        rb = home_ribbon(s, kw.get("style"))
    elif tab == "Insert":
        rb = insert_ribbon(s)
    elif tab == "View":
        rb = view_ribbon(s, kw.get("nav", False))
    else:
        ribbon_box(s)
        rb = {}
    s.rect(15, 184, W - 30, h - 224, fill=CANVAS)
    status_bar(s, h, kw.get("words", "18 words"))
    return tabs, rb


def mark_box(top, box, n, side="left", r=6, pad=3):
    x, y, w, h = box
    top.ring(x - pad, y - pad, w + 2 * pad, h + 2 * pad, r)
    if side == "left":
        top.mark(n, x - pad - 15, y + h / 2)
    elif side == "right":
        top.mark(n, x + w + pad + 15, y + h / 2)
    elif side == "top":
        top.mark(n, x + w / 2, y - pad - 15)
    else:
        top.mark(n, x + w / 2, y + h + pad + 15)


def note(top, x, y, w, text):
    """An orange label with a short instruction (a key to press, a word to type)."""
    top.rect(x, y, w, 26, fill=MARK_SOFT, stroke=MARK, sw=2, rx=13)
    top.text(x + w / 2, y + 18, text, 13, 700, MARK_INK, "middle")


# ---------- The screens --------------------------------------------------------

def lab_open_1(s, top):
    """Windows 11: click Search on the taskbar, type word, click Word."""
    h = 420
    frame(s, h)
    s.rect(15, 15, W - 30, h - 30, fill="#dfe8f3", rx=9)
    # the search panel
    s.rect(170, 40, 560, 300, fill="#f7f7f7", stroke="#c9c9c9", sw=1, rx=10)
    s.rect(190, 56, 520, 34, fill="#ffffff", stroke=WORD, sw=1.6, rx=17)
    icon_search(s, 210, 73, GREY)
    s.text(228, 78, "word", 14, 400, INK)
    s.line(262, 64, 262, 82, INK, 1.4)
    s.text(196, 118, "Best match", 12, 700, INK)
    s.rect(190, 126, 250, 56, fill="#dbe7f8", rx=6)
    s.rect(202, 136, 34, 36, fill=WORD, rx=5)
    s.rect(209, 143, 20, 22, fill="#ffffff", rx=2)
    for i in range(3):
        s.line(212, 149 + i * 5, 226, 149 + i * 5, WORD, 1.5)
    s.text(248, 152, "Word", 14, 700, INK)
    s.text(248, 170, "App", 11.5, 400, GREY)
    s.text(196, 206, "Apps", 12, 700, INK)
    s.text(204, 230, "WordPad", 12.5, 400, INK)
    s.text(204, 254, "Notepad", 12.5, 400, INK)
    # right side: the app and Open
    s.rect(460, 112, 250, 210, fill="#ffffff", rx=8)
    s.rect(560, 128, 50, 54, fill=WORD, rx=7)
    s.rect(571, 139, 28, 32, fill="#ffffff", rx=3)
    for i in range(4):
        s.line(575, 146 + i * 6, 595, 146 + i * 6, WORD, 1.6)
    s.text(585, 206, "Word", 16, 700, INK, "middle")
    s.text(585, 224, "App", 12, 400, GREY, "middle")
    s.line(480, 240, 690, 240, LINE, 1)
    icon_folder(s, 486, 254, WORD)
    s.text(518, 268, "Open", 13, 600, WORD)
    # the taskbar
    s.rect(15, h - 64, W - 30, 49, fill="#eef1f5")
    s.rect(15, h - 25, W - 30, 10, fill="#eef1f5", rx=9)
    for i in range(4):
        s.rect(372 + (i % 2) * 11, h - 52 + (i // 2) * 11, 9, 9, fill=WORD, rx=1.5)
    s.rect(405, h - 52, 150, 26, fill="#ffffff", stroke="#c9c9c9", sw=1, rx=13)
    icon_search(s, 421, h - 39, GREY)
    s.text(436, h - 34.5, "Search", 12, 400, GREY)
    s.rect(600, h - 50, 22, 18, fill="#f2b705", rx=2)
    s.rect(634, h - 52, 22, 22, fill="#0f6cbd", rx=4)
    mark_box(top, (405, h - 52, 150, 26), 1, "right", 13)
    top.label(30, 60, 132, "type: word", arrow_to=(188, 73))
    mark_box(top, (190, 126, 250, 56), 2, "left")


def lab_open_2(s, top):
    """Word opens on its start screen: click Blank document."""
    h = 380
    frame(s, h)
    s.rect(15, 15, 150, h - 30, fill="#f3f3f3", rx=9)
    s.rect(150, 15, 15, h - 30, fill="#f3f3f3")
    s.text(32, 46, "Word", 16, 700, WORD)
    for i, t in enumerate(("Home", "New", "Open")):
        y = 86 + 36 * i
        if t == "Home":
            s.rect(22, y - 21, 136, 30, fill="#e1e1e1", rx=4)
            s.rect(22, y - 17, 3, 22, fill=WORD, rx=1.5)
        s.text(40, y, t, 13.5, 600 if t == "Home" else 400, INK)
    s.text(40, h - 70, "Account", 13, 400, INK)
    s.text(40, h - 40, "Options", 13, 400, INK)
    s.text(196, 62, "Good morning", 24, 300, INK)
    names = ("Blank document", "Take a tour", "Single spaced (blank)", "Blog post")
    for i, t in enumerate(names):
        x = 196 + i * 166
        s.rect(x, 92, 140, 180, fill="#ffffff", stroke=WORD if i == 0 else "#c9c9c9", sw=2 if i == 0 else 1)
        if i == 1:
            s.text(x + 70, 160, "Welcome", 14, 700, WORD, "middle")
            for k in range(4):
                s.line(x + 24, 180 + k * 12, x + 116, 180 + k * 12, "#c3c3c3", 3)
        if i == 2:
            for k in range(6):
                s.line(x + 20, 120 + k * 12, x + 120, 120 + k * 12, "#d3d3d3", 2)
        if i == 3:
            s.rect(x + 18, 110, 104, 40, fill="#dbe7f8")
            for k in range(5):
                s.line(x + 18, 168 + k * 12, x + 122, 168 + k * 12, "#d3d3d3", 2)
        s.text(x + 70, 296, t, 12.5, 600 if i == 0 else 400, INK, "middle")
    s.text(196, 340, "Recent", 14, 700, INK)
    mark_box(top, (196, 92, 140, 180), 1, "top")




def lab_styles_1(s, top):
    """Home › Styles: click in the first line, click Title."""
    h = 520
    _, rb = word_window(s, h, "Home", style="Title")
    paras = [("Title", "Book Fair")] + TYPED[1:]
    boxes, _ = page(s, 430, 196, 480, h - 250, paras, caret=0)
    mark_box(top, boxes[0], 1, "left")
    mark_box(top, rb["Title"], 2, "bottom")


def lab_styles_2(s, top):
    """Home › Styles: click in a heading line, click Heading 1 (then the same for Prices)."""
    h = 540
    _, rb = word_window(s, h, "Home", style="Heading 1")
    paras = [("Title", "Book Fair"), ("Heading 1", "When and where"), TYPED[2], TYPED[3], ("Heading 1", "Prices")]
    boxes, _ = page(s, 430, 196, 480, h - 250, paras, caret=1)
    mark_box(top, boxes[1], 1, "left")
    mark_box(top, rb["Heading 1"], 2, "bottom")
    mark_box(top, boxes[4], 3, "left")


def lab_nav_1(s, top):
    """View › Navigation Pane: the headings in a pane on the left."""
    h = 520
    tabs, rb = word_window(s, h, "View", nav=True)
    s.rect(15, 184, 230, h - 224, fill="#ffffff")
    s.line(245, 184, 245, h - 40, "#d0d0d0", 1)
    s.text(30, 210, "Navigation", 14, 700, INK)
    s.rect(30, 222, 200, 26, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.text(38, 239, "Search document", 11.5, 400, GREY)
    s.text(36, 274, "Headings", 12, 700, WORD)
    s.line(36, 279, 92, 279, WORD, 2)
    s.text(104, 274, "Pages", 12, 400, INK)
    s.text(150, 274, "Results", 12, 400, INK)
    s.rect(30, 290, 200, 24, fill=WORD_SOFT)
    s.text(40, 307, "When and where", 12.5, 400, INK)
    s.text(40, 333, "Prices", 12.5, 400, INK)
    paras = [("Title", "Book Fair"), ("Heading 1", "When and where"), TYPED[2], TYPED[3], ("Heading 1", "Prices")]
    page(s, 300, 196, 480, h - 250, paras)
    mark_box(top, tabs["View"], 1, "top", 6, 1)
    mark_box(top, rb["nav"], 2, "bottom")
    mark_box(top, (30, 290, 200, 48), 3, "bottom", 6, 4)


def lab_format_1(s, top):
    """Home › Paragraph: click in the title, click Center."""
    h = 520
    _, rb = word_window(s, h, "Home", style="Title")
    paras = [("Title", "Book Fair"), ("Heading 1", "When and where"), TYPED[2], TYPED[3], ("Heading 1", "Prices")]
    boxes, _ = page(s, 210, 196, 480, h - 250, paras, center=(0,), caret=0)
    mark_box(top, boxes[0], 1, "left")
    mark_box(top, rb["center"], 2, "bottom", 5, 2)


def lab_format_2(s, top):
    """Home › Font: select the word free, click Bold, then a colour."""
    h = 540
    _, rb = word_window(s, h, "Home")
    paras = [("Title", "Book Fair"), ("Heading 1", "When and where"), TYPED[2], ("Normal", "Entry is free."),
             ("Heading 1", "Prices")]
    s_boxes, _ = page(s, 330, 196, 480, h - 250, paras, center=(0,), red_word=(3, "free"))
    # the word "free": its box on the page
    bx, by, bw, bh = s_boxes[3]
    ws = bx + width("Entry is ", 13.5)
    mark_box(top, (ws - 2, by, width("free", 13.5) + 4, bh), 1, "right", 4, 2)
    mark_box(top, rb["bold"], 2, "bottom", 5, 2)
    mark_box(top, rb["color"], 3, "top", 5, 2)
    # the colour list, open under the button
    s2 = top
    s2.rect(304, 152, 176, 92, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s2.text(314, 170, "Standard Colors", 11, 700, INK)
    cols = ["#c00000", "#ff0000", "#ffc000", "#ffff00", "#92d050", "#00b050", "#00b0f0", "#0070c0", "#002060", "#7030a0"]
    for i, c in enumerate(cols):
        s2.rect(314 + i * 16, 180, 13, 13, fill=c, stroke="#7a7a7a", sw=0.6)
    s2.text(314, 214, "More Colors...", 11, 400, INK)
    s2.text(314, 234, "Gradient", 11, 400, INK)
    s2.ring(328, 177, 19, 19, 3)


def lab_table_1(s, top):
    """Insert › Table: move over the squares to 2x4 Table, then click."""
    h = 560
    tabs, rb = word_window(s, h, "Insert")
    paras = [("Title", "Book Fair"), ("Heading 1", "When and where"), TYPED[2], ("Normal", "Entry is free."),
             ("Heading 1", "Prices"), ("Normal", "")]
    boxes, _ = page(s, 390, 196, 480, h - 250, paras, center=(0,), caret=5)
    # the Table list
    x0, y0 = 128, 168
    s.rect(x0, y0, 230, 250, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.rect(x0, y0, 230, 26, fill="#f3f3f3")
    s.text(x0 + 10, y0 + 18, "2x4 Table", 12.5, 700, INK)
    for r in range(8):
        for c in range(10):
            on = c < 2 and r < 4
            s.rect(x0 + 12 + c * 20.5, y0 + 34 + r * 20.5, 17, 17, fill="#fde0cd" if on else "#ffffff",
                   stroke=MARK if on else "#9a9a9a", sw=1.2 if on else 0.8)
    s.line(x0, y0 + 205, x0 + 230, y0 + 205, LINE, 1)
    s.text(x0 + 14, y0 + 224, "Insert Table...", 12, 400, INK)
    mark_box(top, tabs["Insert"], 1, "top", 6, 1)
    mark_box(top, rb["table"], 2, "right", 6, 1)
    top.ring(x0 + 10, y0 + 32, 43, 84, 4)
    top.mark(3, x0 + 31, y0 + 136)
    top.label(x0 + 240, y0 + 60, 150, "2 across, 4 down", arrow_to=(x0 + 58, y0 + 74))








def lab_spell_1(s, top):
    """A red wavy line: right-click the word, click the right spelling."""
    h = 620
    word_window(s, h, "Home", words="45 words")
    paras = [("Heading 1", "About the fair"), ("Normal", "Come to the book fair in the college library!"),
             ("Normal", "It is open from Sunday to Tuesday, 10:00 to 15:00."),
             ("Normal", "Entry is free for all studnets.")]
    _, words = page(s, 210, 196, 480, h - 250, paras, squiggle=(3, "studnets"))
    _, wx, wy, ww, wh = words[0]
    mx, my = wx + ww - 10, wy + wh + 2
    s.rect(mx, my, 220, 196, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=4)
    s.rect(mx + 2, my + 4, 216, 26, fill="#e8f0fb")
    s.text(mx + 16, my + 22, "students", 13, 700, INK)
    s.text(mx + 16, my + 48, "student's", 13, 400, INK)
    s.text(mx + 16, my + 74, "students'", 13, 400, INK)
    s.line(mx, my + 86, mx + 220, my + 86, LINE, 1)
    s.text(mx + 16, my + 106, "Ignore All", 12.5, 400, INK)
    s.text(mx + 16, my + 130, "Add to Dictionary", 12.5, 400, INK)
    s.line(mx, my + 142, mx + 220, my + 142, LINE, 1)
    s.text(mx + 16, my + 162, "Cut", 12.5, 400, INK)
    s.text(mx + 16, my + 186, "Copy", 12.5, 400, INK)
    mark_box(top, (wx, wy, ww, wh), 1, "right", 4, 2)
    top.label(36, wy + 3, 120, "right-click", arrow_to=(wx - 4, wy + 16))
    mark_box(top, (mx + 2, my + 4, 216, 26), 2, "right", 5, 1)




def lab_save_2(s, top):
    """The Save As window of Windows: Desktop, the file name, Save."""
    h = 440
    frame(s, h)
    s.rect(15, 15, W - 30, 34, fill="#f3f3f3", rx=9)
    s.rect(15, 35, W - 30, 14, fill="#f3f3f3")
    s.text(30, 37, "Save As", 13, 400, INK)
    s.line(W - 46, 27, W - 36, 39, INK, 1.3)
    s.line(W - 46, 39, W - 36, 27, INK, 1.3)
    s.rect(30, 58, 600, 28, fill="#ffffff", stroke="#c9c9c9", sw=1, rx=4)
    s.text(44, 77, "This PC  >  Desktop", 12.5, 400, INK)
    s.rect(646, 58, 222, 28, fill="#ffffff", stroke="#c9c9c9", sw=1, rx=4)
    icon_search(s, 660, 72, GREY)
    s.text(674, 77, "Search Desktop", 12, 400, GREY)
    folders = ("Home", "Desktop", "Downloads", "Documents", "Pictures", "This PC")
    for i, t in enumerate(folders):
        y = 112 + 30 * i
        if t == "Desktop":
            s.rect(28, y - 18, 180, 26, fill="#dbe7f8", rx=4)
        icon_folder(s, 38, y - 13, "#d29b00" if t != "Desktop" else WORD)
        s.text(72, y, t, 12.5, 600 if t == "Desktop" else 400, INK)
    s.line(216, 96, 216, 300, LINE, 1)
    s.text(236, 116, "Name", 12, 600, GREY)
    s.text(520, 116, "Date modified", 12, 600, GREY)
    s.line(230, 124, W - 30, 124, LINE, 1)
    icon_doc(s, 238, 136, "#185abd", 16, 20)
    s.text(264, 151, "Old report", 12.5, 400, INK)
    s.rect(15, 300, W - 30, 125, fill="#f3f3f3")
    s.rect(15, 410, W - 30, 15, fill="#f3f3f3", rx=9)
    s.text(150, 330, "File name:", 12.5, 400, INK, "end")
    s.rect(162, 314, 520, 26, fill="#ffffff", stroke=WORD, sw=1.6, rx=3)
    s.text(172, 332, "book-fair-Huda", 13, 400, INK)
    s.text(150, 364, "Save as type:", 12.5, 400, INK, "end")
    s.rect(162, 348, 520, 26, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.text(172, 366, "Word Document (*.docx)", 13, 400, INK)
    s.rect(640, 386, 110, 30, fill=WORD, rx=4)
    s.text(695, 406, "Save", 13.5, 700, "#ffffff", "middle")
    s.rect(760, 386, 110, 30, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=4)
    s.text(815, 406, "Cancel", 13.5, 400, INK, "middle")
    mark_box(top, (28, 112 + 30 - 18, 180, 26), 1, "right", 4, 1)
    mark_box(top, (162, 314, 520, 26), 2, "right", 4, 2)
    mark_box(top, (640, 386, 110, 30), 3, "left", 4, 2)


def lab_result_1(s, top):
    """The notice at the end of the worksheet."""
    h = 760
    word_window(s, h, "Home", name="book-fair-Huda - Word", words="42 words")
    paras = [("Title", "Book Fair"), ("Heading 1", "When and where"), TYPED[2], ("Normal", "Entry is free."),
             ("Heading 1", "Prices"), ("Heading 1", "About the fair"),
             ("Normal", "Come to the book fair in the college library!"),
             ("Normal", "It is open from Sunday to Tuesday, 10:00 to 15:00."),
             ("Normal", "Entry is free for all students.")]
    page(s, 210, 192, 480, h - 236, paras, center=(0,), bold_word=(3, "free", RED), table=PRICES, table_at=4)


# name: (the drawing, the part of it that the worksheet shows: x, y, width, height).
# A crop zooms in on the buttons of the step, so that they are big on paper.
SCREENS = {
    "lab-open-1": (lab_open_1, None),
    "lab-open-2": (lab_open_2, (176, 28, 370, 300)),
    "lab-styles-1": (lab_styles_1, (440, 80, 445, 220)),
    "lab-styles-2": (lab_styles_2, (440, 80, 445, 340)),
    "lab-nav-1": (lab_nav_1, (15, 26, 650, 350)),
    "lab-format-1": (lab_format_1, (220, 80, 480, 200)),
    "lab-format-2": (lab_format_2, (90, 80, 470, 320)),
    "lab-table-1": (lab_table_1, (20, 26, 530, 410)),
    "lab-spell-1": (lab_spell_1, (24, 200, 640, 380)),
    "lab-save-2": (lab_save_2, None),
    "lab-result-1": (lab_result_1, (200, 186, 500, 530)),
}

def draw(fn, crop=None):
    s, top = Svg(), Svg()
    fn(s, top)
    # the height is the one of the frame (the first element)
    h = float(s.out[0].split('height="')[1].split('"')[0])
    x, y, w, hh = crop or (0, 0, W, h)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="%g %g %g %g" font-family="%s">'
           % (w, hh, x, y, w, hh, FONT)]
    out.extend(s.out)
    out.extend(top.out)
    out.append("</svg>")
    return "\n".join(out) + "\n"


def has_font(name):
    try:
        return name.lower() in subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout.lower()
    except OSError:
        return False


def export_png(svg_path):
    png = svg_path[:-4] + ".png"
    src = svg_path
    tmp = None
    if not (has_font("Helvetica") or has_font("Arial")) and has_font("Liberation Sans"):
        with open(svg_path, encoding="utf-8") as f:
            text = f.read().replace(FONT, "Liberation Sans")
        tmp = tempfile.NamedTemporaryFile("w", suffix=".svg", dir=os.path.dirname(svg_path), delete=False,
                                          encoding="utf-8")
        tmp.write(text)
        tmp.close()
        src = tmp.name
    try:
        subprocess.run(["quarto", "typst", "compile", "--root", ROOT, "--input",
                        "svg=/" + os.path.relpath(src, ROOT).replace(os.sep, "/"),
                        os.path.join(ROOT, "shared", "sims", "export-poster.typ"), png, "--ppi", "200"], check=True)
    finally:
        if tmp:
            os.unlink(tmp.name)


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for name, (fn, crop) in SCREENS.items():
        if only and not any(o in name for o in only):
            continue
        svg = os.path.join(ROOT, OUT + name + ".svg")
        with open(svg, "w", encoding="utf-8") as f:
            f.write(draw(fn, crop))
        if "--svg" not in sys.argv:
            export_png(svg)
        print("wrote", os.path.relpath(svg, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
