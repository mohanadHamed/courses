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
from phone_screens import (Svg, FONT, INK, GREY, LIGHT, LINE, BG, MARK, MARK_INK, MARK_SOFT,  # noqa: E402
                           icon_search, icon_folder, icon_doc)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "courses/digital-skills/"   # + "week-WW/images/<name>" (the keys of SCREENS)

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

def open_search(s, top, app="Word", color=WORD):
    """Windows 11: click Search on the taskbar, type the name of the app, click the app."""
    h = 420
    frame(s, h)
    s.rect(15, 15, W - 30, h - 30, fill="#dfe8f3", rx=9)
    # the search panel
    s.rect(170, 40, 560, 300, fill="#f7f7f7", stroke="#c9c9c9", sw=1, rx=10)
    s.rect(190, 56, 520, 34, fill="#ffffff", stroke=color, sw=1.6, rx=17)
    icon_search(s, 210, 73, GREY)
    s.text(228, 78, app.lower(), 14, 400, INK)
    s.line(232 + width(app.lower(), 14), 64, 232 + width(app.lower(), 14), 82, INK, 1.4)
    s.text(196, 118, "Best match", 12, 700, INK)
    s.rect(190, 126, 250, 56, fill="#dbe7f8", rx=6)
    s.rect(202, 136, 34, 36, fill=color, rx=5)
    s.rect(209, 143, 20, 22, fill="#ffffff", rx=2)
    for i in range(3):
        s.line(212, 149 + i * 5, 226, 149 + i * 5, color, 1.5)
    s.text(248, 152, app, 14, 700, INK)
    s.text(248, 170, "App", 11.5, 400, GREY)
    s.text(196, 206, "Apps", 12, 700, INK)
    s.text(204, 230, "WordPad", 12.5, 400, INK)
    s.text(204, 254, "Notepad", 12.5, 400, INK)
    # right side: the app and Open
    s.rect(460, 112, 250, 210, fill="#ffffff", rx=8)
    s.rect(560, 128, 50, 54, fill=color, rx=7)
    s.rect(571, 139, 28, 32, fill="#ffffff", rx=3)
    for i in range(4):
        s.line(575, 146 + i * 6, 595, 146 + i * 6, color, 1.6)
    s.text(585, 206, app, 16, 700, INK, "middle")
    s.text(585, 224, "App", 12, 400, GREY, "middle")
    s.line(480, 240, 690, 240, LINE, 1)
    icon_folder(s, 486, 254, color)
    s.text(518, 268, "Open", 13, 600, color)
    # the taskbar
    s.rect(15, h - 64, W - 30, 49, fill="#eef1f5")
    s.rect(15, h - 25, W - 30, 10, fill="#eef1f5", rx=9)
    for i in range(4):
        s.rect(372 + (i % 2) * 11, h - 52 + (i // 2) * 11, 9, 9, fill=color, rx=1.5)
    s.rect(405, h - 52, 150, 26, fill="#ffffff", stroke="#c9c9c9", sw=1, rx=13)
    icon_search(s, 421, h - 39, GREY)
    s.text(436, h - 34.5, "Search", 12, 400, GREY)
    s.rect(600, h - 50, 22, 18, fill="#f2b705", rx=2)
    s.rect(634, h - 52, 22, 22, fill="#0f6cbd", rx=4)
    mark_box(top, (405, h - 52, 150, 26), 1, "right", 13)
    top.label(26, 60, 140, "type: " + app.lower(), arrow_to=(188, 73))
    mark_box(top, (190, 126, 250, 56), 2, "left")




def lab_open_1(s, top):
    open_search(s, top)


def open_start(s, top, app="Word", color=WORD, blank="Blank document"):
    """The start screen of the app: click Blank document (workbook, presentation)."""
    h = 380
    frame(s, h)
    s.rect(15, 15, 150, h - 30, fill="#f3f3f3", rx=9)
    s.rect(150, 15, 15, h - 30, fill="#f3f3f3")
    s.text(32, 46, app, 16, 700, color)
    for i, t in enumerate(("Home", "New", "Open")):
        y = 86 + 36 * i
        if t == "Home":
            s.rect(22, y - 21, 136, 30, fill="#e1e1e1", rx=4)
            s.rect(22, y - 17, 3, 22, fill=color, rx=1.5)
        s.text(40, y, t, 13.5, 600 if t == "Home" else 400, INK)
    s.text(40, h - 70, "Account", 13, 400, INK)
    s.text(40, h - 40, "Options", 13, 400, INK)
    s.text(196, 62, "Good morning", 24, 300, INK)
    names = (blank, "Take a tour", "Templates", "More")
    for i, t in enumerate(names):
        x = 196 + i * 166
        s.rect(x, 92, 140, 180, fill="#ffffff", stroke=color if i == 0 else "#c9c9c9", sw=2 if i == 0 else 1)
        if i == 1:
            s.text(x + 70, 160, "Welcome", 14, 700, color, "middle")
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


def lab_open_2(s, top):
    """Word opens on its start screen: click Blank document."""
    open_start(s, top)


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
    """A red wavy line under a word that you typed: right-click it, click the right spelling."""
    h = 560
    word_window(s, h, "Home", words="18 words")
    paras = [("Title", "Book Fair"), ("Heading 1", "When and where"),
             ("Normal", "Sunday to Tuesday, 10:00 to 15:00, in the college libary."), ("Normal", "Entry is free.")]
    _, words = page(s, 120, 196, 560, h - 250, paras, squiggle=(2, "libary"))
    _, wx, wy, ww, wh = words[0]
    mx, my = wx - 60, wy + wh + 2
    s.rect(mx, my, 200, 150, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=4)
    s.rect(mx + 2, my + 4, 196, 26, fill="#e8f0fb")
    s.text(mx + 16, my + 22, "library", 13, 700, INK)
    s.text(mx + 16, my + 48, "libraries", 13, 400, INK)
    s.line(mx, my + 60, mx + 200, my + 60, LINE, 1)
    s.text(mx + 16, my + 80, "Ignore All", 12.5, 400, INK)
    s.text(mx + 16, my + 104, "Add to Dictionary", 12.5, 400, INK)
    s.line(mx, my + 116, mx + 200, my + 116, LINE, 1)
    s.text(mx + 16, my + 138, "Copy", 12.5, 400, INK)
    mark_box(top, (wx, wy, ww, wh), 1, "right", 4, 2)
    top.label(wx + ww + 40, wy - 36, 120, "right-click", arrow_to=(wx + ww + 2, wy + 4))
    mark_box(top, (mx + 2, my + 4, 196, 26), 2, "left", 5, 1)


def browser(s, h, address, tab=None):
    """A browser window (Microsoft Edge or Chrome on Windows): the tab bar and the address."""
    frame(s, h)
    s.rect(15, 15, W - 30, 70, fill="#f3f3f3", rx=9)
    s.rect(30, 22, 200, 26, fill="#ffffff", rx=6)
    s.text(46, 40, tab or address, 12.5, 400, INK)
    s.rect(30, 54, W - 60, 24, fill="#ffffff", stroke="#d6d6d6", sw=1, rx=12)
    s.text(48, 70.5, address, 12.5, 400, INK)


TEAL = "#0f7a6e"         # the colour of tutudocs.com
TEAL_SOFT = "#e3f4f1"


def tutu_doc_icon(s, x, y):
    s.path("M%g %g h11 l6 6 v14 h-17 z" % (x, y), fill="#4a7ff0")
    for i in range(3):
        s.line(x + 4, y + 9 + i * 3.5, x + 13, y + 9 + i * 3.5, "#ffffff", 1.2)


def lab_tutu_1(s, top):
    """tutudocs.com, the home page: no sign-up; click the drop box and choose the file."""
    h = 470
    browser(s, h, "tutudocs.com", "TutuDocs")
    s.rect(15, 85, W - 30, h - 100, fill="#f6fafa")
    s.text(40, 112, "TutuDocs", 16, 700, INK)
    for x, w_ in ((520, "Templates"), (600, "Tools"), (650, "AI assistant")):
        s.text(x, 112, w_, 12.5, 400, GREY)
    s.rect(790, 96, 76, 26, fill="#ffffff", stroke="#d6d6d6", sw=1, rx=6)
    s.text(828, 113.5, "Sign in", 12.5, 600, INK, "middle")
    s.text(W / 2, 162, "Free online Word, Excel & PowerPoint", 25, 700, INK, "middle")
    s.text(W / 2, 186, "No sign-up · No install · Unlimited use · Free AI every day", 12.5, 400, GREY, "middle")
    for i, (a_, b_) in enumerate((("Write a document", "Word · DOCX"), ("Make a spreadsheet", "Excel · XLSX"), ("Make slides", "Slides · PPTX"))):
        x = 200 + i * 172
        s.rect(x, 202, 160, 74, fill="#ffffff", stroke="#dde3e3", sw=1, rx=10)
        s.rect(x + 66, 210, 28, 24, fill=TEAL_SOFT, rx=6)
        s.text(x + 80, 254, a_, 13, 700, INK, "middle")
        s.text(x + 80, 269, b_, 10.5, 400, GREY, "middle")
    s.rect(200, 290, 504, 78, fill="#ffffff", stroke="#a9bdb9", sw=1.4, rx=10)
    s.raw('<rect x="200" y="290" width="504" height="78" rx="10" fill="none" stroke="#a9bdb9" stroke-width="1.6" stroke-dasharray="6 5"/>')
    s.path("M452 312 v-12 M446 306 l6 -6 l6 6 M444 316 h16", stroke=TEAL, sw=1.8)
    s.text(W / 2, 338, "Drop a file anywhere on this page, or click to choose", 14, 600, INK, "middle")
    s.text(W / 2, 356, "Word / Excel / PPT / PDF / CSV / TXT all open", 11, 400, GREY, "middle")
    s.rect(200, 382, 504, 40, fill="#ffffff", stroke="#dde3e3", sw=1, rx=10)
    s.text(222, 407, "Tell us what you need…", 12.5, 400, LIGHT)
    s.rect(616, 388, 80, 28, fill="#8fc7bf", rx=6)
    s.text(656, 406.5, "Send to AI", 11.5, 600, "#ffffff", "middle")
    mark_box(top, (200, 290, 504, 78), 1, "left", 10, 3)
    top.label(430, 430, 290, "then: Desktop › your file › Open")


def tutu_editor(s, h, title_blue=True, panel=True):
    browser(s, h, "tutudocs.com/doc", "book-fair-Huda")
    tutu_doc_icon(s, 30, 96)
    s.text(56, 112, "book-fair-Huda", 15, 400, INK)
    s.text(170, 111, "Saved locally · Sign in to save to cloud", 11, 400, "#2b8a3e")
    ai = (430, 96, 112, 26)
    s.rect(*ai, fill=TEAL_SOFT, stroke="#8fd1c4", sw=1.2, rx=6)
    s.text(486, 113.5, "AI Assistant", 12.5, 700, TEAL, "middle")
    s.rect(560, 96, 92, 26, fill="#d8e9fb", rx=13)
    s.text(606, 113.5, "Share", 12.5, 700, INK, "middle")
    s.rect(800, 96, 70, 26, fill=TEAL, rx=13)
    s.text(835, 113.5, "Sign in", 12.5, 700, "#ffffff", "middle")
    menus = {}
    x = 30
    for m in ("File", "Edit", "View", "Insert", "Format", "Tools", "Help"):
        s.text(x, 145, m, 12.5, 400, INK)
        menus[m] = (x - 6, 131, 7.6 * len(m) + 12, 20)
        x += 7.6 * len(m) + 22
    s.line(15, 156, W - 15, 156, "#e6e6e6", 1)
    for i, c in enumerate(("B", "I", "U")):
        s.text(40 + i * 26, 175, c, 13, 700 if c == "B" else 400, GREY)
    s.text(130, 175, "Normal", 12, 400, GREY)
    s.text(190, 175, "11", 12, 400, GREY)
    s.text(225, 175, "Arial", 12, 400, GREY)
    s.line(15, 186, W - 15, 186, "#e6e6e6", 1)
    pw = 560 if panel else W - 30
    s.rect(15, 187, pw, h - 202, fill="#f4f5f7")
    s.rect(50, 200, pw - 70, h - 222, fill="#ffffff", stroke="#e0e0e0", sw=1)
    ys = 238
    s.text(80, ys, "Book Fair", 22, 400, "#1c7ed6" if title_blue else INK)
    s.text(80, ys + 34, "When and where", 16, 700, INK)
    s.text(80, ys + 56, "Sunday to Tuesday, 10:00 to 15:00, in the college library.", 11.5, 400, INK)
    s.raw('<text x="80" y="%g" font-size="11.5" fill="%s">Entry is <tspan font-weight="700">free</tspan>.</text>' % (ys + 72, INK))
    s.text(80, ys + 102, "Prices", 16, 700, INK)
    return ai, menus


def lab_tutu_2(s, top):
    """The editor: AI Assistant, the request, and the answer; the title is blue in the page."""
    h = 470
    ai, _ = tutu_editor(s, h)
    px = 575
    s.rect(px, 187, W - 15 - px, h - 202, fill="#ffffff")
    s.line(px, 187, px, h - 15, "#e3e3e3", 1)
    s.text(px + 14, 210, "AI assistant", 13.5, 700, INK)
    s.rect(px + 90, 228, 205, 26, fill="#d9f0f5", rx=12)
    s.text(px + 192, 245.5, "Make the title Book Fair blue.", 11.5, 400, INK, "middle")
    s.text(px + 14, 282, "Done: the title Book Fair is", 12, 400, INK)
    s.text(px + 14, 299, "now blue. Everything else is", 12, 400, INK)
    s.text(px + 14, 316, "the same.", 12, 400, INK)
    box = (px + 10, 372, W - 25 - px - 10, 72)
    s.rect(*box, fill="#ffffff", stroke=TEAL, sw=1.4, rx=12)
    s.text(px + 24, 395, "Ask AI anything…", 12.5, 400, LIGHT)
    s.circle(W - 52, 424, 13, fill="#eef0f2")
    s.poly([(W - 59, 418), (W - 44, 424), (W - 59, 430), (W - 56, 424)], fill=GREY)
    mark_box(top, ai, 1, "bottom", 6, 2)
    mark_box(top, (box[0], box[1], box[2], 36), 2, "left", 10, 2)
    mark_box(top, (px + 90, 228, 205, 26), 3, "left", 12, 2)
    top.label(330, 214, 170, "the title is blue!", arrow_to=(190, 230))


def lab_tutu_3(s, top):
    """File › Download › Microsoft Word (.docx)."""
    h = 470
    _, menus = tutu_editor(s, h, panel=False)
    mx, my = 20, 156
    items = ("New document", "Open...", "Make a copy", "Share", "Download", "Rename", "Save to browser", "Print...")
    s.rect(mx, my, 220, 30 * len(items) + 10, fill="#ffffff", stroke="#d0d0d0", sw=1, rx=8)
    for i, it in enumerate(items):
        y = my + 8 + i * 30
        if it == "Download":
            s.rect(mx + 4, y, 212, 28, fill=TEAL_SOFT, rx=5)
            s.text(mx + 200, y + 19, "›", 14, 700, INK)
        s.text(mx + 18, y + 19, it, 12.5, 600 if it == "Download" else 400, INK)
    dy = my + 8 + 4 * 30
    sx = mx + 222
    subs = ("Microsoft Word (.docx)", "PDF", "HTML", "Plain text", "Markdown (.md)")
    s.rect(sx, dy, 200, 30 * len(subs) + 8, fill="#ffffff", stroke="#d0d0d0", sw=1, rx=8)
    for i, it in enumerate(subs):
        y = dy + 4 + i * 30
        if i == 0:
            s.rect(sx + 4, y, 192, 28, fill=TEAL_SOFT, rx=5)
        s.text(sx + 16, y + 19, it, 12.5, 600 if i == 0 else 400, INK)
    mark_box(top, menus["File"], 1, "top", 4, 1)
    mark_box(top, (mx + 4, dy, 212, 28), 2, "left", 5, 1)
    mark_box(top, (sx + 4, dy + 4, 192, 28), 3, "right", 5, 1)


def save_as(s, top, name="book-fair-Huda", kind="Word Document (*.docx)", color=WORD):
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
    s.text(172, 332, name, 13, 400, INK)
    s.text(150, 364, "Save as type:", 12.5, 400, INK, "end")
    s.rect(162, 348, 520, 26, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.text(172, 366, kind, 13, 400, INK)
    s.rect(640, 386, 110, 30, fill=color, rx=4)
    s.text(695, 406, "Save", 13.5, 700, "#ffffff", "middle")
    s.rect(760, 386, 110, 30, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=4)
    s.text(815, 406, "Cancel", 13.5, 400, INK, "middle")
    mark_box(top, (28, 112 + 30 - 18, 180, 26), 1, "right", 4, 1)
    mark_box(top, (162, 314, 520, 26), 2, "right", 4, 2)
    mark_box(top, (640, 386, 110, 30), 3, "left", 4, 2)


def lab_save_2(s, top):
    save_as(s, top)


def lab_result_1(s, top):
    """The notice at the end of the worksheet."""
    h = 560
    word_window(s, h, "Home", name="book-fair-Huda - Word", words="27 words")
    paras = [("Title", "Book Fair"), ("Heading 1", "When and where"), TYPED[2], ("Normal", "Entry is free."),
             ("Heading 1", "Prices")]
    page(s, 210, 192, 480, h - 236, paras, center=(0,), bold_word=(3, "free", RED), table=PRICES, table_at=4)



# =====================================================================
# Generic tutudocs.com screens (the AI Extra of every lecture): the home
# page is the same for every file; the editor shows a document, a sheet or
# slides; the Download menu ends with the file type of the app.
# =====================================================================

def tutu_home(s, top):
    lab_tutu_1(s, top)


def tutu_shell(s, h, name, kind, panel=True):
    """The online editor of tutudocs.com, its top bar and menus; returns (AI button, menus, page box)."""
    browser(s, h, "tutudocs.com/" + {"doc": "doc", "sheet": "excel", "slides": "ppt"}[kind], name)
    colour = {"doc": "#4a7ff0", "sheet": "#1f9d55", "slides": "#f0a020"}[kind]
    s.path("M30 96 h11 l6 6 v14 h-17 z", fill=colour)
    s.text(56, 112, name, 15, 400, INK)
    s.text(56 + width(name, 15) + 12, 111, "Saved locally · Sign in to save to cloud", 11, 400, "#2b8a3e")
    ai = (470, 96, 112, 26)
    s.rect(*ai, fill=TEAL_SOFT, stroke="#8fd1c4", sw=1.2, rx=6)
    s.text(526, 113.5, "AI Assistant", 12.5, 700, TEAL, "middle")
    s.rect(600, 96, 92, 26, fill="#d8e9fb", rx=13)
    s.text(646, 113.5, "Share", 12.5, 700, INK, "middle")
    s.rect(800, 96, 70, 26, fill=TEAL, rx=13)
    s.text(835, 113.5, "Sign in", 12.5, 700, "#ffffff", "middle")
    names = {"doc": ("File", "Edit", "View", "Insert", "Format", "Tools", "Help"),
             "sheet": ("File", "Edit", "View", "Insert", "Format", "Data", "Help"),
             "slides": ("File", "Edit", "View", "Insert", "Format", "Slide", "Arrange", "Tools", "Help")}[kind]
    menus, x = {}, 30
    for m in names:
        s.text(x, 145, m, 12.5, 400, INK)
        menus[m] = (x - 6, 131, 7.6 * len(m) + 12, 20)
        x += 7.6 * len(m) + 22
    s.line(15, 156, W - 15, 156, "#e6e6e6", 1)
    s.line(15, 186, W - 15, 186, "#e6e6e6", 1)
    pw = 560 if panel else W - 30
    s.rect(15, 187, pw, h - 202, fill="#f4f5f7")
    return ai, menus, (15, 187, pw, h - 202)


def tutu_ai(s, top, name, kind, ask, answer, draw_page, note=None, note_to=None):
    """The AI Assistant: the request and the answer; draw_page(s, box) draws the changed file."""
    h = 470
    ai, _, box = tutu_shell(s, h, name, kind)
    draw_page(s, box)
    px = 575
    s.rect(px, 187, W - 15 - px, h - 202, fill="#ffffff")
    s.line(px, 187, px, h - 15, "#e3e3e3", 1)
    s.text(px + 14, 210, "AI assistant", 13.5, 700, INK)
    lines = wrap_text(ask, 11.5, 230)
    bh = 12 + 16 * len(lines)
    s.rect(W - 25 - 250, 224, 250, bh, fill="#d9f0f5", rx=12)
    for i, ln in enumerate(lines):
        s.text(W - 25 - 238, 241 + 16 * i, ln, 11.5, 400, INK)
    for i, ln in enumerate(wrap_text(answer, 12, 270)):
        s.text(px + 14, 224 + bh + 30 + 17 * i, ln, 12, 400, INK)
    b = (px + 10, 372, W - 25 - px - 10, 72)
    s.rect(*b, fill="#ffffff", stroke=TEAL, sw=1.4, rx=12)
    s.text(px + 24, 395, "Ask AI anything…", 12.5, 400, LIGHT)
    s.circle(W - 52, 424, 13, fill="#eef0f2")
    s.poly([(W - 59, 418), (W - 44, 424), (W - 59, 430), (W - 56, 424)], fill=GREY)
    mark_box(top, ai, 1, "bottom", 6, 2)
    mark_box(top, (b[0], b[1], b[2], 36), 2, "left", 10, 2)
    mark_box(top, (W - 25 - 250, 224, 250, bh), 3, "left", 12, 2)
    if note:
        top.label(330, 200, 170, note, arrow_to=note_to)


def tutu_download(s, top, name, kind, pick=0):
    """File › Download › the file of the app."""
    h = 470
    _, menus, box = tutu_shell(s, h, name, kind, panel=False)
    mx, my = 20, 156
    items = ("New", "Open...", "Make a copy", "Share", "Download", "Rename", "Save to browser", "Print...")
    s.rect(mx, my, 220, 30 * len(items) + 10, fill="#ffffff", stroke="#d0d0d0", sw=1, rx=8)
    for i, it in enumerate(items):
        y = my + 8 + i * 30
        if it == "Download":
            s.rect(mx + 4, y, 212, 28, fill=TEAL_SOFT, rx=5)
            s.text(mx + 200, y + 19, "›", 14, 700, INK)
        s.text(mx + 18, y + 19, it, 12.5, 600 if it == "Download" else 400, INK)
    dy, sx = my + 8 + 4 * 30, mx + 222
    first = {"doc": "Microsoft Word (.docx)", "sheet": "Microsoft Excel (.xlsx)", "slides": "Microsoft PowerPoint (.pptx)"}[kind]
    subs = (first, "PDF", "HTML", "Plain text")
    s.rect(sx, dy, 220, 30 * len(subs) + 8, fill="#ffffff", stroke="#d0d0d0", sw=1, rx=8)
    for i, it in enumerate(subs):
        y = dy + 4 + i * 30
        if i == pick:
            s.rect(sx + 4, y, 212, 28, fill=TEAL_SOFT, rx=5)
        s.text(sx + 16, y + 19, it, 12.5, 600 if i == pick else 400, INK)
    mark_box(top, menus["File"], 1, "top", 4, 1)
    mark_box(top, (mx + 4, dy, 212, 28), 2, "left", 5, 1)
    mark_box(top, (sx + 4, dy + 4 + 30 * pick, 212, 28), 3, "right", 5, 1)


def wrap_text(text, size, maxw):
    out, line = [], ""
    for w_ in text.split():
        trial = (line + " " + w_).strip()
        if width(trial, size) > maxw and line:
            out.append(line)
            line = w_
        else:
            line = trial
    if line:
        out.append(line)
    return out


# =====================================================================
# PowerPoint for Windows (Lecture 5): the window, the Home, Design,
# Transitions and Animations tabs, the thumbnails, the slide and the notes.
# =====================================================================

PPT = "#c43e1c"
PPT_SOFT = "#fbe3dc"
PPT_TABS = ("File", "Home", "Insert", "Draw", "Design", "Transitions", "Animations", "Slide Show", "Review", "View", "Help")


def ppt_tabs(s, active):
    s.rect(15, 49, W - 30, 30, fill=TITLE_BG)
    x, pos = 30, {}
    for tname in PPT_TABS:
        w_ = width(tname, 13) + 4
        on = tname == active
        s.text(x, 69, tname, 13, 700 if on else 400, PPT if on else INK)
        if on:
            s.rect(x - 2, 74, w_, 3, fill=PPT, rx=1.5)
        pos[tname] = (x - 6, 52, w_ + 12, 26)
        x += w_ + 14
    return pos


def ppt_ribbon(s, tab, theme=None, trans=None, anim=None):
    ribbon_box(s)
    p = {}
    if tab == "Home":
        s.rect(34, 92, 30, 36, fill="#ffffff", stroke="#7a7a7a", sw=1.3, rx=3)
        s.text(46, 156, "Paste", 11.5, 400, INK)
        group(s, 20, 96, "Clipboard")
        p["newslide"] = (104, 88, 70, 80)
        s.rect(104, 88, 70, 80, fill=BTN, rx=4)
        s.rect(122, 94, 34, 26, fill="#ffffff", stroke=PPT, sw=1.4, rx=2)
        s.rect(126, 98, 26, 5, fill=PPT_SOFT)
        s.text(139, 140, "New", 11.5, 400, INK, "middle")
        s.text(139, 154, "Slide ▾", 11.5, 400, INK, "middle")
        p["layout"] = (180, 92, 70, 20)
        s.text(184, 106, "Layout ▾", 11.5, 400, INK)
        s.text(184, 128, "Reset", 11.5, 400, INK)
        s.text(184, 150, "Section ▾", 11.5, 400, INK)
        group(s, 96, 262, "Slides")
        dropdown(s, 272, 92, 120, "Aptos (Body)")
        dropdown(s, 396, 92, 44, "28")
        for i, c in enumerate(("B", "I", "U", "S")):
            small_btn(s, 272 + i * 26, 124, 24, 24, c, 13, 800 if c == "B" else 400)
        s.rect(380, 124, 32, 24, fill=BTN, rx=3)
        s.text(392, 139, "A", 14, 700, INK, "middle")
        s.rect(384, 142, 16, 4, fill=RED)
        group(s, 262, 450, "Font")
        for i, k in enumerate(("left", "center", "right", "justify")):
            s.rect(460 + i * 28 - 4, 124, 24, 24, fill=BTN, rx=3)
            align_icon(s, 460 + i * 28, 130, k)
        list_icon(s, 460, 96)
        list_icon(s, 490, 96, True)
        group(s, 450, 590, "Paragraph")
        for i, sh in enumerate(("Shapes", "Arrange", "Quick Styles")):
            s.text(600, 104 + i * 22, sh, 11.5, 400, INK)
        group(s, 590, 700, "Drawing")
        s.text(712, 104, "Find", 11.5, 400, INK)
        s.text(712, 126, "Replace", 11.5, 400, INK)
        s.text(712, 148, "Select", 11.5, 400, INK)
        group(s, 700, 790, "Editing")
        big_btn(s, 800, 70, "Designer", ic_page)
        s.text(835, 177, "Designer", 10.5, 400, GREY, "middle")
    elif tab == "Design":
        themes = [("Office Theme", "#ffffff", INK), ("Facet", "#e7f4e4", "#2b7a3b"), ("Integral", "#eaf2fb", "#1f4e8c"),
                  ("Ion", "#1a6e8e", "#ffffff"), ("Retrospect", "#fbefe3", "#a14f17"), ("Slice", "#244a6b", "#ffffff")]
        for i, (n, bg, fg) in enumerate(themes):
            x = 24 + i * 76
            on = n == theme
            p["theme:" + n] = (x, 88, 70, 62)
            s.rect(x, 88, 70, 62, fill=bg, stroke=PPT if on else "#cfcfcf", sw=2 if on else 1, rx=3)
            s.text(x + 10, 112, "Aa", 18, 400, fg)
            s.rect(x + 10, 132, 50, 4, fill=fg, opacity=0.6)
        group(s, 20, 484, "Themes")
        for i, c in enumerate(("#2b7a3b", "#1f4e8c", "#a14f17", "#6b3fa0")):
            x = 494 + i * 40
            p["variant:%d" % i] = (x, 96, 34, 50)
            s.rect(x, 96, 34, 50, fill="#ffffff", stroke="#cfcfcf", sw=1, rx=3)
            s.rect(x + 4, 136, 26, 6, fill=c)
        group(s, 488, 660, "Variants")
        s.text(672, 108, "Slide Size ▾", 11.5, 400, INK)
        s.text(672, 132, "Format Background", 11.5, 400, INK)
        group(s, 664, 790, "Customize")
        big_btn(s, 800, 70, "Designer", ic_page)
        s.text(835, 177, "Designer", 10.5, 400, GREY, "middle")
    elif tab == "Insert":
        big_btn(s, 24, 64, "New", ic_page, "Slide ▾")
        group(s, 20, 96, "Slides")
        big_btn(s, 104, 54, "Table", ic_table)
        group(s, 100, 166, "Tables")
        big_btn(s, 176, 64, "Pictures", ic_picture)
        p["icons"] = (244, 88, 54, 80)
        big_btn(s, 244, 54, "Icons", lambda s_, x, y: s_.poly([(x, y - 13), (x + 4, y - 4), (x + 13, y - 4), (x + 6, y + 2), (x + 9, y + 12), (x, y + 6), (x - 9, y + 12), (x - 6, y + 2), (x - 13, y - 4), (x - 4, y - 4)], fill=PPT))
        big_btn(s, 302, 58, "Shapes", ic_shapes)
        group(s, 172, 370, "Images & Illustrations")
        big_btn(s, 380, 60, "Text", ic_page, "Box")
        group(s, 376, 450, "Text")
    elif tab == "Transitions":
        big_btn(s, 24, 60, "Preview", ic_page)
        group(s, 20, 92, "Preview")
        for i, n in enumerate(("None", "Morph", "Fade", "Push", "Wipe", "Split", "Vortex")):
            x = 102 + i * 66
            on = n == trans
            p["t:" + n] = (x, 88, 60, 62)
            s.rect(x, 88, 60, 62, fill=PPT_SOFT if on else "#ffffff", stroke=PPT if on else "#e0e0e0", sw=1.4 if on else 1, rx=3)
            s.rect(x + 18, 96, 24, 24, fill="#f3f3f3", stroke="#9a9a9a", sw=1, rx=2)
            s.text(x + 30, 142, n, 11, 400, INK, "middle")
        group(s, 98, 572, "Transition to This Slide")
        s.text(584, 106, "Effect Options ▾", 11.5, 400, INK)
        s.text(690, 106, "Duration: 01.00", 11.5, 400, INK)
        p["applyall"] = (684, 136, 110, 24)
        s.rect(684, 136, 110, 24, fill=BTN, rx=3)
        s.text(739, 152.5, "Apply To All", 11.5, 700, INK, "middle")
        s.text(584, 152.5, "Sound: [No Sound]", 11, 400, GREY)
        group(s, 576, 820, "Timing")
    elif tab == "Animations":
        big_btn(s, 24, 60, "Preview", ic_page)
        group(s, 20, 92, "Preview")
        for i, (n, c) in enumerate((("None", "#9a9a9a"), ("Appear", "#2b8a3e"), ("Fade", "#2b8a3e"), ("Fly In", "#2b8a3e"),
                                    ("Float In", "#2b8a3e"), ("Wipe", "#2b8a3e"), ("Zoom", "#2b8a3e"))):
            x = 102 + i * 66
            on = n == anim
            p["a:" + n] = (x, 88, 60, 62)
            s.rect(x, 88, 60, 62, fill=PPT_SOFT if on else "#ffffff", stroke=PPT if on else "#e0e0e0", sw=1.4 if on else 1, rx=3)
            s.poly([(x + 30, 96), (x + 40, 116), (x + 20, 116)], fill=c)
            s.text(x + 30, 142, n, 11, 400, INK, "middle")
        group(s, 98, 572, "Animation")
        s.text(584, 106, "Effect Options ▾", 11.5, 400, INK)
        s.text(584, 130, "Add Animation ▾", 11.5, 400, INK)
        s.text(584, 154, "Animation Pane", 11.5, 400, INK)
        s.text(700, 106, "Start: On Click", 11.5, 400, INK)
        s.text(700, 130, "Duration: 00.50", 11.5, 400, INK)
        group(s, 576, 820, "Timing")
    return p


SLIDES = {
    "title": {"title": "Our Book Fair", "sub": "Sunrise College · Sunday to Tuesday"},
    "when": {"title": "When and where", "points": ["Sunday to Tuesday", "10:00 to 15:00", "The college library"]},
}


def ppt_slide(s, x, y, w, slide, theme=None, empty=False, sel=None, scale=1.0):
    """A slide 16:9 at (x, y), width w; returns the boxes of its title and body."""
    hgt = w * 9 / 16
    bg, fg, acc = {"Facet": ("#e7f4e4", "#1f3d28", "#2b7a3b"), "Ion": ("#1a6e8e", "#ffffff", "#ffd43b"),
                   "Integral": ("#eaf2fb", "#1f2f4c", "#1f4e8c")}.get(theme, ("#ffffff", INK, INK))
    s.rect(x, y, w, hgt, fill=bg, stroke="#bfbfbf", sw=1)
    if theme == "Facet":
        s.rect(x, y, w * 0.06, hgt, fill=acc)
    boxes = {}
    k = w / 480
    if slide is None or empty:
        tb = (x + 30 * k, y + 70 * k, w - 60 * k, 70 * k)
        s.raw('<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="#9a9a9a" stroke-dasharray="4 3"/>' % tb)
        s.text(x + w / 2, tb[1] + tb[3] / 2 + 8 * k, "Click to add title", 26 * k, 400, GREY, "middle")
        sb = (x + 70 * k, y + 160 * k, w - 140 * k, 40 * k)
        s.raw('<rect x="%g" y="%g" width="%g" height="%g" fill="none" stroke="#9a9a9a" stroke-dasharray="4 3"/>' % sb)
        s.text(x + w / 2, sb[1] + sb[3] / 2 + 6 * k, "Click to add subtitle", 16 * k, 400, GREY, "middle")
        boxes.update(title=tb, body=sb)
        return boxes
    if "sub" in slide:
        s.text(x + w / 2, y + 115 * k, slide["title"], 34 * k, 400, fg, "middle")
        s.text(x + w / 2, y + 175 * k, slide["sub"], 15 * k, 400, fg, "middle")
        boxes.update(title=(x + 30 * k, y + 80 * k, w - 60 * k, 50 * k), body=(x + 70 * k, y + 155 * k, w - 140 * k, 30 * k))
    else:
        s.text(x + 34 * k, y + 52 * k, slide["title"], 26 * k, 400, fg)
        for i, pt in enumerate(slide.get("points", [])):
            s.circle(x + 42 * k, y + (96 + 30 * i) * k, 3 * k, fill=fg)
            s.text(x + 54 * k, y + (102 + 30 * i) * k, pt, 17 * k, 400, fg)
        boxes.update(title=(x + 28 * k, y + 24 * k, w - 56 * k, 40 * k), body=(x + 28 * k, y + 76 * k, w - 56 * k, 30 * len(slide.get("points", [])) * k + 12 * k))
    if sel == "body":
        s.rect(*boxes["body"], stroke="#7a7a7a", sw=1)
    return boxes


def ppt_window(s, h, tab, slides, cur=0, theme=None, notes=None, name="Presentation1 - PowerPoint", empty=False, **kw):
    frame(s, h)
    title_bar(s, name)
    tabs = ppt_tabs(s, tab)
    rb = ppt_ribbon(s, tab, theme=kw.get("theme_sel"), trans=kw.get("trans"), anim=kw.get("anim"))
    s.rect(15, 184, W - 30, h - 224, fill="#e9e9e9")
    # thumbnails
    for i, sl in enumerate(slides):
        y = 196 + i * 78
        s.text(26, y + 12, str(i + 1), 11, 400, GREY)
        if i == cur:
            s.rect(36, y - 3, 118, 72, stroke=PPT, sw=2.5, rx=3)
        ppt_slide(s, 40, y, 110, sl, theme, empty=empty and i == 0)
    nb = notes is not None
    sh = h - 224 - (54 if nb else 14)
    sw_ = min(560, (sh - 16) * 16 / 9)
    sx = 170 + (W - 30 - 170 - sw_) / 2
    boxes = ppt_slide(s, sx, 194, sw_, slides[cur] if slides else None, theme, empty=empty, sel=kw.get("sel"))
    nbox = None
    if nb:
        nbox = (170, h - 92, W - 200, 46)
        s.rect(*nbox, fill="#ffffff", stroke="#d0d0d0", sw=1)
        s.text(184, h - 64, notes or "Click to add notes", 12.5, 400, INK if notes else GREY)
    s.rect(15, h - 40, W - 30, 25, fill=TITLE_BG)
    s.rect(15, h - 25, W - 30, 10, fill=TITLE_BG, rx=9)
    s.text(30, h - 23, "Slide %d of %d" % (cur + 1, max(1, len(slides))), 11, 400, GREY)
    s.text(140, h - 23, "English (United States)", 11, 400, GREY)
    s.text(W - 200, h - 23, "Notes", 11, 400, GREY)
    return tabs, rb, boxes, nbox


def lab_ppt_open(s, top):
    open_search(s, top, "PowerPoint", PPT)


def lab_ppt_start(s, top):
    open_start(s, top, "PowerPoint", PPT, "Blank Presentation")


def lab_ppt_title(s, top):
    """The first slide: click in Click to add title, type; then the subtitle."""
    _, _, boxes, _ = ppt_window(s, 470, "Home", [None], 0, empty=True)
    mark_box(top, boxes["title"], 1, "left", 4, 2)
    mark_box(top, boxes["body"], 2, "left", 4, 2)


def lab_ppt_newslide(s, top):
    """Home › New Slide ▾ › Title and Content."""
    h = 520
    _, rb, _, _ = ppt_window(s, h, "Home", [SLIDES["title"]], 0)
    x0, y0 = 104, 168
    s.rect(x0, y0, 330, 250, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.text(x0 + 10, y0 + 20, "Office Theme", 12, 700, INK)
    lays = ("Title Slide", "Title and Content", "Section Header", "Two Content", "Comparison", "Title Only")
    for i, n in enumerate(lays):
        x = x0 + 10 + (i % 3) * 106
        y = y0 + 32 + (i // 3) * 104
        s.rect(x, y, 98, 58, fill="#ffffff", stroke=PPT if i == 1 else "#c9c9c9", sw=2 if i == 1 else 1)
        s.rect(x + 10, y + 8, 78, 10, fill="#d9d9d9")
        if i in (1, 3, 4):
            for k in range(3):
                s.rect(x + 10, y + 26 + k * 8, 34 if i != 1 else 70, 4, fill="#e6e6e6")
        s.text(x + 49, y + 74, n, 10.5, 600 if i == 1 else 400, INK, "middle")
    mark_box(top, rb["newslide"], 1, "right", 6, 1)
    mark_box(top, (x0 + 10 + 106, y0 + 32, 98, 58), 2, "right", 4, 3)


def lab_ppt_notes(s, top):
    """Slide 2: the title and three points; the notes pane under the slide."""
    h = 520
    _, _, boxes, nbox = ppt_window(s, h, "Home", [SLIDES["title"], SLIDES["when"]], 1, notes="")
    mark_box(top, boxes["title"], 1, "left", 4, 2)
    mark_box(top, boxes["body"], 2, "left", 4, 2)
    mark_box(top, nbox, 3, "left", 4, 2)


def lab_ppt_design(s, top):
    """Design › a theme (Facet here) › a variant."""
    h = 470
    tabs, rb, _, _ = ppt_window(s, h, "Design", [SLIDES["title"], SLIDES["when"]], 0, theme="Facet", theme_sel="Facet")
    mark_box(top, tabs["Design"], 1, "top", 6, 1)
    mark_box(top, rb["theme:Facet"], 2, "bottom", 4, 2)
    mark_box(top, rb["variant:1"], 3, "bottom", 4, 2)


def lab_ppt_transition(s, top):
    """Transitions › Fade › Apply To All."""
    h = 470
    tabs, rb, _, _ = ppt_window(s, h, "Transitions", [SLIDES["title"], SLIDES["when"]], 0, theme="Facet", trans="Fade")
    mark_box(top, tabs["Transitions"], 1, "top", 6, 1)
    mark_box(top, rb["t:Fade"], 2, "bottom", 4, 2)
    mark_box(top, rb["applyall"], 3, "bottom", 4, 2)


def lab_ppt_animation(s, top):
    """Slide 2: click the list; Animations › Appear."""
    h = 470
    tabs, rb, boxes, _ = ppt_window(s, h, "Animations", [SLIDES["title"], SLIDES["when"]], 1, theme="Facet", anim="Appear", sel="body")
    mark_box(top, boxes["body"], 1, "left", 4, 2)
    mark_box(top, tabs["Animations"], 2, "top", 6, 1)
    mark_box(top, rb["a:Appear"], 3, "bottom", 4, 2)


def lab_ppt_save(s, top):
    save_as(s, top, "talk-Huda", "PowerPoint Presentation (*.pptx)", PPT)


def lab_post_save(s, top):
    save_as(s, top, "post-Huda", "PowerPoint Presentation (*.pptx)", PPT)


def lab_ppt_result(s, top):
    """The talk at the end: two slides with the theme."""
    h = 470
    ppt_window(s, h, "Home", [SLIDES["title"], SLIDES["when"]], 0, theme="Facet", name="talk-Huda - PowerPoint")


def _ppt_ai_page(s, box):
    x, y, w_, hh = box
    ppt_slide(s, x + 30, y + 14, 230, SLIDES["title"], "Facet")
    ppt_slide(s, x + 280, y + 14, 230, {"title": "What you can bring", "points": ["Old books in good shape", "Your student card", "A bag for new books"]}, "Facet")
    s.rect(x + 278, y + 12, 234, 133, stroke="#f2c94c", sw=3, rx=3)


def lab_ppt_tutu_ai(s, top):
    tutu_ai(s, top, "talk-Huda", "slides", "Add a slide with 3 short points: what students can bring to the book fair.",
            "Done: slide 3, What you can bring, has three short points.", _ppt_ai_page)


def lab_ppt_tutu_dl(s, top):
    tutu_download(s, top, "talk-Huda", "slides")



# =====================================================================
# Excel for Windows (Lectures 6 and 7): the window, the formula bar, the
# grid, the Home, Insert and Data tabs.
# =====================================================================

XL = "#107c41"
XL_SOFT = "#d3e8d9"
XL_TABS = ("File", "Home", "Insert", "Page Layout", "Formulas", "Data", "Review", "View", "Help")
SHOP = [["Item", "Price", "Qty", "Total"], ["Pens", "2", "10", ""], ["Notebooks", "3", "5", ""], ["Bags", "7", "2", ""]]
SALES = [["Item", "Sales (JD)", "Type"], ["Water", "12", "Drinks"], ["Cake", "25", "Food"], ["Juice", "18", "Drinks"],
         ["Sandwich", "30", "Food"], ["Tea", "9", "Drinks"], ["Chips", "15", "Food"]]


def xl_tabs(s, active):
    s.rect(15, 49, W - 30, 30, fill=TITLE_BG)
    x, pos = 30, {}
    for tname in XL_TABS:
        w_ = width(tname, 13) + 4
        on = tname == active
        s.text(x, 69, tname, 13, 700 if on else 400, XL if on else INK)
        if on:
            s.rect(x - 2, 74, w_, 3, fill=XL, rx=1.5)
        pos[tname] = (x - 6, 52, w_ + 12, 26)
        x += w_ + 14
    return pos


def xl_ribbon(s, tab):
    ribbon_box(s)
    p = {}
    if tab == "Home":
        s.rect(34, 92, 30, 36, fill="#ffffff", stroke="#7a7a7a", sw=1.3, rx=3)
        s.text(46, 156, "Paste", 11.5, 400, INK)
        group(s, 20, 96, "Clipboard")
        dropdown(s, 104, 92, 120, "Aptos Narrow")
        dropdown(s, 228, 92, 44, "11")
        for i, c in enumerate(("B", "I", "U")):
            small_btn(s, 104 + i * 26, 124, 24, 24, c, 13, 800 if c == "B" else 400)
        group(s, 96, 282, "Font")
        for i, k in enumerate(("left", "center", "right")):
            s.rect(292 + i * 28 - 4, 124, 24, 24, fill=BTN, rx=3)
            align_icon(s, 292 + i * 28, 130, k)
        group(s, 282, 380, "Alignment")
        dropdown(s, 390, 92, 96, "General")
        s.text(392, 140, "$  %  ,", 13, 400, INK)
        group(s, 380, 496, "Number")
        p["cf"] = (504, 88, 84, 80)
        big_btn(s, 504, 84, "Conditional", lambda s_, x, y: s_.rect(x - 12, y - 12, 24, 24, fill="#ffffff", stroke=XL, sw=1.4), "Formatting ▾")
        big_btn(s, 592, 70, "Format as", lambda s_, x, y: s_.rect(x - 12, y - 12, 24, 24, fill=XL_SOFT, stroke=XL, sw=1.2), "Table ▾")
        group(s, 496, 668, "Styles")
        p["autosum"] = (680, 92, 96, 22)
        s.text(684, 108, "Σ AutoSum ▾", 12, 700, INK)
        s.text(684, 130, "Fill ▾", 11.5, 400, INK)
        s.text(684, 152, "Clear ▾", 11.5, 400, INK)
        p["sortfilter"] = (780, 92, 80, 70)
        s.text(790, 112, "Sort &", 11.5, 400, INK)
        s.text(790, 128, "Filter ▾", 11.5, 400, INK)
        group(s, 672, 870, "Editing")
    elif tab == "Data":
        big_btn(s, 24, 64, "Get", ic_page, "Data ▾")
        group(s, 20, 96, "Get & Transform Data")
        p["az"] = (106, 92, 46, 30)
        p["za"] = (106, 128, 46, 30)
        s.rect(106, 92, 46, 30, fill=BTN, rx=3)
        s.text(129, 112, "A→Z", 12, 700, INK, "middle")
        s.rect(106, 128, 46, 30, fill=BTN, rx=3)
        s.text(129, 148, "Z→A", 12, 700, INK, "middle")
        big_btn(s, 158, 54, "Sort", ic_page)
        p["filter"] = (216, 88, 58, 80)
        big_btn(s, 216, 58, "Filter", lambda s_, x, y: s_.poly([(x - 12, y - 10), (x + 12, y - 10), (x + 3, y + 2), (x + 3, y + 12), (x - 3, y + 12), (x - 3, y + 2)], fill="#ffffff", stroke=XL, sw=1.4))
        p["clear"] = (280, 92, 70, 22)
        s.text(284, 108, "Clear", 11.5, 400, INK)
        s.text(284, 130, "Reapply", 11.5, 400, LIGHT)
        s.text(284, 152, "Advanced", 11.5, 400, INK)
        group(s, 100, 360, "Sort & Filter")
        for i, n in enumerate(("Text to Columns", "Flash Fill", "Remove Duplicates")):
            s.text(372, 108 + i * 22, n, 11.5, 400, INK)
        group(s, 360, 520, "Data Tools")
    elif tab == "Insert":
        big_btn(s, 24, 64, "PivotTable", ic_table)
        big_btn(s, 92, 52, "Table", ic_table)
        group(s, 20, 150, "Tables")
        big_btn(s, 160, 64, "Pictures", ic_picture)
        group(s, 156, 232, "Illustrations")
        big_btn(s, 242, 80, "Recommended", lambda s_, x, y: [s_.rect(x - 14 + i * 10, y + 8 - (6, 14, 10)[i], 7, (6, 14, 10)[i], fill=XL) for i in range(3)], "Charts")
        p["column"] = (330, 92, 40, 30)
        s.rect(330, 92, 40, 30, fill=BTN, rx=3)
        for i, hh in enumerate((8, 16, 12)):
            s.rect(337 + i * 9, 116 - hh, 6, hh, fill="#4472c4")
        s.text(356, 140, "▾", 10, 400, INK, "middle")
        s.text(380, 112, "Line ▾", 11.5, 400, INK)
        s.text(380, 136, "Pie ▾", 11.5, 400, INK)
        s.text(440, 112, "Bar ▾", 11.5, 400, INK)
        group(s, 236, 500, "Charts")
    return p


def xl_grid(s, x0, y0, data, widths=(110, 90, 90, 90, 80), rows=8, sel=None, rng=None, red=(), arrows=False, vals=None):
    """The grid; data[r][c] text; sel = (r, c) the active cell; rng = (r1, c1, r2, c2); returns the box of each cell."""
    boxes = {}
    xs = [x0 + 34]
    for wd in widths:
        xs.append(xs[-1] + wd)
    s.rect(x0, y0, 34, 22, fill="#f3f3f3", stroke="#dadada", sw=1)
    for c, wd in enumerate(widths):
        on = sel is not None and sel[1] == c
        s.rect(xs[c], y0, wd, 22, fill=XL_SOFT if on else "#f3f3f3", stroke="#dadada", sw=1)
        s.text(xs[c] + wd / 2, y0 + 16, "ABCDEFG"[c], 12, 700 if on else 400, XL if on else GREY, "middle")
    for r in range(rows):
        y = y0 + 22 + r * 24
        on = sel is not None and sel[0] == r
        s.rect(x0, y, 34, 24, fill=XL_SOFT if on else "#f3f3f3", stroke="#dadada", sw=1)
        s.text(x0 + 17, y + 17, str(r + 1), 12, 700 if on else 400, XL if on else GREY, "middle")
        for c, wd in enumerate(widths):
            inr = rng and rng[0] <= r <= rng[2] and rng[1] <= c <= rng[3]
            fill = "#ffc7ce" if (r, c) in red else ("#e8f3ec" if inr else "#ffffff")
            s.rect(xs[c], y, wd, 24, fill=fill, stroke="#e3e3e3", sw=1)
            txt = data[r][c] if r < len(data) and c < len(data[r]) else ""
            if txt:
                num = txt.replace(".", "").isdigit()
                col = "#9c0006" if (r, c) in red else INK
                s.text(xs[c] + wd - 6 if num else xs[c] + 6, y + 17, txt, 12.5, 400, col, "end" if num else "start")
            if arrows and r == 0 and txt:
                s.rect(xs[c] + wd - 18, y + 4, 15, 15, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=2)
                s.poly([(xs[c] + wd - 14, y + 10), (xs[c] + wd - 7, y + 10), (xs[c] + wd - 10.5, y + 14)], fill=INK)
            boxes[(r, c)] = (xs[c], y, wd, 24)
    if rng:
        bx = boxes[(rng[0], rng[1])]
        ex = boxes[(rng[2], rng[3])]
        s.rect(bx[0], bx[1], ex[0] + ex[2] - bx[0], ex[1] + ex[3] - bx[1], stroke=XL, sw=2)
    if sel is not None:
        b = boxes[sel]
        s.rect(b[0], b[1], b[2], b[3], stroke=XL, sw=2.5)
        s.rect(b[0] + b[2] - 4, b[1] + b[3] - 4, 8, 8, fill=XL, stroke="#ffffff", sw=1)
    return boxes


def xl_window(s, h, tab, data, name="Book1 - Excel", sel=None, formula="", ref_name="A1", **kw):
    frame(s, h)
    title_bar(s, name)
    tabs = xl_tabs(s, tab)
    rb = xl_ribbon(s, tab)
    s.rect(15, 184, W - 30, 28, fill="#ffffff")
    s.rect(24, 189, 70, 20, fill="#ffffff", stroke="#c9c9c9", sw=1)
    s.text(30, 203.5, ref_name, 12, 400, INK)
    s.text(106, 204, "fx", 12, 400, GREY)
    s.line(124, 188, 124, 210, "#d6d6d6", 1)
    s.text(132, 204, formula, 12.5, 400, INK)
    fb = (128, 188, 300, 22)
    s.line(15, 212, W - 15, 212, "#d6d6d6", 1)
    s.rect(15, 213, W - 30, h - 253, fill="#ffffff")
    boxes = xl_grid(s, 15, 213, data, kw.get("widths", (110, 90, 90, 90, 80)), kw.get("rows", min(10, int((h - 253 - 22) / 24))),
                    sel=sel, rng=kw.get("rng"), red=kw.get("red", ()), arrows=kw.get("arrows", False))
    s.rect(15, h - 40, W - 30, 25, fill=TITLE_BG)
    s.rect(15, h - 25, W - 30, 10, fill=TITLE_BG, rx=9)
    s.text(30, h - 23, "Ready", 11, 400, GREY)
    s.rect(30, h - 62, 64, 20, fill="#ffffff", stroke="#c9c9c9", sw=1)
    s.text(62, h - 47, "Sheet1", 11.5, 700, XL, "middle")
    return tabs, rb, boxes, fb


def filled(data, col, vals):
    out = [list(r) + [""] * (5 - len(r)) for r in data]
    for i, v in enumerate(vals):
        out[i + 1][col] = v
    return out


def lab_xl_open(s, top):
    open_search(s, top, "Excel", XL)


def lab_xl_start(s, top):
    open_start(s, top, "Excel", XL, "Blank workbook")


def lab_xl_type(s, top):
    """The shop list typed: Tab goes to the next cell, Enter to the next row."""
    _, _, boxes, _ = xl_window(s, 470, "Home", SHOP, sel=(3, 2), formula="2", ref_name="C4")
    top.label(560, 290, 230, "Tab: the next cell", arrow_to=(470, 300))
    top.label(560, 330, 230, "Enter: the next row", arrow_to=(470, 330))


def lab_xl_formula(s, top):
    """D2: =B2*C2, in the cell and the formula bar."""
    data = filled(SHOP, 3, ["20"])
    _, _, boxes, fb = xl_window(s, 430, "Home", data, sel=(1, 3), formula="=B2*C2", ref_name="D2")
    mark_box(top, boxes[(1, 3)], 1, "right", 2, 2)
    mark_box(top, (fb[0], fb[1], 90, fb[3]), 2, "bottom", 4, 1)


def lab_xl_fill(s, top):
    """D2 selected: double-click its fill handle; D3 and D4 get their totals."""
    data = filled(SHOP, 3, ["20", "15", "14"])
    _, _, boxes, _ = xl_window(s, 430, "Home", data, sel=(1, 3), formula="=B2*C2", ref_name="D2", rng=(1, 3, 3, 3))
    b = boxes[(1, 3)]
    top.ring_circle(b[0] + b[2], b[1] + b[3], 9)
    top.mark(1, b[0] + b[2] + 22, b[1] + b[3])
    top.label(b[0] + b[2] + 40, b[1] + b[3] + 12, 210, "double-click the small square")
    mark_box(top, (b[0], boxes[(2, 3)][1], b[2], 48), 2, "left", 2, 2)


def lab_xl_sum(s, top):
    """D5: Home › AutoSum, then Enter; D6: =MAX(D2:D4)."""
    data = filled(SHOP, 3, ["20", "15", "14"]) + [["Total", "", "", "49", ""], ["Biggest", "", "", "", ""]]
    _, rb, boxes, _ = xl_window(s, 470, "Home", data, sel=(4, 3), formula="=SUM(D2:D4)", ref_name="D5")
    mark_box(top, boxes[(4, 3)], 1, "right", 2, 2)
    mark_box(top, rb["autosum"], 2, "bottom", 4, 2)


def lab_xl_save(s, top):
    save_as(s, top, "shop-Huda", "Excel Workbook (*.xlsx)", XL)


def lab_xl_result(s, top):
    data = filled(SHOP, 3, ["20", "15", "14"]) + [["Total", "", "", "49", ""], ["Biggest", "", "", "20", ""]]
    xl_window(s, 430, "Home", data, name="shop-Huda - Excel", sel=(5, 3), formula="=MAX(D2:D4)", ref_name="D6")


def _xl_ai_page(s, box, data, fresh=(), head_fill=None):
    x, y, w_, hh = box
    s.rect(x + 20, y + 12, w_ - 40, hh - 24, fill="#ffffff", stroke="#e0e0e0", sw=1)
    cw = (w_ - 80) / max(len(r) for r in data)
    for r, row in enumerate(data):
        for c, v in enumerate(row):
            cx, cy = x + 40 + c * cw, y + 30 + r * 26
            fill = "#fff3bf" if (r, c) in fresh else (head_fill if (r == 0 and head_fill) else "#ffffff")
            s.rect(cx, cy, cw, 26, fill=fill, stroke="#e3e3e3", sw=1)
            s.text(cx + 6, cy + 18, v, 12, 700 if r == 0 else 400, INK)


def lab_xl_tutu_ai(s, top):
    data = [r[:] for r in filled(SHOP, 3, ["20", "15", "14"])] + [["Rulers", "1", "6", "6", ""]]
    tutu_ai(s, top, "shop-Huda", "sheet", "Add a row: Rulers, price 1, quantity 6, and its total.",
            "Done: row 5 is Rulers, 1, 6, and the total 6.", lambda s_, b: _xl_ai_page(s_, b, [r[:4] for r in data], {(4, 0), (4, 1), (4, 2), (4, 3)}))


def lab_xl_tutu_dl(s, top):
    tutu_download(s, top, "shop-Huda", "sheet")


# Lecture 7: sort, filter, a colour rule and a chart (the sales of a week).

def lab_xl7_type(s, top):
    _, _, boxes, _ = xl_window(s, 470, "Home", SALES, sel=(6, 2), formula="Food", ref_name="C7", widths=(110, 100, 90, 90, 80))
    top.label(560, 300, 230, "Tab: the next cell", arrow_to=(420, 300))
    top.label(560, 340, 230, "Enter: the next row", arrow_to=(420, 340))


def lab_xl7_sort(s, top):
    """Click a cell of Sales; Data › Z→A (Sort Largest to Smallest)."""
    data = [SALES[0]] + sorted(SALES[1:], key=lambda r: -int(r[1]))
    tabs, rb, boxes, _ = xl_window(s, 470, "Data", data, sel=(1, 1), formula="30", ref_name="B2", widths=(110, 100, 90, 90, 80))
    mark_box(top, boxes[(1, 1)], 1, "right", 2, 2)
    mark_box(top, tabs["Data"], 2, "top", 6, 1)
    mark_box(top, rb["za"], 3, "right", 4, 2)


def lab_xl7_filter(s, top):
    """Data › Filter; the arrow of Type; only Drinks; OK."""
    tabs, rb, boxes, _ = xl_window(s, 500, "Data", SALES, sel=(0, 2), formula="Type", ref_name="C1", widths=(110, 100, 90, 90, 80), arrows=True)
    b = boxes[(0, 2)]
    mx, my = b[0] - 40, b[1] + 26
    s.rect(mx, my, 190, 170, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.text(mx + 12, my + 22, "Sort A to Z", 11.5, 400, INK)
    s.line(mx, my + 32, mx + 190, my + 32, LINE, 1)
    for i, (v, on) in enumerate((("(Select All)", False), ("Drinks", True), ("Food", False))):
        yy = my + 48 + i * 24
        checkbox(s, mx + 12, yy - 10, on, v)
    s.rect(mx + 100, my + 132, 74, 26, fill=XL, rx=3)
    s.text(mx + 137, my + 150, "OK", 12, 700, "#ffffff", "middle")
    mark_box(top, rb["filter"], 1, "right", 4, 1)
    mark_box(top, (b[0] + b[2] - 18, b[1] + 4, 15, 15), 2, "top", 3, 2)
    mark_box(top, (mx + 8, my + 60, 120, 22), 3, "left", 4, 1)
    mark_box(top, (mx + 100, my + 132, 74, 26), 4, "right", 4, 2)


def lab_xl7_cf(s, top):
    """Select B2:B7; Home › Conditional Formatting › Highlight Cells Rules › Greater Than › 20 › OK."""
    tabs, rb, boxes, _ = xl_window(s, 500, "Home", SALES, sel=None, formula="12", ref_name="B2", widths=(110, 100, 90, 90, 80), rng=(1, 1, 6, 1),
                                   red={(2, 1), (4, 1)})
    x0, y0 = 504, 168
    s.rect(x0, y0, 220, 58, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.rect(x0 + 2, y0 + 4, 216, 24, fill=XL_SOFT)
    s.text(x0 + 12, y0 + 21, "Highlight Cells Rules ›", 12, 700, INK)
    s.text(x0 + 12, y0 + 47, "Top/Bottom Rules ›", 12, 400, INK)
    s.rect(x0 + 222, y0 + 4, 150, 50, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.rect(x0 + 224, y0 + 6, 146, 22, fill=XL_SOFT)
    s.text(x0 + 234, y0 + 22, "Greater Than...", 12, 700, INK)
    s.text(x0 + 234, y0 + 46, "Less Than...", 12, 400, INK)
    dx, dy = 470, 300
    s.rect(dx, dy, 300, 120, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=4)
    s.text(dx + 12, dy + 22, "Greater Than", 13, 700, INK)
    s.text(dx + 12, dy + 46, "Format cells that are GREATER THAN:", 11.5, 400, INK)
    s.rect(dx + 12, dy + 56, 80, 24, fill="#ffffff", stroke=XL, sw=1.6)
    s.text(dx + 20, dy + 73, "20", 12.5, 400, INK)
    s.text(dx + 104, dy + 73, "Light Red Fill with Dark Red Text", 10.5, 400, GREY)
    s.rect(dx + 206, dy + 88, 80, 24, fill=XL, rx=3)
    s.text(dx + 246, dy + 105, "OK", 12, 700, "#ffffff", "middle")
    mark_box(top, (boxes[(1, 1)][0], boxes[(1, 1)][1], 100, 144), 1, "left", 2, 2)
    mark_box(top, rb["cf"], 2, "top", 4, 1)
    mark_box(top, (x0 + 224, y0 + 6, 146, 22), 3, "bottom", 4, 1)
    mark_box(top, (dx + 12, dy + 56, 80, 24), 4, "left", 3, 2)
    mark_box(top, (dx + 206, dy + 88, 80, 24), 5, "right", 3, 2)


def lab_xl7_chart(s, top):
    """Select A1:B7; Insert › Column › Clustered Column; click Chart Title and type."""
    tabs, rb, boxes, _ = xl_window(s, 500, "Insert", SALES, ref_name="A1", formula="Item", widths=(110, 100, 90, 90, 80), rng=(0, 0, 6, 1))
    cx, cy = 470, 220
    s.rect(cx, cy, 380, 230, fill="#ffffff", stroke="#a6a6a6", sw=1)
    s.text(cx + 190, cy + 26, "Sales of the week", 15, 400, INK, "middle")
    vals = [int(r[1]) for r in SALES[1:]]
    for i, v in enumerate(vals):
        bh = v / 30 * 140
        s.rect(cx + 40 + i * 54, cy + 190 - bh, 30, bh, fill="#4472c4")
        s.text(cx + 55 + i * 54, cy + 208, SALES[i + 1][0], 10, 400, GREY, "middle")
    s.line(cx + 30, cy + 190, cx + 360, cy + 190, "#9a9a9a", 1)
    mark_box(top, (boxes[(0, 0)][0], boxes[(0, 0)][1], 210, 168), 1, "left", 2, 2)
    mark_box(top, tabs["Insert"], 2, "top", 6, 1)
    mark_box(top, rb["column"], 3, "bottom", 4, 2)
    mark_box(top, (cx + 110, cy + 8, 160, 26), 4, "right", 4, 2)


def lab_xl7_save(s, top):
    save_as(s, top, "sales-Huda", "Excel Workbook (*.xlsx)", XL)


def lab_xl7_result(s, top):
    data = [SALES[0]] + sorted(SALES[1:], key=lambda r: -int(r[1]))
    xl_window(s, 430, "Home", data, name="sales-Huda - Excel", ref_name="A1", formula="Item", widths=(110, 100, 90, 90, 80),
              red={(1, 1), (2, 1)}, arrows=True)


def lab_xl7_tutu_ai(s, top):
    data = [r[:] for r in SALES] + [["Total", "109", ""]]
    tutu_ai(s, top, "sales-Huda", "sheet", "Add a row at the end: Total, with the sum of the sales.",
            "Done: row 8 is Total, 109 (the sum of the sales).", lambda s_, b: _xl_ai_page(s_, b, data, {(7, 0), (7, 1)}))


def lab_xl7_tutu_dl(s, top):
    tutu_download(s, top, "sales-Huda", "sheet")



# =====================================================================
# Access for Windows (Lecture 8): a blank database, Design View, the
# datasheet, Query Design, and Export to Excel.
# =====================================================================

AC = "#a4373a"
AC_SOFT = "#f3dcdc"
AC_TABS = ("File", "Home", "Create", "External Data", "Database Tools", "Help")
CUSTOMERS = [("1", "Huda", "Amman"), ("2", "Omar", "Irbid"), ("3", "Rana", "Amman")]


def ac_tabs(s, active, extra=None):
    s.rect(15, 49, W - 30, 30, fill=TITLE_BG)
    x, pos = 30, {}
    for tname in AC_TABS + ((extra,) if extra else ()):
        w_ = width(tname, 13) + 4
        on = tname == active
        s.text(x, 69, tname, 13, 700 if on else 400, AC if on else INK)
        if on:
            s.rect(x - 2, 74, w_, 3, fill=AC, rx=1.5)
        pos[tname] = (x - 6, 52, w_ + 12, 26)
        x += w_ + 14
    return pos


def ac_ribbon(s, tab):
    ribbon_box(s)
    p = {}
    if tab == "Home":
        p["view"] = (24, 88, 60, 80)
        big_btn(s, 24, 60, "View", ic_table)
        s.text(54, 163, "▾", 11, 400, INK, "middle")
        group(s, 20, 92, "Views")
        s.rect(104, 92, 30, 36, fill="#ffffff", stroke="#7a7a7a", sw=1.3, rx=3)
        s.text(118, 156, "Paste", 11.5, 400, INK, "middle")
        group(s, 92, 150, "Clipboard")
        for i, n in enumerate(("Ascending", "Descending", "Filter")):
            s.text(160, 108 + i * 22, n, 11.5, 400, INK)
        group(s, 150, 260, "Sort & Filter")
        for i, n in enumerate(("New", "Save", "Delete ▾")):
            s.text(270, 108 + i * 22, n, 11.5, 400, INK)
        group(s, 260, 340, "Records")
    elif tab == "Create":
        for i, n in enumerate(("Table", "Table Design")):
            big_btn(s, 24 + i * 70, 64, n.split()[0], ic_table, n.split()[1] if " " in n else None)
        group(s, 20, 160, "Tables")
        big_btn(s, 170, 70, "Query", ic_page, "Wizard")
        p["qdesign"] = (244, 88, 70, 80)
        big_btn(s, 244, 70, "Query", lambda s_, x, y: [s_.rect(x - 14, y - 12, 12, 16, fill="#ffffff", stroke=AC, sw=1.3), s_.rect(x + 2, y - 4, 12, 16, fill="#ffffff", stroke=AC, sw=1.3)], "Design")
        group(s, 166, 320, "Queries")
        big_btn(s, 330, 56, "Form", ic_page)
        group(s, 326, 450, "Forms")
        big_btn(s, 460, 60, "Report", ic_page)
        group(s, 456, 580, "Reports")
    elif tab == "Table Design":
        p["key"] = (24, 88, 60, 80)
        big_btn(s, 24, 60, "Primary", lambda s_, x, y: s_.circle(x - 4, y, 6, stroke="#d29b00", sw=2.5), "Key")
        big_btn(s, 88, 60, "Builder", ic_page)
        group(s, 20, 220, "Tools")
    elif tab == "Query Design":
        p["run"] = (24, 88, 50, 80)
        s.rect(24, 88, 50, 80, fill=BTN, rx=4)
        s.text(49, 128, "!", 34, 800, AC, "middle")
        s.text(49, 156, "Run", 11.5, 400, INK, "middle")
        big_btn(s, 78, 50, "View", ic_table)
        group(s, 20, 134, "Results")
        for i, n in enumerate(("Select", "Make Table", "Append")):
            s.text(146, 108 + i * 22, n, 11.5, 400, INK)
        group(s, 134, 260, "Query Type")
    return p


def ac_window(s, h, tab, extra_tab=None, objs=("Customers",), queries=()):
    frame(s, h)
    title_bar(s, "shop-Huda : Database - Access")
    tabs = ac_tabs(s, tab, extra_tab)
    rb = ac_ribbon(s, tab)
    s.rect(15, 184, 170, h - 224, fill="#ffffff")
    s.line(185, 184, 185, h - 40, "#d6d6d6", 1)
    s.text(26, 204, "All Access Objects", 11.5, 700, INK)
    s.text(26, 228, "Tables", 11, 400, GREY)
    nav = {}
    for i, o in enumerate(objs):
        y = 236 + i * 24
        s.rect(22, y, 156, 22, fill=AC_SOFT if i == 0 else "#ffffff", rx=3)
        s.rect(30, y + 6, 12, 10, stroke=AC, sw=1.2)
        s.text(50, y + 16, o, 12, 400, INK)
        nav[o] = (22, y, 156, 22)
    if queries:
        y = 236 + len(objs) * 24 + 10
        s.text(26, y + 8, "Queries", 11, 400, GREY)
        for i, q in enumerate(queries):
            s.text(50, y + 30 + i * 22, q, 12, 400, INK)
    s.rect(186, 184, W - 201, h - 224, fill="#ffffff")
    s.rect(15, h - 40, W - 30, 25, fill=TITLE_BG)
    s.rect(15, h - 25, W - 30, 10, fill=TITLE_BG, rx=9)
    return tabs, rb, nav


def ac_table(s, x, y, head, rows, widths, new=False):
    boxes = {}
    xx = x
    for c, (hd, wd) in enumerate(zip(head, widths)):
        s.rect(xx, y, wd, 24, fill="#f3f3f3", stroke="#d6d6d6", sw=1)
        s.text(xx + 6, y + 16, hd, 12, 700, INK)
        xx += wd
    for r, row in enumerate(list(rows) + ([("(New)",) + ("",) * (len(head) - 1)] if new else [])):
        xx = x
        for c, (v, wd) in enumerate(zip(row, widths)):
            s.rect(xx, y + 24 + r * 22, wd, 22, fill="#ffffff", stroke="#e0e0e0", sw=1)
            s.text(xx + 6, y + 40 + r * 22, v, 12, 400, INK)
            boxes[(r, c)] = (xx, y + 24 + r * 22, wd, 22)
            xx += wd
    return boxes


def lab_ac_open(s, top):
    open_search(s, top, "Access", AC)


def lab_ac_new(s, top):
    """Access starts: Blank database, the file name, Create."""
    open_start(s, top, "Access", AC, "Blank database")
    s.rect(380, 100, 300, 170, fill="#ffffff", stroke="#a6a6a6", sw=1.2, rx=6)
    s.text(396, 128, "Blank database", 16, 400, INK)
    s.text(396, 160, "File Name", 11.5, 400, GREY)
    s.rect(396, 168, 240, 26, fill="#ffffff", stroke=AC, sw=1.6, rx=2)
    s.text(404, 186, "shop-Huda", 13, 400, INK)
    s.rect(396, 222, 80, 30, fill=AC, rx=4)
    s.text(436, 242, "Create", 13, 700, "#ffffff", "middle")
    mark_box(top, (196, 92, 140, 180), 1, "top")
    mark_box(top, (396, 168, 240, 26), 2, "right", 3, 2)
    mark_box(top, (396, 222, 80, 30), 3, "right", 4, 2)


def lab_ac_design(s, top):
    """Home › View ▾ › Design View; Save As: Customers, OK."""
    h = 430
    tabs, rb, nav = ac_window(s, h, "Home", objs=("Table1",))
    vx, vy = 24, 168
    s.rect(vx, vy, 170, 60, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.text(vx + 14, vy + 22, "Datasheet View", 12, 400, INK)
    s.rect(vx + 2, vy + 32, 166, 24, fill=AC_SOFT)
    s.text(vx + 14, vy + 49, "Design View", 12, 700, INK)
    dx, dy = 360, 240
    s.rect(dx, dy, 300, 130, fill="#ffffff", stroke="#a6a6a6", sw=1.2, rx=4)
    s.text(dx + 14, dy + 24, "Save As", 13, 700, INK)
    s.text(dx + 14, dy + 50, "Table Name:", 11.5, 400, INK)
    s.rect(dx + 14, dy + 58, 270, 24, fill="#ffffff", stroke=AC, sw=1.6, rx=2)
    s.text(dx + 22, dy + 75, "Customers", 12.5, 400, INK)
    s.rect(dx + 200, dy + 92, 84, 26, fill=AC, rx=3)
    s.text(dx + 242, dy + 110, "OK", 12.5, 700, "#ffffff", "middle")
    mark_box(top, rb["view"], 1, "right", 4, 1)
    mark_box(top, (vx + 2, vy + 32, 166, 24), 2, "right", 3, 1)
    mark_box(top, (dx + 14, dy + 58, 270, 24), 3, "left", 3, 2)
    mark_box(top, (dx + 200, dy + 92, 84, 26), 4, "right", 3, 2)


def lab_ac_fields(s, top):
    """Design View: ID (AutoNumber, the key), Name and City (Short Text)."""
    h = 400
    tabs, rb, nav = ac_window(s, h, "Table Design", extra_tab="Table Design")
    x, y = 210, 200
    rows = [("ID", "AutoNumber"), ("Name", "Short Text"), ("City", "Short Text")]
    s.rect(x, y, 26, 24, fill="#f3f3f3", stroke="#d6d6d6", sw=1)
    s.rect(x + 26, y, 220, 24, fill="#f3f3f3", stroke="#d6d6d6", sw=1)
    s.text(x + 34, y + 16, "Field Name", 12, 700, INK)
    s.rect(x + 246, y, 200, 24, fill="#f3f3f3", stroke="#d6d6d6", sw=1)
    s.text(x + 254, y + 16, "Data Type", 12, 700, INK)
    for i, (n, ty) in enumerate(rows):
        yy = y + 24 + i * 24
        s.rect(x, yy, 26, 24, fill="#ffffff", stroke="#e0e0e0", sw=1)
        if i == 0:
            s.circle(x + 10, yy + 12, 4, stroke="#d29b00", sw=2)
            s.line(x + 14, yy + 12, x + 22, yy + 12, "#d29b00", 2)
        s.rect(x + 26, yy, 220, 24, fill="#ffffff", stroke="#e0e0e0", sw=1)
        s.text(x + 34, yy + 16, n, 12.5, 400, INK)
        s.rect(x + 246, yy, 200, 24, fill="#ffffff", stroke="#e0e0e0", sw=1)
        s.text(x + 254, yy + 16, ty, 12.5, 400, INK)
        s.poly([(x + 430, yy + 10), (x + 438, yy + 10), (x + 434, yy + 15)], fill=INK)
    mark_box(top, (x + 26, y + 48, 220, 48), 1, "left", 2, 2)
    mark_box(top, (x + 246, y + 48, 200, 48), 2, "right", 2, 2)
    mark_box(top, (x, y + 24, 26, 24), 3, "left", 2, 2)


def lab_ac_records(s, top):
    """Home › View › Datasheet View; three customers typed (ID counts by itself)."""
    h = 400
    tabs, rb, nav = ac_window(s, h, "Home")
    boxes = ac_table(s, 210, 200, ("ID", "Name", "City"), CUSTOMERS, (70, 160, 160), new=True)
    mark_box(top, rb["view"], 1, "right", 4, 1)
    mark_box(top, (boxes[(0, 1)][0], boxes[(0, 1)][1], 320, 66), 2, "right", 3, 2)


def lab_ac_query1(s, top):
    """Create › Query Design; the table Customers: double-click Name and City."""
    h = 430
    tabs, rb, nav = ac_window(s, h, "Create")
    x, y = 260, 200
    s.rect(x, y, 150, 120, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.rect(x, y, 150, 22, fill=AC_SOFT)
    s.text(x + 8, y + 16, "Customers", 12, 700, INK)
    for i, f in enumerate(("*", "ID", "Name", "City")):
        s.text(x + 12, y + 40 + i * 20, f, 12, 400, INK)
    s.rect(x + 4, y + 66, 142, 40, fill="#ffe8a3")
    s.text(x + 12, y + 80, "Name", 12, 400, INK)
    s.text(x + 12, y + 100, "City", 12, 400, INK)
    mark_box(top, tabs["Create"], 1, "top", 6, 1)
    mark_box(top, rb["qdesign"], 2, "right", 4, 1)
    mark_box(top, (x + 4, y + 66, 142, 40), 3, "right", 3, 2)
    top.label(x + 190, y + 76, 170, "double-click each one")


def lab_ac_query2(s, top):
    """The grid: Sort under Name: Ascending; Criteria under City: Amman; Run."""
    h = 430
    tabs, rb, nav = ac_window(s, h, "Query Design", extra_tab="Query Design")
    x, y = 210, 214
    labels = ("Field:", "Table:", "Sort:", "Show:", "Criteria:")
    cols = (("Name", "Customers", "Ascending", "✓", ""), ("City", "Customers", "", "✓", "\"Amman\""))
    for i, lab in enumerate(labels):
        yy = y + i * 26
        s.rect(x, yy, 80, 26, fill="#f3f3f3", stroke="#d6d6d6", sw=1)
        s.text(x + 8, yy + 17, lab, 12, 700, INK)
        for c, col in enumerate(cols):
            s.rect(x + 80 + c * 170, yy, 170, 26, fill="#ffffff", stroke="#e0e0e0", sw=1)
            s.text(x + 88 + c * 170, yy + 17, col[i], 12.5, 400, INK)
    mark_box(top, (x + 80, y + 52, 170, 26), 1, "bottom", 2, 2)
    mark_box(top, (x + 250, y + 104, 170, 26), 2, "right", 2, 2)
    mark_box(top, rb["run"], 3, "right", 4, 1)


def lab_ac_export(s, top):
    """Right-click Customers › Export › Excel; then OK."""
    h = 430
    tabs, rb, nav = ac_window(s, h, "Home", queries=("Amman customers",))
    nx, ny, nw, nh = nav["Customers"]
    mx, my = nx + 60, ny + 20
    s.rect(mx, my, 150, 130, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    for i, it in enumerate(("Open", "Design View", "Export", "Rename", "Delete")):
        if it == "Export":
            s.rect(mx + 2, my + 6 + i * 24, 146, 22, fill=AC_SOFT)
        s.text(mx + 12, my + 22 + i * 24, it + (" ›" if it == "Export" else ""), 12, 700 if it == "Export" else 400, INK)
    sx = mx + 150
    s.rect(sx, my + 50, 150, 60, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=3)
    s.rect(sx + 2, my + 54, 146, 22, fill=AC_SOFT)
    s.text(sx + 12, my + 70, "Excel", 12, 700, INK)
    s.text(sx + 12, my + 96, "Text File", 12, 400, INK)
    mark_box(top, (nx, ny, nw, nh), 1, "top", 3, 1)
    mark_box(top, (mx + 2, my + 54, 146, 22), 2, "left", 3, 1)
    mark_box(top, (sx + 2, my + 54, 146, 22), 3, "right", 3, 1)
    top.label(560, 330, 270, "then: OK, and Close")


def lab_ac_result(s, top):
    """The query Amman customers: Huda and Rana."""
    h = 340
    ac_window(s, h, "Home", queries=("Amman customers",))
    ac_table(s, 210, 200, ("Name", "City"), [("Huda", "Amman"), ("Rana", "Amman")], (160, 160))


def lab_ac_tutu_ai(s, top):
    data = [["ID", "Name", "City"]] + [list(r) for r in CUSTOMERS] + [["4", "Sami", "Zarqa"], ["5", "Lina", "Aqaba"], ["6", "Yousef", "Amman"]]
    tutu_ai(s, top, "Customers", "sheet", "Add 3 customers with a name and a city in Jordan.",
            "Done: rows 5 to 7 are three new customers.", lambda s_, b: _xl_ai_page(s_, b, data, {(r, c) for r in (4, 5, 6) for c in range(3)}))


def lab_ac_tutu_dl(s, top):
    tutu_download(s, top, "Customers", "sheet")



# =====================================================================
# Lecture 9: the plan of the service in Word, and an order form in
# Microsoft Forms (forms.office.com, signed in with the university account).
# =====================================================================

FO = "#036c70"
FO_SOFT = "#e3f2f1"
PLAN = [("Title", "Mona's Cakes: the plan"), ("Normal", "The customer: students and families in Amman."),
        ("Normal", "The need: a fresh cake on the right day."), ("Normal", "The steps: see the cakes, choose, order, collect.")]


def lab_w9_plan(s, top):
    """Word: the plan typed; the first line with the style Title."""
    h = 470
    _, rb = word_window(s, h, "Home", style="Title")
    boxes, _ = page(s, 330, 196, 520, h - 250, PLAN, caret=0)
    mark_box(top, boxes[0], 1, "left")
    mark_box(top, rb["Title"], 2, "bottom")


def lab_w9_save(s, top):
    save_as(s, top, "plan-Huda", "Word Document (*.docx)", WORD)


def forms_shell(s, h, tab="Questions", preview=False):
    browser(s, h, "forms.office.com", "Microsoft Forms")
    s.rect(15, 85, W - 30, h - 100, fill="#f1f8f6")
    s.rect(15, 85, W - 30, 44, fill="#ffffff")
    s.text(32, 113, "Forms", 15, 700, FO)
    p = {}
    for i, n in enumerate(("Questions", "Responses")):
        x = 360 + i * 110
        s.text(x, 113, n, 13, 700 if n == tab else 400, FO if n == tab else INK)
        if n == tab and not preview:
            s.rect(x - 4, 124, width(n, 13) + 8, 3, fill=FO)
        p[n] = (x - 8, 96, width(n, 13) + 16, 30)
    p["preview"] = (640, 98, 80, 26)
    s.rect(*p["preview"], fill="#ffffff", stroke="#c9d6d4", sw=1, rx=4)
    s.text(680, 116, "Preview", 12, 600, INK, "middle")
    s.rect(730, 98, 140, 26, fill=FO, rx=4)
    s.text(800, 116, "Collect responses", 12, 600, "#ffffff", "middle")
    return p


def fcard(s, x, y, w_, hh, head=False):
    s.rect(x, y, w_, hh, fill="#ffffff", stroke="#dfe7e5", sw=1, rx=8)
    if head:
        s.rect(x, y, w_, 6, fill=FO, rx=3)


def lab_fo_new(s, top):
    """forms.office.com, signed in: New Form."""
    h = 380
    browser(s, h, "forms.office.com", "Microsoft Forms")
    s.rect(15, 85, W - 30, h - 100, fill="#f1f8f6")
    s.text(40, 120, "Forms", 18, 700, FO)
    s.rect(780, 102, 70, 26, fill="#ffffff", stroke="#c9d6d4", sw=1, rx=13)
    s.text(815, 119, "HU", 12, 700, INK, "middle")
    s.text(40, 166, "Start a new form", 13, 600, INK)
    s.rect(40, 180, 150, 120, fill="#ffffff", stroke=FO, sw=2, rx=8)
    s.text(115, 236, "New Form", 14, 700, FO, "middle")
    s.rect(206, 180, 150, 120, fill="#ffffff", stroke="#dfe7e5", sw=1, rx=8)
    s.text(281, 236, "New Quiz", 14, 400, INK, "middle")
    for i, n in enumerate(("Event registration", "Customer feedback")):
        s.rect(372 + i * 166, 180, 150, 120, fill="#ffffff", stroke="#dfe7e5", sw=1, rx=8)
        s.text(447 + i * 166, 236, n, 12, 400, GREY, "middle")
    mark_box(top, (40, 180, 150, 120), 1, "bottom", 8, 3)
    top.label(400, 320, 330, "first: Sign in with the university account")


def lab_fo_title(s, top):
    """The title, then + Add new and the kinds of questions."""
    h = 430
    forms_shell(s, h)
    fcard(s, 200, 146, 500, 80, True)
    s.text(220, 186, "Mona's Cakes: order", 20, 400, INK)
    s.line(220, 196, 680, 196, "#c9d6d4", 1)
    s.text(220, 214, "Description", 11.5, 400, LIGHT)
    s.rect(200, 246, 100, 30, fill=FO, rx=4)
    s.text(250, 266, "+ Add new", 12.5, 700, "#ffffff", "middle")
    kinds = ("Choice", "Text", "Rating", "Date")
    for i, k in enumerate(kinds):
        x = 200 + i * 96
        s.rect(x, 292, 88, 30, fill="#ffffff", stroke="#c9d6d4", sw=1, rx=15)
        s.text(x + 44, 312, k, 12.5, 600, INK, "middle")
    mark_box(top, (210, 166, 300, 34), 1, "left", 4, 2)
    mark_box(top, (200, 246, 100, 30), 2, "left", 4, 2)
    mark_box(top, (296, 292, 88, 30), 3, "bottom", 15, 2)
    top.label(560, 250, 260, "Text, Choice, Date", arrow_to=(500, 300))


def lab_fo_questions(s, top):
    """Three questions: Text (Required), Choice with three options, Date."""
    h = 560
    forms_shell(s, h)
    fcard(s, 200, 140, 500, 80)
    s.text(216, 166, "1. Your name", 13, 700, INK)
    s.text(216, 190, "Enter your answer", 11.5, 400, LIGHT)
    s.rect(560, 198, 14, 14, fill=FO, rx=2)
    s.text(582, 210, "Required", 11.5, 400, INK)
    fcard(s, 200, 230, 500, 150)
    s.text(216, 256, "2. Which cake?", 13, 700, INK)
    for i, o in enumerate(("Chocolate", "Strawberry", "Vanilla")):
        s.rect(226, 268 + i * 30, 260, 24, fill="#ffffff", stroke="#e3e3e3", sw=1, rx=12)
        s.text(240, 285 + i * 30, o, 12, 400, INK)
    s.text(500, 360, "+ Add option", 11.5, 600, FO)
    fcard(s, 200, 390, 500, 80)
    s.text(216, 416, "3. When do you want it?", 13, 700, INK)
    s.text(216, 440, "Please input date (dd/MM/yyyy)", 11.5, 400, LIGHT)
    mark_box(top, (556, 194, 90, 22), 1, "right", 4, 2)
    mark_box(top, (226, 268, 260, 84), 2, "left", 4, 2)
    mark_box(top, (210, 400, 300, 50), 3, "left", 4, 2)


def lab_fo_preview(s, top):
    """Preview: a test order, then Submit."""
    h = 520
    p = forms_shell(s, h, preview=True)
    fcard(s, 200, 140, 500, 50, True)
    s.text(216, 172, "Mona's Cakes: order", 17, 400, INK)
    fcard(s, 200, 198, 500, 60)
    s.text(216, 220, "1. Your name *", 12.5, 700, INK)
    s.text(216, 246, "Huda", 12.5, 400, INK)
    s.line(216, 250, 500, 250, "#c9d6d4", 1)
    fcard(s, 200, 266, 500, 96)
    s.text(216, 288, "2. Which cake?", 12.5, 700, INK)
    for i, o in enumerate(("Chocolate", "Strawberry", "Vanilla")):
        s.circle(226, 306 + i * 20, 6, fill=FO if i == 0 else "#ffffff", stroke=FO, sw=1.4)
        s.text(240, 310 + i * 20, o, 12, 400, INK)
    fcard(s, 200, 370, 500, 60)
    s.text(216, 392, "3. When do you want it?", 12.5, 700, INK)
    s.text(216, 418, "05/12/2026", 12.5, 400, INK)
    s.rect(200, 444, 90, 30, fill=FO, rx=4)
    s.text(245, 464, "Submit", 13, 700, "#ffffff", "middle")
    mark_box(top, p["preview"], 1, "bottom", 4, 2)
    mark_box(top, (210, 230, 300, 120), 2, "left", 4, 2)
    mark_box(top, (200, 444, 90, 30), 3, "right", 4, 2)


def lab_fo_responses(s, top):
    """Responses: 1 response, and Open results in Excel."""
    h = 400
    p = forms_shell(s, h, tab="Responses")
    fcard(s, 200, 146, 500, 200)
    s.text(220, 186, "1", 34, 700, INK)
    s.text(250, 186, "Responses", 16, 400, INK)
    s.rect(220, 206, 190, 28, fill="#107c41", rx=4)
    s.text(315, 225, "Open results in Excel", 12, 700, "#ffffff", "middle")
    s.text(220, 270, "2. Which cake?", 12.5, 700, INK)
    s.rect(220, 284, 300, 14, fill="#e9ecef", rx=3)
    s.rect(220, 284, 300, 14, fill=FO, rx=3)
    s.text(530, 296, "Chocolate  1", 11.5, 400, INK)
    mark_box(top, p["Responses"], 1, "bottom", 4, 1)
    mark_box(top, (220, 206, 190, 28), 2, "right", 4, 2)


def _doc_ai_page(s, box, paras, fresh=()):
    x, y, w_, hh = box
    s.rect(x + 35, y + 13, w_ - 70, hh - 26, fill="#ffffff", stroke="#e0e0e0", sw=1)
    cy = y + 50
    for i, (st, txt, col) in enumerate(paras):
        size = {"Title": 20, "Normal": 11.5}[st]
        if i in fresh:
            s.rect(x + 60, cy - size, w_ - 130, size + 8, fill="#fff3bf")
        s.text(x + 65, cy, txt, size, 400, col or INK)
        cy += size + 16


def lab_w9_tutu_ai(s, top):
    paras = [("Title", "Mona's Cakes: the plan", None), ("Normal", "Welcome to Mona's Cakes: fresh cakes, made at home.", None),
             ("Normal", "The customer: students and families in Amman.", None), ("Normal", "The need: a fresh cake on the right day.", None)]
    tutu_ai(s, top, "plan-Huda", "doc", "Add a short welcome sentence for the customers under the title.",
            "Done: a welcome sentence is under the title.", lambda s_, b: _doc_ai_page(s_, b, paras, {1}))


def lab_w9_tutu_dl(s, top):
    tutu_download(s, top, "plan-Huda", "doc")



# =====================================================================
# Lecture 10: a site in Google Sites, and a web page in Notepad.
# =====================================================================

GS = "#1a73e8"
GS_SOFT = "#e8f0fe"
HTML_LINES = ["<html>", '<body style="font-family: Arial">', '<h1 style="color: brown">Mona\'s Cakes</h1>',
              "<p>Fresh cakes, made at home.</p>", "</body>", "</html>"]


def sites_shell(s, h, panel="Pages", name="Mona's Cakes", title="Mona's Cakes", pages=("Home",), theme=("#ffffff", INK, GS)):
    browser(s, h, "sites.google.com", "Google Sites")
    s.rect(15, 85, W - 30, 40, fill="#ffffff")
    s.text(30, 111, name or "Untitled site", 14, 400, INK if name else GREY)
    p = {"name": (24, 94, 220, 26)}
    p["preview"] = (650, 96, 36, 22)
    s.circle(668, 107, 9, stroke=INK, sw=1.6)
    s.circle(668, 107, 3, fill=INK)
    s.rect(720, 94, 80, 28, fill=GS, rx=4)
    s.text(760, 113, "Publish", 12.5, 700, "#ffffff", "middle")
    s.rect(15, 125, W - 30, h - 140, fill="#f1f3f4")
    bg, fg, acc = theme
    s.rect(40, 140, 560, h - 170, fill=bg, stroke="#dadce0", sw=1)
    s.text(56, 166, name or "Untitled site", 12, 700, fg)
    x = 400
    links = {}
    for pg in pages:
        s.text(x, 166, pg, 12, 700 if pg == "Home" else 400, acc if pg == "Home" else fg)
        links[pg] = (x - 4, 154, width(pg, 12) + 8, 18)
        x += width(pg, 12) + 18
    s.rect(40, 176, 560, 3, fill=acc)
    s.rect(40, 180, 560, 90, fill=acc)
    s.raw('<rect x="56" y="206" width="420" height="40" fill="none" stroke="#ffffff" stroke-dasharray="4 3"/>')
    s.text(64, 234, title or "Your page title", 22, 700, "#ffffff")
    p["title"] = (56, 206, 420, 40)
    s.text(56, 296, "Fresh cakes, made at home. Order two days before.", 12, 400, fg)
    px = 620
    s.rect(px, 125, W - 15 - px, h - 140, fill="#ffffff")
    for i, n in enumerate(("Insert", "Pages", "Themes")):
        xx = px + 16 + i * 84
        s.text(xx, 148, n, 12.5, 700 if n == panel else 400, GS if n == panel else INK)
        if n == panel:
            s.rect(xx - 2, 154, width(n, 12.5) + 4, 3, fill=GS)
        p["tab:" + n] = (xx - 6, 134, width(n, 12.5) + 12, 26)
    return p, links


def lab_gs_new(s, top):
    """sites.google.com, signed in with Google: Blank site."""
    h = 360
    browser(s, h, "sites.google.com", "Google Sites")
    s.rect(15, 85, W - 30, h - 100, fill="#f1f3f4")
    s.text(40, 120, "Start a new site", 14, 600, INK)
    s.rect(40, 136, 150, 110, fill="#ffffff", stroke=GS, sw=2, rx=6)
    s.circle(115, 182, 18, fill="#ffffff", stroke="#ea4335", sw=3)
    s.line(105, 182, 125, 182, "#4285f4", 3)
    s.text(115, 268, "Blank site", 12.5, 600, INK, "middle")
    for i, n in enumerate(("Event", "Portfolio", "Small business")):
        s.rect(206 + i * 166, 136, 150, 110, fill="#ffffff", stroke="#dadce0", sw=1, rx=6)
        s.text(281 + i * 166, 268, n, 12.5, 400, INK, "middle")
    mark_box(top, (40, 136, 150, 110), 1, "right", 6, 3)
    top.label(420, 300, 300, "first: Sign in with Google")


def lab_gs_name(s, top):
    p, _ = sites_shell(s, 360, "Insert")
    mark_box(top, p["name"], 1, "bottom", 4, 2)
    mark_box(top, p["title"], 2, "right", 4, 2)


def lab_gs_pages(s, top):
    """Pages › + New page › Name › Done; the menu gets the new links."""
    h = 400
    p, links = sites_shell(s, h, "Pages", pages=("Home", "Cakes", "Order"))
    px = 620
    for i, n in enumerate(("Home", "Cakes", "Order")):
        s.text(px + 20, 186 + i * 26, ("⌂ " if i == 0 else "▢ ") + n, 12.5, 400, INK)
    s.rect(px + 18, 268, 110, 28, fill=GS, rx=14)
    s.text(px + 73, 287, "+ New page", 12, 700, "#ffffff", "middle")
    s.rect(px + 14, 304, 220, 80, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=6)
    s.text(px + 26, 324, "New page", 12.5, 700, INK)
    s.rect(px + 26, 332, 130, 24, fill="#ffffff", stroke=GS, sw=1.6)
    s.text(px + 32, 349, "Order", 12, 400, INK)
    s.rect(px + 164, 332, 60, 24, fill=GS, rx=3)
    s.text(px + 194, 349, "Done", 12, 700, "#ffffff", "middle")
    mark_box(top, p["tab:Pages"], 1, "top", 4, 1)
    mark_box(top, (px + 18, 268, 110, 28), 2, "left", 14, 2)
    mark_box(top, (px + 26, 332, 130, 24), 3, "left", 3, 2)
    mark_box(top, (px + 164, 332, 60, 24), 4, "bottom", 3, 2)
    mark_box(top, (links["Cakes"][0], links["Cakes"][1], links["Order"][0] + links["Order"][2] - links["Cakes"][0], 18), 5, "bottom", 3, 2)


def lab_gs_themes(s, top):
    h = 400
    theme = ("#f6efe6", "#3e2723", "#8d6e63")
    p, _ = sites_shell(s, h, "Themes", pages=("Home", "Cakes", "Order"), theme=theme)
    px = 620
    for i, (n, c) in enumerate((("Simple", GS), ("Aristotle", "#8d6e63"), ("Diplomat", "#0b57d0"), ("Vision", "#f6b26b"))):
        y = 176 + i * 46
        s.rect(px + 16, y, 234, 38, fill=GS_SOFT if i == 1 else "#ffffff", stroke=GS if i == 1 else "#dadce0", sw=1.4 if i == 1 else 1, rx=4)
        s.rect(px + 26, y + 8, 30, 22, fill="#ffffff", stroke=c, sw=3)
        s.text(px + 66, y + 24, n, 12.5, 600 if i == 1 else 400, INK)
    mark_box(top, p["tab:Themes"], 1, "top", 4, 1)
    mark_box(top, (px + 16, 222, 234, 38), 2, "left", 4, 2)
    mark_box(top, p["preview"], 3, "bottom", 10, 3)


def lab_gs_phone(s, top):
    """Preview: Phone; the menu becomes three lines."""
    h = 430
    browser(s, h, "sites.google.com", "Google Sites")
    s.rect(15, 85, W - 30, h - 100, fill="#f1f3f4")
    for i, n in enumerate(("Phone", "Tablet", "Large screen")):
        s.rect(300 + i * 100, 96, 92, 26, fill=GS_SOFT if i == 0 else "#ffffff", stroke=GS if i == 0 else "#dadce0", sw=1, rx=4)
        s.text(346 + i * 100, 114, n, 12, 600 if i == 0 else 400, INK, "middle")
    s.rect(380, 134, 160, 270, fill="#202124", rx=18)
    s.rect(388, 142, 144, 254, fill="#f6efe6", rx=10)
    s.text(398, 166, "Mona's Cakes", 10.5, 700, "#3e2723")
    for k in range(3):
        s.line(508, 158 + k * 5, 522, 158 + k * 5, "#3e2723", 1.6)
    s.rect(388, 178, 144, 70, fill="#8d6e63")
    s.text(398, 222, "Mona's Cakes", 15, 700, "#ffffff")
    for k, ln in enumerate(("Fresh cakes, made at", "home. Order two", "days before.")):
        s.text(398, 270 + k * 16, ln, 10.5, 400, "#3e2723")
    mark_box(top, (300, 96, 92, 26), 1, "left", 4, 2)
    mark_box(top, (504, 152, 22, 16), 2, "right", 3, 2)


def notepad(s, h, lines, name="Untitled - Notepad", caret=True):
    frame(s, h)
    s.rect(15, 15, W - 30, 34, fill=TITLE_BG, rx=9)
    s.rect(15, 35, W - 30, 14, fill=TITLE_BG)
    s.text(30, 37, name, 12.5, 400, INK)
    s.rect(15, 49, W - 30, 26, fill="#ffffff")
    menus = {}
    x = 30
    for m in ("File", "Edit", "View"):
        s.text(x, 67, m, 12.5, 400, INK)
        menus[m] = (x - 6, 52, width(m, 12.5) + 12, 22)
        x += width(m, 12.5) + 22
    s.line(15, 75, W - 15, 75, "#e0e0e0", 1)
    s.rect(15, 76, W - 30, h - 91, fill="#ffffff")
    for i, ln in enumerate(lines):
        s.raw('<text x="30" y="%g" font-size="14" font-family="Consolas, DejaVu Sans Mono, monospace" fill="%s">%s</text>' % (100 + i * 22, INK, ln.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")))
    return menus


def lab_np_type(s, top):
    notepad(s, 260, HTML_LINES)
    top.label(560, 150, 260, "type it exactly, line by line", arrow_to=(520, 145))


def lab_np_save(s, top):
    """File › Save as: Desktop, page-Huda.html, Save as type: All files."""
    save_as(s, top, "page-Huda.html", "All files (*.*)", "#0067c0")


def lab_np_browser(s, top):
    """The page in the browser (double-click page-Huda.html on the Desktop)."""
    h = 260
    browser(s, h, "C:/Users/Huda/Desktop/page-Huda.html", "Mona's Cakes")
    s.rect(15, 85, W - 30, h - 100, fill="#ffffff")
    s.text(40, 130, "Mona's Cakes", 28, 700, "#8b4513")
    s.text(40, 166, "Fresh cakes, made at home.", 14, 400, INK)
    top.label(420, 112, 300, "the colour comes from the CSS: brown", arrow_to=(250, 120))


def lab_np_result(s, top):
    h = 260
    browser(s, h, "C:/Users/Huda/Desktop/page-Huda.html", "Mona's Cakes")
    s.rect(15, 85, W - 30, h - 100, fill="#ffffff")
    s.text(40, 130, "Mona's Cakes", 28, 700, "#2b8a3e")
    s.text(40, 166, "Fresh cakes, made at home.", 14, 400, INK)


def lab_gs_tutu_ai(s, top):
    paras = [("Title", "Mona's Cakes", "#8b4513"), ("Normal", "Fresh cakes, made at home.", None),
             ("Normal", "Our three cakes are chocolate, strawberry and vanilla.", None)]
    tutu_ai(s, top, "page-Huda", "doc", "Add a short paragraph: our three cakes are chocolate, strawberry and vanilla.",
            "Done: a short paragraph about the three cakes is at the end.", lambda s_, b: _doc_ai_page(s_, b, paras, {2}))


def lab_gs_tutu_dl(s, top):
    tutu_download(s, top, "page-Huda", "doc", pick=2)



# =====================================================================
# Lecture 11: a post for social media made in PowerPoint (one slide), saved
# as a picture (PNG).
# =====================================================================

POST = {"title": "Fresh cakes for your party!", "sub": "Order today on our website"}


def lab_post_title(s, top):
    _, _, boxes, _ = ppt_window(s, 470, "Home", [None], 0, empty=True)
    mark_box(top, boxes["title"], 1, "left", 4, 2)
    mark_box(top, boxes["body"], 2, "left", 4, 2)


def lab_post_design(s, top):
    tabs, rb, _, _ = ppt_window(s, 470, "Design", [POST], 0, theme="Ion", theme_sel="Ion")
    mark_box(top, tabs["Design"], 1, "top", 6, 1)
    mark_box(top, rb["theme:Ion"], 2, "bottom", 4, 2)


def lab_post_icons(s, top):
    """Insert › Icons; search cake; a cake icon; Insert."""
    h = 500
    tabs, rb, boxes, _ = ppt_window(s, h, "Insert", [POST], 0, theme="Ion")
    x0, y0 = 250, 168
    s.rect(x0, y0, 330, 220, fill="#ffffff", stroke="#a6a6a6", sw=1, rx=4)
    s.rect(x0 + 14, y0 + 14, 300, 26, fill="#ffffff", stroke=PPT, sw=1.4, rx=13)
    icon_search(s, x0 + 30, y0 + 27, GREY)
    s.text(x0 + 44, y0 + 32, "cake", 12.5, 400, INK)
    for i in range(4):
        x = x0 + 20 + i * 76
        s.rect(x, y0 + 56, 64, 64, fill="#ffffff" if i else PPT_SOFT, stroke=PPT if i == 0 else "#e0e0e0", sw=2 if i == 0 else 1, rx=4)
        cx, cy = x + 32, y0 + 92
        s.rect(cx - 18, cy - 4, 36, 18, fill="#5c5c5c", rx=2)
        s.rect(cx - 14, cy - 14, 28, 12, fill="#5c5c5c", rx=2)
        s.rect(cx - 1, cy - 24, 2, 9, fill="#5c5c5c")
    s.rect(x0 + 230, y0 + 176, 84, 28, fill=PPT, rx=4)
    s.text(x0 + 272, y0 + 195, "Insert", 12.5, 700, "#ffffff", "middle")
    mark_box(top, tabs["Insert"], 1, "top", 6, 1)
    mark_box(top, rb["icons"], 2, "right", 4, 1)
    mark_box(top, (x0 + 14, y0 + 14, 300, 26), 3, "right", 13, 2)
    mark_box(top, (x0 + 20, y0 + 56, 64, 64), 4, "left", 4, 2)
    mark_box(top, (x0 + 230, y0 + 176, 84, 28), 5, "right", 4, 2)


def lab_post_png(s, top):
    save_as(s, top, "post-Huda", "PNG Portable Network Graphics Format (*.png)", PPT)


def lab_post_result(s, top):
    h = 400
    frame(s, h)
    ppt_slide(s, 210, 40, 480, POST, "Ion")
    cx, cy = 640, 260
    s.rect(cx - 22, cy - 6, 44, 22, fill="#ffffff", rx=3)
    s.rect(cx - 17, cy - 18, 34, 14, fill="#ffffff", rx=3)
    s.rect(cx - 1.5, cy - 30, 3, 11, fill="#ffffff")
    top.label(330, 330, 240, "post-Huda.png: ready to share")


def lab_post_tutu_ai(s, top):
    def draw_page(s_, box):
        x, y, w_, hh = box
        ppt_slide(s_, x + 30, y + 14, 230, POST, "Ion")
        ppt_slide(s_, x + 280, y + 14, 230, {"title": "Our cakes", "points": ["Chocolate · 8 JD", "Strawberry · 9 JD", "Vanilla · 7 JD"]}, "Ion")
        s_.rect(x + 278, y + 12, 234, 133, stroke="#f2c94c", sw=3, rx=3)
    tutu_ai(s, top, "post-Huda", "slides", "Add a second slide with our three cakes and their prices.",
            "Done: slide 2 shows the three cakes and their prices.", draw_page)


def lab_post_tutu_dl(s, top):
    tutu_download(s, top, "post-Huda", "slides")


# name: (the drawing, the part of it that the worksheet shows: x, y, width, height).
# A crop zooms in on the buttons of the step, so that they are big on paper.
SCREENS = {
    "week-04/images/lab-open-1": (lab_open_1, None),
    "week-04/images/lab-open-2": (lab_open_2, (176, 28, 370, 300)),
    "week-04/images/lab-styles-1": (lab_styles_1, (440, 80, 445, 220)),
    "week-04/images/lab-styles-2": (lab_styles_2, (440, 80, 445, 340)),
    "week-04/images/lab-nav-1": (lab_nav_1, (15, 26, 650, 350)),
    "week-04/images/lab-format-1": (lab_format_1, (220, 80, 480, 200)),
    "week-04/images/lab-format-2": (lab_format_2, (90, 80, 470, 320)),
    "week-04/images/lab-table-1": (lab_table_1, (20, 26, 530, 410)),
    "week-04/images/lab-spell-1": (lab_spell_1, (100, 184, 785, 330)),
    "week-04/images/lab-tutu-1": (lab_tutu_1, (150, 86, 610, 374)),
    "week-04/images/lab-tutu-2": (lab_tutu_2, (15, 86, 870, 370)),
    "week-04/images/lab-tutu-3": (lab_tutu_3, (0, 86, 470, 366)),
    "week-04/images/lab-save-2": (lab_save_2, None),
    "week-04/images/lab-result-1": (lab_result_1, (200, 186, 500, 340)),
    # Lecture 5, PowerPoint (week-06)
    "week-06/images/lab-open-1": (lab_ppt_open, None),
    "week-06/images/lab-open-2": (lab_ppt_start, (176, 28, 370, 300)),
    "week-06/images/lab-title-1": (lab_ppt_title, (15, 180, 870, 255)),
    "week-06/images/lab-newslide-1": (lab_ppt_newslide, (15, 80, 520, 350)),
    "week-06/images/lab-notes-1": (lab_ppt_notes, (15, 184, 870, 300)),
    "week-06/images/lab-design-1": (lab_ppt_design, (15, 26, 870, 330)),
    "week-06/images/lab-transition-1": (lab_ppt_transition, (15, 26, 870, 330)),
    "week-06/images/lab-animation-1": (lab_ppt_animation, (15, 26, 870, 400)),
    "week-06/images/lab-save-1": (lab_ppt_save, None),
    "week-06/images/lab-result-1": (lab_ppt_result, (15, 184, 870, 250)),
    "week-06/images/lab-tutu-1": (lab_tutu_1, (150, 86, 610, 374)),
    "week-06/images/lab-tutu-2": (lab_ppt_tutu_ai, (15, 86, 870, 370)),
    "week-06/images/lab-tutu-3": (lab_ppt_tutu_dl, (0, 86, 470, 366)),
    # Lecture 6, Excel (1) (week-07)
    "week-07/images/lab-open-1": (lab_xl_open, None),
    "week-07/images/lab-open-2": (lab_xl_start, (176, 28, 370, 300)),
    "week-07/images/lab-type-1": (lab_xl_type, (15, 180, 870, 250)),
    "week-07/images/lab-formula-1": (lab_xl_formula, (15, 180, 620, 170)),
    "week-07/images/lab-fill-1": (lab_xl_fill, (15, 180, 760, 170)),
    "week-07/images/lab-sum-1": (lab_xl_sum, (15, 80, 870, 300)),
    "week-07/images/lab-save-1": (lab_xl_save, None),
    "week-07/images/lab-result-1": (lab_xl_result, (15, 180, 560, 210)),
    "week-07/images/lab-tutu-1": (lab_tutu_1, (150, 86, 610, 374)),
    "week-07/images/lab-tutu-2": (lab_xl_tutu_ai, (15, 86, 870, 370)),
    "week-07/images/lab-tutu-3": (lab_xl_tutu_dl, (0, 86, 470, 366)),
    # Lecture 7, Excel (2) (week-09)
    "week-09/images/lab-open-1": (lab_xl_open, None),
    "week-09/images/lab-open-2": (lab_xl_start, (176, 28, 370, 300)),
    "week-09/images/lab-type-1": (lab_xl7_type, (15, 180, 870, 260)),
    "week-09/images/lab-sort-1": (lab_xl7_sort, (15, 26, 600, 360)),
    "week-09/images/lab-filter-1": (lab_xl7_filter, (15, 26, 600, 400)),
    "week-09/images/lab-cf-1": (lab_xl7_cf, (15, 26, 870, 410)),
    "week-09/images/lab-chart-1": (lab_xl7_chart, (15, 26, 870, 440)),
    "week-09/images/lab-save-1": (lab_xl7_save, None),
    "week-09/images/lab-result-1": (lab_xl7_result, (15, 180, 560, 210)),
    "week-09/images/lab-tutu-1": (lab_tutu_1, (150, 86, 610, 374)),
    "week-09/images/lab-tutu-2": (lab_xl7_tutu_ai, (15, 86, 870, 370)),
    "week-09/images/lab-tutu-3": (lab_xl7_tutu_dl, (0, 86, 470, 366)),
    # Lecture 8, Access (week-10)
    "week-10/images/lab-open-1": (lab_ac_open, None),
    "week-10/images/lab-new-1": (lab_ac_new, (176, 28, 540, 300)),
    "week-10/images/lab-design-1": (lab_ac_design, (15, 26, 660, 360)),
    "week-10/images/lab-fields-1": (lab_ac_fields, (15, 26, 700, 290)),
    "week-10/images/lab-records-1": (lab_ac_records, (15, 80, 640, 240)),
    "week-10/images/lab-query-1": (lab_ac_query1, (15, 26, 640, 340)),
    "week-10/images/lab-query-2": (lab_ac_query2, (15, 26, 660, 350)),
    "week-10/images/lab-export-1": (lab_ac_export, (15, 180, 840, 240)),
    "week-10/images/lab-result-1": (lab_ac_result, (15, 180, 560, 120)),
    "week-10/images/lab-tutu-1": (lab_tutu_1, (150, 86, 610, 374)),
    "week-10/images/lab-tutu-2": (lab_ac_tutu_ai, (15, 86, 870, 370)),
    "week-10/images/lab-tutu-3": (lab_ac_tutu_dl, (0, 86, 470, 366)),
    # Lecture 9, a digital service: Word and Microsoft Forms (week-11)
    "week-11/images/lab-open-1": (lab_open_1, None),
    "week-11/images/lab-plan-1": (lab_w9_plan, (320, 80, 565, 300)),
    "week-11/images/lab-save-1": (lab_w9_save, None),
    "week-11/images/lab-forms-1": (lab_fo_new, (15, 15, 870, 350)),
    "week-11/images/lab-forms-2": (lab_fo_title, (15, 85, 870, 260)),
    "week-11/images/lab-forms-3": (lab_fo_questions, (150, 130, 600, 360)),
    "week-11/images/lab-forms-4": (lab_fo_preview, (150, 85, 740, 410)),
    "week-11/images/lab-result-1": (lab_fo_responses, (15, 85, 870, 280)),
    "week-11/images/lab-tutu-1": (lab_tutu_1, (150, 86, 610, 374)),
    "week-11/images/lab-tutu-2": (lab_w9_tutu_ai, (15, 86, 870, 370)),
    "week-11/images/lab-tutu-3": (lab_w9_tutu_dl, (0, 86, 470, 366)),
    # Lecture 10, a website: Google Sites and Notepad (week-12)
    "week-12/images/lab-sites-1": (lab_gs_new, (15, 15, 870, 330)),
    "week-12/images/lab-sites-2": (lab_gs_name, (15, 85, 870, 260)),
    "week-12/images/lab-sites-3": (lab_gs_pages, (15, 85, 870, 300)),
    "week-12/images/lab-sites-4": (lab_gs_themes, (15, 85, 870, 300)),
    "week-12/images/lab-sites-5": (lab_gs_phone, (250, 85, 400, 330)),
    "week-12/images/lab-notepad-1": (lab_np_type, (15, 15, 870, 230)),
    "week-12/images/lab-save-1": (lab_np_save, None),
    "week-12/images/lab-browser-1": (lab_np_browser, (15, 15, 870, 230)),
    "week-12/images/lab-result-1": (lab_np_result, (15, 15, 600, 230)),
    "week-12/images/lab-tutu-1": (lab_tutu_1, (150, 86, 610, 374)),
    "week-12/images/lab-tutu-2": (lab_gs_tutu_ai, (15, 86, 870, 370)),
    "week-12/images/lab-tutu-3": (lab_gs_tutu_dl, (0, 86, 495, 366)),
    # Lecture 11, a post in PowerPoint (week-14)
    "week-14/images/lab-open-1": (lab_ppt_open, None),
    "week-14/images/lab-open-2": (lab_ppt_start, (176, 28, 370, 300)),
    "week-14/images/lab-post-1": (lab_post_title, (15, 180, 870, 255)),
    "week-14/images/lab-post-2": (lab_post_design, (15, 26, 870, 330)),
    "week-14/images/lab-post-3": (lab_post_icons, (15, 26, 870, 400)),
    "week-14/images/lab-save-1": (lab_post_save, None),
    "week-14/images/lab-save-2": (lab_post_png, None),
    "week-14/images/lab-result-1": (lab_post_result, (180, 26, 540, 330)),
    "week-14/images/lab-tutu-1": (lab_tutu_1, (150, 86, 610, 374)),
    "week-14/images/lab-tutu-2": (lab_post_tutu_ai, (15, 86, 870, 370)),
    "week-14/images/lab-tutu-3": (lab_post_tutu_dl, (0, 86, 470, 366)),
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
        os.makedirs(os.path.dirname(svg), exist_ok=True)
        with open(svg, "w", encoding="utf-8") as f:
            f.write(draw(fn, crop))
        if "--svg" not in sys.argv:
            export_png(svg)
        print("wrote", os.path.relpath(svg, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
