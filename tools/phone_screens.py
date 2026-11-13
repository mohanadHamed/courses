#!/usr/bin/env python3
"""Draw the phone screens of an online activity (AUTHORING.md, "Screens of every app step").

A student who works alone must see the app before using it: one picture
for each step, drawn close to the real app of the current version (its
layout, its words, where its buttons are), without logos. A numbered orange
circle marks what to tap; the step itself is the caption under the picture
on the page (`::: {.screens}`, inside a tab for each phone).

Every screen is a function below. Look at the real app before you draw it:
its official help page, or the app in the iOS Simulator of Xcode for an
iPhone. Add a new screen to SCREENS, then run from the project root:

    python3 tools/phone_screens.py          # every SVG and its PNG
    python3 tools/phone_screens.py --svg    # the SVGs only

The PNG is exported like the posters (shared/sims/README.md): quarto typst
compile, 200 ppi, font Helvetica (or Arial).
"""

import os
import subprocess
import sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "Helvetica, Arial, sans-serif"

W, H = 340, 640                              # the picture
BX, BY, BW, BH, BR = 20, 20, 300, 600, 46    # the phone
SX, SY, SW, SH, SR = 28, 28, 284, 584, 38    # its screen

INK = "#1f2328"
GREY = "#5f656b"
LIGHT = "#a3a8ad"
LINE = "#e3e5e8"
BG = "#fff9f2"           # the card of the course figures
BODY = "#25292e"
KEY = "#3d434a"
MARK = "#d9480f"         # what to tap: the course orange
MARK_INK = "#a3360b"
MARK_SOFT = "#fff1e6"
TEAL = "#0b7285"         # an Android app (its colours change with the phone)
TEAL_SOFT = "#d5f0f4"
TEAL_INK = "#095664"
IOS_RED = "#e5484d"      # Calendar on an iPhone
IOS_BLUE = "#1c7ed6"     # Files on an iPhone
IOS_BG = "#f2f2f7"
IOS_FILL = "#ececf0"
DARK = "#17191c"         # a camera


def _paint(fill="none", stroke=None, sw=1.5, opacity=None):
    a = ' fill="%s"' % fill
    if stroke:
        a += ' stroke="%s" stroke-width="%g" stroke-linecap="round" stroke-linejoin="round"' % (stroke, sw)
    if opacity is not None:
        a += ' opacity="%g"' % opacity
    return a


class Svg:
    """A list of SVG elements, with a few helpers."""

    def __init__(self):
        self.out = []

    def raw(self, s):
        self.out.append(s)

    def rect(self, x, y, w, h, fill="none", stroke=None, sw=1.5, rx=0, opacity=None):
        r = ' rx="%g"' % rx if rx else ""
        self.out.append('<rect x="%g" y="%g" width="%g" height="%g"%s%s/>'
                        % (x, y, w, h, r, _paint(fill, stroke, sw, opacity)))

    def circle(self, cx, cy, r, fill="none", stroke=None, sw=1.5, opacity=None):
        self.out.append('<circle cx="%g" cy="%g" r="%g"%s/>' % (cx, cy, r, _paint(fill, stroke, sw, opacity)))

    def line(self, x1, y1, x2, y2, stroke=INK, sw=2):
        self.out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"%s/>' % (x1, y1, x2, y2, _paint("none", stroke, sw)))

    def path(self, d, fill="none", stroke=None, sw=2, opacity=None):
        self.out.append('<path d="%s"%s/>' % (d, _paint(fill, stroke, sw, opacity)))

    def poly(self, pts, fill="none", stroke=None, sw=2, closed=True):
        tag = "polygon" if closed else "polyline"
        p = " ".join("%g,%g" % xy for xy in pts)
        self.out.append('<%s points="%s"%s/>' % (tag, p, _paint(fill, stroke, sw)))

    def text(self, x, y, s, size=15, weight=400, fill=INK, anchor="start"):
        self.out.append('<text x="%g" y="%g" font-size="%g" font-weight="%d" fill="%s" text-anchor="%s">%s</text>'
                        % (x, y, size, weight, fill, anchor, escape(s)))

    # What to tap: an orange frame and a numbered circle.
    def ring(self, x, y, w, h, r=10):
        self.rect(x, y, w, h, stroke=MARK, sw=3, rx=r)

    def ring_circle(self, cx, cy, r):
        self.circle(cx, cy, r, stroke=MARK, sw=3)

    def mark(self, n, x, y):
        self.circle(x, y, 12.5, fill=MARK, stroke="#ffffff", sw=2)
        self.text(x, y + 5, str(n), 14.5, 800, "#ffffff", "middle")

    def label(self, x, y, w, s, arrow_to=None):
        """An orange label for a key on the side of the phone, with its arrow."""
        self.rect(x, y, w, 26, fill=MARK_SOFT, stroke=MARK, sw=2, rx=13)
        self.text(x + w / 2, y + 18, s, 13, 700, MARK_INK, "middle")
        if arrow_to is not None:
            ax, ay = arrow_to
            sx = x + w if ax > x else x
            self.line(sx, y + 13, ax, ay, MARK, 2.5)
            d = 1 if ax > sx else -1
            self.poly([(ax, ay), (ax - 8 * d, ay - 5), (ax - 8 * d, ay + 5)], fill=MARK)


# ---------- Small icons (no cross shapes: see check_figures.py) ----------

def icon_menu(s, cx, cy, c=INK):
    for dy in (-6, 0, 6):
        s.line(cx - 8, cy + dy, cx + 8, cy + dy, c, 2)


def icon_search(s, cx, cy, c=INK):
    s.circle(cx - 2, cy - 2, 6, stroke=c, sw=2)
    s.line(cx + 2.5, cy + 2.5, cx + 7, cy + 7, c, 2.2)


def icon_close(s, cx, cy, c=INK, r=6):
    s.line(cx - r, cy - r, cx + r, cy + r, c, 2.2)
    s.line(cx + r, cy - r, cx - r, cy + r, c, 2.2)


def icon_check(s, cx, cy, c=INK, k=1.0, sw=2.4):
    s.poly([(cx - 7 * k, cy), (cx - 2 * k, cy + 5 * k), (cx + 7 * k, cy - 6 * k)], stroke=c, sw=sw, closed=False)


def icon_bell(s, cx, cy, c=GREY):
    s.path("M%g %g C%g %g %g %g %g %g C%g %g %g %g %g %g Z" % (
        cx - 7, cy + 5, cx - 7, cy - 9, cx - 2, cy - 8, cx, cy - 8,
        cx + 2, cy - 8, cx + 7, cy - 9, cx + 7, cy + 5), stroke=c, sw=1.8)
    s.circle(cx, cy + 8, 1.8, fill=c)


def icon_clock(s, cx, cy, c=GREY):
    s.circle(cx, cy, 8, stroke=c, sw=1.8)
    s.line(cx, cy, cx, cy - 5, c, 1.8)
    s.line(cx, cy, cx + 4, cy, c, 1.8)


def icon_repeat(s, cx, cy, c=GREY):
    s.path("M%g %g A7 7 0 1 1 %g %g" % (cx - 7, cy, cx - 1, cy + 7), stroke=c, sw=1.8)
    s.poly([(cx - 10, cy - 2), (cx - 7, cy + 3), (cx - 3, cy - 1)], fill=c)


def icon_people(s, cx, cy, c=GREY):
    s.circle(cx, cy - 4, 3.6, stroke=c, sw=1.8)
    s.path("M%g %g Q%g %g %g %g" % (cx - 7, cy + 7, cx, cy - 2, cx + 7, cy + 7), stroke=c, sw=1.8)


def icon_pin(s, cx, cy, c=GREY):
    s.path("M%g %g C%g %g %g %g %g %g C%g %g %g %g %g %g Z" % (
        cx, cy + 9, cx - 9, cy, cx - 7, cy - 9, cx, cy - 9,
        cx + 7, cy - 9, cx + 9, cy, cx, cy + 9), stroke=c, sw=1.8)
    s.circle(cx, cy - 2, 2.4, fill=c)


def icon_cal(s, cx, cy, c=GREY):
    s.rect(cx - 8, cy - 7, 16, 15, stroke=c, sw=1.8, rx=3)
    s.line(cx - 7, cy - 2.5, cx + 7, cy - 2.5, c, 1.6)
    s.circle(cx - 3, cy + 3, 1.3, fill=c)
    s.circle(cx + 2, cy + 3, 1.3, fill=c)


def icon_lines(s, cx, cy, c=GREY):
    for dy, w in ((-5, 16), (0, 16), (5, 10)):
        s.line(cx - 8, cy + dy, cx - 8 + w, cy + dy, c, 1.8)


def icon_task(s, cx, cy, c=INK):
    s.circle(cx, cy, 8, stroke=c, sw=1.8)
    icon_check(s, cx, cy, c, 0.55, 1.8)


def icon_camera(s, cx, cy, c=INK):
    s.rect(cx - 11, cy - 6, 22, 15, stroke=c, sw=2, rx=3.5)
    s.path("M%g %g L%g %g L%g %g L%g %g" % (cx - 5, cy - 6, cx - 3, cy - 9, cx + 3, cy - 9, cx + 5, cy - 6),
           stroke=c, sw=2)
    s.circle(cx, cy + 1.5, 4, stroke=c, sw=2)


def icon_doc(s, x, y, c, w=20, h=26, label=None):
    s.path("M%g %g L%g %g L%g %g L%g %g L%g %g Z" % (x, y, x + w - 7, y, x + w, y + 7, x + w, y + h, x, y + h),
           fill="#ffffff", stroke=c, sw=1.8)
    if label:
        s.rect(x - 3, y + h - 12, w + 6, 9, fill=c, rx=2)
        s.text(x + w / 2, y + h - 4.8, label, 6.5, 800, "#ffffff", "middle")
    else:
        for i in range(3):
            s.line(x + 4, y + 10 + 4.5 * i, x + w - 4, y + 10 + 4.5 * i, c, 1.4)


def icon_folder(s, x, y, c, w=24, h=18):
    s.path("M%g %g L%g %g L%g %g L%g %g L%g %g L%g %g Z" % (
        x, y + 3, x + 8, y + 3, x + 10, y, x + w, y, x + w, y + h, x, y + h), fill=c)


def icon_image(s, x, y, c, w=22, h=18):
    s.rect(x, y, w, h, stroke=c, sw=1.8, rx=3)
    s.poly([(x + 3, y + h - 3), (x + 9, y + 8), (x + 13, y + 12), (x + 15, y + 10), (x + w - 3, y + h - 3)], fill=c)
    s.circle(x + w - 6, y + 6, 2, fill=c)


def icon_home(s, cx, cy, c=INK, fill="none"):
    s.poly([(cx - 8, cy - 1), (cx, cy - 8), (cx + 8, cy - 1), (cx + 8, cy + 8), (cx - 8, cy + 8)], fill=fill, stroke=c,
           sw=1.8)


def icon_star(s, cx, cy, c=INK):
    import math
    pts = []
    for i in range(10):
        r = 8.5 if i % 2 == 0 else 3.8
        a = math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    s.poly(pts, stroke=c, sw=1.6)


def icon_shared(s, cx, cy, c=INK):
    s.circle(cx - 3, cy - 3, 3.4, stroke=c, sw=1.7)
    s.circle(cx + 5, cy - 2, 2.6, stroke=c, sw=1.7)
    s.path("M%g %g Q%g %g %g %g" % (cx - 9, cy + 8, cx - 3, cy + 1, cx + 3, cy + 8), stroke=c, sw=1.7)
    s.path("M%g %g Q%g %g %g %g" % (cx + 3, cy + 3, cx + 7, cy + 2, cx + 10, cy + 7), stroke=c, sw=1.7)


def icon_pencil(s, cx, cy, c=INK):
    s.poly([(cx - 7, cy + 7), (cx - 7, cy + 3), (cx + 4, cy - 8), (cx + 8, cy - 4), (cx - 3, cy + 7)], stroke=c,
           sw=1.8)


def icon_dots(s, cx, cy, c=INK, vertical=False, r=2.2, gap=7):
    for k in (-1, 0, 1):
        s.circle(cx + (0 if vertical else k * gap), cy + (k * gap if vertical else 0), r, fill=c)


def icon_list(s, cx, cy, c=INK):
    s.rect(cx - 10, cy - 8, 20, 16, stroke=c, sw=1.8, rx=3)
    s.line(cx - 4, cy - 2, cx + 6, cy - 2, c, 1.6)
    s.line(cx - 4, cy + 3, cx + 6, cy + 3, c, 1.6)
    for dy in (-4, 0, 4):
        s.circle(cx - 13, cy + dy, 1.1, fill=c)


def icon_grid(s, cx, cy, c=INK):
    s.rect(cx - 9, cy - 8, 18, 16, stroke=c, sw=1.8, rx=3)
    for i in range(3):
        for j in range(2):
            s.circle(cx - 4.5 + 4.5 * i, cy - 1 + 4 * j, 1.1, fill=c)


def icon_inbox(s, cx, cy, c=INK):
    s.path("M%g %g L%g %g L%g %g L%g %g L%g %g Z" % (
        cx - 10, cy + 1, cx - 6, cy - 7, cx + 6, cy - 7, cx + 10, cy + 1, cx + 10, cy + 8), stroke=c, sw=1.8)
    s.path("M%g %g L%g %g L%g %g Q%g %g %g %g L%g %g" % (
        cx - 10, cy + 1, cx - 10, cy + 8, cx + 10, cy + 8, cx, cy + 6, cx - 4, cy + 1, cx - 10, cy + 1),
        stroke=c, sw=1.4)


