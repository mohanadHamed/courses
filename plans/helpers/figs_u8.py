#!/usr/bin/env python3
"""Figures and posters of Digital Skills Unit 8 (week-11, a digital service)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Svg, INK, MUTED, LINE, ORANGE, PEACH, SOFT, GREEN, BLUE, EXCEL, GREY_BG
from figs_u3 import poster_head
from figs_u7 import table, choices

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = os.path.join(ROOT, "courses", "digital-skills", "week-11")


def icon_cart(s, cx, cy, c):
    s.poly([(cx - 22, cy - 14), (cx - 14, cy - 14), (cx - 6, cy + 8), (cx + 18, cy + 8), (cx + 22, cy - 8), (cx - 10, cy - 8)], stroke=c, sw=3, close=False)
    s.circle(cx - 3, cy + 16, 4, fill=c)
    s.circle(cx + 15, cy + 16, 4, fill=c)


def icon_calendar(s, cx, cy, c):
    s.rect(cx - 20, cy - 16, 40, 36, rx=5, fill="#ffffff", stroke=c, sw=3)
    s.rect(cx - 20, cy - 16, 40, 10, rx=3, fill=c, stroke=None)
    for i in range(3):
        for j in range(2):
            s.rect(cx - 13 + 10 * i, cy + 0 + 9 * j, 6, 5, rx=1, fill=c, stroke=None)


def icon_form(s, cx, cy, c):
    s.rect(cx - 17, cy - 22, 34, 44, rx=4, fill="#ffffff", stroke=c, sw=3)
    for k in range(3):
        s.rect(cx - 10, cy - 12 + 11 * k, 6, 6, rx=1, fill="#ffffff", stroke=c, sw=1.8)
        s.line(cx - 1, cy - 9 + 11 * k, cx + 11, cy - 9 + 11 * k, stroke=c, sw=2)


def icon_download(s, cx, cy, c):
    s.doc(cx - 16, cy - 22, w=32, h=40, c=c, rows=0)
    s.line(cx, cy - 8, cx, cy + 8, stroke=c, sw=3)
    s.poly([(cx - 7, cy + 2), (cx, cy + 10), (cx + 7, cy + 2)], stroke=c, sw=3, close=False)


def service_kinds():
    s = Svg(680, 200)
    items = [("online store", "choose and pay", icon_cart), ("booking", "a day and a time", icon_calendar),
             ("online form", "answer questions", icon_form), ("digital product", "download a file", icon_download)]
    for i, (t, sub, ic) in enumerate(items):
        x = 14 + i * 166
        s.rect(x, 14, 154, 170, rx=14, fill=SOFT, stroke=PEACH)
        ic(s, x + 77, 70, ORANGE)
        s.text(x + 77, 132, t, size=14, anchor="middle", weight=800)
        s.text(x + 77, 154, sub, size=12, anchor="middle", fill=MUTED, weight=700)
    s.save(os.path.join(W, "images", "service-kinds.svg"))


def service_plan():
    s = Svg(680, 240)
    s.text(20, 28, "Mona's Cakes: orders online", size=15, weight=800)
    for i, (lab, txt) in enumerate([("The customer", "families who want a cake for a party"), ("The need", "to order without a phone call")]):
        y = 44 + i * 44
        s.rect(20, y, 640, 36, rx=10, fill=SOFT, stroke=PEACH)
        s.text(34, y + 23, lab, size=13, weight=800, fill=ORANGE)
        s.text(170, y + 23, txt, size=13, weight=700)
    s.text(20, 152, "The steps of the customer", size=13, weight=800, fill=ORANGE)
    steps = ["See the cakes", "Fill in the form", "Get a confirmation", "Collect and pay"]
    for i, t in enumerate(steps):
        x = 20 + i * 166
        s.rect(x, 164, 146, 54, rx=10, fill="#ffffff", stroke=ORANGE, sw=2)
        s.badge(x + 18, 191, i + 1)
        s.text(x + 36, 196, t, size=12, weight=800)
        if i < 3:
            s.line(x + 148, 191, x + 164, 191, stroke=ORANGE, sw=2, arrow=True)
    s.save(os.path.join(W, "images", "service-plan.svg"))


def form_sheet():
    s = Svg(680, 260)
    s.rect(20, 14, 260, 232, rx=12, fill="#ffffff", stroke=LINE)
    s.rect(20, 14, 260, 40, rx=12, fill="#e3fafc", stroke=None)
    s.text(34, 40, "Mona's Cakes: order", size=14, weight=800)
    qs = [("Which cake?", "Choice"), ("How many cakes?", "Number"), ("Pick-up day", "Date")]
    for i, (q, t) in enumerate(qs):
        y = 70 + i * 52
        s.text(34, y, q, size=12.5, weight=800)
        s.rect(34, y + 8, 160, 24, rx=6, fill=GREY_BG, stroke=LINE)
        s.text(200, y + 25, t, size=11.5, fill=BLUE, weight=800)
    s.rect(34, 220, 70, 20, rx=6, fill=BLUE, stroke=None)
    s.text(69, 234, "Submit", size=11, fill="#ffffff", anchor="middle", weight=800)
    s.line(292, 130, 340, 130, stroke=INK, sw=2, arrow=True)
    s.text(316, 118, "1 response", size=11, anchor="middle", fill=MUTED, weight=800)
    s.text(316, 150, "= 1 row", size=11, anchor="middle", fill=MUTED, weight=800)
    s.text(350, 40, "The sheet (Excel)", size=14, weight=800, fill=EXCEL)
    table(s, 350, 52, ["ID", "Which cake?", "How many?", "Day"], [[1, "Chocolate", 2, "20/11"], [2, "Lemon", 1, "21/11"], [3, "Fruit", 3, "21/11"]],
          [34, 100, 84, 62], hi_row=0)
    s.save(os.path.join(W, "images", "form-sheet.svg"))


def poster(name, title, hint, task, body, h=360):
    s = Svg(640, h)
    poster_head(s, title, hint, task)
    body(s)
    s.save(os.path.join(W, "sims", name + ".svg"))


if __name__ == "__main__":
    service_kinds()
    service_plan()
    form_sheet()
    poster("service-sorter", "Service Sorter: which kind of digital service?", "Read each service and choose its kind.",
           "Service 1 of 8: which kind is it?",
           lambda s: (s.rect(24, 116, 560, 50, rx=14, fill="#ffffff", stroke=LINE),
                      s.text(38, 146, "Sunrise Shop online: choose notebooks and bags, pay, and get them at home.", size=12, weight=700),
                      choices(s, 184, ["online store", "booking", "online form", "digital product"])), h=240)
    poster("service-planner", "Service Planner: the customer, the need, the steps", "Plan a digital service in three parts.",
           "1 · Who is the customer?",
           lambda s: [s.rect(24, 116 + 40 * i, 420, 32, rx=8, fill="#ffffff", stroke=ORANGE) for i in range(3)] +
                     [s.text(38, 137 + 40 * i, t, size=12.5, fill=ORANGE, weight=800) for i, t in
                      enumerate(["families who want a cake for a party", "the bank", "Mona's oven"])], h=250)
    poster("form-builder", "Form Builder: an order form and its sheet", "Give each question its type, then send a test order.",
           "Choose the right type for each question.",
           lambda s: [(s.rect(24, 114 + 50 * i, 520, 42, rx=10, fill="#ffffff", stroke=LINE),
                       s.text(38, 140 + 50 * i, "%d. %s" % (i + 1, q), size=12.5, weight=800),
                       choices(s, 120 + 50 * i, ["Text", "Choice", "Number", "Date"], x0=250))
                      for i, q in enumerate(["Your name", "Which cake?", "How many cakes?", "Pick-up day"])], h=330)
    s = Svg(640, 360)
    s.text(24, 34, "Service Desk at Sunrise Company", size=21, weight=800)
    s.text(24, 56, "Help your colleagues to plan their digital services.", size=12, fill=MUTED)
    s.text(24, 88, "Message 1 / 8", size=13, weight=800)
    s.text(616, 88, "0 stars", size=13, fill=ORANGE, anchor="end", weight=800)
    s.rect(24, 102, 560, 74, rx=14, fill=SOFT, stroke=PEACH)
    s.text(38, 122, "Omar (shop)", size=10.5, fill=MUTED, weight=700)
    s.lines(38, 142, ["Customers want to buy our notebooks online and pay by", "card. Which kind of digital service is it?"], size=12.5, weight=800, gap=18)
    for i, t in enumerate(["an online store", "a booking", "a digital product"]):
        y = 194 + i * 42
        s.rect(24, y, 592, 34, rx=10, fill="#ffffff", stroke=ORANGE)
        s.text(38, y + 22, t, size=13, fill=ORANGE, weight=800)
    s.save(os.path.join(W, "sims", "service-desk.svg"))
