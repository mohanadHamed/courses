#!/usr/bin/env python3
"""Draw the screens of Google BigQuery (Google Cloud console) for the lab
worksheets of Big Data and Data Analysis (courses/big-data, Labs 1-3).

The worksheet is a guide (the lab model, courses/big-data/NOTES.md): every
step shows its screen, drawn close to BigQuery Studio in Chrome on Windows
(late 2026), without logos. A numbered orange circle marks what to click.
The numbers in the tables are examples close to the real public tables.

Every screen is a function below, listed in SCREENS. Run from the project root:

    python3 tools/bq_screens.py            # every SVG and its PNG
    python3 tools/bq_screens.py --svg      # the SVGs only
    python3 tools/bq_screens.py bq-query   # only the screens whose name has "bq-query"
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phone_screens import INK, GREY, LIGHT  # noqa: E402
import lab_screens  # noqa: E402
from lab_screens import W, browser, mark_box, note, draw, export_png  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "courses/big-data/"     # + "week-WW/images/<name>" (the keys of SCREENS)

BLUE = "#1a73e8"              # the buttons of Google Cloud
BLUE_SOFT = "#e8f0fe"
EDGE = "#dadce0"
PANE = "#f8f9fa"
CODE = "#3c4043"
GREEN = "#188038"

TABLE = "bigquery-public-data.chicago_taxi_trips.taxi_trips"
QUERY_YEAR = ["SELECT EXTRACT(YEAR FROM trip_start_timestamp) AS year,",
              "  COUNT(*) AS trips",
              "FROM `%s`" % TABLE,
              "GROUP BY year",
              "ORDER BY year;"]
QUERY_PAY = ["SELECT payment_type, COUNT(*) AS trips",
             "FROM `%s`" % TABLE,
             "GROUP BY payment_type",
             "ORDER BY trips DESC;"]
# Example numbers (close to the real table, which ends in 2023).
YEARS = [("2013", "27,217,716"), ("2014", "37,395,436"), ("2015", "32,385,875"), ("2016", "31,759,339"),
         ("2017", "24,988,003"), ("2018", "20,732,088"), ("2019", "16,477,365"), ("2020", "3,889,032")]
PAYS = [("Cash", "100,218,417"), ("Credit Card", "84,320,995"), ("Unknown", "7,936,210"),
        ("Mobile", "5,016,447"), ("Prcard", "4,731,203"), ("No Charge", "1,105,718")]


# ---------- The console ------------------------------------------------------

def btn(s, x, y, w, label, primary=True, h=30):
    s.rect(x, y, w, h, fill=BLUE if primary else "#ffffff", stroke=None if primary else EDGE, sw=1, rx=4)
    s.text(x + w / 2, y + h / 2 + 4.5, label, 13, 600, "#ffffff" if primary else BLUE, "middle")
    return (x, y, w, h)


def console(s, h, project="big-data-lab", sandbox=True, address="console.cloud.google.com/bigquery"):
    """Chrome with the Google Cloud console: the top bar (project, search, profile)."""
    browser(s, h, address, "BigQuery – Google Cloud")
    s.rect(15, 85, W - 30, 44, fill="#ffffff")
    s.line(15, 129, W - 15, 129, EDGE, 1)
    for i in range(3):
        s.line(30, 100 + i * 6, 44, 100 + i * 6, GREY, 2)
    s.text(56, 112, "Google Cloud", 15, 600, GREY)
    s.rect(160, 95, 150, 26, fill="#ffffff", stroke=EDGE, sw=1, rx=4)
    s.text(172, 112.5, project, 12.5, 600, INK)
    s.path("M292 105 l5 5 l5 -5", stroke=GREY, sw=1.6)
    s.rect(324, 95, 380, 26, fill=PANE, stroke=EDGE, sw=1, rx=4)
    s.text(340, 112.5, "Search (/) for resources, docs, products, and more", 12, 400, LIGHT)
    s.circle(860, 108, 13, fill="#7048e8")
    s.text(860, 113, "S", 13, 700, "#ffffff", "middle")
    y = 129
    if sandbox:
        s.rect(15, y, W - 30, 28, fill="#fef7e0")
        s.text(30, y + 18.5, "Sandbox: you are using BigQuery for free, with limits.", 12.5, 400, INK)
        s.text(W - 30, y + 18.5, "Upgrade", 12.5, 700, BLUE, "end")
        y += 28
    return y


def rail(s, y, h):
    """The thin column of BigQuery icons on the left (Studio is active)."""
    s.rect(15, y, 42, h - y - 15, fill=PANE)
    s.line(57, y, 57, h - 15, EDGE, 1)
    for i in range(5):
        cy = y + 22 + i * 38
        s.rect(26, cy - 10, 20, 20, fill=BLUE_SOFT if i == 0 else "none", stroke=BLUE if i == 0 else LIGHT, sw=1.5, rx=4)


def explorer(s, y, h, tree=(), sel=None, x=57, w=250):
    """The Explorer pane: its search box, Add data, and the tree of projects."""
    s.rect(x, y, w, h - y - 15, fill="#ffffff")
    s.line(x + w, y, x + w, h - 15, EDGE, 1)
    s.text(x + 14, y + 26, "Explorer", 15, 700, INK)
    add = (x + w - 98, y + 10, 86, 26)
    s.rect(*add, fill="#ffffff", stroke=EDGE, sw=1, rx=4)
    s.text(add[0] + 43, add[1] + 17.5, "+ Add data", 12.5, 600, BLUE, "middle")
    s.rect(x + 12, y + 46, w - 24, 26, fill=PANE, stroke=EDGE, sw=1, rx=4)
    s.text(x + 24, y + 63, "Search BigQuery resources", 12, 400, LIGHT)
    boxes = {}
    ty = y + 98
    for depth, label, kind in tree:
        tx = x + 16 + depth * 16
        if label == sel:
            s.rect(x + 4, ty - 16, w - 8, 24, fill=BLUE_SOFT, rx=4)
        s.path("M%g %g l4 4 l-4 4" % (tx, ty - 9), stroke=GREY, sw=1.4) if kind != "table" else None
        ix = tx + 12
        if kind == "project":
            s.rect(ix, ty - 11, 12, 12, fill="none", stroke=GREY, sw=1.4, rx=2)
        elif kind == "dataset":
            s.rect(ix, ty - 11, 13, 11, fill="none", stroke=GREY, sw=1.4, rx=1)
            s.line(ix, ty - 7, ix + 13, ty - 7, GREY, 1)
        else:
            s.rect(ix, ty - 11, 12, 12, fill="none", stroke=GREY, sw=1.2, rx=1)
            s.line(ix, ty - 7, ix + 12, ty - 7, GREY, 1)
            s.line(ix + 6, ty - 7, ix + 6, ty + 1, GREY, 1)
        s.text(ix + 20, ty, label, 12.5, 700 if label == sel else 400, INK)
        boxes[label] = (ix - 2, ty - 14, min(w - (ix - x) - 10, 7.2 * len(label) + 26), 20)
        ty += 28
    return add, boxes


PUBLIC_TREE = [(0, "big-data-lab", "project"), (0, "bigquery-public-data", "project"),
               (1, "chicago_taxi_trips", "dataset"), (2, "taxi_trips", "table")]


def main_tabs(s, x, y, tabs, active):
    """The tabs of the work area (a table, Untitled query)."""
    s.rect(x, y, W - 15 - x, 34, fill=PANE)
    s.line(x, y + 34, W - 15, y + 34, EDGE, 1)
    cx = x + 6
    boxes = {}
    for t in tabs:
        w = 9 * len(t) + 34
        if t == active:
            s.rect(cx, y + 4, w, 30, fill="#ffffff", stroke=EDGE, sw=1, rx=4)
            s.rect(cx + 1, y + 31, w - 2, 4, fill="#ffffff")
        s.text(cx + 14, y + 24, t, 12.5, 600 if t == active else 400, INK if t == active else GREY)
        s.text(cx + w - 14, y + 24, "×", 13, 400, LIGHT)
        boxes[t] = (cx, y + 4, w, 30)
        cx += w + 4
    return boxes


def sub_tabs(s, x, y, tabs, active):
    """Schema, Details, Preview … (a table) or Job information, Results … (a query)."""
    boxes = {}
    cx = x
    for t in tabs:
        w = 7.4 * len(t) + 22
        if t == active:
            s.rect(cx, y + 26, w, 3, fill=BLUE)
        s.text(cx + w / 2, y + 18, t.upper(), 11.5, 700, BLUE if t == active else GREY, "middle")
        boxes[t] = (cx, y, w, 30)
        cx += w + 6
    s.line(x, y + 29, W - 15, y + 29, EDGE, 1)
    return boxes


def table_toolbar(s, x, y, name="taxi_trips"):
    s.text(x, y + 22, name, 18, 600, INK)
    q = (x + 130, y + 6, 92, 26)
    s.rect(*q, fill="#ffffff", stroke=EDGE, sw=1, rx=4)
    s.text(q[0] + 14, q[1] + 17.5, "Query", 12.5, 600, BLUE)
    s.path("M%g %g l4 4 l4 -4" % (q[0] + 72, q[1] + 11), stroke=BLUE, sw=1.6)
    for i, t in enumerate(("Share", "Copy", "Snapshot", "Delete", "Export")):
        s.text(x + 240 + i * 66, y + 23, t, 12.5, 600, BLUE)
    return q


def grid(s, x, y, head, rows, widths, rh=24, num=True):
    s.rect(x, y, sum(widths) + (34 if num else 0), rh, fill=PANE)
    cx = x
    if num:
        s.text(cx + 8, y + 16, "Row", 11.5, 700, GREY)
        cx += 34
    for hd, w in zip(head, widths):
        s.text(cx + 8, y + 16, hd, 11.5, 700, INK)
        cx += w
    for r, row in enumerate(rows):
        ry = y + rh * (r + 1)
        s.line(x, ry, x + sum(widths) + (34 if num else 0), ry, EDGE, 1)
        cx = x
        if num:
            s.text(cx + 8, ry + 16, str(r + 1), 11.5, 400, GREY)
            cx += 34
        for v, w in zip(row, widths):
            s.text(cx + 8, ry + 16, v, 11.5, 400, INK)
            cx += w
    return y + rh * (len(rows) + 1)


def editor(s, x, y, w, lines, h=None):
    h = h or 30 + 20 * len(lines)
    s.rect(x, y, w, h, fill="#ffffff", stroke=EDGE, sw=1)
    for i, ln in enumerate(lines):
        s.text(x + 10, y + 22 + 20 * i, str(i + 1), 11.5, 400, LIGHT, "end" if False else "start")
        s.text(x + 34, y + 22 + 20 * i, ln, 12.5, 400, CODE)
    return (x, y, w, h)


def query_bar(s, x, y, valid="1.55 GB"):
    run = (x, y, 72, 28)
    s.rect(*run, fill=BLUE, rx=4)
    s.path("M%g %g l9 5.5 l-9 5.5 z" % (x + 12, y + 8.5), fill="#ffffff")
    s.text(x + 46, y + 18.5, "Run", 13, 700, "#ffffff", "middle")
    for i, t in enumerate(("Save", "Share")):
        s.text(x + 96 + i * 62, y + 19, t, 12.5, 600, GREY)
    vbox = None
    if valid:
        s.circle(W - 300, y + 14, 8, fill=GREEN)
        s.path("M%g %g l3 3 l5 -6" % (W - 304, y + 14), stroke="#ffffff", sw=1.8)
        msg = "This query will process %s when run." % valid
        s.text(W - 286, y + 18.5, msg, 12, 400, INK)
        vbox = (W - 312, y + 2, 284, 24)
    return run, vbox


# ---------- Lab 1: the screens ------------------------------------------------

def bq_open(s, top):
    """Chrome: type the address of BigQuery."""
    h = 210
    browser(s, h, "console.cloud.google.com/bigquery", "New Tab")
    s.rect(15, 85, W - 30, h - 100, fill="#ffffff")
    s.text(W / 2, 150, "Type the address, then press Enter.", 15, 400, GREY, "middle")
    mark_box(top, (30, 54, 330, 24), 1, "bottom", 12, 3)
    note(top, 380, 54, 120, "press Enter")


def bq_signin(s, top):
    """The Google sign-in page: the e-mail, Next, then the password."""
    h = 420
    browser(s, h, "accounts.google.com", "Sign in – Google Accounts")
    s.rect(15, 85, W - 30, h - 100, fill="#f0f4f9")
    s.rect(130, 110, 640, 280, fill="#ffffff", rx=24)
    s.text(170, 165, "Sign in", 28, 400, INK)
    s.text(170, 195, "with your Google Account.", 14, 400, GREY)
    field = (470, 150, 270, 50)
    s.rect(*field, fill="#ffffff", stroke=BLUE, sw=2, rx=5)
    s.text(486, 181, "sara.student@gmail.com", 14, 400, INK)
    s.text(478, 146, "Email or phone", 11.5, 400, BLUE)
    s.text(470, 228, "Forgot email?", 13, 600, BLUE)
    s.text(560, 340, "Create account", 13, 600, BLUE, "end")
    nxt = btn(s, 660, 322, 80, "Next", h=32)
    mark_box(top, field, 1, "left", 6, 3)
    mark_box(top, nxt, 2, "bottom", 6, 3)
    top.label(150, 312, 300, "then your password, then Next")


def bq_welcome(s, top):
    """The first visit: choose the country, agree to the terms."""
    h = 430
    y = console(s, h, project="Select a project", sandbox=False)
    s.rect(15, y, W - 30, h - y - 15, fill=PANE)
    s.rect(150, y + 22, 600, 250, fill="#ffffff", stroke=EDGE, sw=1, rx=8)
    s.text(176, y + 60, "Welcome Sara!", 22, 400, INK)
    s.text(176, y + 86, "Create and manage your Google Cloud resources from one place.", 13, 400, GREY)
    s.text(176, y + 116, "Country", 11.5, 400, GREY)
    country = (176, y + 122, 260, 34)
    s.rect(*country, fill="#ffffff", stroke=EDGE, sw=1, rx=4)
    s.text(188, y + 144, "Jordan", 14, 400, INK)
    s.path("M%g %g l5 5 l5 -5" % (414, y + 136), stroke=GREY, sw=1.6)
    tick = (176, y + 172, 16, 16)
    s.rect(*tick, fill=BLUE, rx=2)
    s.path("M%g %g l4 4 l7 -8" % (179, y + 180), stroke="#ffffff", sw=2)
    s.text(202, y + 185, "I agree to the Google Cloud Platform Terms of Service.", 13, 400, INK)
    agree = btn(s, 176, y + 212, 170, "AGREE AND CONTINUE", h=32)
    mark_box(top, country, 1, "right", 6, 3)
    mark_box(top, tick, 2, "left", 4, 4)
    mark_box(top, agree, 3, "right", 6, 3)


def bq_create(s, top):
    """BigQuery without a project: Create project."""
    h = 360
    y = console(s, h, project="Select a project", sandbox=False)
    rail(s, y, h)
    s.rect(58, y, W - 73, h - y - 15, fill="#ffffff")
    s.text(100, y + 60, "Welcome to BigQuery Studio", 22, 400, INK)
    s.text(100, y + 90, "To start, create a project. It is free: the BigQuery sandbox needs no card.", 13.5, 400, GREY)
    cp = btn(s, 100, y + 118, 140, "Create project", h=32)
    mark_box(top, cp, 1, "right", 6, 3)


def bq_new_project(s, top):
    """New Project: the name, No organization, Create."""
    h = 460
    y = console(s, h, project="Select a project", sandbox=False, address="console.cloud.google.com/projectcreate")
    s.rect(15, y, W - 30, h - y - 15, fill="#ffffff")
    s.text(40, y + 40, "New Project", 22, 400, INK)
    s.text(60, y + 80, "Project name *", 11.5, 400, BLUE)
    name = (60, y + 86, 360, 38)
    s.rect(*name, fill="#ffffff", stroke=BLUE, sw=2, rx=4)
    s.text(74, y + 111, "big-data-lab", 14, 400, INK)
    s.text(60, y + 142, "Project ID: big-data-lab-4821 (Google adds the numbers)", 12, 400, GREY)
    s.text(60, y + 176, "Organization", 11.5, 400, GREY)
    org = (60, y + 182, 360, 38)
    s.rect(*org, fill="#ffffff", stroke=EDGE, sw=1, rx=4)
    s.text(74, y + 207, "No organization", 14, 400, INK)
    s.path("M%g %g l5 5 l-5 0" % (398, y + 198), stroke=None)
    s.path("M%g %g l5 5 l5 -5" % (395, y + 197), stroke=GREY, sw=1.6)
    create = btn(s, 60, y + 246, 90, "CREATE", h=34)
    s.text(176, y + 268, "CANCEL", 13, 600, BLUE)
    mark_box(top, name, 1, "right", 6, 3)
    mark_box(top, org, 2, "right", 6, 3)
    mark_box(top, create, 3, "right", 6, 3)


def bq_home(s, top):
    """BigQuery Studio in the new project: the sandbox notice."""
    h = 400
    y = console(s, h)
    rail(s, y, h)
    explorer(s, y, h, [(0, "big-data-lab", "project")])
    x = 308
    s.text(x + 30, y + 50, "BigQuery Studio", 22, 400, INK)
    s.text(x + 30, y + 78, "Create new", 13, 700, GREY)
    for i, t in enumerate(("SQL query", "Notebook", "Data canvas")):
        s.rect(x + 30 + i * 150, y + 90, 138, 60, fill="#ffffff", stroke=EDGE, sw=1, rx=8)
        s.text(x + 99 + i * 150, y + 125, t, 13, 600, BLUE, "middle")
    mark_box(top, (20, 132, 520, 22), 1, "bottom", 6, 3)
    mark_box(top, (160, 95, 150, 26), 2, "bottom", 6, 3)


def bq_add_data(s, top):
    """Explorer: + Add data, then Public datasets."""
    h = 470
    y = console(s, h)
    rail(s, y, h)
    add, _ = explorer(s, y, h, [(0, "big-data-lab", "project")])
    s.rect(308, y, W - 323, h - y - 15, fill="#5f6368", opacity=0.35)
    dx, dy = 360, y + 30
    s.rect(dx, dy, 480, 250, fill="#ffffff", rx=8)
    s.text(dx + 24, dy + 38, "Add data", 20, 400, INK)
    s.text(dx + 24, dy + 64, "Choose where your data comes from.", 13, 400, GREY)
    items = [("Local file", "Upload a CSV or JSON file"), ("Google Cloud Storage", "Load files from a bucket"),
             ("Public datasets", "Free data that Google and others share")]
    pub = None
    for i, (a, b) in enumerate(items):
        iy = dy + 84 + i * 52
        s.rect(dx + 20, iy, 440, 44, fill=BLUE_SOFT if i == 2 else "#ffffff", stroke=EDGE, sw=1, rx=6)
        s.text(dx + 36, iy + 19, a, 13.5, 700, INK)
        s.text(dx + 36, iy + 35, b, 11.5, 400, GREY)
        if i == 2:
            pub = (dx + 20, iy, 440, 44)
    mark_box(top, add, 1, "bottom", 6, 3)
    mark_box(top, pub, 2, "right", 6, 3)


def bq_market(s, top):
    """Marketplace: search Chicago Taxi Trips, open it, View dataset."""
    h = 430
    browser(s, h, "console.cloud.google.com/marketplace", "Marketplace – Google Cloud")
    s.rect(15, 85, W - 30, h - 100, fill="#ffffff")
    s.text(40, 125, "Marketplace", 20, 400, INK)
    search = (40, 140, 420, 34)
    s.rect(*search, fill="#ffffff", stroke=BLUE, sw=2, rx=4)
    s.text(56, 162, "chicago taxi", 14, 400, INK)
    card = (40, 192, 420, 92)
    s.rect(*card, fill="#ffffff", stroke=EDGE, sw=1, rx=8)
    s.rect(56, 208, 44, 44, fill="#fff3bf", rx=6)
    s.text(116, 222, "Chicago Taxi Trips", 15, 700, INK)
    s.text(116, 242, "City of Chicago", 12.5, 400, GREY)
    s.text(116, 264, "Taxi trips in Chicago, from 2013. Public dataset.", 12, 400, GREY)
    s.line(490, 100, 490, h - 30, EDGE, 1)
    s.text(520, 130, "Chicago Taxi Trips", 18, 400, INK)
    s.text(520, 152, "City of Chicago · Datasets", 12.5, 400, GREY)
    view = btn(s, 520, 170, 130, "VIEW DATASET", h=34)
    s.text(520, 240, "Overview", 14, 700, INK)
    for i, t in enumerate(("Every taxi trip reported to the City", "of Chicago: the time, the fare, the",
                           "tip, the payment type and the company.")):
        s.text(520, 264 + i * 19, t, 12.5, 400, GREY)
    mark_box(top, search, 1, "left", 6, 3)
    mark_box(top, card, 2, "left", 8, 3)
    mark_box(top, view, 3, "right", 6, 3)


def bq_tree(s, top):
    """The Explorer shows bigquery-public-data: open chicago_taxi_trips, click taxi_trips."""
    h = 390
    y = console(s, h)
    rail(s, y, h)
    _, boxes = explorer(s, y, h, PUBLIC_TREE, sel="taxi_trips")
    s.rect(308, y, W - 323, h - y - 15, fill="#ffffff")
    s.text(340, y + 60, "Click a table to open it here.", 14, 400, GREY)
    mark_box(top, boxes["chicago_taxi_trips"], 1, "right", 5, 2)
    mark_box(top, boxes["taxi_trips"], 2, "right", 5, 2)


def table_view(s, h, active):
    y = console(s, h)
    rail(s, y, h)
    explorer(s, y, h, PUBLIC_TREE, sel="taxi_trips")
    x = 308
    main_tabs(s, x, y, ["taxi_trips"], "taxi_trips")
    q = table_toolbar(s, x + 16, y + 44)
    tabs = sub_tabs(s, x + 16, y + 84, ["Schema", "Details", "Preview", "Lineage"], active)
    return y + 124, tabs, q


def bq_details(s, top):
    """The Details tab: Number of rows and Total logical bytes."""
    h = 530
    y, tabs, _ = table_view(s, h, "Details")
    x = 330
    s.text(x, y + 26, "Table info", 15, 700, INK)
    for i, (a, b) in enumerate((("Table ID", TABLE), ("Data location", "US"), ("Last modified", "2023"))):
        s.text(x, y + 52 + i * 22, a, 12.5, 400, GREY)
        s.text(x + 150, y + 52 + i * 22, b if len(b) < 46 else b[:44] + "…", 12.5, 400, INK)
    s.text(x, y + 140, "Storage info", 15, 700, INK)
    rows = (x - 6, y + 152, 330, 24)
    for i, (a, b) in enumerate((("Number of rows", "208,943,621"), ("Total logical bytes", "75.12 GB"))):
        s.text(x, y + 168 + i * 26, a, 12.5, 400, GREY)
        s.text(x + 170, y + 168 + i * 26, b, 13, 700, INK)
    mark_box(top, tabs["Details"], 1, "top", 5, 2)
    mark_box(top, (rows[0], rows[1], rows[2], 50), 2, "right", 6, 3)


def bq_schema(s, top):
    """The Schema tab: the columns of the table and their types."""
    h = 470
    y, tabs, _ = table_view(s, h, "Schema")
    rows = [("unique_key", "STRING"), ("taxi_id", "STRING"), ("trip_start_timestamp", "TIMESTAMP"),
            ("trip_seconds", "INTEGER"), ("trip_miles", "FLOAT"), ("fare", "FLOAT"), ("tips", "FLOAT"),
            ("payment_type", "STRING"), ("company", "STRING")]
    grid(s, 330, y + 12, ["Field name", "Type", "Mode"], [(a, b, "NULLABLE") for a, b in rows], (200, 110, 100), rh=22, num=False)
    mark_box(top, tabs["Schema"], 1, "top", 5, 2)


def bq_preview(s, top):
    """The Preview tab: the first rows, free (no query)."""
    h = 400
    y, tabs, _ = table_view(s, h, "Preview")
    rows = [("2016-02-11 08:15", "780", "9.25", "0.00", "Cash", "Taxi Affiliation"),
            ("2016-02-11 08:30", "420", "6.50", "2.00", "Credit Card", "Flash Cab"),
            ("2016-02-11 08:45", "1260", "21.75", "4.00", "Credit Card", "Sun Taxi"),
            ("2016-02-11 09:00", "300", "5.25", "0.00", "Cash", "Taxi Affiliation"),
            ("2016-02-11 09:15", "900", "12.00", "0.00", "Cash", "Medallion"),
            ("2016-02-11 09:15", "660", "8.75", "1.00", "Mobile", "Flash Cab")]
    grid(s, 322, y + 10, ["trip_start_time…", "trip_secon…", "fare", "tips", "payment_type", "company"], rows,
         (122, 72, 50, 44, 90, 112), rh=24)
    mark_box(top, tabs["Preview"], 1, "top", 5, 2)


def query_view(s, h, lines, valid, tabs_active=None):
    y = console(s, h)
    rail(s, y, h)
    explorer(s, y, h, PUBLIC_TREE, sel=None)
    x = 308
    main_tabs(s, x, y, ["taxi_trips", "Untitled query"], "Untitled query")
    run, vbox = query_bar(s, x + 16, y + 44, valid)
    ed = editor(s, x + 16, y + 80, W - 15 - x - 32, lines, h=30 + 20 * 5)
    return y, x, run, vbox, ed


def bq_query(s, top):
    """Table › Query, type the SQL, read the estimate, Run."""
    h = 380
    y, x, run, vbox, ed = query_view(s, h, QUERY_YEAR, "1.55 GB")
    s.text(x + 16, y + 238, "Tip: Query (on the table) opens a new tab with a short query in it. Delete it,", 12, 400, GREY)
    s.text(x + 16, y + 256, "then type the query of the worksheet.", 12, 400, GREY)
    mark_box(top, (ed[0], ed[1], ed[2], 110), 1, "left", 4, 2)
    mark_box(top, vbox, 2, "top", 6, 2)
    mark_box(top, run, 3, "left", 6, 3)


def results(s, h, lines, valid, head, rows, active, widths):
    y, x, run, vbox, ed = query_view(s, h, lines, valid)
    ry = ed[1] + ed[3] + 10
    s.text(x + 16, ry + 22, "Query results", 15, 700, INK)
    tabs = sub_tabs(s, x + 16, ry + 30, ["Job information", "Results", "Visualization", "JSON"], active)
    return y, x, ry + 70, tabs


def bq_results(s, top):
    """Query results: one row for each year."""
    h = 690
    y, x, ty, tabs = results(s, h, QUERY_YEAR, "1.55 GB", None, None, "Results", None)
    grid(s, x + 16, ty, ["year", "trips"], YEARS, (90, 130), rh=24)
    mark_box(top, tabs["Results"], 1, "top", 5, 2)
    note(top, x + 300, ty + 60, 250, "one row for each year")


def bq_job(s, top):
    """Job information: Bytes processed and Duration."""
    h = 590
    y, x, ty, tabs = results(s, h, QUERY_YEAR, "1.55 GB", None, None, "Job information", None)
    info = [("Job ID", "big-data-lab-4821:US.bquxjob_1a2b3c"), ("Start time", "Nov 22, 2026, 10:12:04 AM"),
            ("Duration", "2 sec"), ("Bytes processed", "1.55 GB"), ("Bytes billed", "1.55 GB")]
    for i, (a, b) in enumerate(info):
        s.text(x + 16, ty + 14 + i * 24, a, 12.5, 400, GREY)
        s.text(x + 190, ty + 14 + i * 24, b, 12.5, 700 if i in (2, 3) else 400, INK)
    mark_box(top, tabs["Job information"], 1, "left", 5, 2)
    mark_box(top, (x + 10, ty + 44, 300, 50), 2, "right", 6, 3)


def bq_pay(s, top):
    """The second query: trips by payment type."""
    h = 640
    y, x, ty, tabs = results(s, h, QUERY_PAY, "1.32 GB", None, None, "Results", None)
    grid(s, x + 16, ty, ["payment_type", "trips"], PAYS, (130, 130), rh=24)
    note(top, x + 330, ty + 40, 230, "Cash and cards: most trips")


def bq_signout(s, top):
    """Before you leave: the profile picture, Sign out."""
    h = 360
    y = console(s, h)
    s.rect(15, y, W - 30, h - y - 15, fill=PANE)
    mx, my = 560, 128
    s.rect(mx, my, 320, 200, fill="#ffffff", stroke=EDGE, sw=1, rx=10)
    s.circle(mx + 160, my + 46, 24, fill="#7048e8")
    s.text(mx + 160, my + 53, "S", 20, 700, "#ffffff", "middle")
    s.text(mx + 160, my + 96, "sara.student@gmail.com", 13, 400, INK, "middle")
    s.text(mx + 160, my + 124, "Manage your Google Account", 12.5, 600, BLUE, "middle")
    so = (mx + 110, my + 148, 100, 32)
    s.rect(*so, fill="#ffffff", stroke=EDGE, sw=1, rx=16)
    s.text(mx + 160, my + 169, "Sign out", 13, 600, INK, "middle")
    top.ring_circle(860, 108, 17)
    top.mark(1, 830, 108)
    mark_box(top, so, 2, "left", 16, 3)


def cluster_poster(s, top):
    """The poster of Cluster Lab: one computer with 600 blocks, and a cluster that shares them."""
    h = 400
    s.rect(0, 0, W, h, fill="#fff5f5", rx=18)
    s.text(40, 52, "Cluster Lab: one computer or many?", 26, 700, "#a51d1d")
    s.text(40, 82, "A table of 75 GB in 600 blocks. Each computer reads its own blocks.", 15, 400, GREY)
    cols = ["#c92a2a", "#e8590c", "#f08c00", "#2f9e44", "#1971c2", "#7048e8"]

    def pc(x, y, w, blocks, label):
        s.rect(x, y, w, 70, fill="#ffffff", stroke="#ced4da", sw=2, rx=8)
        for i in range(blocks):
            s.rect(x + 8 + (i % 8) * 13, y + 10 + (i // 8) * 13, 10, 10, fill=cols[i % len(cols)], rx=2)
        s.text(x + w / 2, y + 88, label, 13, 600, INK, "middle")
    pc(40, 120, 120, 32, "1 computer")
    s.text(100, 236, "12 min 48 s", 22, 800, "#c92a2a", "middle")
    for r in range(2):
        for c in range(6):
            pc(240 + c * 106, 110 + r * 110, 90, 3, "")
    s.text(560, 336, "100 computers: 7.7 s", 22, 800, "#c92a2a", "middle")
    s.text(560, 362, "each block kept on 3 computers", 14, 400, GREY, "middle")


def query_steps_poster(s, top):
    """The poster of Query Steps: the query with one line lit, and the small table after it."""
    h = 400
    s.rect(0, 0, W, h, fill="#fff5f5", rx=18)
    s.text(40, 50, "Query Steps: what each line does", 26, 700, "#a51d1d")
    s.rect(40, 74, 470, 150, fill="#f8f9fa", stroke=EDGE, sw=1, rx=8)
    for i, ln in enumerate(QUERY_YEAR):
        y = 100 + i * 26
        if i == 3:
            s.rect(41, y - 18, 468, 26, fill="#ffe8cc")
            s.rect(41, y - 18, 4, 26, fill="#d9480f")
        s.text(58, y, str(i + 1), 13, 400, LIGHT)
        s.text(80, y, ln if len(ln) < 52 else ln[:50] + "…", 13, 700 if i == 3 else 400, CODE)
    s.text(40, 262, "GROUP BY year: one group for each year.", 17, 700, INK)
    s.text(40, 290, "Each colour is one group. Then COUNT(*) counts each group.", 15, 400, GREY)
    rows = [("2016-02-11", "2016", "#fff3bf"), ("2016-07-19", "2016", "#fff3bf"), ("2013-05-02", "2013", "#d3f9d8"),
            ("2013-11-30", "2013", "#d3f9d8"), ("2014-01-08", "2014", "#d0ebff"), ("2014-09-14", "2014", "#d0ebff")]
    s.rect(560, 74, 300, 26, fill="#f1f3f5")
    s.text(572, 92, "trip_start_timestamp", 12.5, 700, INK)
    s.text(780, 92, "year", 12.5, 700, INK)
    for i, (a, b, col) in enumerate(rows):
        y = 100 + i * 26
        s.rect(560, y, 300, 26, fill=col, stroke=EDGE, sw=1)
        s.text(572, y + 18, a, 12.5, 400, INK)
        s.text(780, y + 18, b, 12.5, 700, INK)


SCREENS = {
    "week-01/sims/query-steps": (query_steps_poster, (0, 0, W, 330)),
    # The posters of the Lab 1 simulators (week-01/sims)
    "week-01/sims/cluster-lab": (cluster_poster, (0, 0, W, 400)),
    "week-01/sims/bq-lab-find": (bq_details, (0, 86, W, 444)),
    "week-01/sims/bq-lab-query": (bq_results, (290, 86, 610, 604)),
    # Lab 1, a first look at BigQuery (week-01)
    "week-01/images/bq-signin-1": (bq_signin, (100, 86, 700, 324)),
    "week-01/images/bq-welcome-1": (bq_welcome, (120, 86, 660, 330)),
    "week-01/images/bq-project-1": (bq_new_project, (15, 86, 600, 360)),
    "week-01/images/bq-add-1": (bq_add_data, (0, 86, W, 384)),
    "week-01/images/bq-market-1": (bq_market, (0, 0, W, 330)),
    "week-01/images/bq-tree-1": (bq_tree, (0, 86, 620, 290)),
    "week-01/images/bq-details-1": (bq_details, (0, 86, W, 444)),
    "week-01/images/bq-query-1": (bq_query, (290, 86, 610, 294)),
    "week-01/images/bq-results-1": (bq_results, (290, 362, 610, 328)),
    "week-01/images/bq-job-1": (bq_job, (290, 362, 610, 228)),
    "week-01/images/bq-signout-1": (bq_signout, (480, 86, 420, 274)),
}


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
    lab_screens  # the shared helpers of the lab worksheets
    sys.exit(main())
