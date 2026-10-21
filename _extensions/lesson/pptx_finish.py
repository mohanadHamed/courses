#!/usr/bin/env python3
"""Finish the lesson slides (.pptx) after Quarto renders them.

Quarto (pandoc) makes plain slides. This project post-render step adds:

- the course look: colours from courses/<slug>/_metadata.yml (accent, accent2),
  fonts, a soft background, shapes and a footer with the course name;
- a title slide in the course colour, with the site URL (`site-url` in
  _quarto.yml) big on a white label, so students can read it or take a photo;
- answer cards from `::: {.answer}` (one card per item, elastic zoom on click);
- click-by-click text from `::: {.reveal}` (fade in from the left);
- coloured "Try it N" / "Think" / "Example" / "Watch out" / "Game challenge" labels in slide titles,
  and a fade between slides;
- text that fits its box: long text is made smaller (PowerPoint autofit
  values), and on a "Comparison" slide (the `task` line of a simulator above
  its recording and QR code) the line gets the room it needs.

Only the Python standard library is used. The script runs on every render
(local, preview and CI) and skips files it already finished.
"""

import glob
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
for _k, _v in NS.items():
    ET.register_namespace(_k, _v)
A = "{%s}" % NS["a"]
P = "{%s}" % NS["p"]

MARK_ANSWER, MARK_REVEAL, MARK_STOP = "\ue000", "\ue001", "\ue00f"
DONE_NAME = "lesson-finish"            # name of a master shape = "already finished"

EMU = 914400                           # EMU per inch
SLIDE_W, SLIDE_H = 9144000, 5143500    # 16:9 (pandoc default)
MARGIN_X = 457200
CONTENT_TOP = 1200151                  # body placeholder top (pandoc master)
ZONE_BOTTOM = 4690000                  # answer cards end here, above the footer
FONT = "Trebuchet MS"                  # on Windows and macOS, friendly and clear


# ---------------------------------------------------------------- colours

def hex_rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(c):
    return "".join("%02X" % max(0, min(255, round(v))) for v in c)


def mix(c1, c2, t):
    """t = 0 → c1, t = 1 → c2."""
    return tuple(a + (b - a) * t for a, b in zip(c1, c2))


WHITE, BLACK = (255, 255, 255), (0, 0, 0)


def palette(course):
    acc, acc2 = hex_rgb(course["accent"]), hex_rgb(course["accent2"])
    return {
        "accent": rgb_hex(acc),
        "accent2": rgb_hex(acc2),
        "dark": rgb_hex(mix(acc, BLACK, 0.45)),       # titles
        "deep": rgb_hex(mix(acc, BLACK, 0.62)),       # title slide gradient end
        "ink": rgb_hex(mix(acc, BLACK, 0.86)),        # body text
        "muted": rgb_hex(mix(mix(acc, BLACK, 0.6), WHITE, 0.35)),
        "bg": rgb_hex(mix(acc2, WHITE, 0.95)),        # slide background
        "card": rgb_hex(mix(acc2, WHITE, 0.72)),      # answer card
    }


# ---------------------------------------------------------------- course data

def read_course(project_dir, slug):
    path = os.path.join(project_dir, "courses", slug, "_metadata.yml")
    course = {"title": "", "code": "", "accent": "#2F9E44", "accent2": "#A9E34B"}
    if not os.path.exists(path):
        return course
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r'^\s{2}(title|code|accent|accent2):\s*"?([^"#\n]*(?:#[0-9A-Fa-f]{6})?)"?', line)
            if m:
                course[m.group(1)] = m.group(2).strip()
    return course


# ---------------------------------------------------------------- XML helpers

def parse(data):
    return ET.fromstring(data)


def dump(root):
    return b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(root, encoding="utf-8")


def frag(xml):
    """Parse an XML fragment that uses the a:/p:/r: prefixes."""
    wrap = '<w xmlns:a="%s" xmlns:p="%s" xmlns:r="%s">%s</w>' % (NS["a"], NS["p"], NS["r"], xml)
    return list(ET.fromstring(wrap))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def para_text(p):
    return "".join(t.text or "" for t in p.iter(A + "t"))


def solid(hexc, alpha=None):
    a = '<a:alpha val="%d"/>' % alpha if alpha is not None else ""
    return '<a:solidFill><a:srgbClr val="%s">%s</a:srgbClr></a:solidFill>' % (hexc, a)


def shape(sid, name, x, y, w, h, geom, fill, line="<a:ln><a:noFill/></a:ln>", text="", body_pr="", extra=""):
    tx = ""
    if text or body_pr:
        tx = '<p:txBody>%s<a:lstStyle/>%s</p:txBody>' % (body_pr or "<a:bodyPr/>", text or "<a:p><a:endParaRPr/></a:p>")
    return (
        '<p:sp><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="%s"><a:avLst/></a:prstGeom>%s%s%s</p:spPr>%s</p:sp>'
        % (sid, esc(name), x, y, w, h, geom, fill, line, extra, tx)
    )


def text_para(s, size, color, bold=False, algn="l", spacing=None):
    b = ' b="1"' if bold else ""
    spc = ' spc="%d"' % spacing if spacing else ""
    return (
        '<a:p><a:pPr algn="%s"/><a:r><a:rPr lang="en-US" sz="%d"%s%s dirty="0">%s'
        '<a:latin typeface="%s"/></a:rPr><a:t>%s</a:t></a:r></a:p>'
        % (algn, size, b, spc, solid(color), FONT, esc(s))
    )