def icon_updown(s, cx, cy, c=GREY):
    s.poly([(cx - 4, cy - 3), (cx, cy - 7), (cx + 4, cy - 3)], stroke=c, sw=1.6, closed=False)
    s.poly([(cx - 4, cy + 3), (cx, cy + 7), (cx + 4, cy + 3)], stroke=c, sw=1.6, closed=False)


def icon_chev(s, cx, cy, c=INK, left=True, k=1.0):
    d = 1 if left else -1
    s.poly([(cx + 4 * d * k, cy - 8 * k), (cx - 4 * d * k, cy), (cx + 4 * d * k, cy + 8 * k)], stroke=c, sw=2.4,
           closed=False)


def icon_flash(s, cx, cy, c="#ffffff"):
    s.poly([(cx + 2, cy - 9), (cx - 5, cy + 1), (cx, cy + 1), (cx - 2, cy + 9), (cx + 5, cy - 1), (cx, cy - 1)],
           stroke=c, sw=1.6)


def icon_filters(s, cx, cy, c="#ffffff"):
    for dx, dy in ((-3.5, -2), (3.5, -2), (0, 3.5)):
        s.circle(cx + dx, cy + dy, 4.6, stroke=c, sw=1.5)


def icon_scan(s, cx, cy, c=INK):
    k = 8
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        x, y = cx + sx * k, cy + sy * k
        s.path("M%g %g L%g %g L%g %g" % (x, y - sy * 4, x, y, x - sx * 4, y), stroke=c, sw=1.8)
    s.rect(cx - 3.5, cy - 4.5, 7, 9, stroke=c, sw=1.5, rx=1)


def icon_monitor(s, cx, cy, c=INK):
    s.rect(cx - 9, cy - 8, 18, 12, stroke=c, sw=1.8, rx=2)
    s.path("M%g %g L%g %g L%g %g" % (cx - 1, cy + 4, cx - 1, cy + 7, cx - 5, cy + 8), stroke=c, sw=1.6)


def icon_squares(s, cx, cy, c=INK):
    for dx in (-4.5, 4.5):
        for dy in (-4.5, 4.5):
            s.rect(cx + dx - 3.5, cy + dy - 3.5, 7, 7, stroke=c, sw=1.5, rx=1.5)


def icon_info(s, cx, cy, c=INK):
    s.circle(cx, cy, 8.5, stroke=c, sw=1.6)
    s.text(cx, cy + 4.5, "i", 12, 700, c, "middle")


def icon_box(s, cx, cy, c=INK):
    s.rect(cx - 9, cy - 7, 18, 5, stroke=c, sw=1.6, rx=1.5)
    s.path("M%g %g L%g %g L%g %g L%g %g" % (cx - 8, cy - 2, cx - 8, cy + 8, cx + 8, cy + 8, cx + 8, cy - 2),
           stroke=c, sw=1.6)


def icon_copy(s, cx, cy, c=INK):
    s.rect(cx - 7, cy - 4, 11, 12, stroke=c, sw=1.6, rx=2.5)
    s.path("M%g %g L%g %g Q%g %g %g %g L%g %g" % (cx - 3, cy - 6, cx - 3, cy - 7, cx - 3, cy - 8, cx - 1, cy - 8,
                                                 cx + 7, cy - 8), stroke=c, sw=1.6)
    s.path("M%g %g L%g %g" % (cx + 7, cy - 8, cx + 7, cy + 3), stroke=c, sw=1.6)


def icon_share(s, cx, cy, c=INK):
    s.path("M%g %g L%g %g L%g %g L%g %g L%g %g" % (cx - 3, cy - 3, cx - 7, cy - 3, cx - 7, cy + 9, cx + 7, cy + 9,
                                                cx + 7, cy - 3), stroke=c, sw=1.6)
    s.path("M%g %g L%g %g" % (cx + 3, cy - 3, cx + 7, cy - 3), stroke=c, sw=1.6)
    s.line(cx, cy + 3, cx, cy - 9, c, 1.6)
    s.poly([(cx - 3.5, cy - 5.5), (cx, cy - 9), (cx + 3.5, cy - 5.5)], stroke=c, sw=1.6, closed=False)


def icon_trash(s, cx, cy, c=IOS_RED):
    s.line(cx - 8, cy - 5, cx + 8, cy - 5, c, 1.6)
    s.path("M%g %g L%g %g L%g %g L%g %g" % (cx - 6, cy - 5, cx - 5, cy + 8, cx + 5, cy + 8, cx + 6, cy - 5),
           stroke=c, sw=1.6)
    s.path("M%g %g L%g %g L%g %g L%g %g" % (cx - 3, cy - 5, cx - 3, cy - 8, cx + 3, cy - 8, cx + 3, cy - 5),
           stroke=c, sw=1.6)


def icon_retake(s, cx, cy, c="#ffffff"):
    s.path("M%g %g A7 7 0 1 0 %g %g" % (cx + 7, cy, cx + 2, cy - 6.7), stroke=c, sw=1.8)
    s.poly([(cx + 1, cy - 11), (cx + 6, cy - 7), (cx + 1, cy - 3)], fill=c)


def icon_corners(s, cx, cy, c="#ffffff"):
    icon_scan(s, cx, cy, c)


def icon_eraser(s, cx, cy, c="#ffffff"):
    s.poly([(cx - 9, cy + 3), (cx - 1, cy - 7), (cx + 8, cy - 7), (cx, cy + 3)], stroke=c, sw=1.6)
    s.line(cx - 9, cy + 7, cx + 9, cy + 7, c, 1.6)


def switch(s, x, y, on=False):
    s.rect(x, y, 38, 22, fill=TEAL if on else "#dde1e4", rx=11)
    s.circle(x + (27 if on else 11), y + 11, 8, fill="#ffffff" if on else "#7b8287")


def chip(s, x, y, w, label):
    s.rect(x, y, w, 15, fill=TEAL_SOFT, rx=3)
    s.text(x + 3, y + 11, label, 9, 700, TEAL_INK)


def pill(s, x, y, w, label, icon):
    s.rect(x, y, w, 42, fill="#ffffff", rx=21)
    icon(s, x + 21, y + 21, INK)
    s.text(x + 38, y + 26.5, label, 15, 600)


def page_lines(s, x, y, w, rows, gap=20, c="#9aa5b1"):
    """Lines of handwriting on a page."""
    lengths = (1.0, 0.82, 0.93, 0.66, 0.88, 0.74, 0.95, 0.6, 0.85, 0.7, 0.9, 0.55)
    for i in range(rows):
        s.line(x, y + i * gap, x + w * lengths[i % len(lengths)], y + i * gap, c, 2.2)


# ---------- The phone ----------

KEYS = {
    # (side, top, height) of each key; the labels of a screenshot point at them.
    "android": {"volume up": ("right", 300, 36), "volume down": ("right", 340, 36), "power": ("right", 398, 34)},
    "iphone": {"action": ("left", 250, 24), "volume up": ("left", 300, 40), "volume down": ("left", 350, 40),
               "side": ("right", 312, 70)},
}


def status_bar(s, kind, dark):
    c = "#ffffff" if dark else INK
    if kind == "iphone":
        s.text(80, 52, "10:30", 14, 700, c, "middle")
        s.rect(136, 36, 68, 22, fill="#000000", rx=11)
    else:
        s.text(46, 51, "10:30", 13, 600, c)
        s.circle(170, 45, 6, fill="#000000")
    for i, h in enumerate((4, 6, 8, 10)):
        s.rect(243 + 4.2 * i, 51 - h, 2.8, h, fill=c, rx=0.8)
    s.path("M266 51 L259.5 43.5 A9 9 0 0 1 272.5 43.5 Z", fill=c)
    s.rect(277, 41.5, 21, 10.5, stroke=c, sw=1.2, rx=3)
    s.rect(279, 43.5, 15, 6.5, fill=c, rx=1.5)


def home_bar(s, kind, dark):
    c = "#ffffff" if dark else "#111111"
    if kind == "iphone":
        s.rect(120, 600, 100, 4.5, fill=c, rx=2.25)
    else:
        s.rect(130, 601, 80, 4, fill=c, rx=2, opacity=0.75)


def draw_phone(fn):
    kind, dark, keys = fn.kind, fn.dark, fn.keys
    screen, top = Svg(), Svg()
    fn(screen, top)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="%s">'
           % (W, H, W, H, FONT)]
    if getattr(fn, "cross_ok", False):
        out.append("<!-- cross-ok: a + button of the app -->")
    out.append('<rect width="%d" height="%d" rx="18" fill="%s"/>' % (W, H, BG))
    for name, (side, y, h) in KEYS[kind].items():
        x = BX + BW - 2 if side == "right" else BX - 4
        out.append('<rect x="%g" y="%g" width="6" height="%g" rx="2" fill="%s"/>'
                   % (x, y, h, MARK if name in keys else KEY))
    out.append('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s"/>' % (BX, BY, BW, BH, BR, BODY))
    out.append('<clipPath id="screen"><rect x="%g" y="%g" width="%g" height="%g" rx="%g"/></clipPath>'
               % (SX, SY, SW, SH, SR))
    out.append('<g clip-path="url(#screen)">')
    out.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>' % (SX, SY, SW, SH, DARK if dark else "#ffffff"))
    out.extend(screen.out)
    bars = Svg()
    status_bar(bars, kind, dark)
    home_bar(bars, kind, dark)
    out.extend(bars.out)
    out.append("</g>")
    out.extend(top.out)
    out.append("</svg>")
    return "\n".join(out) + "\n"


def screen(kind, dark=False, keys=(), cross_ok=False):
    def wrap(fn):
        fn.kind, fn.dark, fn.keys, fn.cross_ok = kind, dark, keys, cross_ok
        return fn
    return wrap


# =====================================================================
# Digital Skills, Online activity 2 (week-02): the model of Step 1 is
# Huda's study group (room 105, Sunday 22 November 2026, 2:00-3:00 PM,
# a reminder 1 hour before); the model of Step 2 is Omar's math homework 3
# (math-homework3.pdf). Never the data of the tasks.
# =====================================================================

@screen("android", cross_ok=True)
def calendar_android_1(s, top):
    """Google Calendar: tap + (Create) at the bottom right, then Event."""
    icon_menu(s, 49, 86)
    s.text(72, 93, "November", 19, 600)
    s.path("M174 84 L183 84 L178.5 90 Z", fill=INK)
    icon_search(s, 250, 86)
    s.rect(272, 76, 21, 21, stroke=INK, sw=1.8, rx=5)
    s.text(282.5, 90.5, "10", 10, 700, INK, "middle")
    x0, cw = 36, (304 - 36) / 7.0
    for i, d in enumerate("SMTWTFS"):
        s.text(x0 + cw * (i + 0.5), 127, d, 11, 600, GREY, "middle")
    y0, rh = 136, 56
    for r in range(6):
        s.line(x0, y0 + r * rh, 304, y0 + r * rh, LINE, 1)
    for c in range(1, 7):
        s.line(x0 + c * cw, y0, x0 + c * cw, y0 + 5 * rh, LINE, 1)
    day = 1
    for r in range(5):
        for c in range(7):
            cx, y = x0 + cw * (c + 0.5), y0 + r * rh
            label = str(day) if day <= 30 else str(day - 30)
            if day == 10:
                s.circle(cx, y + 13, 10.5, fill=TEAL)
                s.text(cx, y + 17.5, label, 12, 700, "#ffffff", "middle")
            else:
                s.text(cx, y + 17.5, label, 12, 500, INK if day <= 30 else LIGHT, "middle")
            day += 1
    chip(s, x0 + 4 * cw + 2, y0 + rh + 28, cw - 4, "Exam")
    chip(s, x0 + 3 * cw + 2, y0 + 2 * rh + 28, cw - 4, "Club")
    # The menu of + is open.
    s.rect(SX, SY, SW, SH, fill="#000000", opacity=0.32)
    pill(s, 200, 418, 96, "Task", icon_task)
    pill(s, 190, 470, 106, "Event", icon_cal)
    s.rect(240, 526, 56, 56, fill=TEAL_SOFT, rx=17)
    s.text(268, 566, "+", 38, 400, TEAL_INK, "middle")
    top.ring(235, 521, 66, 66, 20)
    top.mark(1, 222, 554)
    top.ring(185, 465, 116, 52, 26)
    top.mark(2, 172, 491)


