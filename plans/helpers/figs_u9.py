#!/usr/bin/env python3
"""Figures and posters of Digital Skills Unit 9 (week-12, website design)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Svg, INK, MUTED, LINE, ORANGE, PEACH, SOFT, GREEN, BLUE, GREY_BG
from figs_u3 import poster_head
from figs_u7 import choices

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = os.path.join(ROOT, "courses", "digital-skills", "week-12")
BROWN = "#a3360b"


def page(s, x, y, w, h, name, rows, active):
    s.rect(x, y, w, h, rx=8, fill="#ffffff", stroke=LINE)
    s.rect(x, y, w, 30, rx=8, fill=SOFT, stroke=None)
    s.text(x + 10, y + 20, "Mona's Cakes", size=11, weight=800, fill=BROWN)
    for i, t in enumerate(["Home", "Service", "Contact"]):
        s.text(x + w - 150 + 50 * i, y + 20, t, size=10, weight=800 if t == active else 600, fill=ORANGE if t == active else INK)
    for i, r in enumerate(rows):
        s.text(x + 10, y + 52 + 18 * i, r, size=10.5, weight=700)


def site_pages():
    s = Svg(700, 210)
    page(s, 10, 30, 220, 150, "Home", ["Welcome to Mona's Cakes!", "Cakes made at home.", "[ a photo of a cake ]"], "Home")
    page(s, 240, 30, 220, 150, "Service", ["Chocolate 12 JD", "Lemon 10 JD · Fruit 11 JD", "[ Order now ]"], "Service")
    page(s, 470, 30, 220, 150, "Contact", ["Phone 079 000 0000", "Amman", "Sun to Thu, 9:00 to 17:00"], "Contact")
    for i, t in enumerate(["Home", "Service", "Contact"]):
        s.text(120 + 230 * i, 20, t, size=13, weight=800, anchor="middle")
    s.text(350, 202, "The menu at the top of every page joins the three pages.", size=12, anchor="middle", fill=MUTED, weight=700)
    s.save(os.path.join(W, "images", "site-pages.svg"))


def site_design():
    s = Svg(700, 230)
    s.rect(10, 10, 330, 200, rx=8, fill="#ffffff", stroke=LINE)
    s.text(24, 40, "Mona's Cakes", size=16, weight=800, fill="#dee2e6")
    s.text(24, 64, "Cakes made at home.", size=12, fill="#ced4da", weight=600)
    s.rect(24, 76, 300, 120, rx=6, fill="#ffd8a8", stroke=None)
    s.xmark(320, 26)
    s.text(175, 225, "light grey text, no menu, a huge picture", size=11, anchor="middle", fill=MUTED, weight=700)
    s.rect(360, 10, 330, 200, rx=8, fill="#ffffff", stroke=LINE)
    s.rect(360, 10, 330, 32, rx=8, fill=SOFT, stroke=None)
    s.text(374, 31, "Mona's Cakes", size=13, weight=800, fill=BROWN)
    for i, t in enumerate(["Home", "Service", "Contact"]):
        s.text(530 + 52 * i, 31, t, size=11, weight=700)
    s.text(374, 70, "Cakes made at home", size=15, weight=800, fill=BROWN)
    s.text(374, 92, "For every party. Order online.", size=12, weight=700)
    s.rect(374, 104, 150, 80, rx=6, fill="#ffd8a8", stroke=None)
    s.tick(676, 26)
    s.text(525, 225, "dark text, one theme, a menu, a good picture", size=11, anchor="middle", fill=MUTED, weight=700)
    s.save(os.path.join(W, "images", "site-design.svg"))


def html_css():
    s = Svg(700, 210)
    s.rect(10, 10, 380, 190, rx=10, fill="#212529", stroke=None)
    code = ["<style>", "  h1 { color: brown; font-size: 28px; }", "</style>", "<h1>Mona's Cakes</h1>",
            "<p>Cakes made at home.</p>", '<a href="order.html">Order now</a>']
    for i, c in enumerate(code):
        s.text(24, 38 + 26 * i, c, size=12.5, fill=("#ffc078" if i in (1,) else "#f8f9fa"), weight=600)
    s.text(395, 60, "CSS: the look", size=12, fill=ORANGE, weight=800)
    s.text(395, 140, "HTML: the content", size=12, fill=BLUE, weight=800)
    s.line(520, 105, 545, 105, stroke=INK, sw=2, arrow=True)
    s.rect(550, 30, 140, 150, rx=8, fill="#ffffff", stroke=LINE)
    s.text(560, 64, "Mona's Cakes", size=15, weight=800, fill=BROWN)
    s.text(560, 90, "Cakes made at home.", size=10.5, weight=600)
    s.text(560, 116, "Order now", size=11, weight=700, fill=BLUE)
    s.line(560, 119, 614, 119, stroke=BLUE, sw=1)
    s.save(os.path.join(W, "images", "html-css.svg"))


def poster(name, title, hint, task, body, h=360):
    s = Svg(640, h)
    poster_head(s, title, hint, task)
    body(s)
    s.save(os.path.join(W, "sims", name + ".svg"))


if __name__ == "__main__":
    site_pages()
    site_design()
    html_css()
    poster("site-planner", "Site Planner: what goes on which page?", "Put each part of the content on the right page.",
           "Part 1 of 6: which page?",
           lambda s: [s.rect(24, 114, 560, 34, rx=10, fill="#ffffff", stroke=ORANGE),
                      s.text(38, 136, "Welcome to Mona's Cakes! Cakes made at home, for every party.", size=12.5, weight=800),
                      choices(s, 160, ["Home", "Service", "Contact"])] +
                     [(s.rect(24 + 196 * i, 206, 188, 130, rx=10, fill="#ffffff", stroke=LINE),
                       s.rect(30 + 196 * i, 212, 176, 22, rx=6, fill=SOFT, stroke=None),
                       s.text(118 + 196 * i, 228, t, size=12, anchor="middle", weight=800)) for i, t in enumerate(["Home", "Service", "Contact"])])
    poster("design-check", "Design Check: fix the page", "The home page of Mona's Cakes has four design problems.",
           "Tap a problem to fix it (4 left).",
           lambda s: [choices(s, 114, ["Text: light grey on white", "Fonts: five different fonts"]),
                      choices(s, 152, ["Picture: very big", "Menu: no links"]),
                      s.rect(24, 196, 420, 150, rx=10, fill="#ffffff", stroke=INK, sw=2),
                      s.text(38, 222, "Mona's Cakes", size=13, weight=800),
                      s.text(38, 252, "Cakes made at home", size=17, weight=800, fill="#dee2e6"),
                      s.rect(38, 266, 390, 70, rx=6, fill="#ffd8a8", stroke=None)])
    poster("html-lab", "HTML Lab: a look at HTML and CSS", "Change one part of the page, and see the page change.",
           "Change the colour and the size, then answer: which tag makes the big heading?",
           lambda s: [s.rect(24, 114, 380, 110, rx=10, fill="#212529", stroke=None)] +
                     [s.text(36, 136 + 18 * i, c, size=11.5, fill="#f8f9fa", weight=600) for i, c in enumerate(
                         ["h1 { color: brown; font-size: 28px; }", "<h1>Mona's Cakes</h1>", "<p>Cakes made at home.</p>", '<a href="order.html">Order now</a>'])] +
                     [s.rect(24, 236, 380, 70, rx=10, fill="#ffffff", stroke=INK, sw=2),
                      s.text(38, 268, "Mona's Cakes", size=20, weight=800, fill=BROWN),
                      s.text(38, 292, "Cakes made at home.", size=12, weight=600),
                      choices(s, 318, ["<h1>", "<p>", "<a>"])], h=360)
    s = Svg(640, 360)
    s.text(24, 34, "Web Desk at Sunrise Company", size=21, weight=800)
    s.text(24, 56, "Help your colleagues with their websites.", size=12, fill=MUTED)
    s.text(24, 88, "Message 1 / 8", size=13, weight=800)
    s.text(616, 88, "0 stars", size=13, fill=ORANGE, anchor="end", weight=800)
    s.rect(24, 102, 560, 56, rx=14, fill=SOFT, stroke=PEACH)
    s.text(38, 122, "Omar (shop)", size=10.5, fill=MUTED, weight=700)
    s.text(38, 144, "Our shop website needs pages. Which three are enough?", size=12.5, weight=800)
    for i, t in enumerate(["Home, Service and Contact", "twenty pages, one for each product", "only one page with everything"]):
        y = 176 + i * 42
        s.rect(24, y, 592, 34, rx=10, fill="#ffffff", stroke=ORANGE)
        s.text(38, y + 22, t, size=13, fill=ORANGE, weight=800)
    s.save(os.path.join(W, "sims", "web-desk.svg"))
