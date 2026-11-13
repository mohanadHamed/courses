#!/usr/bin/env python3
"""Figures and posters of Digital Skills Unit 7 (week-09, databases), drawn with svgkit."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import Svg, INK, MUTED, LINE, ORANGE, PEACH, SOFT, GREEN, BLUE, ACCESS, GREY_BG
from figs_u3 import poster_head

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = os.path.join(ROOT, "courses", "digital-skills", "week-09")


def table(s, x, y, fields, rows, widths, head_fill=GREY_BG, key=None, hi_row=None, hi_col=None):
    for c, f in enumerate(fields):
        cx = x + sum(widths[:c])
        s.rect(cx, y, widths[c], 26, rx=0, fill=("#fff4e6" if c == hi_col else head_fill), stroke=LINE, sw=1)
        s.text(cx + 8, y + 18, f, size=12, weight=800)
        if key == c:
            s.circle(cx + widths[c] - 14, y + 13, 4.5, fill=None or "#ffffff", stroke="#e67700", sw=2)
            s.line(cx + widths[c] - 10, y + 16, cx + widths[c] - 4, y + 22, stroke="#e67700", sw=2)
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            cx = x + sum(widths[:c])
            fill = "#e7f5ff" if r == hi_row else ("#fff4e6" if c == hi_col else "#ffffff")
            s.rect(cx, y + 26 + 24 * r, widths[c], 24, rx=0, fill=fill, stroke=LINE, sw=1)
            s.text(cx + 8, y + 26 + 24 * r + 16, str(v), size=12, weight=600)


def db_table():
    s = Svg(660, 250)
    s.text(24, 30, "Customers", size=15, weight=800, fill=ACCESS)
    table(s, 24, 42, ["CustomerID", "Name", "City"], [[1, "Huda", "Amman"], [2, "Omar", "Zarqa"], [3, "Lina", "Amman"]],
          [110, 110, 110], hi_row=1, hi_col=2)
    s.line(420, 104, 362, 104, stroke=BLUE, sw=2, arrow=True)
    s.text(428, 100, "a record: one row,", size=12.5, weight=800, fill=BLUE)
    s.text(428, 116, "one customer", size=12.5, weight=800, fill=BLUE)
    s.line(299, 30, 330, 30, stroke=ORANGE, sw=2)
    s.text(340, 34, "a field: one column (City)", size=12.5, weight=800, fill=ORANGE)
    s.text(24, 182, "Data types", size=13, weight=800)
    for i, (t, e) in enumerate([("Short Text", "Huda"), ("Number", "10"), ("Currency", "2.00 JD"), ("Date/Time", "03/11/2026"), ("Yes/No", "Yes")]):
        x = 24 + i * 126
        s.rect(x, 194, 118, 44, rx=8, fill=SOFT, stroke=PEACH)
        s.text(x + 59, 213, t, size=12, anchor="middle", weight=800)
        s.text(x + 59, 230, e, size=11, anchor="middle", fill=MUTED, weight=700)
    s.save(os.path.join(W, "images", "db-table.svg"))


def db_relationship():
    s = Svg(660, 200)
    s.text(24, 26, "Customers", size=14, weight=800, fill=ACCESS)
    table(s, 24, 36, ["CustomerID", "Name", "City"], [[1, "Huda", "Amman"], [2, "Omar", "Zarqa"], [3, "Lina", "Amman"]],
          [124, 66, 70], key=0)
    s.text(330, 26, "Orders", size=14, weight=800, fill=ACCESS)
    table(s, 330, 36, ["OrderID", "CustomerID", "Item", "Total"], [[1, 1, "Notebook", "2.00"], [2, 3, "Bag", "12.00"], [3, 1, "Pen", "0.50"]],
          [90, 96, 74, 60], key=0)
    s.path("M86 128 C 86 175, 468 175, 468 128", stroke=ORANGE, sw=2.5)
    s.text(70, 150, "1", size=16, weight=800, fill=ORANGE)
    s.text(476, 150, "many", size=13, weight=800, fill=ORANGE)
    s.text(280, 192, "one customer, many orders (one-to-many)", size=12.5, anchor="middle", weight=800)
    s.save(os.path.join(W, "images", "db-relationship.svg"))


def db_query():
    s = Svg(660, 220)
    s.text(24, 26, "Query Design", size=14, weight=800, fill=ACCESS)
    rows = [("Field:", "Name", "City"), ("Sort:", "Ascending", ""), ("Criteria:", "", "Amman")]
    for r, (lab, a, b) in enumerate(rows):
        y = 40 + r * 30
        s.text(24, y + 19, lab, size=12, weight=800, fill=MUTED)
        for c, v in enumerate((a, b)):
            x = 100 + c * 120
            s.rect(x, y, 116, 28, rx=0, fill=("#fff4e6" if v in ("Amman", "Ascending") else "#ffffff"), stroke=LINE, sw=1)
            s.text(x + 8, y + 19, v, size=12, weight=700)
    s.rect(100, 140, 70, 30, rx=8, fill=ACCESS, stroke=None)
    s.text(135, 160, "! Run", size=13, fill="#ffffff", anchor="middle", weight=800)
    s.line(360, 90, 400, 90, stroke=INK, sw=2, arrow=True)
    s.text(420, 26, "The result", size=14, weight=800, fill=ACCESS)
    table(s, 420, 36, ["Name", "City"], [["Huda", "Amman"], ["Lina", "Amman"]], [100, 100])
    s.text(420, 140, "2 records. Omar (Zarqa) is", size=12, weight=700, fill=MUTED)
    s.text(420, 156, "still in the table.", size=12, weight=700, fill=MUTED)
    s.save(os.path.join(W, "images", "db-query.svg"))


def poster_simple(name, title, hint, task, body):
    s = Svg(640, 360)
    poster_head(s, title, hint, task)
    body(s)
    s.save(os.path.join(W, "sims", name + ".svg"))


def choices(s, y, labels, x0=24):
    x = x0
    for t in labels:
        w = 18 + 8 * len(t)
        s.rect(x, y, w, 30, rx=8, fill="#ffffff", stroke=ORANGE)
        s.text(x + w / 2, y + 20, t, size=12.5, fill=ORANGE, anchor="middle", weight=800)
        x += w + 8


PRODUCTS = [[1, "Notebook", "Paper", "2.00", "Yes"], [2, "Pen", "Paper", "0.50", "Yes"], [3, "Bag", "Bags", "12.00", "Yes"],
            [4, "Water", "Drinks", "0.50", "No"], [5, "Juice", "Drinks", "1.00", "Yes"]]

if __name__ == "__main__":
    db_table()
    db_relationship()
    db_query()
    poster_simple("field-lab", "Field Lab: the right data type", "Read the field and its examples, then choose its type.",
                  "Field 1 of 6: which data type?",
                  lambda s: (s.rect(24, 116, 400, 56, rx=14, fill="#ffffff", stroke=LINE), s.text(38, 140, "Name", size=14, weight=800),
                             s.text(38, 160, "Examples: Huda · Omar · Lina", size=12, fill=MUTED),
                             choices(s, 188, ["Short Text", "Number", "Currency", "Date/Time", "Yes/No"])))
    poster_simple("key-lab", "Key Lab: the primary key and the relationship", "A primary key has a different value in every record.",
                  "Task 1 of 4: choose the primary key of the Customers table.",
                  lambda s: (table(s, 24, 116, ["CustomerID", "Name", "City"], [[1, "Huda", "Amman"], [2, "Omar", "Zarqa"], [3, "Lina", "Amman"], [4, "Huda", "Irbid"]], [110, 100, 100]),
                             choices(s, 250, ["CustomerID", "Name", "City"])))
    poster_simple("query-lab", "Query Lab: ask the table a question", "Choose a criterion and a sort, then press Run.",
                  "Task 1: show only the products of the type Drinks.",
                  lambda s: (s.text(24, 132, "Criterion:  (none)   =", size=12.5, weight=800), s.text(24, 156, "Sort:  (none)   Ascending", size=12.5, weight=800),
                             table(s, 24, 172, ["ProductID", "Name", "Type", "Price", "InStock"], PRODUCTS, [80, 100, 80, 70, 70])))
    poster_simple("form-lab", "Form Lab: one record at a time", "A form shows one record of a table at a time, in big boxes.",
                  "Task 1 of 2: use the arrow to go to record 7. Which product is it?",
                  lambda s: [s.rect(24, 116, 380, 220, rx=14, fill=GREY_BG, stroke=LINE)] + [
                      (s.text(40, 150 + 34 * i, f, size=12.5, weight=800), s.rect(140, 134 + 34 * i, 240, 26, rx=6, fill="#ffffff", stroke=LINE),
                       s.text(150, 152 + 34 * i, v, size=12.5, weight=700))
                      for i, (f, v) in enumerate([("ProductID", "1"), ("Name", "Notebook"), ("Type", "Paper"), ("Price", "2.00"), ("InStock", "Yes")])
                  ] + [s.text(40, 326, "Record 1 of 8", size=12.5, weight=800)])
    poster_simple("report-lab", "Report Lab: a report to print", "Group, sort and add totals; the report is ready to print.",
                  "Task 1 of 3: group the products by Type.",
                  lambda s: [s.text(24, 132, "Group by Type    Sort by Price    Total of each group", size=12.5, weight=800),
                             s.rect(24, 146, 380, 196, rx=6, fill="#ffffff", stroke=LINE),
                             s.text(40, 172, "Products of the Sunrise shop", size=14, weight=800)] + [
                      (s.text(40, 198 + 20 * i, n, size=12, weight=600), s.text(380, 198 + 20 * i, p + " JD", size=12, anchor="end", weight=600))
                      for i, (n, p) in enumerate([("Notebook (Paper)", "2.00"), ("Pen (Paper)", "0.50"), ("Bag (Bags)", "12.00"), ("Water (Drinks)", "0.50"), ("Juice (Drinks)", "1.00"), ("Folder (Paper)", "1.50"), ("Lunch box (Bags)", "6.00")])])
    s = Svg(640, 360)
    s.text(24, 34, "Data Desk at Sunrise Company", size=21, weight=800)
    s.text(24, 56, "Help your colleagues with the shop database.", size=12, fill=MUTED)
    s.text(24, 88, "Message 1 / 8", size=13, weight=800)
    s.text(616, 88, "0 stars", size=13, fill=ORANGE, anchor="end", weight=800)
    s.rect(24, 102, 560, 74, rx=14, fill=SOFT, stroke=PEACH)
    s.text(38, 122, "Omar (shop)", size=10.5, fill=MUTED, weight=700)
    s.lines(38, 142, ["In the Customers table, which field must have a different", "value in every record?"], size=12.5, weight=800, gap=18)
    for i, t in enumerate(["CustomerID: the primary key", "Name", "City"]):
        y = 194 + i * 42
        s.rect(24, y, 592, 34, rx=10, fill="#ffffff", stroke=ORANGE)
        s.text(38, y + 22, t, size=13, fill=ORANGE, weight=800)
    s.save(os.path.join(W, "sims", "data-desk.svg"))