def insert_back(sptree, xml):
    """Insert shapes right after the group properties: behind everything else."""
    children = list(sptree)
    pos = next(i for i, c in enumerate(children) if c.tag == P + "grpSpPr") + 1
    for k, el in enumerate(frag(xml)):
        sptree.insert(pos + k, el)


# ---------------------------------------------------------------- theme, master, layouts

def finish_theme(xml, pal):
    s = xml.decode("utf-8")
    scheme = (
        '<a:clrScheme name="Lesson">'
        '<a:dk1><a:srgbClr val="%(ink)s"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>'
        '<a:dk2><a:srgbClr val="%(dark)s"/></a:dk2><a:lt2><a:srgbClr val="%(bg)s"/></a:lt2>'
        '<a:accent1><a:srgbClr val="%(accent)s"/></a:accent1><a:accent2><a:srgbClr val="%(accent2)s"/></a:accent2>'
        '<a:accent3><a:srgbClr val="%(dark)s"/></a:accent3><a:accent4><a:srgbClr val="%(card)s"/></a:accent4>'
        '<a:accent5><a:srgbClr val="%(muted)s"/></a:accent5><a:accent6><a:srgbClr val="E8590C"/></a:accent6>'
        '<a:hlink><a:srgbClr val="%(dark)s"/></a:hlink><a:folHlink><a:srgbClr val="%(dark)s"/></a:folHlink>'
        '</a:clrScheme>' % pal
    )
    s = re.sub(r"<a:clrScheme .*?</a:clrScheme>", scheme, s, count=1, flags=re.S)
    for part in ("majorFont", "minorFont"):
        s = re.sub(r"(<a:%s>\s*<a:latin typeface=\")[^\"]*(\"/>\s*<a:ea typeface=\"[^\"]*\"/>\s*<a:cs typeface=\")[^\"]*(\")" % part,
                   r"\g<1>%s\g<2>Arial\g<3>" % FONT, s, count=1)
    return s.encode("utf-8")


def finish_master(xml, pal, course):
    root = parse(xml)
    csld = root.find(P + "cSld")
    bg = csld.find(P + "bg")
    if bg is not None:
        csld.remove(bg)
    csld.insert(0, frag('<p:bg><p:bgPr>%s<a:effectLst/></p:bgPr></p:bg>' % solid(pal["bg"]))[0])

    sptree = csld.find(P + "spTree")
    footer = "%s · %s" % (course["title"], course["code"]) if course["title"] else ""
    deco = "".join([
        # soft circles, top right (partly outside the slide)
        shape(9001, DONE_NAME, 7890000, -640000, 1900000, 1900000, "ellipse", solid(pal["accent2"], 38000)),
        shape(9002, "deco-dot", 8460000, 1010000, 300000, 300000, "ellipse", solid(pal["accent"], 30000)),
        shape(9003, "deco-ring", 7300000, 120000, 520000, 520000, "ellipse", "<a:noFill/>",
              '<a:ln w="28575">%s</a:ln>' % solid(pal["accent"], 45000)),
        # short bar under the title
        shape(9004, "deco-title-bar", MARGIN_X, 1010000, 760000, 64000, "roundRect", solid(pal["accent"])),
        # band at the bottom: accent → accent2
        shape(9005, "deco-band", 0, SLIDE_H - 82000, SLIDE_W, 82000, "rect",
              '<a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0"><a:srgbClr val="%s"/></a:gs>'
              '<a:gs pos="100000"><a:srgbClr val="%s"/></a:gs></a:gsLst><a:lin ang="0" scaled="0"/></a:gradFill>'
              % (pal["accent"], pal["accent2"])),
        shape(9006, "deco-footer", MARGIN_X, 4790000, 7000000, 230000, "rect", "<a:noFill/>",
              text=text_para(footer, 900, pal["muted"]),
              body_pr='<a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>'),
    ])
    insert_back(sptree, deco)

    # Titles: left, bold, course dark colour. Body: round bullets in the accent colour.
    ts = root.find(P + "txStyles")
    t1 = ts.find(P + "titleStyle").find(A + "lvl1pPr")
    t1.set("algn", "l")
    d = t1.find(A + "defRPr")
    d.set("sz", "3000")
    d.set("b", "1")
    for f in d.findall(A + "solidFill"):
        d.remove(f)
    d.insert(0, frag('<a:solidFill><a:schemeClr val="tx2"/></a:solidFill>')[0])
    body = ts.find(P + "bodyStyle")
    for lvl in body:
        bu = lvl.find(A + "buChar")
        if bu is None:
            continue
        idx = list(lvl).index(bu)
        for old in ("buClr", "buSzPct"):
            o = lvl.find(A + old)
            if o is not None:
                lvl.remove(o)
                idx = list(lvl).index(bu)
        bf = lvl.find(A + "buFont")
        if bf is not None:
            idx = list(lvl).index(bf)
        lvl.insert(idx, frag('<a:buClr><a:schemeClr val="accent1"/></a:buClr>')[0])
        lvl.insert(idx + 1, frag('<a:buSzPct val="85000"/>')[0])
        bu.set("char", "●" if lvl.tag == A + "lvl1pPr" else "○")
        sb = lvl.find(A + "spcBef")
        if sb is not None:
            sb.clear()
            sb.append(frag('<a:spcPts val="900"/>')[0])
    return dump(root)


def finish_title_layout(xml):
    root = parse(xml)
    root.set("showMasterSp", "0")      # the title slide draws its own shapes
    return dump(root)