@screen("android")
def calendar_android_2(s, top):
    """Google Calendar: the new event, with its title, date, time and notification."""
    icon_close(s, 51, 87)
    s.rect(232, 70, 66, 34, fill=TEAL, rx=17)
    s.text(265, 92, "Save", 15, 700, "#ffffff", "middle")
    s.text(72, 145, "Study group, room 105", 19, 500)
    s.line(SX, 166, SX + SW, 166, LINE, 1)
    icon_clock(s, 50, 192)
    s.text(72, 197, "All-day", 15)
    switch(s, 260, 181)
    s.text(72, 235, "Sun, 22 Nov 2026", 15)
    s.text(298, 235, "2:00 PM", 15, 400, INK, "end")
    s.text(72, 271, "Sun, 22 Nov 2026", 15)
    s.text(298, 271, "3:00 PM", 15, 400, INK, "end")
    icon_repeat(s, 50, 302)
    s.text(72, 307, "Does not repeat", 15)
    s.line(SX, 328, SX + SW, 328, LINE, 1)
    icon_people(s, 50, 352)
    s.text(72, 357, "Add people", 15, 400, GREY)
    icon_pin(s, 50, 390)
    s.text(72, 395, "Add location", 15, 400, GREY)
    s.line(SX, 414, SX + SW, 414, LINE, 1)
    icon_bell(s, 50, 440)
    s.text(72, 445, "1 hour before", 15, 600)
    s.text(72, 478, "Add another notification", 14, 400, GREY)
    s.line(SX, 498, SX + SW, 498, LINE, 1)
    s.circle(50, 522, 7, fill=TEAL)
    s.text(72, 527, "Default colour", 15)
    icon_lines(s, 50, 560)
    s.text(72, 565, "Add description", 15, 400, GREY)
    top.ring(64, 123, 238, 32, 9)
    top.mark(3, 47, 139)
    top.ring(64, 214, 240, 68, 10)
    top.mark(4, 47, 248)
    top.ring(64, 425, 132, 30, 9)
    top.mark(5, 210, 440)
    top.ring(228, 66, 74, 42, 21)
    top.mark(6, 213, 87)


@screen("android", keys=("volume down", "power"))
def calendar_android_3(s, top):
    """Google Calendar: the saved event; a screenshot with Power + Volume down."""
    icon_close(s, 51, 87)
    icon_pencil(s, 248, 87)
    icon_dots(s, 286, 87, INK, vertical=True, r=2, gap=6)
    s.rect(42, 126, 18, 18, fill=TEAL, rx=4)
    s.text(72, 142, "Study group,", 21, 500)
    s.text(72, 168, "room 105", 21, 500)
    s.text(72, 199, "Sunday, 22 November", 14, 400, GREY)
    s.text(72, 219, "2:00 - 3:00 PM", 14, 400, GREY)
    s.line(SX, 238, SX + SW, 238, LINE, 1)
    icon_bell(s, 50, 264)
    s.text(72, 269, "1 hour before", 15)
    icon_cal(s, 50, 302)
    s.text(72, 307, "Huda", 15)
    top.label(160, 345, 118, "Volume down", (316, 358))
    top.label(200, 402, 78, "Power", (316, 415))
    top.mark(7, 140, 392)
    top.text(170, 470, "Press both together.", 13, 700, MARK_INK, "middle")


