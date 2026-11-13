#!/usr/bin/env python3
"""Figures and posters of Digital Skills Unit 10 (week-14, e-marketing)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Svg, INK, MUTED, LINE, ORANGE, PEACH, SOFT, GREEN, BLUE, GREY_BG
from figs_u3 import poster_head
from figs_u7 import table
from figs_u8 import icon_form

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = os.path.join(ROOT, "courses", "digital-skills", "week-14")


def message_parts():
    s = Svg(700, 230)
    s.rect(14, 60, 170, 110, rx=14, fill=SOFT, stroke=PEACH)
    s.person(70, 104, c=ORANGE, r=14)
    s.person(110, 108, c="#e67700", r=11)
    s.text(99, 146, "The audience", size=13, anchor="middle", weight=800)
    s.text(99, 162, "families in Amman", size=11, anchor="middle", fill=MUTED, weight=700)
    s.line(190, 115, 236, 115, stroke=INK, sw=2, arrow=True)
    s.rect(244, 14, 440, 200, rx=14, fill="#ffffff", stroke=LINE)
    rows = [("headline", "A birthday cake made at home"), ("benefit", "Fresh, made on the day, in Amman"),
            ("offer", "10% off this week"), ("call to action", "Order now: tap the link")]
    for i, (lab, t) in enumerate(rows):
        y = 34 + 46 * i
        s.rect(258, y, 120, 32, rx=8, fill=SOFT, stroke=PEACH)
        s.text(318, y + 21, lab, size=12, anchor="middle", weight=800, fill=ORANGE)
        s.text(392, y + 21, t, size=12.5, weight=800 if i == 3 else 700, fill=(ORANGE if i == 3 else INK))
    s.save(os.path.join(W, "images", "message-parts.svg"))


def channels():
    s = Svg(700, 200)
    items = [("search engines", "people who search", "free map listing"), ("social media", "photos for followers", "free"),
             ("e-mail", "people who know you", "free"), ("paid ads", "chosen people, fast", "you pay")]
    for i, (t, a, b) in enumerate(items):
        x = 14 + i * 170
        s.rect(x, 14, 158, 172, rx=14, fill=SOFT, stroke=PEACH)
        cx, cy = x + 79, 64
        if i == 0:
            s.circle(cx - 4, cy - 4, 15, fill="#ffffff", stroke=ORANGE, sw=3); s.line(cx + 7, cy + 7, cx + 18, cy + 18, stroke=ORANGE, sw=4)
        elif i == 1:
            s.rect(cx - 22, cy - 20, 44, 40, rx=10, fill="#ffffff", stroke=ORANGE, sw=3); s.circle(cx, cy, 9, fill="#ffffff", stroke=ORANGE, sw=3)
        elif i == 2:
            s.rect(cx - 24, cy - 16, 48, 32, rx=4, fill="#ffffff", stroke=ORANGE, sw=3)
            s.poly([(cx - 24, cy - 16), (cx, cy + 4), (cx + 24, cy - 16)], stroke=ORANGE, sw=3, close=False)
        else:
            s.rect(cx - 24, cy - 14, 48, 28, rx=4, fill="#ffffff", stroke=ORANGE, sw=3); s.text(cx, cy + 6, "Ad", size=16, anchor="middle", weight=800, fill=ORANGE)
        s.text(x + 79, 122, t, size=14, anchor="middle", weight=800)
        s.text(x + 79, 144, a, size=11.5, anchor="middle", fill=MUTED, weight=700)
        s.text(x + 79, 164, b, size=11.5, anchor="middle", fill=(GREEN if b != "you pay" else ORANGE), weight=800)
    s.save(os.path.join(W, "images", "channels.svg"))


def post_results():
    s = Svg(700, 220)
    for i, (n, v, c, o, r) in enumerate([("Post A", 1000, 20, 3, 2), ("Post B", 500, 25, 6, 5)]):
        x = 14 + i * 350
        s.rect(x, 14, 330, 192, rx=14, fill="#ffffff", stroke=(GREEN if i else LINE), sw=(2.5 if i else 1.5))
        s.rect(x + 14, 28, 120, 120, rx=10, fill="#ffd8a8", stroke=None)
        s.text(x + 74, 92, n, size=15, anchor="middle", weight=800, fill="#7a3a00")
        for k, (lab, val) in enumerate([("views", v), ("clicks", c), ("orders", o)]):
            s.text(x + 150, 52 + 28 * k, "%s: %s" % (lab, val), size=13, weight=700)
        s.text(x + 150, 140, "%d clicks for" % r, size=13, weight=800, fill=(GREEN if i else ORANGE))
        s.text(x + 150, 158, "every 100 views", size=13, weight=800, fill=(GREEN if i else ORANGE))
        s.text(x + 165, 192, "%d ÷ %d × 100 = %d" % (c, v, r), size=12, anchor="middle", fill=MUTED, weight=700)
    s.tick(676, 30)
    s.save(os.path.join(W, "images", "post-results.svg"))


def quiz_poster(name, title, hint, task, opts, h=280, extra=None):
    s = Svg(640, h)
    poster_head(s, title, hint, task)
    for i, t in enumerate(opts):
        y = 114 + 40 * i
        s.rect(24, y, 592, 32, rx=10, fill="#ffffff", stroke=ORANGE)
        s.text(38, y + 21, t, size=12.5, fill=ORANGE, weight=800)
    if extra:
        extra(s)
    s.save(os.path.join(W, "sims", name + ".svg"))


if __name__ == "__main__":
    message_parts()
    channels()
    post_results()
    quiz_poster("message-builder", "Message Builder: the right message", "Build Mona's post for families in Amman, part by part.",
                "Part 1 of 5: Who is the audience?", ["everybody in the world", "other cake shops", "families in Amman with a birthday soon"])
    quiz_poster("channel-mixer", "Channel Mixer: the right channel for the goal", "Choose the best channel for each goal.",
                "Goal 1 of 4: people search \"cakes Amman\". Mona wants to appear there.",
                ["an e-mail to old customers", "a printed poster", "a search engine (and a map listing)"])
    quiz_poster("results-reader", "Results Reader: which post worked better?", "Read the results: views, clicks, orders.",
                "Question 1 of 4: post A: 1000 views, 20 clicks. Clicks for every 100 views?", ["20", "50", "2"], h=330,
                extra=lambda s: table(s, 24, 240, ["", "Views", "Clicks", "Orders"], [["Post A", 1000, 20, 3]], [90, 90, 90, 90]))
    quiz_poster("product-page-lab", "Product Page Lab: a page that sells", "Build the product page of the lemon cake, part by part.",
                "Part 1 of 5: Which product name?", ["Product 17", "A very very nice cake", "Lemon cake, 1 kg"])
    quiz_poster("picture-rights", "Picture Rights: may I use this picture?", "A picture belongs to the person who made it.",
                "Picture 1 of 5: a photo that Mona took of her own cake.", ["no", "yes"])
    quiz_poster("plan-builder", "Plan Builder: a short marketing plan", "Goal, audience, message, channels, budget, measure.",
                "Row 1 of 6: the goal (a number and a time):", ["be famous", "more", "40 orders in December"])
    s = Svg(640, 360)
    s.text(24, 34, "Market Desk at Sunrise Company", size=21, weight=800)
    s.text(24, 56, "Help your colleagues to market their services online.", size=12, fill=MUTED)
    s.text(24, 88, "Message 1 / 8", size=13, weight=800)
    s.text(616, 88, "0 stars", size=13, fill=ORANGE, anchor="end", weight=800)
    s.rect(24, 102, 560, 56, rx=14, fill=SOFT, stroke=PEACH)
    s.text(38, 122, "Omar (shop)", size=10.5, fill=MUTED, weight=700)
    s.text(38, 144, "Who is the audience of our new school bags?", size=12.5, weight=800)
    for i, t in enumerate(["parents and students before the school year", "everybody", "other shops"]):
        y = 176 + i * 42
        s.rect(24, y, 592, 34, rx=10, fill="#ffffff", stroke=ORANGE)
        s.text(38, y + 22, t, size=13, fill=ORANGE, weight=800)
    s.save(os.path.join(W, "sims", "market-desk.svg"))