# ---------------------------------------------------------------- slides

def renumber(sptree):
    n = 2
    for el in sptree.iter(P + "cNvPr"):
        el.set("id", str(n))
        n += 1


def find_ph(sptree, kinds):
    for sp in sptree.findall(P + "sp"):
        ph = sp.find("./%snvSpPr/%snvPr/%sph" % (P, P, P))
        if ph is None:
            continue
        t = ph.get("type", "obj")
        if t in kinds or (ph.get("idx") == "1" and "body" in kinds and t not in ("subTitle",)):
            return sp
    return None


def set_xfrm(sp, x, y, w, h):
    sppr = sp.find(P + "spPr")
    old = sppr.find(A + "xfrm")
    if old is not None:
        sppr.remove(old)
    sppr.insert(0, frag('<a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>' % (x, y, w, h))[0])


def style_runs(p, size=None, color=None, bold=None):
    for r in p.findall(A + "r"):
        rpr = r.find(A + "rPr")
        if rpr is None:
            rpr = ET.SubElement(r, A + "rPr")
            r.remove(rpr)
            r.insert(0, rpr)
        if size:
            rpr.set("sz", str(size))
        if bold:
            rpr.set("b", "1")
        if color:
            for f in rpr.findall(A + "solidFill"):
                rpr.remove(f)
            rpr.insert(0, frag(solid(color))[0])


SITE_RID = "rIdSiteUrl"                # relationship id of the site link on the title slide


def site_label(site_url):
    """https://example.github.io/courses/ → example.github.io/courses"""
    return re.sub(r"^https?://", "", site_url).rstrip("/")


def site_url_shapes(site_url, pal):
    """Big, clear site URL on a white label (title slide), clickable."""
    label = site_label(site_url)
    run = ('<a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="2800" b="1" u="none" dirty="0">%s'
           '<a:latin typeface="%s"/><a:hlinkClick r:id="%s"/></a:rPr><a:t>%s</a:t></a:r></a:p>'
           % (solid(pal["dark"]), FONT, SITE_RID, esc(label)))
    return shape(9109, "site-url", 685800, 3900000, 6400000, 600000, "roundRect", solid("FFFFFF"),
                 text=run,
                 body_pr='<a:bodyPr wrap="square" lIns="90000" tIns="0" rIns="90000" bIns="0" anchor="ctr"/>')