@screen("iphone", cross_ok=True)
def calendar_iphone_1(s, top):
    """Calendar on an iPhone: tap + at the top right."""
    s.rect(36, 66, 112, 34, fill=IOS_FILL, rx=17)
    icon_chev(s, 52, 83, INK, True, 0.8)
    s.text(64, 89, "November", 16, 500)
    s.rect(192, 66, 112, 34, fill=IOS_FILL, rx=17)
    icon_list(s, 220, 83)
    icon_search(s, 252, 83)
    s.text(283, 93, "+", 28, 400, INK, "middle")
    x0, cw = 36, (304 - 36) / 7.0
    for i, (d, n) in enumerate(zip("SMTWTFS", range(8, 15))):
        cx = x0 + cw * (i + 0.5)
        s.text(cx, 145, d, 11, 600, INK if n < 13 else LIGHT, "middle")
        if n == 10:
            s.circle(cx, 166, 15, fill=IOS_RED)
            s.text(cx, 172, str(n), 17, 600, "#ffffff", "middle")
        else:
            s.text(cx, 172, str(n), 17, 400, INK if n < 13 else LIGHT, "middle")
    s.line(SX, 190, SX + SW, 190, LINE, 1)
    s.text(170, 211, "Tuesday - 10 Nov 2026", 13, 700, INK, "middle")
    s.line(SX, 222, SX + SW, 222, LINE, 1)
    for k, h in enumerate(("Noon", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM")):
        y = 250 + 44 * k
        s.text(68, y, h, 11, 600 if h == "Noon" else 400, GREY, "end")
        s.line(76, y - 4, SX + SW, y - 4, LINE, 1)
    s.rect(40, 552, 78, 36, fill=IOS_FILL, rx=18)
    s.text(79, 575, "Today", 15, 500, INK, "middle")
    s.rect(222, 552, 82, 36, fill=IOS_FILL, rx=18)
    icon_grid(s, 245, 570)
    icon_inbox(s, 281, 570)
    top.ring_circle(283, 83, 19)
    top.mark(1, 283, 117)


@screen("iphone")
def calendar_iphone_2(s, top):
    """Calendar on an iPhone: the new event (title, Starts, Ends, Alert)."""
    s.rect(SX, SY, SW, SH, fill="#c9c9ce")
    s.rect(SX, 58, SW, 560, fill=IOS_BG, rx=26)
    s.circle(56, 92, 17, fill="#ffffff")
    icon_close(s, 56, 92, INK, 5.5)
    s.text(170, 98, "New", 17, 700, INK, "middle")
    s.circle(284, 92, 17, fill=IOS_RED)
    icon_check(s, 284, 92, "#ffffff", 0.9, 2.6)
    s.rect(40, 118, 260, 30, fill="#e3e3e8", rx=15)
    s.rect(42, 120, 128, 26, fill="#ffffff", rx=13)
    s.text(106, 138, "Event", 13, 600, INK, "middle")
    s.text(235, 138, "Reminder", 13, 500, INK, "middle")
    s.rect(36, 160, 268, 76, fill="#ffffff", rx=14)
    s.text(52, 189, "Study group, room 105", 15)
    s.line(52, 198, 304, 198, LINE, 1)
    s.text(52, 224, "Location or Video Call", 15, 400, LIGHT)
    s.rect(36, 248, 268, 134, fill="#ffffff", rx=14)
    s.text(52, 275, "All-day", 15)
    s.rect(254, 262, 38, 22, fill="#e3e3e8", rx=11)
    s.circle(265, 273, 9, fill="#ffffff", stroke="#d0d0d5", sw=1)
    s.line(52, 291, 304, 291, LINE, 1)
    s.text(52, 318, "Starts", 15)
    s.rect(146, 300, 88, 28, fill="#efeff3", rx=14)
    s.text(190, 319, "22 Nov 2026", 13, 400, INK, "middle")
    s.rect(238, 300, 58, 28, fill="#efeff3", rx=14)
    s.text(267, 319, "2:00 PM", 13, 400, INK, "middle")
    s.line(52, 336, 304, 336, LINE, 1)
    s.text(52, 362, "Ends", 15)
    s.rect(146, 344, 88, 28, fill="#efeff3", rx=14)
    s.text(190, 363, "22 Nov 2026", 13, 400, INK, "middle")
    s.rect(238, 344, 58, 28, fill="#efeff3", rx=14)
    s.text(267, 363, "3:00 PM", 13, 400, INK, "middle")
    for y, left, right in ((394, "Repeat", "Never"), (446, "Alert", "1 hour before")):
        s.rect(36, y, 268, 42, fill="#ffffff", rx=14)
        s.text(52, y + 26, left, 15)
        s.text(282, y + 26, right, 15, 400, GREY, "end")
        icon_updown(s, 293, y + 21)
    s.rect(36, 498, 268, 42, fill="#ffffff", rx=14)
    s.text(52, 524, "Add attachment...", 15)
    s.rect(36, 552, 268, 70, fill="#ffffff", rx=14)
    s.text(52, 578, "URL", 15, 400, LIGHT)
    top.ring(42, 168, 256, 30, 9)
    top.mark(2, 34, 183)
    top.ring(141, 295, 160, 82, 12)
    top.mark(3, 126, 336)
    top.ring(40, 449, 260, 36, 13)
    top.mark(4, 34, 467)
    top.ring_circle(284, 92, 22)
    top.mark(5, 246, 92)


@screen("iphone", keys=("volume up", "side"))
def calendar_iphone_3(s, top):
    """Calendar on an iPhone: the saved event; a screenshot with the Side button + Volume up."""
    s.circle(54, 88, 17, fill=IOS_FILL)
    icon_chev(s, 53, 88, INK, True, 0.75)
    s.rect(248, 71, 56, 34, fill=IOS_FILL, rx=17)
    s.text(276, 93, "Edit", 15, 500, INK, "middle")
    s.text(40, 144, "Study group, room 105", 20, 700)
    s.text(40, 173, "Sunday 22 Nov 2026", 14, 400, GREY)
    s.text(40, 193, "from 2:00 PM to 3:00 PM", 14, 400, GREY)
    s.line(40, 212, 304, 212, LINE, 1)
    s.text(40, 238, "Calendar", 15)
    s.circle(222, 233, 4.5, fill="#339af0")
    s.text(300, 238, "Calendar", 15, 400, GREY, "end")
    s.line(40, 252, 304, 252, LINE, 1)
    s.text(40, 278, "Alert", 15)
    s.text(300, 278, "1 hour before", 15, 400, GREY, "end")
    s.line(40, 292, 304, 292, LINE, 1)
    s.text(170, 572, "Delete Event", 16, 500, IOS_RED, "middle")
    top.label(40, 307, 100, "Volume up", (24, 320))
    top.label(186, 334, 104, "Side button", (316, 347))
    top.mark(6, 170, 404)
    top.text(170, 440, "Press both together.", 13, 700, MARK_INK, "middle")


@screen("android", cross_ok=True)
def scan_android_1(s, top):
    """Google Drive: tap the camera at the bottom right."""
    s.rect(36, 66, 268, 42, fill="#eef1f3", rx=21)
    icon_menu(s, 56, 87, GREY)
    s.text(78, 92, "Search in Drive", 15, 400, GREY)
    s.circle(284, 87, 13, fill=TEAL)
    s.text(284, 92, "O", 13, 700, "#ffffff", "middle")
    s.text(42, 140, "Suggested", 15, 700)
    rows = (("doc", "Class report.docx", "You opened it today"),
            ("pdf", "Timetable.pdf", "You opened it yesterday"),
            ("folder", "Homework", "In My Drive"),
            ("image", "Notes photo.jpg", "You uploaded it"))
    for i, (kind, name, sub) in enumerate(rows):
        y = 156 + 54 * i
        if kind == "doc":
            icon_doc(s, 44, y + 6, "#1c7ed6", 18, 24)
        elif kind == "pdf":
            icon_doc(s, 44, y + 6, "#e03131", 18, 24, "PDF")
        elif kind == "folder":
            icon_folder(s, 41, y + 10, "#868e96")
        else:
            icon_image(s, 42, y + 9, "#2b8a3e")
        s.text(78, y + 20, name, 15, 500)
        s.text(78, y + 39, sub, 12.5, 400, GREY)
    s.rect(248, 420, 52, 52, fill=TEAL_SOFT, rx=16)
    icon_camera(s, 274, 447, TEAL_INK)
    s.rect(196, 482, 104, 54, fill=TEAL_SOFT, rx=17)
    s.text(224, 519, "+", 30, 400, TEAL_INK, "middle")
    s.text(264, 515, "New", 15, 700, TEAL_INK, "middle")
    s.line(SX, 548, SX + SW, 548, LINE, 1)
    for cx, name in ((66, "Home"), (134, "Starred"), (206, "Shared"), (274, "Files")):
        if name == "Home":
            s.rect(cx - 20, 556, 40, 22, fill=TEAL_SOFT, rx=11)
            icon_home(s, cx, 567, TEAL_INK, TEAL_INK)
        elif name == "Starred":
            icon_star(s, cx, 567)
        elif name == "Shared":
            icon_shared(s, cx, 567)
        else:
            icon_folder(s, cx - 10, 560, INK, 20, 15)
        s.text(cx, 593, name, 11, 600 if name == "Home" else 500, INK, "middle")
    top.ring(243, 415, 62, 62, 19)
    top.mark(1, 228, 446)


@screen("android", dark=True)
def scan_android_2(s, top):
    """Google Drive scanner: the page in the blue line, then Done."""
    icon_close(s, 51, 87, "#ffffff")
    icon_flash(s, 252, 87)
    s.text(290, 92, "Auto", 13, 700, "#ffffff", "end")
    s.rect(SX, 112, SW, 392, fill="#2b2e33")
    s.rect(70, 130, 200, 296, fill="#ffffff", rx=3)
    s.text(88, 162, "Math homework 3", 14, 700, "#343a40")
    s.text(88, 190, "1)  3 x 4 = 12", 13, 500, "#495057")
    s.text(88, 214, "2)  15 - 6 = 9", 13, 500, "#495057")
    s.text(88, 238, "3)  8 + 9 = 17", 13, 500, "#495057")
    page_lines(s, 88, 266, 160, 7, 22)
    s.rect(64, 124, 212, 308, stroke="#4dabf7", sw=3, rx=4)
    for cx, name, icon in ((62, "Retake", icon_retake), (132, "Crop & rotate", icon_corners),
                           (206, "Filter", icon_filters), (268, "Clean", icon_eraser)):
        icon(s, cx, 466)
        s.text(cx, 494, name, 11, 500, "#ffffff", "middle")
    s.rect(SX, 504, SW, 108, fill=DARK)
    s.rect(44, 530, 28, 38, fill="#ffffff", rx=3)
    page_lines(s, 49, 540, 18, 4, 7, "#adb5bd")
    s.rect(214, 528, 86, 42, fill="#c5f0f6", rx=21)
    s.text(257, 554, "Done", 16, 700, "#0b2f36", "middle")
    top.mark(2, 64, 124)
    top.ring(209, 523, 96, 52, 26)
    top.mark(3, 196, 549)


@screen("android")
def scan_android_3(s, top):
    """Google Drive scanner: the name, .pdf, Save."""
    icon_close(s, 51, 87)
    s.rect(128, 72, 84, 112, fill="#ffffff", stroke="#ced4da", sw=1.5, rx=2)
    s.text(136, 90, "Math homework 3", 6.5, 700, "#343a40")
    page_lines(s, 136, 102, 66, 8, 9, "#adb5bd")
    s.text(42, 220, "File name", 12.5, 600, GREY)
    s.rect(36, 228, 268, 46, stroke=TEAL, sw=2, rx=10)
    s.text(52, 257, "math-homework3", 16)
    s.text(42, 300, "Suggested titles", 12.5, 600, GREY)
    s.rect(36, 308, 128, 32, stroke="#ced4da", sw=1.5, rx=16)
    s.text(100, 329, "Math homework", 13, 500, INK, "middle")
    s.rect(170, 308, 108, 32, stroke="#ced4da", sw=1.5, rx=16)
    s.text(224, 329, "Homework 3", 13, 500, INK, "middle")
    s.text(42, 370, "File type", 12.5, 600, GREY)
    s.rect(36, 378, 88, 36, fill=TEAL_SOFT, stroke=TEAL, sw=1.5, rx=18)
    icon_check(s, 56, 396, TEAL_INK, 0.6, 2)
    s.text(90, 401, ".pdf", 15, 700, TEAL_INK, "middle")
    s.rect(150, 378, 80, 36, stroke="#ced4da", sw=1.5, rx=18)
    s.text(190, 401, ".jpg", 15, 500, INK, "middle")
    s.text(42, 446, "Location", 12.5, 600, GREY)
    icon_folder(s, 40, 460, "#868e96", 22, 16)
    s.text(72, 474, "My Drive", 15)
    icon_chev(s, 292, 469, GREY, False, 0.6)
    s.rect(212, 532, 88, 42, fill=TEAL, rx=21)
    s.text(256, 558, "Save", 15, 700, "#ffffff", "middle")
    top.ring(31, 223, 278, 56, 13)
    top.mark(4, 300, 223)
    top.ring(31, 373, 98, 46, 22)
    top.mark(5, 137, 396)
    top.ring(207, 527, 98, 52, 26)
    top.mark(6, 194, 553)


@screen("iphone")
def scan_iphone_1(s, top):
    """Files on an iPhone: tap the More button, then Scan Documents."""
    s.circle(284, 82, 19, fill=IOS_FILL)
    icon_dots(s, 284, 82, INK, r=2.3, gap=7)
    s.text(40, 132, "Recents", 30, 800)
    s.rect(36, 146, 268, 36, fill="#efeff2", rx=18)
    icon_search(s, 56, 164, GREY)
    s.text(72, 169, "Search", 15, 400, GREY)
    for i, (name, c, label) in enumerate((("Timetable", "#e03131", "PDF"), ("Report", "#1c7ed6", None),
                                          ("Photo", "#2b8a3e", "img"))):
        x = 52 + 88 * i
        if label == "img":
            icon_image(s, x, 222, c, 44, 36)
        else:
            icon_doc(s, x + 4, 206, c, 36, 48, label)
        s.text(x + 22, 280, name, 12, 500, INK, "middle")
    # The menu of the More button.
    s.rect(122, 108, 186, 214, fill="#000000", rx=18, opacity=0.06)
    s.rect(118, 104, 186, 214, fill="#fbfbfd", stroke="#e4e4e8", sw=1, rx=18)
    items = ((134, "Select", icon_task), (174, "Scan Documents", icon_scan), (214, "Connect to Server", icon_monitor))
    for y, name, icon in items:
        icon(s, 142, y, INK)
        s.text(160, y + 5, name, 14.5, 500 if name == "Scan Documents" else 400)
    s.line(130, 236, 292, 236, "#e4e4e8", 1)
    icon_check(s, 135, 262, INK, 0.6, 1.8)
    icon_squares(s, 152, 262)
    s.text(168, 267, "Icons", 14.5)
    icon_menu(s, 152, 300, INK)
    s.text(168, 305, "List", 14.5)
    s.rect(70, 546, 200, 52, fill="#f7f7f9", stroke="#e7e7eb", sw=1, rx=26)
    s.rect(76, 551, 66, 42, fill="#e9e9ee", rx=21)
    s.circle(109, 565, 8.5, fill=IOS_BLUE)
    s.line(109, 565, 109, 560, "#ffffff", 1.6)
    s.line(109, 565, 112.5, 565, "#ffffff", 1.6)
    s.text(109, 588, "Recents", 10.5, 600, IOS_BLUE, "middle")
    icon_folder(s, 160, 557, INK, 20, 15)
    s.text(170, 588, "Shared", 10.5, 500, INK, "middle")
    icon_folder(s, 222, 557, INK, 20, 15)
    s.text(232, 588, "Browse", 10.5, 500, INK, "middle")
    top.ring_circle(284, 82, 24)
    top.mark(1, 246, 74)
    top.ring(124, 156, 176, 36, 10)
    top.mark(2, 110, 174)


@screen("iphone", dark=True)
def scan_iphone_2(s, top):
    """The scanner on an iPhone: the page, then the Done button (a check mark)."""
    icon_close(s, 52, 86, "#ffffff", 6)
    icon_flash(s, 148, 86)
    icon_filters(s, 192, 86)
    s.text(292, 91, "Auto", 14, 700, "#ffffff", "end")
    s.rect(SX, 112, SW, 404, fill="#2b2e33")
    s.poly([(80, 160), (262, 150), (272, 452), (68, 462)], fill="#ffffff")
    s.text(96, 192, "Math homework 3", 14, 700, "#343a40")
    s.text(96, 220, "1)  3 x 4 = 12", 13, 500, "#495057")
    s.text(96, 244, "2)  15 - 6 = 9", 13, 500, "#495057")
    s.text(96, 268, "3)  8 + 9 = 17", 13, 500, "#495057")
    page_lines(s, 96, 296, 150, 7, 22)
    s.raw('<polygon points="80,160 262,150 272,452 68,462" fill="#4dabf7" opacity="0.22"/>')
    s.poly([(80, 160), (262, 150), (272, 452), (68, 462)], stroke="#4dabf7", sw=2.5)
    s.rect(44, 534, 30, 40, fill="#ffffff", rx=3)
    page_lines(s, 49, 544, 20, 4, 7, "#adb5bd")
    s.circle(170, 554, 30, stroke="#ffffff", sw=4)
    s.circle(170, 554, 24, fill="#ffffff")
    s.circle(278, 554, 22, fill="#f1f3f5")
    icon_check(s, 278, 554, INK, 1.0, 2.6)
    top.mark(3, 78, 152)
    top.ring_circle(278, 554, 27)
    top.mark(4, 238, 528)


@screen("iphone")
def scan_iphone_3(s, top):
    """Files on an iPhone: the scan in On My iPhone; touch and hold it, then Rename."""
    s.circle(54, 82, 17, fill=IOS_FILL)
    icon_chev(s, 53, 82, INK, True, 0.75)
    s.circle(284, 82, 17, fill=IOS_FILL)
    icon_dots(s, 284, 82, INK, r=2.2, gap=7)
    s.text(40, 132, "On My iPhone", 26, 800)
    for i, (name, c, label) in enumerate((("Scanned", "#e03131", "PDF"), ("Timetable", "#e03131", "PDF"),
                                          ("Report", "#1c7ed6", None))):
        x = 52 + 88 * i
        icon_doc(s, x + 4, 158, c, 36, 48, label)
        s.text(x + 22, 226, name, 12, 500, INK, "middle")
        if i == 0:
            s.text(x + 22, 241, "Document", 12, 500, INK, "middle")
    s.rect(SX, SY, SW, SH, fill="#000000", opacity=0.18)
    # Touch and hold: the file comes up, and its menu opens.
    s.rect(42, 148, 104, 108, fill="#ffffff", rx=16)
    icon_doc(s, 76, 160, "#e03131", 36, 48, "PDF")
    s.text(94, 228, "Scanned", 12, 600, INK, "middle")
    s.text(94, 243, "Document", 12, 600, INK, "middle")
    s.rect(42, 266, 220, 280, fill="#fbfbfd", rx=16)
    items = (("Get Info", icon_info, INK), ("Rename", icon_pencil, INK), ("Compress", icon_box, INK),
             ("Duplicate", icon_copy, INK), ("Share", icon_share, INK), ("Delete", icon_trash, IOS_RED))
    for i, (name, icon, c) in enumerate(items):
        y = 266 + 46.5 * i
        if i:
            s.line(54, y, 250, y, "#e4e4e8", 1)
        s.text(58, y + 29, name, 15, 600 if name == "Rename" else 400, c)
        icon(s, 236, y + 23, c)
    top.mark(5, 238, 120)
    top.ring(46, 316, 212, 40, 10)
    top.mark(6, 36, 336)


# =====================================================================
# Computer windows (Word, Excel, a browser): the same marks, a window frame
# instead of a phone. Digital Skills, Online activity 3 (week-03): the
# models are Omar's club notice (club-notice.docx), Lina's table (A1:B3)
# and Sami's notes shared with his teacher. Never the data of the tasks.
# =====================================================================

WW, WH = 560, 360                           # the picture of a window
WORD = "#185abd"; EXCEL = "#107c41"; WEB = "#f3f3f3"


def draw_window(fn):
    s, top = Svg(), Svg()
    fn(s, top)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="%s">'
           % (WW, WH, WW, WH, FONT),
           '<rect width="%d" height="%d" rx="18" fill="%s"/>' % (WW, WH, BG),
           '<rect x="14" y="14" width="%d" height="%d" rx="10" fill="#ffffff" stroke="#c9cdd2" stroke-width="1.5"/>'
           % (WW - 28, WH - 28)]
    out.extend(s.out)
    out.extend(top.out)
    out.append("</svg>")
    return "\n".join(out) + "\n"


def window(kind):
    def wrap(fn):
        fn.window = kind
        return fn
    return wrap


def office_bar(s, app, color, name, tabs=("File", "Home", "Insert", "Layout", "Review", "View"), active="Home"):
    """The title bar, the tabs and a short ribbon of a desktop Office app."""
    s.rect(15, 15, WW - 30, 34, fill=color, rx=9)
    s.rect(15, 35, WW - 30, 14, fill=color)
    s.text(30, 37, app, 13, 700, "#ffffff")
    s.text(WW / 2, 37, name, 13, 400, "#ffffff", "middle")
    x = 28
    for tab in tabs:
        s.text(x, 70, tab, 12.5, 600 if tab == active else 400, INK)
        if tab == active:
            s.line(x, 76, x + 34, 76, color, 2.5)
        x += 14 + 8 * len(tab)
    s.rect(15, 82, WW - 30, 40, fill="#f5f6f7")
    for i in range(7):
        s.rect(30 + 40 * i, 90, 26, 24, fill="#e3e6ea", rx=4)
    s.line(15, 122, WW - 15, 122, LINE, 1)


def word_page(s, x=150, y=134, w=260, h=200, rows=5):
    s.rect(x, y, w, h, fill="#ffffff", stroke="#d0d4d9", sw=1)
    page_lines(s, x + 24, y + 30, w - 48, rows)


@window("computer")
def pdf_win_1(s, top):
    """Word for Windows: click File."""
    office_bar(s, "Word", WORD, "club-notice.docx")
    s.rect(15, 123, WW - 30, 222, fill="#eef0f2")
    word_page(s)
    top.ring(20, 56, 40, 22, 6)
    top.mark(1, 40, 98)


@window("computer")
def pdf_win_2(s, top):
    """Word for Windows: Save As, the type PDF (*.pdf), Save."""
    s.rect(15, 15, 150, WH - 30, fill=WORD, rx=9)
    s.rect(150, 15, 15, WH - 30, fill=WORD)
    for i, item in enumerate(["Home", "New", "Open", "Save", "Save As", "Print", "Share", "Export"]):
        y = 50 + 34 * i
        if item == "Save As":
            s.rect(15, y - 20, 150, 30, fill="#0f4a99")
        s.text(36, y, item, 13, 700 if item == "Save As" else 400, "#ffffff")
    s.text(190, 54, "Save As", 22, 300, INK)
    s.text(190, 92, "Documents", 13, 600, GREY)
    s.rect(190, 104, 340, 30, fill="#ffffff", stroke="#8a9096", sw=1.2, rx=3)
    s.text(200, 124, "club-notice", 13.5, 400, INK)
    s.rect(190, 144, 340, 30, fill="#ffffff", stroke="#8a9096", sw=1.2, rx=3)
    s.text(200, 164, "Word Document (*.docx)", 13.5, 400, INK)
    s.path("M512 156 L520 156 L516 162 Z", fill=INK)
    s.rect(190, 176, 340, 92, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=3)
    for i, ty in enumerate(["Word Document (*.docx)", "PDF (*.pdf)", "Plain Text (*.txt)"]):
        y = 200 + 28 * i
        if i == 1:
            s.rect(192, y - 19, 336, 26, fill="#e8f0fb")
        s.text(204, y, ty, 13.5, 600 if i == 1 else 400, INK)
    s.rect(440, 288, 90, 32, fill=WORD, rx=4)
    s.text(485, 309, "Save", 14, 700, "#ffffff", "middle")
    top.ring(190, 208, 340, 28, 6)
    top.mark(2, 175, 222)
    top.ring(436, 284, 98, 40, 8)
    top.mark(3, 422, 304)


@window("browser")
def pdf_web_1(s, top):
    """Word on the web (office.com): File, Export, Download as PDF."""
    s.rect(15, 15, WW - 30, 30, fill=WEB, rx=9)
    s.rect(70, 21, 300, 18, fill="#ffffff", rx=9)
    s.text(82, 34, "office.com", 11.5, 400, GREY)
    s.rect(15, 45, WW - 30, 28, fill=WORD)
    s.text(30, 64, "Word", 13, 700, "#ffffff")
    s.text(WW / 2, 64, "club-notice", 12.5, 400, "#ffffff", "middle")
    x = 28
    for tab in ("File", "Home", "Insert", "Layout", "Review", "View"):
        s.text(x, 92, tab, 12.5, 400, INK)
        x += 14 + 8 * len(tab)
    s.rect(15, 100, WW - 30, 245, fill="#eef0f2")
    word_page(s, 260, 112, 240, 220)
    s.rect(24, 102, 190, 170, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=6)
    for i, item in enumerate(["New", "Open", "Save a copy", "Export", "Print", "Share"]):
        y = 124 + 26 * i
        if item == "Export":
            s.rect(26, y - 17, 186, 24, fill="#e8f0fb")
        s.text(40, y, item, 13, 600 if item == "Export" else 400, INK)
    s.rect(214, 180, 200, 34, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=6)
    s.text(228, 202, "Download as PDF", 13, 600, INK)
    top.ring(20, 78, 40, 22, 6)
    top.mark(1, 12, 89)
    top.ring(26, 183, 186, 26, 6)
    top.mark(2, 180, 165)
    top.ring(214, 180, 200, 34, 8)
    top.mark(3, 428, 197)


def grid_cells(s, x0, y0, cols, rows, cw=90, rh=26, data=None, sel=None):
    for c in range(cols):
        s.rect(x0 + 30 + c * cw, y0, cw, 20, fill="#f0f1f3", stroke=LINE, sw=1)
        s.text(x0 + 30 + c * cw + cw / 2, y0 + 15, "ABCDE"[c], 11.5, 600, GREY, "middle")
    for r in range(rows):
        y = y0 + 20 + r * rh
        s.rect(x0, y, 30, rh, fill="#f0f1f3", stroke=LINE, sw=1)
        s.text(x0 + 15, y + 17, str(r + 1), 11.5, 600, GREY, "middle")
        for c in range(cols):
            s.rect(x0 + 30 + c * cw, y, cw, rh, fill="#ffffff", stroke=LINE, sw=1)
            if data and r < len(data) and c < len(data[r]):
                s.text(x0 + 38 + c * cw, y + 18, data[r][c], 12.5, 700 if r == 0 else 400, INK)
    if sel:
        c1, r1, c2, r2 = sel
        s.rect(x0 + 30 + c1 * cw, y0 + 20 + r1 * rh, (c2 - c1 + 1) * cw, (r2 - r1 + 1) * rh,
               fill=EXCEL, stroke=EXCEL, sw=2.5, opacity=0.12)
        s.rect(x0 + 30 + c1 * cw, y0 + 20 + r1 * rh, (c2 - c1 + 1) * cw, (r2 - r1 + 1) * rh, stroke=EXCEL, sw=2.5)


LINA = [["Item", "Hours"], ["Reading", "4"], ["Exercises", "3"]]


@window("computer")
def paste_win_1(s, top):
    """Excel for Windows: select A1:B3 and press Ctrl + C."""
    office_bar(s, "Excel", EXCEL, "study-hours.xlsx", ("File", "Home", "Insert", "Formulas", "Data", "View"))
    grid_cells(s, 30, 140, 5, 6, cw=92, data=LINA, sel=(0, 0, 1, 2))
    top.mark(1, 252, 170)
    top.label(330, 196, 110, "Ctrl + C", arrow_to=(250, 215))


@window("computer")
def paste_win_2(s, top):
    """Word for Windows: Ctrl + V, the Paste Options button, Use Destination Styles."""
    office_bar(s, "Word", WORD, "study-report.docx")
    s.rect(15, 123, WW - 30, 222, fill="#eef0f2")
    s.rect(70, 130, 300, 210, fill="#ffffff", stroke="#d0d4d9", sw=1)
    s.text(90, 158, "My study week", 15, 700, INK)
    for r, row in enumerate(LINA):
        for c, v in enumerate(row):
            s.rect(90 + c * 110, 172 + r * 26, 110, 26, stroke="#9aa5b1", sw=1)
            s.text(98 + c * 110, 190 + r * 26, v, 12.5, 700 if r == 0 else 400, INK)
    s.rect(300, 252, 34, 22, fill="#ffffff", stroke="#8a9096", sw=1.2, rx=3)
    s.text(317, 268, "Ctrl", 10.5, 700, INK, "middle")
    s.rect(330, 278, 200, 64, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=6)
    s.text(340, 296, "Paste Options:", 12, 600, GREY)
    for i in range(6):
        s.rect(340 + 30 * i, 304, 24, 24, fill="#e3e6ea" if i != 1 else "#e8f0fb", rx=3)
    s.rect(400, 250, 150, 24, fill="#323130", rx=4)
    s.text(475, 266, "Use Destination Styles", 11, 600, "#ffffff", "middle")
    top.label(392, 140, 110, "Ctrl + V", arrow_to=(372, 160))
    top.mark(2, 286, 263)
    top.ring(368, 302, 28, 28, 5)
    top.mark(3, 382, 344)


@window("computer")
def share_win_1(s, top):
    """Word for Windows: Share at the top right, above the ribbon."""
    office_bar(s, "Word", WORD, "sami-notes.docx")
    s.rect(452, 54, 80, 24, fill=WORD, rx=5)
    s.text(492, 71, "Share", 12.5, 700, "#ffffff", "middle")
    s.rect(15, 123, WW - 30, 222, fill="#eef0f2")
    word_page(s)
    top.ring(448, 50, 88, 32, 8)
    top.mark(1, 434, 66)


@window("computer")
def share_win_2(s, top):
    """The Share dialog: the name, the link settings (Specific people), Can view, Send."""
    s.rect(15, 15, WW - 30, WH - 30, fill="#eef0f2", rx=9)
    s.rect(90, 30, 380, 300, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=10)
    s.text(110, 60, "Share “sami-notes”", 16, 700, INK)
    s.rect(110, 78, 250, 32, fill="#ffffff", stroke="#8a9096", sw=1.2, rx=4)
    s.text(120, 99, "Ms Rana Khalil", 13.5, 400, INK)
    s.rect(368, 78, 86, 32, fill="#ffffff", stroke="#8a9096", sw=1.2, rx=4)
    s.text(380, 99, "Can view", 13, 600, INK)
    s.path("M440 92 L448 92 L444 98 Z", fill=INK)
    s.text(110, 140, "Link settings", 13, 600, GREY)
    for i, who in enumerate(["Anyone", "People in your organization", "Specific people"]):
        y = 166 + 28 * i
        s.circle(122, y - 4, 7, stroke=GREY, sw=1.5, fill="#ffffff")
        if who == "Specific people":
            s.circle(122, y - 4, 3.5, fill=WORD)
        s.text(138, y, who, 13, 600 if who == "Specific people" else 400, INK)
    s.rect(370, 282, 84, 32, fill=WORD, rx=4)
    s.text(412, 303, "Send", 14, 700, "#ffffff", "middle")
    top.mark(2, 100, 94)
    top.ring(112, 205, 160, 26, 6)
    top.mark(3, 290, 218)
    top.ring(364, 74, 94, 40, 8)
    top.mark(4, 472, 94)
    top.ring(366, 278, 92, 40, 8)
    top.mark(5, 472, 298)


# =====================================================================
# Digital Skills, Online activity 3 (week-03, syllabus v3): safe devices
# and accounts. The models: Lina signs in to her university account on a
# lab computer (the number 47); a fake parcel message on Omar's phone
# (parcel-jo-pay.info) and a fake e-mail reported in Outlook; Sami's photo
# app PhotoFix, whose location permission he turns off. Never the data of
# the tasks (the mailbox e-mail of Task 2, the Camera app of Task 3).
# =====================================================================

def browser_bar(s, address):
    s.rect(15, 15, WW - 30, 30, fill=WEB, rx=9)
    s.rect(70, 21, 300, 18, fill="#ffffff", rx=9)
    s.text(82, 34, address, 11.5, 400, GREY)


@window("browser")
def twostep_win_1(s, top):
    """The sign-in page of the university account asks to approve the sign-in with a number."""
    browser_bar(s, "login.microsoftonline.com")
    s.rect(15, 45, WW - 30, WH - 60, fill="#f2f3f5")
    s.rect(140, 62, 280, 270, fill="#ffffff", stroke="#d0d4d9", sw=1, rx=6)
    s.text(164, 92, "lina@university", 12.5, 400, GREY)
    s.text(164, 122, "Approve sign in request", 18, 700, INK)
    s.text(164, 150, "Open your Authenticator app, and", 12.5, 400, INK)
    s.text(164, 168, "enter the number shown to sign in.", 12.5, 400, INK)
    s.text(280, 236, "47", 46, 700, INK, "middle")
    s.text(164, 300, "No numbers in your app? Make sure to", 11, 400, GREY)
    s.text(164, 316, "upgrade to the latest version.", 11, 400, GREY)
    top.ring(240, 192, 80, 56, 10)
    top.mark(1, 226, 196)


@screen("android")
def twostep_phone_1(s, top):
    """The authenticator app asks: Are you trying to sign in? Type the number, then Yes."""
    s.rect(28, 28, 284, 584, fill="#3d434a")
    s.rect(44, 150, 252, 300, fill="#ffffff", rx=18)
    s.text(170, 186, "Are you trying to sign in?", 16, 700, INK, "middle")
    s.text(170, 212, "University", 13, 600, GREY, "middle")
    s.text(170, 230, "lina@university", 13, 400, GREY, "middle")
    s.text(170, 262, "Enter the number shown to sign in.", 12.5, 400, INK, "middle")
    s.rect(110, 276, 120, 44, fill="#ffffff", stroke=INK, sw=1.5, rx=6)
    s.text(170, 306, "47", 22, 700, INK, "middle")
    s.line(44, 352, 296, 352, LINE, 1)
    s.line(170, 352, 170, 450, LINE, 1)
    s.text(107, 398, "No, it's not me", 13.5, 600, TEAL, "middle")
    s.text(233, 398, "Yes", 15, 700, TEAL, "middle")
    top.ring(104, 270, 132, 56, 10)
    top.mark(2, 88, 300)
    top.ring(184, 368, 98, 50, 10)
    top.mark(3, 284, 360)


@screen("android")
def link_phone_1(s, top):
    """Messages: touch and hold the link; the menu shows its real address."""
    icon_chev(s, 46, 86, INK)
    s.text(70, 92, "+962 7 9000 0000", 16, 600)
    s.rect(44, 130, 236, 120, fill="#eceff1", rx=18)
    s.text(58, 156, "Your parcel is waiting.", 14, 400)
    s.text(58, 176, "Pay 0.50 JD in 24 hours, or", 14, 400)
    s.text(58, 196, "it goes back:", 14, 400)
    s.text(58, 220, "parcel-jo-pay.info/track", 14, 600, "#1c7ed6")
    s.rect(28, 260, 284, 352, fill="#000000", opacity=0.25)
    s.rect(52, 300, 236, 160, fill="#ffffff", rx=14)
    s.text(68, 330, "http://parcel-jo-pay.info/track", 12.5, 700, INK)
    for i, t in enumerate(["Open", "Copy link", "Share"]):
        s.text(68, 372 + 34 * i, t, 14.5, 400, INK)
    top.ring(52, 202, 200, 28, 8)
    top.mark(1, 40, 216)
    top.ring(58, 312, 226, 28, 8)
    top.mark(2, 296, 300)


@window("browser")
def report_win_1(s, top):
    """Outlook on the web: an e-mail is open; Report, then Report phishing."""
    browser_bar(s, "outlook.office.com")
    s.rect(15, 45, WW - 30, 34, fill="#f5f6f7")
    for i, t in enumerate(["Delete", "Archive", "Report", "Move to"]):
        s.text(34 + 86 * i, 67, t, 12.5, 600 if t == "Report" else 400, INK)
    s.text(40, 112, "Sunrise Bank <service@sunrise-bank-help.co>", 12.5, 700, INK)
    s.text(40, 134, "Your card is blocked. Sign in now to open it.", 12.5, 400, INK)
    page_lines(s, 40, 168, 300, 4)
    s.rect(196, 80, 170, 78, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=6)
    s.text(212, 108, "Report phishing", 13, 600, INK)
    s.text(212, 140, "Report junk", 13, 400, INK)
    top.ring(198, 50, 70, 26, 6)
    top.mark(1, 188, 52)
    top.ring(202, 90, 158, 28, 6)
    top.mark(2, 376, 104)


def settings_row(s, y, text, value=None, bold=False, chev=True):
    s.text(48, y, text, 15, 600 if bold else 400, INK)
    if value:
        s.text(268 if chev else 290, y, value, 13.5, 400, GREY, "end")
    if chev:
        icon_chev(s, 286, y - 5, LIGHT, left=False, k=0.7)
    s.line(48, y + 16, 300, y + 16, LINE, 1)


@screen("android")
def perm_android_1(s, top):
    """Settings › Apps › PhotoFix: App info, then Permissions."""
    icon_chev(s, 46, 86, INK)
    s.text(70, 92, "App info", 19, 600)
    s.rect(140, 118, 60, 60, fill="#f59f00", rx=16)
    s.circle(170, 148, 14, fill="#ffffff")
    s.circle(170, 148, 7, fill="#f59f00")
    s.text(170, 202, "PhotoFix", 18, 600, INK, "middle")
    s.text(170, 222, "Installed", 12.5, 400, GREY, "middle")
    for i, (t, v) in enumerate([("Notifications", "Allowed"), ("Permissions", "Camera, Location and Photos"),
                                ("Storage", "120 MB"), ("Mobile data", None)]):
        y = 270 + 56 * i
        s.text(48, y, t, 15.5, 500, INK)
        if v:
            s.text(48, y + 20, v, 12.5, 400, GREY)
    top.ring(36, 306, 268, 50, 10)
    top.mark(1, 300, 312)


@screen("android")
def perm_android_2(s, top):
    """Location permission of PhotoFix: Don't allow."""
    icon_chev(s, 46, 86, INK)
    s.text(70, 92, "Location permission", 18, 600)
    s.text(48, 134, "PhotoFix", 13, 600, GREY)
    opts = ["Allow all the time", "Allow only while using the app", "Ask every time", "Don't allow"]
    for i, t in enumerate(opts):
        y = 182 + 52 * i
        s.circle(58, y - 5, 10, stroke=GREY, sw=2, fill="#ffffff")
        if t == "Don't allow":
            s.circle(58, y - 5, 10, stroke=TEAL, sw=2, fill="#ffffff")
            s.circle(58, y - 5, 5, fill=TEAL)
        s.text(80, y, t, 14.5, 400, INK)
    s.text(48, 420, "A photo app does not need", 12.5, 400, GREY)
    s.text(48, 438, "your location to edit photos.", 12.5, 400, GREY)
    top.ring(40, 320, 260, 40, 10)
    top.mark(2, 296, 326)


@screen("iphone")
def perm_iphone_1(s, top):
    """Settings › Privacy & Security › Location Services: the list of apps."""
    s.rect(28, 28, 284, 584, fill=IOS_BG)
    icon_chev(s, 46, 86, IOS_BLUE)
    s.text(60, 92, "Privacy & Security", 15, 400, IOS_BLUE)
    s.text(40, 136, "Location Services", 26, 800)
    s.rect(36, 152, 268, 44, fill="#ffffff", rx=12)
    s.text(50, 180, "Location Services", 14.5, 400, INK)
    s.rect(252, 163, 40, 24, fill="#34c759", rx=12)
    s.circle(280, 175, 10, fill="#ffffff")
    s.rect(36, 214, 268, 176, fill="#ffffff", rx=12)
    for i, (app, v) in enumerate([("Camera", "While Using"), ("Maps", "While Using"), ("PhotoFix", "Always"), ("Weather", "Never")]):
        y = 244 + 44 * i
        s.text(52, y, app, 14.5, 400, INK)
        s.text(270, y, v, 13, 400, GREY, "end")
        icon_chev(s, 286, y - 5, LIGHT, left=False, k=0.6)
        if i < 3:
            s.line(52, y + 16, 304, y + 16, LINE, 1)
    top.ring(40, 314, 262, 38, 10)
    top.mark(1, 300, 312)


@screen("iphone")
def perm_iphone_2(s, top):
    """PhotoFix: Allow location access: Never."""
    s.rect(28, 28, 284, 584, fill=IOS_BG)
    icon_chev(s, 46, 86, IOS_BLUE)
    s.text(60, 92, "Location Services", 15, 400, IOS_BLUE)
    s.text(40, 136, "PhotoFix", 26, 800)
    s.text(48, 172, "ALLOW LOCATION ACCESS", 11.5, 500, GREY)
    s.rect(36, 182, 268, 176, fill="#ffffff", rx=12)
    for i, t in enumerate(["Never", "Ask Next Time Or When I Share", "While Using the App", "Always"]):
        y = 212 + 44 * i
        s.text(52, y, t, 14, 400, INK)
        if t == "Never":
            icon_check(s, 284, y - 5, IOS_BLUE, 0.8, 2.2)
        if i < 3:
            s.line(52, y + 16, 304, y + 16, LINE, 1)
    s.text(48, 390, "A photo app does not need your", 12.5, 400, GREY)
    s.text(48, 408, "location to edit photos.", 12.5, 400, GREY)
    top.ring(40, 188, 262, 38, 10)
    top.mark(2, 300, 186)


# =====================================================================
# Digital Skills, Online activity 4 (week-04, syllabus v3): PowerPoint.
# The model is Omar's short talk "Saving Water at Home" (three slides);
# never the data of the task (the college library).
# =====================================================================

PPT = "#c43e1c"


def ppt_frame(s, tab, name="saving-water.pptx"):
    office_bar(s, "PowerPoint", PPT, name, tabs=("File", "Home", "Insert", "Design", "Transitions", "View"), active=tab)
    s.rect(15, 123, WW - 30, 222, fill="#eef0f2")
    for i in range(3):
        s.rect(26, 134 + 62 * i, 84, 50, fill="#ffffff", stroke=PPT if i == 1 else "#c9cdd2", sw=1.5 if i == 1 else 1)
        s.text(20, 150 + 62 * i, str(i + 1), 10, 400, GREY)
    s.rect(130, 134, 400, 200, fill="#ffffff", stroke="#d0d4d9", sw=1)


@window("computer")
def ppt_newslide_1(s, top):
    """PowerPoint: Home › New Slide, then a layout (Title and Content)."""
    ppt_frame(s, "Home")
    s.rect(30, 86, 74, 32, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    s.text(67, 107, "New Slide", 11.5, 600, INK, "middle")
    s.rect(30, 124, 330, 200, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=6)
    for i, name in enumerate(["Title Slide", "Title and Content", "Two Content", "Blank"]):
        x = 44 + (i % 2) * 156
        y = 138 + (i // 2) * 92
        s.rect(x, y, 140, 62, fill="#ffffff", stroke=PPT if i == 1 else "#c9cdd2", sw=2 if i == 1 else 1)
        if i == 0:
            s.rect(x + 20, y + 18, 100, 12, fill="#e3e6ea"); s.rect(x + 40, y + 36, 60, 8, fill="#eef0f2")
        elif i == 1:
            s.rect(x + 10, y + 8, 120, 10, fill="#e3e6ea"); page_lines(s, x + 14, y + 30, 100, 3, gap=10)
        elif i == 2:
            s.rect(x + 10, y + 8, 120, 10, fill="#e3e6ea"); page_lines(s, x + 12, y + 30, 50, 3, gap=10)
            s.rect(x + 74, y + 26, 54, 28, fill="#eef0f2")
        s.text(x + 70, y + 78, name, 11, 600 if i == 1 else 400, INK, "middle")
    top.ring(26, 82, 82, 40, 6)
    top.mark(1, 120, 100)
    top.ring(196, 134, 148, 70, 8)
    top.mark(2, 352, 146)


@window("computer")
def ppt_design_1(s, top):
    """PowerPoint: the Design tab, then a theme."""
    ppt_frame(s, "Design")
    s.rect(15, 82, WW - 30, 40, fill="#f5f6f7")
    colors = [("#ffffff", "#2a2f2c"), ("#1d3557", "#ffffff"), ("#e9f5db", "#2b6a4f"), ("#fff4e6", "#d9480f"), ("#f1f3f5", "#495057")]
    for i, (bg, fg) in enumerate(colors):
        x = 30 + 62 * i
        s.rect(x, 86, 54, 32, fill=bg, stroke="#c9cdd2", sw=1, rx=3)
        s.text(x + 27, 107, "Aa", 13, 700, fg, "middle")
    s.text(372, 106, "Variants", 12, 400, GREY)
    s.rect(130, 134, 400, 200, fill="#e9f5db", stroke="#d0d4d9", sw=1)
    s.text(330, 220, "Saving Water at Home", 20, 700, "#2b6a4f", "middle")
    s.text(330, 250, "A short talk for the Sunrise staff", 12.5, 400, "#2b6a4f", "middle")
    top.ring(192, 54, 60, 26, 6)
    top.mark(1, 264, 66)
    top.ring(150, 82, 62, 40, 6)
    top.mark(2, 222, 132)


@window("computer")
def ppt_picture_1(s, top):
    """PowerPoint: Insert › Pictures › Stock Images."""
    ppt_frame(s, "Insert")
    s.rect(30, 86, 74, 32, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    s.text(67, 107, "Pictures", 11.5, 600, INK, "middle")
    s.rect(30, 124, 190, 112, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=6)
    for i, t in enumerate(["This Device...", "Stock Images...", "Online Pictures..."]):
        y = 152 + 32 * i
        if i == 1:
            s.rect(32, y - 20, 186, 28, fill="#fdecea")
        s.text(46, y, t, 12.5, 600 if i == 1 else 400, INK)
    top.ring(130, 54, 54, 26, 6)
    top.mark(1, 196, 66)
    top.ring(26, 82, 82, 40, 6)
    top.mark(2, 18, 102)
    top.ring(34, 162, 182, 30, 6)
    top.mark(3, 230, 178)


# =====================================================================
# Digital Skills, Online activity 6 (week-07, syllabus v3): a PivotTable.
# The model is Rana's March (Paper 206, Drinks 71, Bags 78 JD); never the
# data of the task (the training hours).
# =====================================================================

def excel_grid(s, rows, x=30, y=134, cw=(70, 70, 60, 70)):
    for r, row in enumerate(rows):
        cx = x
        for c, v in enumerate(row):
            s.rect(cx, y + 22 * r, cw[c], 22, fill="#ffffff" if r else "#f1f3f5", stroke="#d0d4d9", sw=0.8)
            s.text(cx + 5, y + 22 * r + 15, str(v), 11, 600 if r == 0 else 400, INK)
            cx += cw[c]


@window("computer")
def pivot_win_1(s, top):
    """Excel: click in the data, Insert › PivotTable, then OK."""
    office_bar(s, "Excel", EXCEL, "march.xlsx", tabs=("File", "Home", "Insert", "Data", "View"), active="Insert")
    s.rect(30, 86, 74, 32, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    s.text(67, 107, "PivotTable", 11.5, 600, INK, "middle")
    excel_grid(s, [["Week", "Item", "Type", "Total"], [1, "Coffee", "Drinks", 6], [1, "Pen", "Paper", 8],
                   [1, "Juice", "Drinks", 2], [1, "Notebook", "Paper", 60], [2, "Bag", "Bags", 12]])
    s.rect(320, 150, 210, 150, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=6)
    s.text(334, 176, "Create PivotTable", 13.5, 700, INK)
    s.text(334, 202, "Table/Range: March!A1:E25", 11.5, 400, GREY)
    s.text(334, 228, "New Worksheet", 11.5, 400, INK)
    s.rect(440, 262, 76, 26, fill=EXCEL, rx=4)
    s.text(478, 280, "OK", 13, 700, "#ffffff", "middle")
    top.ring(116, 54, 54, 26, 6)
    top.mark(1, 182, 66)
    top.ring(26, 82, 82, 40, 6)
    top.mark(2, 18, 102)
    top.ring(436, 258, 84, 34, 6)
    top.mark(3, 422, 296)


@window("computer")
def pivot_win_2(s, top):
    """The PivotTable Fields: Type to Rows, Total to Values; the result."""
    s.rect(15, 15, WW - 30, WH - 30, fill="#ffffff", rx=9)
    excel_grid(s, [["Row Labels", "Sum of Total"], ["Bags", 78], ["Drinks", 71], ["Paper", 206], ["Grand Total", 355]],
               x=30, y=40, cw=(100, 100))
    s.rect(330, 26, 200, 310, fill="#f8f9fa", stroke="#c9cdd2", sw=1, rx=6)
    s.text(344, 50, "PivotTable Fields", 13, 700, INK)
    for i, f in enumerate(["Week", "Item", "Type", "Total"]):
        y = 76 + 24 * i
        s.rect(344, y - 12, 12, 12, fill="#ffffff", stroke=GREY, sw=1, rx=2)
        if f in ("Type", "Total"):
            icon_check(s, 350, y - 6, EXCEL, 0.5, 1.8)
        s.text(364, y, f, 12, 400, INK)
    s.text(344, 196, "Rows", 11.5, 600, GREY)
    s.rect(344, 204, 172, 26, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=3)
    s.text(352, 222, "Type", 12, 600, INK)
    s.text(344, 258, "Values", 11.5, 600, GREY)
    s.rect(344, 266, 172, 26, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=3)
    s.text(352, 284, "Sum of Total", 12, 600, INK)
    top.ring(340, 200, 180, 34, 6)
    top.mark(4, 330, 196)
    top.ring(340, 262, 180, 34, 6)
    top.mark(5, 330, 258)
    top.ring(26, 124, 204, 26, 6)
    top.mark(6, 244, 138)


@window("computer")
def pivot_chart_1(s, top):
    """Excel: click the PivotTable, Insert › Column chart; the chart of Rana's month."""
    office_bar(s, "Excel", EXCEL, "march.xlsx", tabs=("File", "Home", "Insert", "Data", "View"), active="Insert")
    s.rect(30, 86, 44, 32, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    for i, h in enumerate((10, 18, 14)):
        s.rect(40 + 8 * i, 112 - h, 6, h, fill=EXCEL)
    excel_grid(s, [["Row Labels", "Sum of Total"], ["Bags", 78], ["Drinks", 71], ["Paper", 206], ["Grand Total", 355]],
               x=30, y=140, cw=(90, 90))
    s.rect(250, 140, 280, 190, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    s.text(390, 162, "Sales by type (JD)", 12, 700, INK, "middle")
    for i, (lab, v) in enumerate((("Bags", 78), ("Drinks", 71), ("Paper", 206))):
        h = v * 0.62
        x = 290 + 78 * i
        s.rect(x, 306 - h, 44, h, fill=EXCEL)
        s.text(x + 22, 322, lab, 11, 400, INK, "middle")
    top.ring(116, 54, 54, 26, 6)
    top.mark(1, 182, 66)
    top.ring(26, 82, 52, 40, 6)
    top.mark(2, 92, 102)


# =====================================================================
# Digital Skills, Online activity 8 (week-09, syllabus v3): Access. The
# model is the Books table of the college library (BookID, Title, Type,
# Pages); never the data of the tasks (the Products of the Sunrise shop).
# =====================================================================

ACCESS = "#a4373a"


def access_frame(s, active, name="library : Database"):
    office_bar(s, "Access", ACCESS, name, tabs=("File", "Home", "Create", "External Data", "Database Tools"), active=active)
    s.rect(15, 123, 120, 222, fill="#f8f9fa")
    s.text(24, 142, "All Access Objects", 10.5, 600, GREY)
    s.text(30, 166, "Books", 12, 400, INK)


@window("computer")
def access_form_1(s, top):
    """Access: select the table, Create › Form; the form shows one record."""
    access_frame(s, "Create")
    s.rect(26, 152, 104, 22, fill="#fdecea")
    s.text(30, 166, "Books", 12, 600, INK)
    s.rect(30, 86, 50, 32, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    s.text(55, 107, "Form", 11.5, 600, INK, "middle")
    s.rect(150, 134, 380, 200, fill="#ffffff", stroke="#d0d4d9", sw=1)
    s.text(166, 160, "Books", 15, 700, ACCESS)
    for i, (f, v) in enumerate([("BookID", "1"), ("Title", "Maths 1"), ("Type", "Study"), ("Pages", "220")]):
        y = 186 + 30 * i
        s.text(166, y + 4, f, 12, 600, INK)
        s.rect(250, y - 12, 200, 22, fill="#ffffff", stroke="#c9cdd2", sw=1)
        s.text(258, y + 4, v, 12, 400, INK)
    s.text(166, 322, "Record: 1 of 6", 11.5, 400, GREY)
    top.ring(24, 150, 108, 26, 6)
    top.mark(1, 140, 160)
    top.ring(116, 54, 58, 26, 6)
    top.mark(2, 186, 66)
    top.ring(26, 82, 58, 40, 6)
    top.mark(3, 96, 102)


@window("computer")
def access_query_1(s, top):
    """Access Query Design: the Criteria row, the Sort row, then Run."""
    access_frame(s, "Create")
    s.rect(30, 86, 44, 32, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    s.text(52, 108, "! Run", 11.5, 700, ACCESS, "middle")
    s.rect(150, 134, 120, 70, fill="#ffffff", stroke="#c9cdd2", sw=1)
    s.text(160, 152, "Books", 12, 700, INK)
    for i, f in enumerate(["Title", "Type", "Pages"]):
        s.text(160, 170 + 14 * i, f, 10.5, 400, INK)
    for r, (lab, a, b) in enumerate([("Field:", "Title", "Type"), ("Sort:", "Ascending", ""), ("Criteria:", "", "\"Story\"")]):
        y = 224 + 30 * r
        s.text(150, y + 17, lab, 11.5, 600, GREY)
        for c, v in enumerate((a, b)):
            x = 220 + 130 * c
            s.rect(x, y, 126, 26, fill="#ffffff", stroke="#c9cdd2", sw=1)
            s.text(x + 8, y + 17, v, 11.5, 400, INK)
    top.ring(346, 280, 134, 34, 6)
    top.mark(1, 492, 298)
    top.ring(216, 250, 134, 34, 6)
    top.mark(2, 204, 248)
    top.ring(26, 82, 52, 40, 6)
    top.mark(3, 92, 102)


@window("computer")
def access_report_1(s, top):
    """Access: select the table, Create › Report; the report preview."""
    access_frame(s, "Create")
    s.rect(26, 152, 104, 22, fill="#fdecea")
    s.text(30, 166, "Books", 12, 600, INK)
    s.rect(30, 86, 56, 32, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    s.text(58, 107, "Report", 11.5, 600, INK, "middle")
    s.rect(150, 134, 380, 200, fill="#ffffff", stroke="#d0d4d9", sw=1)
    s.text(166, 160, "Books", 15, 700, ACCESS)
    s.text(166, 184, "Title", 11, 700, INK)
    s.text(300, 184, "Type", 11, 700, INK)
    s.text(420, 184, "Pages", 11, 700, INK)
    for i, (t, ty, p) in enumerate([("Maths 1", "Study", "220"), ("The Old Bridge", "Story", "140"), ("English 2", "Study", "180"), ("Desert Rain", "Story", "200")]):
        y = 206 + 22 * i
        s.text(166, y, t, 11, 400, INK)
        s.text(300, y, ty, 11, 400, INK)
        s.text(420, y, p, 11, 400, INK)
    s.text(166, 318, "Page 1 of 1", 10.5, 400, GREY)
    top.ring(24, 150, 108, 26, 6)
    top.mark(1, 140, 160)
    top.ring(116, 54, 58, 26, 6)
    top.mark(2, 186, 66)
    top.ring(26, 82, 64, 40, 6)
    top.mark(3, 102, 102)


# =====================================================================
# Digital Skills, Online activity 9 (week-11, syllabus v3): Microsoft
# Forms in a browser. The model is the booking form of the college gym
# ("Gym booking": Day, Time); never the data of the tasks (the four
# project services).
# =====================================================================

FORMS = "#038387"


def forms_bar(s, title="Gym booking"):
    browser_bar(s, "forms.office.com")
    s.rect(15, 45, WW - 30, 34, fill=FORMS)
    s.text(30, 67, "Forms", 13, 700, "#ffffff")
    s.text(WW / 2, 67, title, 12.5, 400, "#ffffff", "middle")


@window("browser")
def forms_new_1(s, top):
    """forms.office.com: New Form, then the title."""
    browser_bar(s, "forms.office.com")
    s.rect(15, 45, WW - 30, 34, fill=FORMS)
    s.text(30, 67, "Forms", 13, 700, "#ffffff")
    s.rect(30, 96, 110, 34, fill=FORMS, rx=6)
    s.text(85, 118, "+ New Form", 13, 700, "#ffffff", "middle")
    s.text(160, 118, "New Quiz", 12.5, 400, GREY)
    s.text(30, 160, "Quick start with", 12, 600, GREY)
    for i, t in enumerate(["Event registration", "Customer feedback", "Order form"]):
        x = 30 + 170 * i
        s.rect(x, 172, 156, 90, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=6)
        page_lines(s, x + 14, 196, 120, 3, gap=16)
        s.text(x + 12, 252, t, 11.5, 600, INK)
    s.text(30, 300, "My forms", 12, 600, GREY)
    top.ring(26, 92, 118, 42, 8)
    top.mark(1, 156, 96)


@window("browser")
def forms_question_1(s, top):
    """A new form: + Add new, Choice, the options; Date for the day."""
    forms_bar(s)
    s.rect(15, 79, WW - 30, 266, fill="#e9f5f5")
    s.rect(90, 92, 380, 196, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=6)
    s.text(106, 118, "1. Which time?", 13, 700, INK)
    for i, t in enumerate(["10:00", "12:00", "14:00"]):
        y = 144 + 26 * i
        s.circle(116, y - 4, 7, fill="#ffffff", stroke=GREY, sw=1.5)
        s.text(132, y, t, 12.5, 400, INK)
    s.text(106, 230, "Required", 11.5, 400, GREY)
    s.rect(170, 220, 30, 16, fill=FORMS, rx=8)
    s.circle(192, 228, 6, fill="#ffffff")
    s.rect(90, 298, 110, 30, fill="#ffffff", stroke=FORMS, sw=1.5, rx=6)
    s.text(145, 318, "+ Add new", 12.5, 700, FORMS, "middle")
    for i, t in enumerate(["Choice", "Text", "Rating", "Date"]):
        s.text(214 + 62 * i, 318, t, 12, 600 if t in ("Choice", "Date") else 400, INK)
    top.ring(86, 294, 118, 38, 8)
    top.mark(1, 76, 296)
    top.ring(206, 300, 56, 26, 6)
    top.mark(2, 234, 344)
    top.ring(100, 126, 120, 84, 8)
    top.mark(3, 232, 130)


@window("browser")
def forms_collect_1(s, top):
    """Collect responses: copy the link (or the QR code)."""
    forms_bar(s)
    s.rect(15, 79, WW - 30, 266, fill="#e9f5f5")
    s.rect(400, 86, 130, 30, fill=FORMS, rx=6)
    s.text(465, 106, "Collect responses", 11.5, 700, "#ffffff", "middle")
    s.rect(160, 126, 370, 200, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=8)
    s.text(176, 154, "Send and collect responses", 14, 700, INK)
    s.text(176, 182, "Anyone can respond", 12, 400, GREY)
    s.rect(176, 196, 270, 30, fill="#f1f3f5", stroke="#c9cdd2", sw=1, rx=4)
    s.text(186, 216, "https://forms.office.com/r/aB3...", 11.5, 400, INK)
    s.rect(454, 196, 62, 30, fill=FORMS, rx=4)
    s.text(485, 216, "Copy", 12, 700, "#ffffff", "middle")
    s.rect(176, 244, 40, 40, fill="#ffffff", stroke=INK, sw=1.5, rx=2)
    for i in range(3):
        for j in range(3):
            if (i + j) % 2 == 0:
                s.rect(181 + 11 * i, 249 + 11 * j, 8, 8, fill=INK)
    s.text(226, 270, "QR code", 12, 400, INK)
    top.ring(396, 82, 138, 38, 8)
    top.mark(1, 384, 84)
    top.ring(450, 192, 70, 38, 8)
    top.mark(2, 438, 244)


@window("browser")
def forms_responses_1(s, top):
    """The Responses tab: the number of responses, then Open results in Excel."""
    forms_bar(s)
    s.rect(15, 79, WW - 30, 266, fill="#e9f5f5")
    s.text(190, 104, "Questions", 13, 400, INK)
    s.text(290, 104, "Responses", 13, 700, INK)
    s.line(290, 110, 360, 110, FORMS, 3)
    s.rect(60, 124, 440, 200, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=8)
    s.text(80, 166, "3", 34, 700, INK)
    s.text(80, 190, "Responses", 12, 400, GREY)
    s.rect(330, 146, 150, 32, fill="#ffffff", stroke=FORMS, sw=1.5, rx=6)
    s.text(405, 167, "Open results in Excel", 11.5, 700, FORMS, "middle")
    for i, (t, w) in enumerate([("10:00", 120), ("12:00", 60), ("14:00", 30)]):
        y = 220 + 26 * i
        s.text(80, y, t, 12, 400, INK)
        s.rect(130, y - 12, w, 14, fill=FORMS, rx=3)
    top.ring(284, 86, 82, 30, 6)
    top.mark(1, 378, 98)
    top.ring(326, 142, 158, 40, 8)
    top.mark(2, 494, 162)


# =====================================================================
# Digital Skills, Online activity 10 (week-12, syllabus v3): Google Sites
# in a browser. The model is the website of the college gym ("College
# Gym", with the booking form of Online activity 9); never the data of
# the tasks (the four project services).
# =====================================================================

SITES = "#5e35b1"


def sites_editor(s, page="Home"):
    browser_bar(s, "sites.google.com")
    s.rect(15, 45, WW - 30, 30, fill="#ffffff")
    s.text(30, 65, "College Gym", 13, 700, INK)
    s.rect(440, 50, 76, 22, fill=SITES, rx=4)
    s.text(478, 66, "Publish", 11.5, 700, "#ffffff", "middle")
    s.line(15, 75, WW - 15, 75, LINE, 1)
    s.rect(380, 76, 165, 269, fill="#f8f9fa")
    for i, t in enumerate(["Insert", "Pages", "Themes"]):
        s.text(398 + 52 * i, 96, t, 11.5, 700 if t == page else 400, SITES if t == page else INK)
    s.rect(30, 90, 336, 240, fill="#ffffff", stroke="#d0d4d9", sw=1)


@window("browser")
def sites_pages_1(s, top):
    """Google Sites: Pages, then + to add a page; the menu shows it."""
    sites_editor(s, "Pages")
    s.rect(30, 90, 336, 30, fill="#ede7f6")
    s.text(46, 110, "College Gym", 11.5, 700, SITES)
    for i, t in enumerate(["Home", "Booking", "Contact"]):
        s.text(210 + 52 * i, 110, t, 10.5, 600, INK)
    s.text(46, 160, "Welcome to the College Gym!", 15, 700, INK)
    page_lines(s, 46, 190, 280, 3)
    for i, t in enumerate(["Home", "Booking", "Contact"]):
        s.text(398, 132 + 26 * i, t, 12, 400, INK)
    s.circle(520, 300, 16, fill=SITES)
    s.text(520, 306, "+", 18, 700, "#ffffff", "middle")
    top.ring(444, 84, 50, 20, 5)
    top.mark(1, 506, 112)
    top.ring(500, 280, 40, 40, 20)
    top.mark(2, 490, 268)
    top.ring(204, 96, 160, 22, 5)
    top.mark(3, 190, 136)


@window("browser")
def sites_button_1(s, top):
    """Insert › Button: the name and the link of the form."""
    sites_editor(s, "Insert")
    for i, t in enumerate(["Text box", "Images", "Button", "Divider"]):
        s.text(398, 132 + 26 * i, t, 12, 600 if t == "Button" else 400, INK)
    s.text(46, 120, "Book the gym", 15, 700, INK)
    s.rect(80, 150, 250, 150, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=8)
    s.text(96, 176, "Name", 11, 600, GREY)
    s.rect(96, 182, 218, 26, fill="#ffffff", stroke="#8a9096", sw=1, rx=3)
    s.text(104, 200, "Book now", 12, 400, INK)
    s.text(96, 228, "Link", 11, 600, GREY)
    s.rect(96, 234, 218, 26, fill="#ffffff", stroke="#8a9096", sw=1, rx=3)
    s.text(104, 252, "https://forms.office.com/r/aB3...", 10.5, 400, INK)
    s.rect(254, 270, 60, 24, fill=SITES, rx=4)
    s.text(284, 287, "Insert", 11.5, 700, "#ffffff", "middle")
    top.ring(392, 172, 80, 24, 5)
    top.mark(1, 486, 184)
    top.ring(92, 178, 226, 34, 6)
    top.mark(2, 70, 194)
    top.ring(92, 230, 226, 34, 6)
    top.mark(3, 70, 248)
    top.ring(250, 266, 68, 32, 6)
    top.mark(4, 330, 282)


@window("browser")
def sites_publish_1(s, top):
    """Publish: the web address, then Publish; Preview › the phone first."""
    sites_editor(s, "Pages")
    s.rect(70, 110, 300, 200, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=8)
    s.text(86, 138, "Publish to the web", 14, 700, INK)
    s.text(86, 166, "Web address", 11, 600, GREY)
    s.rect(86, 174, 268, 28, fill="#ffffff", stroke="#8a9096", sw=1, rx=3)
    s.text(94, 193, "sites.google.com/view/", 11, 400, GREY)
    s.text(224, 193, "college-gym", 11, 700, INK)
    s.text(86, 230, "Who can see my site: Anyone", 11.5, 400, INK)
    s.rect(274, 268, 80, 28, fill=SITES, rx=4)
    s.text(314, 287, "Publish", 12, 700, "#ffffff", "middle")
    top.ring(436, 46, 84, 30, 6)
    top.mark(1, 424, 62)
    top.ring(82, 170, 276, 36, 6)
    top.mark(2, 70, 186)
    top.ring(270, 264, 88, 36, 6)
    top.mark(3, 368, 282)


# =====================================================================
# Digital Skills, Online activity 11 (week-14, syllabus v3): Canva in a
# browser. The model is a post of the college gym ("The gym is open ·
# Book now"); never the data of the tasks (the four project services).
# =====================================================================

CANVA = "#7d2ae8"


def canva_bar(s):
    browser_bar(s, "canva.com")
    s.rect(15, 45, WW - 30, 34, fill="#ffffff")
    s.text(30, 67, "Canva", 14, 700, CANVA)
    s.line(15, 79, WW - 15, 79, LINE, 1)


@window("browser")
def canva_search_1(s, top):
    """Canva: search Instagram post, then choose a design (template)."""
    canva_bar(s)
    s.rect(120, 52, 300, 22, fill="#f1f3f5", rx=11)
    s.text(134, 68, "Instagram post", 12, 400, INK)
    for i in range(3):
        x = 40 + 166 * i
        s.rect(x, 100, 150, 150, fill=["#ffe8cc", "#e7f5ff", "#ebfbee"][i], stroke="#c9cdd2", sw=1, rx=6)
        s.text(x + 75, 170, ["Fresh food", "Open today", "New offer"][i], 14, 700, INK, "middle")
        s.rect(x + 40, 196, 70, 20, fill=CANVA, rx=10)
        s.text(x + 75, 210, "Order", 11, 700, "#ffffff", "middle")
    s.text(40, 280, "Choose a design, then change it.", 12, 400, GREY)
    top.ring(116, 48, 308, 30, 15)
    top.mark(1, 104, 62)
    top.ring(36, 96, 158, 158, 8)
    top.mark(2, 200, 104)


@window("browser")
def canva_edit_1(s, top):
    """Canva editor: click the text and type; Elements › Photos (free)."""
    canva_bar(s)
    s.rect(15, 80, 70, 265, fill="#f8f9fa")
    for i, t in enumerate(["Design", "Elements", "Text", "Uploads"]):
        s.text(50, 110 + 34 * i, t, 11, 600 if t == "Elements" else 400, CANVA if t == "Elements" else INK, "middle")
    s.rect(85, 80, 150, 265, fill="#ffffff", stroke="#e3e5e8", sw=1)
    s.text(96, 104, "Photos", 12, 700, INK)
    for i in range(4):
        s.rect(96 + 66 * (i % 2), 116 + 66 * (i // 2), 58, 58, fill=["#ffd8a8", "#c3fae8", "#d0ebff", "#ffe3e3"][i], rx=4)
    s.text(96, 262, "Free photos", 11, 400, GREY)
    s.rect(270, 96, 250, 236, fill="#e7f5ff", stroke="#c9cdd2", sw=1)
    s.rect(300, 116, 190, 90, fill="#a5d8ff", rx=6)
    s.text(395, 236, "The gym is open", 16, 700, INK, "middle")
    s.rect(355, 254, 80, 24, fill=CANVA, rx=12)
    s.text(395, 271, "Book now", 11.5, 700, "#ffffff", "middle")
    s.text(395, 314, "Photo: Canva", 10, 400, GREY, "middle")
    top.ring(290, 220, 210, 26, 6)
    top.mark(1, 512, 232)
    top.ring(24, 120, 54, 26, 6)
    top.mark(2, 24, 112)
    top.ring(92, 112, 64, 64, 6)
    top.mark(3, 166, 112)


@window("browser")
def canva_download_1(s, top):
    """Canva: Share › Download, the type PNG, Download."""
    canva_bar(s)
    s.rect(440, 52, 76, 22, fill=CANVA, rx=4)
    s.text(478, 68, "Share", 11.5, 700, "#ffffff", "middle")
    s.rect(30, 96, 220, 236, fill="#e7f5ff", stroke="#c9cdd2", sw=1)
    s.text(140, 210, "The gym is open", 14, 700, INK, "middle")
    s.rect(280, 86, 240, 200, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=8)
    s.text(296, 112, "Download", 14, 700, INK)
    s.text(296, 140, "File type", 11, 600, GREY)
    s.rect(296, 148, 208, 28, fill="#ffffff", stroke="#8a9096", sw=1, rx=4)
    s.text(306, 167, "PNG (Suggested)", 12, 400, INK)
    s.rect(296, 240, 208, 32, fill=CANVA, rx=6)
    s.text(400, 261, "Download", 12.5, 700, "#ffffff", "middle")
    top.ring(436, 48, 84, 30, 6)
    top.mark(1, 424, 62)
    top.ring(292, 144, 216, 36, 6)
    top.mark(2, 280, 186)
    top.ring(292, 236, 216, 40, 6)
    top.mark(3, 280, 282)


# =====================================================================
# Digital Skills, Online activity 4 (week-04, syllabus v4): a header with
# the name and a page number in Omar's letter (letter.docx); never the
# data of the tasks.
# =====================================================================

@window("computer")
def word_header_1(s, top):
    """Word: Insert › Header, the name in the header; Insert › Page Number."""
    office_bar(s, "Word", WORD, "letter.docx", active="Insert")
    s.rect(30, 86, 60, 32, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    s.text(60, 107, "Header", 11.5, 600, INK, "middle")
    s.rect(98, 86, 96, 32, fill="#ffffff", stroke="#c9cdd2", sw=1, rx=4)
    s.text(146, 107, "Page Number", 11.5, 600, INK, "middle")
    s.rect(15, 123, WW - 30, 222, fill="#eef0f2")
    s.rect(150, 134, 260, 200, fill="#ffffff", stroke="#d0d4d9", sw=1)
    s.line(150, 168, 410, 168, "#9aa5b1", 1)
    s.text(162, 158, "Omar Khaled · letter", 11, 600, INK)
    page_lines(s, 174, 196, 212, 4)
    s.text(396, 324, "1", 11, 600, INK, "end")
    top.ring(26, 82, 68, 40, 6)
    top.mark(1, 18, 102)
    top.ring(156, 142, 150, 24, 5)
    top.mark(2, 318, 154)
    top.ring(94, 82, 104, 40, 6)
    top.mark(3, 210, 102)


SCREENS = {
    "courses/digital-skills/week-02/images/calendar-android-1": calendar_android_1,
    "courses/digital-skills/week-02/images/calendar-android-2": calendar_android_2,
    "courses/digital-skills/week-02/images/calendar-android-3": calendar_android_3,
    "courses/digital-skills/week-02/images/calendar-iphone-1": calendar_iphone_1,
    "courses/digital-skills/week-02/images/calendar-iphone-2": calendar_iphone_2,
    "courses/digital-skills/week-02/images/calendar-iphone-3": calendar_iphone_3,
    "courses/digital-skills/week-02/images/scan-android-1": scan_android_1,
    "courses/digital-skills/week-02/images/scan-android-2": scan_android_2,
    "courses/digital-skills/week-02/images/scan-android-3": scan_android_3,
    "courses/digital-skills/week-02/images/scan-iphone-1": scan_iphone_1,
    "courses/digital-skills/week-02/images/scan-iphone-2": scan_iphone_2,
    "courses/digital-skills/week-02/images/scan-iphone-3": scan_iphone_3,
    "courses/digital-skills/week-03/images/pdf-win-1": pdf_win_1,
    "courses/digital-skills/week-03/images/pdf-win-2": pdf_win_2,
    "courses/digital-skills/week-03/images/pdf-web-1": pdf_web_1,
    "courses/digital-skills/week-03/images/paste-win-1": paste_win_1,
    "courses/digital-skills/week-03/images/paste-win-2": paste_win_2,
    "courses/digital-skills/week-03/images/share-win-1": share_win_1,
    "courses/digital-skills/week-03/images/share-win-2": share_win_2,
    "courses/digital-skills/week-03/images/twostep-win-1": twostep_win_1,
    "courses/digital-skills/week-03/images/twostep-phone-1": twostep_phone_1,
    "courses/digital-skills/week-03/images/link-phone-1": link_phone_1,
    "courses/digital-skills/week-03/images/report-win-1": report_win_1,
    "courses/digital-skills/week-03/images/perm-android-1": perm_android_1,
    "courses/digital-skills/week-03/images/perm-android-2": perm_android_2,
    "courses/digital-skills/week-03/images/perm-iphone-1": perm_iphone_1,
    "courses/digital-skills/week-03/images/perm-iphone-2": perm_iphone_2,
    "courses/digital-skills/week-04/images/word-header-1": word_header_1,
    "courses/digital-skills/week-04/images/ppt-newslide-1": ppt_newslide_1,
    "courses/digital-skills/week-04/images/ppt-design-1": ppt_design_1,
    "courses/digital-skills/week-04/images/ppt-picture-1": ppt_picture_1,
    "courses/digital-skills/week-07/images/pivot-win-1": pivot_win_1,
    "courses/digital-skills/week-07/images/pivot-win-2": pivot_win_2,
    "courses/digital-skills/week-07/images/pivot-chart-1": pivot_chart_1,
    "courses/digital-skills/week-09/images/access-form-1": access_form_1,
    "courses/digital-skills/week-09/images/access-query-1": access_query_1,
    "courses/digital-skills/week-09/images/access-report-1": access_report_1,
    "courses/digital-skills/week-11/images/forms-new-1": forms_new_1,
    "courses/digital-skills/week-11/images/forms-question-1": forms_question_1,
    "courses/digital-skills/week-11/images/forms-collect-1": forms_collect_1,
    "courses/digital-skills/week-11/images/forms-responses-1": forms_responses_1,
    "courses/digital-skills/week-12/images/sites-pages-1": sites_pages_1,
    "courses/digital-skills/week-12/images/sites-button-1": sites_button_1,
    "courses/digital-skills/week-12/images/sites-publish-1": sites_publish_1,
    "courses/digital-skills/week-14/images/canva-search-1": canva_search_1,
    "courses/digital-skills/week-14/images/canva-edit-1": canva_edit_1,
    "courses/digital-skills/week-14/images/canva-download-1": canva_download_1,
}


def export_png(svg):
    png = svg[:-4] + ".png"
    subprocess.run(["quarto", "typst", "compile", "--root", ROOT, "--input",
                    "svg=/" + os.path.relpath(svg, ROOT).replace(os.sep, "/"),
                    os.path.join(ROOT, "shared", "sims", "export-poster.typ"), png, "--ppi", "200"], check=True)


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for base, fn in SCREENS.items():
        if only and not any(o in base for o in only):
            continue
        svg = os.path.join(ROOT, base + ".svg")
        with open(svg, "w", encoding="utf-8") as f:
            f.write(draw_window(fn) if getattr(fn, "window", None) else draw_phone(fn))
        if "--svg" not in sys.argv:
            export_png(svg)
        print("wrote", os.path.relpath(svg, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
