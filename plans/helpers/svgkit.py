"""A small SVG kit for the figures and simulator posters of Digital Skills.

The look of the course figures: white card, Helvetica (Arial), weight 600,
ink #2a2f2c, muted #6b726e, the course orange #D9480F and peach #FFC078.
No emoji and no special symbols inside a figure (AUTHORING.md, "Rich and
visual"); icons are drawn as shapes. Export with plans/helpers/export_png.py.
"""
from xml.sax.saxutils import escape

INK = "#2a2f2c"
MUTED = "#6b726e"
LINE = "#ced4da"
SOFTLINE = "#dee2e6"
ORANGE = "#D9480F"
PEACH = "#FFC078"
SOFT = "#fff4e6"
GREEN = "#2f9e44"
GREEN_SOFT = "#ebfbee"
RED = "#c92a2a"
RED_SOFT = "#fff5f5"
BLUE = "#1971c2"
BLUE_SOFT = "#e7f5ff"
WORD = "#2b579a"
EXCEL = "#217346"
PPT = "#c43e1c"
ACCESS = "#a4373a"
GREY_BG = "#f1f3f5"


class Svg:
    def __init__(self, w, h, bg="#ffffff"):
        self.w, self.h = w, h
        self.parts = []
        self.markers = set()
        if bg:
            self.parts.append('<rect width="%g" height="%g" fill="%s"/>' % (w, h, bg))

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, rx=8, fill="#ffffff", stroke=LINE, sw=1.5, dash=None, opacity=None):
        a = ' stroke-dasharray="%s"' % dash if dash else ""
        if opacity is not None:
            a += ' opacity="%g"' % opacity
        st = ' stroke="%s" stroke-width="%g"' % (stroke, sw) if stroke else ' stroke="none"'
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%g" fill="%s"%s%s/>' % (x, y, w, h, rx, fill, st, a))

    def text(self, x, y, s, size=12, fill=INK, anchor="start", weight=600, italic=False):
        it = ' font-style="italic"' if italic else ""
        self.add('<text x="%.1f" y="%.1f" font-size="%g" fill="%s" text-anchor="%s" font-weight="%s"%s xml:space="preserve">%s</text>'
                 % (x, y, size, fill, anchor, weight, it, escape(s)))

    def lines(self, x, y, rows, size=12, fill=INK, anchor="start", weight=600, gap=None):
        gap = gap or size * 1.35
        for i, r in enumerate(rows):
            self.text(x, y + i * gap, r, size, fill, anchor, weight)

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.5, arrow=False, dash=None):
        m = ""
        if arrow:
            mid = "m" + stroke.strip("#")
            self.markers.add((mid, stroke))
            m = ' marker-end="url(#%s)"' % mid
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%g" stroke-linecap="round"%s%s/>'
                 % (x1, y1, x2, y2, stroke, sw, d, m))

    def circle(self, cx, cy, r, fill="#ffffff", stroke=None, sw=1.5):
        st = ' stroke="%s" stroke-width="%g"' % (stroke, sw) if stroke else ""
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s/>' % (cx, cy, r, fill, st))

    def poly(self, pts, fill="none", stroke=INK, sw=1.5, close=True):
        tag = "polygon" if close else "polyline"
        p = " ".join("%.1f,%.1f" % xy for xy in pts)
        st = ' stroke="%s" stroke-width="%g" stroke-linejoin="round" stroke-linecap="round"' % (stroke, sw) if stroke else ""
        self.add('<%s points="%s" fill="%s"%s/>' % (tag, p, fill, st))

    def path(self, d, fill="none", stroke=INK, sw=1.5):
        st = ' stroke="%s" stroke-width="%g" stroke-linejoin="round" stroke-linecap="round"' % (stroke, sw) if stroke else ""
        self.add('<path d="%s" fill="%s"%s/>' % (d, fill, st))

    def badge(self, cx, cy, n, r=11, fill=ORANGE):
        """A numbered circle (what to look at)."""
        self.circle(cx, cy, r, fill=fill)
        self.text(cx, cy + 4.5, str(n), size=r * 1.15, fill="#ffffff", anchor="middle", weight=800)

    def bar(self, x, y, w, rows=1, gap=12, c=SOFTLINE, h=5):
        for i in range(rows):
            self.rect(x, y + i * gap, w if i < rows - 1 or rows == 1 else w * 0.7, h, rx=2, fill=c, stroke=None)

    def doc(self, x, y, w=60, h=76, c=WORD, rows=4):
        f = min(14, w * 0.3)
        self.poly([(x, y), (x + w - f, y), (x + w, y + f), (x + w, y + h), (x, y + h)], fill="#ffffff", stroke=c, sw=2)
        self.poly([(x + w - f, y), (x + w - f, y + f), (x + w, y + f)], fill=c, stroke=None)
        self.bar(x + 9, y + 24, w - 22, rows=rows, gap=11)

    def clip(self, cx, cy, c=INK):
        """A paperclip."""
        self.path("M%.1f %.1f v-9 a4 4 0 0 1 8 0 v12 a6 6 0 0 1 -12 0 v-10" % (cx - 2, cy + 6), stroke=c, sw=1.8)

    def person(self, cx, cy, c=ORANGE, r=9):
        self.circle(cx, cy - r * 0.6, r * 0.55, fill=c)
        self.path("M%.1f %.1f a%.1f %.1f 0 0 1 %.1f 0 z" % (cx - r, cy + r * 0.9, r, r * 0.9, 2 * r), fill=c, stroke=None)

    def lock(self, cx, cy, c=INK, k=1.0):
        self.rect(cx - 8 * k, cy - 2 * k, 16 * k, 13 * k, rx=2, fill=c, stroke=None)
        self.path("M%.1f %.1f v-4 a%.1f %.1f 0 0 1 %.1f 0 v4" % (cx - 5 * k, cy - 2 * k, 5 * k, 5 * k, 10 * k), stroke=c, sw=2 * k)

    def tick(self, cx, cy, c=GREEN, k=1.0):
        self.poly([(cx - 6 * k, cy), (cx - 2 * k, cy + 4 * k), (cx + 6 * k, cy - 5 * k)], stroke=c, sw=2.6 * k, close=False)

    def xmark(self, cx, cy, c=RED, k=1.0):
        # Two diagonal strokes (an X, never an upright cross).
        self.line(cx - 5 * k, cy - 5 * k, cx + 5 * k, cy + 5 * k, stroke=c, sw=2.6 * k)
        self.line(cx - 5 * k, cy + 5 * k, cx + 5 * k, cy - 5 * k, stroke=c, sw=2.6 * k)

    def save(self, path):
        defs = ""
        if self.markers:
            defs = "<defs>" + "".join(
                '<marker id="%s" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" '
                'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>' % (mid, c)
                for mid, c in sorted(self.markers)) + "</defs>"
        out = ('<svg xmlns="http://www.w3.org/2000/svg" width="%g" height="%g" viewBox="0 0 %g %g" '
               'font-family="Helvetica, Arial, sans-serif" font-weight="600">\n' % (self.w, self.h, self.w, self.h))
        out += defs + "\n" + "\n".join(self.parts) + "\n</svg>\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", path)