def title_size(text, width, height):
    """Largest font size (1/100 pt) at which the lesson title fits its box.

    The box is bottom-anchored, so a title that needs more lines than fit
    would grow upwards into the course name. Estimate the lines from the
    text length (bold sans: about 0.55 em per character, 10 % lost at word
    breaks) and take the largest size whose lines fit the height."""
    width_pt, height_pt = width / 12700, height / 12700
    for pt in (40, 36, 32, 28, 24):
        per_line = max(1, int(width_pt / (0.55 * pt) / 1.1))
        lines = -(-len(text) // per_line)
        if lines * 1.2 * pt <= height_pt:
            return pt * 100
    return 2400


def finish_title_slide(root, pal, course, diploma, site_url=""):
    csld = root.find(P + "cSld")
    csld.insert(0, frag(
        '<p:bg><p:bgPr><a:gradFill rotWithShape="1"><a:gsLst>'
        '<a:gs pos="0"><a:srgbClr val="%s"/></a:gs><a:gs pos="100000"><a:srgbClr val="%s"/></a:gs>'
        '</a:gsLst><a:lin ang="2700000" scaled="0"/></a:gradFill><a:effectLst/></p:bgPr></p:bg>'
        % (pal["accent"], pal["deep"]))[0])
    sptree = csld.find(P + "spTree")
    insert_back(sptree, "".join([
        shape(9101, "deco-big", 6100000, -900000, 3900000, 3900000, "ellipse", solid(pal["accent2"], 22000)),
        shape(9102, "deco-mid", 7650000, 3150000, 1500000, 1500000, "ellipse", solid("FFFFFF", 12000)),
        shape(9103, "deco-ring", 5600000, 2450000, 900000, 900000, "ellipse", "<a:noFill/>",
              '<a:ln w="38100">%s</a:ln>' % solid(pal["accent2"], 70000)),
        shape(9104, "deco-dot", 8300000, 2350000, 260000, 260000, "ellipse", solid(pal["accent2"])),
        shape(9105, "deco-bar", 685800, 2620000, 900000, 70000, "roundRect", solid(pal["accent2"])),
        # Course name: anchored at the bottom, so a long name wraps upwards
        # and never runs into the lesson title below it.
        shape(9106, "course", 685800, 400000, 6400000, 660000, "rect", "<a:noFill/>",
              text=text_para(("%s · %s" % (course["title"], course["code"])).upper(), 1100, pal["accent2"], True, spacing=100),
              body_pr='<a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="b"/>'),
        shape(9107, "diploma", 685800, 4620000, 7600000, 260000, "rect", "<a:noFill/>",
              text=text_para(diploma, 900, "FFFFFF"),
              body_pr='<a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>'),
    ]))
    if site_url:
        for el in frag(site_url_shapes(site_url, pal)):
            sptree.append(el)
    title = find_ph(sptree, ("ctrTitle", "title"))
    sub = find_ph(sptree, ("subTitle",))
    if title is not None:
        set_xfrm(title, 685800, 1150000, 5800000, 1420000)
        bp = title.find("./%stxBody/%sbodyPr" % (P, A))
        bp.set("anchor", "b")
        text = "".join(t.text or "" for t in title.iter(A + "t"))
        size = title_size(text, 5800000, 1420000)
        for p in title.iter(A + "p"):
            ppr = p.find(A + "pPr")
            if ppr is not None:
                ppr.set("algn", "l")
            style_runs(p, size, "FFFFFF", True)
    if sub is not None:
        set_xfrm(sub, 685800, 2760000, 5800000, 820000)
        for p in sub.iter(A + "p"):
            ppr = p.find(A + "pPr")
            if ppr is not None:
                ppr.set("algn", "l")
            style_runs(p, 2000, "FFFFFF")
            runs = p.findall(A + "r")
            if runs:   # first line (Week · Lecture) in the light accent colour
                style_runs_one(runs[0], 2200, pal["accent2"], True)


def style_runs_one(r, size, color, bold):
    rpr = r.find(A + "rPr")
    rpr.set("sz", str(size))
    if bold:
        rpr.set("b", "1")
    for f in rpr.findall(A + "solidFill"):
        rpr.remove(f)
    rpr.insert(0, frag(solid(color))[0])


LABEL = re.compile(r"^(Try it \d+(?:[–-]\d+)?|Try it|Think|Quick check|Your turn|Example|Watch out|Game challenge)\s*([·:—-])?\s*")
NOT_QUESTION = ("Example", "Watch out", "Game challenge")   # coloured label, but no "?"


def finish_title_label(sptree, pal):
    """Colour 'Try it 3 ·' (or 'Example ·') in the title; return True for a question slide."""
    title = find_ph(sptree, ("title",))
    if title is None:
        return False
    paras = title.findall(".//%sp" % A)
    if not paras:
        return False
    p = paras[0]
    runs = p.findall(A + "r")
    if not runs:
        return False
    first = runs[0].find(A + "t")
    m = LABEL.match(first.text or "")
    if not m:
        return False
    label = m.group(1)
    rest = (first.text or "")[m.end():]
    first.text = rest
    lab = frag('<a:r><a:rPr lang="en-US" dirty="0">%s</a:rPr><a:t>%s  </a:t></a:r>'
               % (solid(pal["accent"]), esc(label)))[0]
    p.insert(list(p).index(runs[0]), lab)
    return label not in NOT_QUESTION


def wrapped_lines(text, per_line):
    """Number of lines when the words of `text` wrap at `per_line` characters."""
    lines, used = 1, 0
    for word in text.split():
        if used and used + 1 + len(word) > per_line:
            lines, used = lines + 1, len(word)
        else:
            used += (1 if used else 0) + len(word)
    return lines


def fit_text(body, height, width=SLIDE_W - 2 * MARGIN_X, pt=24):
    """Make the body text smaller when it would not fit its box.

    Try the sizes from `pt` down to 16 pt and keep the largest that fits
    (a smaller font also puts more words on each line)."""
    txb = body.find(P + "txBody")
    texts = [para_text(p) for p in txb.findall(A + "p")]
    texts = [t for t in texts if t.strip()]
    have = height / EMU * 0.9          # a margin: fonts differ between viewers
    line_w = width / EMU - 0.45        # insets and the bullet or label

    def need(size):
        k = size / 24
        per_line = line_w / (0.15 * k)  # characters per line (24 pt: about 0.15 in each)
        lines = sum(wrapped_lines(t, per_line) for t in texts)
        return lines * 0.40 * k + 0.125 * len(texts)

    if need(pt) <= have:
        return
    size = next((s for s in range(pt - 1, 16, -1) if need(s) <= have), 16)
    scale = size / pt
    # Real font sizes, not only autofit values: every viewer (PowerPoint,
    # Keynote, a phone) then shows the same smaller text.
    for p in txb.findall(A + "p"):
        for rpr in list(p.iter(A + "rPr")) + list(p.iter(A + "endParaRPr")):
            old = int(rpr.get("sz", pt * 100))
            rpr.set("sz", str(max(1600, int(old * scale / 100) * 100)))
    bp = txb.find(A + "bodyPr")
    for old in list(bp):
        bp.remove(old)
    bp.append(frag('<a:normAutofit/>')[0])


def card_layout(items):
    """Place answer cards: a grid for short answers, full rows for long ones."""
    width = SLIDE_W - 2 * MARGIN_X
    gap = 120000
    char_w = 0.118 * EMU             # 18 pt text, average character
    pad = 0.55 * EMU
    longest = max(len(t) for t in items) * char_w + pad

    def rows_for(c):
        """Row heights with c columns; None when a card would need over 2 lines."""
        col_w = (width - (c - 1) * gap) / c
        heights = []
        per_line = (col_w - pad) / char_w
        for r in range(math.ceil(len(items) / c)):
            row = items[r * c:(r + 1) * c]
            if c > 1 and max(len(w) for t in row for w in t.split()) > per_line:
                return None            # a long file name cannot wrap
            lines = max(wrapped_lines(t, per_line) for t in row)
            if lines > 2 and c > 1:
                return None
            heights.append(int((0.30 * lines + 0.22) * EMU))
        return heights

    # The lowest block of cards leaves the most room for the questions;
    # with the same height, more columns.
    options = [(sum(h) + gap * (len(h) - 1), -c, c, h)
               for c in range(1, min(5, len(items)) + 1) for h in [rows_for(c)] if h]
    _, _, cols, heights = min(options)
    col_w = (width - (cols - 1) * gap) / cols
    boxes = []
    rows = len(heights)
    top = ZONE_BOTTOM - sum(heights) - gap * (rows - 1)
    y = top
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            if i >= len(items):
                break
            x = MARGIN_X + c * (col_w + gap)
            if cols == 1:
                w = min(width, max(int(longest) + int(0.3 * EMU), int(3.2 * EMU)))
            else:
                w = int(col_w)
            boxes.append((int(x), int(y), w, heights[r]))
        y += heights[r] + gap
    return boxes, top


def card(sid, n, box, para_xml, pal):
    x, y, w, h = box
    return (
        '<p:sp><p:nvSpPr><p:cNvPr id="%d" name="Answer %d"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 22000"/></a:avLst></a:prstGeom>'
        '%s<a:ln w="22225">%s</a:ln>'
        '<a:effectLst><a:outerShdw blurRad="88900" dist="38100" dir="5400000" algn="t" rotWithShape="0">'
        '<a:srgbClr val="000000"><a:alpha val="20000"/></a:srgbClr></a:outerShdw></a:effectLst></p:spPr>'
        '<p:txBody><a:bodyPr wrap="square" lIns="128016" tIns="45720" rIns="128016" bIns="45720" anchor="ctr">'
        '<a:normAutofit/></a:bodyPr><a:lstStyle/>%s</p:txBody></p:sp>'
        % (sid, n, x, y, w, h, solid(pal["card"]), solid(pal["accent"]), para_xml)
    )


def number_label(kind, n):
    """Label of item n (1, 2, …) in a numbered list, e.g. alphaLcParenR → 'a)'."""
    m = re.match(r"(alphaLc|alphaUc|arabic|romanLc|romanUc)(ParenBoth|ParenR|Period|Plain)?", kind or "")
    if not m:
        return None
    base, punct = m.group(1), m.group(2) or "Plain"
    if base.startswith("alpha"):
        t = chr(ord("a") + (n - 1) % 26)
    elif base.startswith("roman"):
        t = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"][(n - 1) % 10]
    else:
        t = str(n)
    if base.endswith("Uc"):
        t = t.upper()
    return {"ParenBoth": "(%s)", "ParenR": "%s)", "Period": "%s.", "Plain": "%s"}[punct] % t


def card_labels(paras):
    """Labels for answer paragraphs from a numbered list (None for others)."""
    labels, count, last = [], 0, None
    for p in paras:
        auto = p.find("./%spPr/%sbuAutoNum" % (A, A))
        if auto is None:
            labels.append(None)
            count, last = 0, None
            continue
        kind = auto.get("type")
        if kind != last:
            count, last = int(auto.get("startAt", "1")) - 1, kind
        count += 1
        labels.append(number_label(kind, count))
    return labels


def card_para(p, label, pal):
    """Turn a body paragraph into card text: no bullet; its label, or a check mark."""
    ppr = p.find(A + "pPr")
    if ppr is not None:
        p.remove(ppr)
    p.insert(0, frag('<a:pPr marL="0" indent="0"><a:buNone/></a:pPr>')[0])
    style_runs(p, 1800, pal["ink"])
    lead = (label + "  ") if label else "✓ "
    p.insert(1, frag('<a:r><a:rPr lang="en-US" sz="1800" b="1" dirty="0">%s</a:rPr><a:t>%s</a:t></a:r>'
                     % (solid(pal["accent"]), esc(lead)))[0])
    return ET.tostring(p, encoding="unicode")


def fixed_labels(txb, pal):
    """Numbered lists (a), 1.): the label as text and a tab, with a hanging
    indent, so the first line starts exactly where the next lines start in
    every viewer (automatic numbers are placed differently by each one)."""
    paras = txb.findall(A + "p")
    for p, label in zip(paras, card_labels(paras)):
        if not label:
            continue
        ppr = p.find(A + "pPr")
        p.remove(ppr)
        p.insert(0, frag('<a:pPr marL="457200" indent="-457200"><a:buNone/>'
                         '<a:tabLst><a:tab pos="457200" algn="l"/></a:tabLst></a:pPr>')[0])
        p.insert(1, frag('<a:r><a:rPr lang="en-US" b="1" dirty="0">%s</a:rPr><a:t>%s\t</a:t></a:r>'
                         % (solid(pal["accent"]), esc(label)))[0])


NUMBER_COMMA = re.compile(r"(?<=\d),\s(?=[−-]?\d)")
DIGIT_HYPHEN = re.compile(r"(?<=\d)-(?=\d)")


def keep_numbers_together(sptree):
    """(2, −3) and (4, 12, −3) never break after a comma (a no-break space),
    and 2026-10-21 or 3-2-1 never break at a hyphen (no-break hyphens)."""
    for t in sptree.iter(A + "t"):
        if t.text and ("," in t.text or "-" in t.text):
            t.text = NUMBER_COMMA.sub(",\u00a0", t.text)
            t.text = DIGIT_HYPHEN.sub("\u2011", t.text)


def finish_code(sptree):
    """Code: Consolas; code blocks a bit smaller, so a line of code fits."""
    for p in sptree.iter(A + "p"):
        runs = p.findall(A + "r")
        mono = [r for r in runs if (r.find("./%srPr/%slatin" % (A, A)) is not None
                                    and r.find("./%srPr/%slatin" % (A, A)).get("typeface") == "Courier")]
        for r in mono:
            r.find("./%srPr/%slatin" % (A, A)).set("typeface", "Consolas")
        if mono and len(mono) == len(runs) and p.find("./%spPr/%sbuNone" % (A, A)) is not None:
            for r in runs:
                r.find(A + "rPr").set("sz", "1800")


def body_placeholders(sptree):
    """Content placeholders (one, or two for a slide with columns)."""
    out = []
    for sp in sptree.findall(P + "sp"):
        ph = sp.find("./%snvSpPr/%snvPr/%sph" % (P, P, P))
        if ph is not None and ph.get("type", "obj") in ("body", "obj") and sp.find(P + "txBody") is not None:
            out.append(sp)
    return out


def geometry(el, layout_geo):
    """(x, y, w, h) of a shape or picture: its own xfrm, else the layout's."""
    off = el.find(".//%sxfrm/%soff" % (A, A))
    ext = el.find(".//%sxfrm/%sext" % (A, A))
    if off is not None and ext is not None:
        return int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy"))
    ph = el.find("./%snvSpPr/%snvPr/%sph" % (P, P, P))
    idx = ph.get("idx", "1") if ph is not None else "1"
    return layout_geo.get(idx, (MARGIN_X, CONTENT_TOP, SLIDE_W - 2 * MARGIN_X, 3394472))


def make_room(sptree, bodies, layout_geo, bottom):
    """Make text and pictures end above `bottom`, where the answer cards go."""
    for body in bodies:
        x, y, w, h = geometry(body, layout_geo)
        if y + h > bottom:
            h = max(500000, bottom - y)
            set_xfrm(body, x, y, w, h)
        fit_text(body, h, w, 24 if w > SLIDE_W / 2 else 21)
    for pic in sptree.findall(P + "pic"):
        x, y, w, h = geometry(pic, layout_geo)
        if y + h > bottom and bottom - y > 300000:
            k = (bottom - y) / h
            nw, nh = int(w * k), int(h * k)
            xfrm = pic.find(".//%sxfrm" % A)
            xfrm.find(A + "off").set("x", str(x + (w - nw) // 2))
            xfrm.find(A + "ext").set("cx", str(nw))
            xfrm.find(A + "ext").set("cy", str(nh))


def placeholder_idx(sp):
    ph = sp.find("./%snvSpPr/%snvPr/%sph" % (P, P, P))
    return (ph.get("type", "obj"), ph.get("idx", "1")) if ph is not None else (None, None)


def comparison_heads(sptree, layout_geo):
    """The text line above each column of a "Comparison" slide."""
    if "4" not in layout_geo:
        return []
    return [sp for sp in sptree.findall(P + "sp") if placeholder_idx(sp) in (("body", "1"), ("body", "3"))]


def finish_comparison(sptree, heads, layout_geo):
    """Give each line above a column the height it needs; the picture goes below it."""
    bottom = sum(layout_geo["2"][1::2]) if "2" in layout_geo else ZONE_BOTTOM
    pics = sptree.findall(P + "pic")
    for head in heads:
        x, y, w, _ = layout_geo[placeholder_idx(head)[1]]
        text = " ".join(para_text(p) for p in head.iter(A + "p"))
        for p in head.iter(A + "p"):
            style_runs(p, 1800)
        lines = wrapped_lines(text, (w / EMU - 0.25) / 0.13)   # 18 pt bold: about 0.13 in per character
        h = int((lines * 0.31 + 0.15) * EMU)
        set_xfrm(head, x, y, w, h)
        bp = head.find("./%stxBody/%sbodyPr" % (P, A))
        if bp is not None:
            bp.set("anchor", "t")      # grow downwards, never into the title
        top = y + h + 60000
        for pic in pics:
            px, py, pw, ph = geometry(pic, layout_geo)
            if not (x <= px + pw / 2 <= x + w) or bottom - top < 300000:
                continue
            k = min(1.0, w / pw, (bottom - top) / ph)
            nw, nh = int(pw * k), int(ph * k)
            xfrm = pic.find(".//%sxfrm" % A)
            xfrm.find(A + "off").set("x", str(x + (w - nw) // 2))
            xfrm.find(A + "off").set("y", str(top))
            xfrm.find(A + "ext").set("cx", str(nw))
            xfrm.find(A + "ext").set("cy", str(nh))


# ---------------------------------------------------------------- animations

class Timing:
    def __init__(self):
        self.next_id = 3
        self.clicks = []
        self.builds = {}

    def nid(self):
        self.next_id += 1
        return self.next_id

    def _visible(self, tgt):
        return ('<p:set><p:cBhvr><p:cTn id="%d" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                '<p:tgtEl>%s</p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
                '<p:to><p:strVal val="visible"/></p:to></p:set>' % (self.nid(), tgt))

    def _anim(self, tgt, attr, frames, dur, extra=""):
        tav = "".join('<p:tav tm="%d"><p:val>%s</p:val></p:tav>' % (tm, v) for tm, v in frames)
        return ('<p:anim calcmode="lin" valueType="num"><p:cBhvr additive="base"><p:cTn id="%d" dur="%d"%s fill="hold"/>'
                '<p:tgtEl>%s</p:tgtEl><p:attrNameLst><p:attrName>%s</p:attrName></p:attrNameLst></p:cBhvr>'
                '<p:tavLst>%s</p:tavLst></p:anim>' % (self.nid(), dur, extra, tgt, attr, tav))

    def _fade(self, tgt, dur):
        return ('<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="%d" dur="%d"/>'
                '<p:tgtEl>%s</p:tgtEl></p:cBhvr></p:animEffect>' % (self.nid(), dur, tgt))

    def _click(self, effect_id, preset, subtype, body):
        a, b = self.nid(), self.nid()
        return ('<p:par><p:cTn id="%d" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
                '<p:par><p:cTn id="%d" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                '<p:par><p:cTn id="%d" presetID="%d" presetClass="entr" presetSubtype="%d" fill="hold" grpId="0" nodeType="clickEffect">'
                '<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>%s</p:childTnLst></p:cTn></p:par>'
                '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>' % (a, b, effect_id, preset, subtype, body))

    def pop(self, spid):
        """Elastic zoom: grow past full size, swing back, settle."""
        tgt = '<p:spTgt spid="%d"/>' % spid
        eid = self.nid()
        frames = lambda v: [(0, '<p:fltVal val="0"/>'),
                            (55000, '<p:strVal val="%s*1.14"/>' % v),
                            (75000, '<p:strVal val="%s*0.94"/>' % v),
                            (90000, '<p:strVal val="%s*1.03"/>' % v),
                            (100000, '<p:strVal val="%s"/>' % v)]
        body = (self._visible(tgt) + self._anim(tgt, "ppt_w", frames("#ppt_w"), 750)
                + self._anim(tgt, "ppt_h", frames("#ppt_h"), 750) + self._fade(tgt, 250))
        self.clicks.append(self._click(eid, 53, 16, body))
        self.builds[spid] = '<p:bldP spid="%d" grpId="0" animBg="1"/>' % spid

    def slide_in(self, spid, para):
        """Fade in and slide a little from the left (one paragraph)."""
        tgt = '<p:spTgt spid="%d"><p:txEl><p:pRg st="%d" end="%d"/></p:txEl></p:spTgt>' % (spid, para, para)
        eid = self.nid()
        body = (self._visible(tgt)
                + self._anim(tgt, "ppt_x", [(0, '<p:strVal val="#ppt_x-0.12"/>'), (100000, '<p:strVal val="#ppt_x"/>')], 550, ' decel="100000"')
                + self._anim(tgt, "ppt_y", [(0, '<p:strVal val="#ppt_y"/>'), (100000, '<p:strVal val="#ppt_y"/>')], 550)
                + self._fade(tgt, 550))
        self.clicks.append(self._click(eid, 2, 8, body))
        self.builds[spid] = '<p:bldP spid="%d" grpId="0" build="p"/>' % spid

    def xml(self):
        if not self.clicks:
            return None
        return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
                '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>%s'
                '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
                '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
                '</p:childTnLst></p:cTn></p:par></p:tnLst><p:bldLst>%s</p:bldLst></p:timing>'
                % ("".join(self.clicks), "".join(self.builds.values())))


def finish_slide(xml, pal, course, diploma, is_title, layout_geo, site_url=""):
    root = parse(xml)
    csld = root.find(P + "cSld")
    sptree = csld.find(P + "spTree")
    if is_title:
        finish_title_slide(root, pal, course, diploma, site_url)
        renumber(sptree)
    else:
        finish_title_label(sptree, pal)
        finish_code(sptree)
        keep_numbers_together(sptree)
        bodies = body_placeholders(sptree)
        steps = []          # (body, "reveal", paragraph) or (body, "answer", [paragraphs])
        for body in bodies:
            txb = body.find(P + "txBody")
            mode, group = None, None
            for p in list(txb.findall(A + "p")):
                t = para_text(p).strip()
                if t in (MARK_ANSWER, MARK_REVEAL):
                    mode = "answer" if t == MARK_ANSWER else "reveal"
                    group = []
                    if mode == "answer":
                        steps.append((body, "answer", group))
                    txb.remove(p)
                    continue
                if t == MARK_STOP:
                    mode = None
                    txb.remove(p)
                    continue
                if mode == "answer":
                    group.append(p)
                    txb.remove(p)
                elif mode == "reveal":
                    steps.append((body, "reveal", p))
            if not txb.findall(A + "p"):
                txb.append(frag("<a:p><a:endParaRPr/></a:p>")[0])

        for body in bodies:
            fixed_labels(body.find(P + "txBody"), pal)

        heads = comparison_heads(sptree, layout_geo)
        if heads:
            finish_comparison(sptree, heads, layout_geo)
        answers = [p for _, kind, g in steps if kind == "answer" for p in g]
        boxes, labels = [], []
        if answers:
            labels = card_labels(answers)
            boxes, top = card_layout([(l or "✓") + "  " + para_text(p) for p, l in zip(answers, labels)])
            make_room(sptree, [b for b in bodies if b not in heads], layout_geo, top - 140000)
        else:
            for body in bodies:
                if body not in heads:
                    x, y, w, h = geometry(body, layout_geo)
                    fit_text(body, h, w, 24 if w > SLIDE_W / 2 else 21)
        for i, (p, box) in enumerate(zip(answers, boxes), start=1):
            sptree.append(frag(card(9300 + i, i, box, card_para(p, labels[i - 1], pal), pal))[0])
        renumber(sptree)

        # Click order = order in the slide source.
        timing = Timing()
        ids = {el.get("name"): int(el.get("id")) for el in sptree.iter(P + "cNvPr")}
        n_card = 0
        for body, kind, item in steps:
            if kind == "reveal":
                body_id = int(body.find("./%snvSpPr/%scNvPr" % (P, P)).get("id"))
                timing.slide_in(body_id, body.find(P + "txBody").findall(A + "p").index(item))
            else:
                for _ in item:
                    n_card += 1
                    timing.pop(ids["Answer %d" % n_card])
        t = timing.xml()
        if t:
            old = root.find(P + "timing")
            if old is not None:
                root.remove(old)
            root.append(frag(t)[0])

    # A soft fade between slides. Order in <p:sld>: cSld, clrMapOvr, transition, timing.
    if root.find(P + "transition") is None:
        tr = frag('<p:transition spd="med"><p:fade/></p:transition>')[0]
        kids = list(root)
        pos = max([kids.index(csld)] + [kids.index(k) for k in kids if k.tag == P + "clrMapOvr"]) + 1
        root.insert(pos, tr)
    return dump(root)


# ---------------------------------------------------------------- one file

def finish(path, project_dir):
    rel = os.path.relpath(os.path.abspath(path), project_dir).replace(os.sep, "/")
    m = re.search(r"courses/([^/]+)/", rel)
    if not m:
        return False
    course = read_course(project_dir, m.group(1))
    pal = palette(course)
    diploma = read_diploma(project_dir, m.group(1))
    site_url = read_site_url(project_dir)

    with zipfile.ZipFile(path) as z:
        files = {n: z.read(n) for n in z.namelist()}
        order = z.namelist()
    master = files.get("ppt/slideMasters/slideMaster1.xml", b"")
    if DONE_NAME.encode() in master:
        return False

    title_layouts = set()
    for name in order:
        if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", name) and re.search(rb'<p:sldLayout[^>]*\stype="title"', files[name]):
            title_layouts.add(name.rsplit("/", 1)[1])
            files[name] = finish_title_layout(files[name])
    files["ppt/theme/theme1.xml"] = finish_theme(files["ppt/theme/theme1.xml"], pal)
    files["ppt/slideMasters/slideMaster1.xml"] = finish_master(master, pal, course)
    for name in order:
        if not re.match(r"ppt/slides/slide\d+\.xml$", name):
            continue
        rels = files.get(name.replace("slides/", "slides/_rels/") + ".rels", b"").decode("utf-8")
        lay = re.search(r'Target="\.\./slideLayouts/(slideLayout\d+\.xml)"', rels)
        is_title = bool(lay and lay.group(1) in title_layouts)
        geo = layout_geometry(files.get("ppt/slideLayouts/" + lay.group(1), b"")) if lay else {}
        files[name] = finish_slide(files[name], pal, course, diploma, is_title, geo, site_url if is_title else "")
        if is_title and site_url:
            rels_name = name.replace("slides/", "slides/_rels/") + ".rels"
            files[rels_name] = add_site_link(files[rels_name], site_url)

    fd, tmp = tempfile.mkstemp(suffix=".pptx", dir=os.path.dirname(os.path.abspath(path)))
    os.close(fd)
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name in order:
            z.writestr(name, files[name])
    shutil.move(tmp, path)
    os.chmod(path, 0o644)
    return True


def layout_geometry(xml):
    """Placeholder idx → (x, y, w, h) from a slide layout."""
    geo = {}
    for m in re.finditer(rb"<p:sp>.*?</p:sp>", xml, re.S):
        sp = m.group(0)
        ph = re.search(rb'<p:ph[^>]*idx="(\d+)"', sp)
        box = re.search(rb'<a:off x="(\d+)" y="(\d+)"\s*/>\s*<a:ext cx="(\d+)" cy="(\d+)"', sp)
        if ph and box:
            geo[ph.group(1).decode()] = tuple(int(v) for v in box.groups())
    return geo


def add_site_link(rels, site_url):
    """Add the external hyperlink relationship used by the site URL label."""
    s = rels.decode("utf-8")
    if SITE_RID not in s:
        s = s.replace("</Relationships>",
                      '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                      'relationships/hyperlink" Target="%s" TargetMode="External"/></Relationships>'
                      % (SITE_RID, esc(site_url)))
    return s.encode("utf-8")


def read_site_url(project_dir):
    try:
        with open(os.path.join(project_dir, "_quarto.yml"), encoding="utf-8") as f:
            m = re.search(r'^\s+site-url:\s*"([^"]*)"', f.read(), re.M)
            return m.group(1) if m else ""
    except OSError:
        return ""


def read_diploma(project_dir, slug=""):
    """The diploma line: courses/<slug>/_metadata.yml first, else _quarto.yml."""
    try:
        with open(os.path.join(project_dir, "courses", slug, "_metadata.yml"), encoding="utf-8") as f:
            m = re.search(r'^diploma-line:\s*"([^"]*)"', f.read(), re.M)
            if m:
                return m.group(1)
    except OSError:
        pass
    try:
        with open(os.path.join(project_dir, "_quarto.yml"), encoding="utf-8") as f:
            m = re.search(r'^diploma-line:\s*"([^"]*)"', f.read(), re.M)
            return m.group(1) if m else ""
    except OSError:
        return ""


def main(argv):
    project_dir = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    if len(argv) > 1:
        paths = argv[1:]
    else:
        listed = os.environ.get("QUARTO_PROJECT_OUTPUT_FILES", "")
        paths = [p for p in listed.splitlines() if p.endswith(".pptx")]
        out_dir = os.path.join(project_dir, os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
        paths += glob.glob(os.path.join(out_dir, "**", "*.pptx"), recursive=True)
    done = 0
    for p in sorted(set(os.path.abspath(os.path.join(project_dir, x)) for x in paths)):
        if os.path.exists(p) and finish(p, project_dir):
            done += 1
    print("pptx_finish: finished %d slide file(s)" % done)


if __name__ == "__main__":
    main(sys.argv)
