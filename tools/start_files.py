#!/usr/bin/env python3
"""Write the start files of the lecture worksheets (AUTHORING.md, "Lecture worksheets").

A worksheet gives every student the same data: an Excel workbook or a Word
document in courses/<slug>/week-WW/files/, listed in the `start-files:` of
lesson-NN-sheet.qmd. This script writes them from the data below, so the
numbers can change every semester (change them here and in the worksheet
together, then run it again):

    python3 tools/start_files.py

Only the Python standard library is used: a small writer for .xlsx (one or
more sheets: text, numbers, formulas, bold header row, column widths) and
for .docx (plain paragraphs, some bold, with the styles of a new Word
document: the students give the styles themselves). A .pptx is a short talk
in Markdown, made by the pandoc of Quarto (a Title Slide, then a Title and
Content slide for every "## " heading).
"""

import os
import shutil
import subprocess
import tempfile
import zipfile
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def put(z, name, data):
    """One file in the zip, with a fixed date: the same data gives the same file."""
    info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(info, data)

# ----------------------------------------------------------------- xlsx

CT_XLSX = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
%s
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="%s"/>
</Relationships>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""


def col_name(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def cell_xml(ref, value, bold):
    style = ' s="1"' if bold else ""
    if value is None or value == "":
        return ""
    if isinstance(value, str) and value.startswith("="):
        return '<c r="%s"%s><f>%s</f></c>' % (ref, style, escape(value[1:]))
    if isinstance(value, (int, float)):
        return '<c r="%s"%s><v>%s</v></c>' % (ref, style, repr(value) if isinstance(value, float) else value)
    return '<c r="%s"%s t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, style, escape(value))


def sheet_xml(rows, widths):
    cols = "".join('<col min="%d" max="%d" width="%s" customWidth="1"/>' % (i + 1, i + 1, w)
                   for i, w in enumerate(widths))
    out = []
    for r, row in enumerate(rows, 1):
        cells = "".join(cell_xml("%s%d" % (col_name(c), r), v, r == 1) for c, v in enumerate(row))
        out.append('<row r="%d">%s</row>' % (r, cells))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            + ("<cols>%s</cols>" % cols if cols else "")
            + "<sheetData>%s</sheetData></worksheet>" % "".join(out))


def write_xlsx(path, sheets):
    """sheets: [(name, rows, column widths)]; row 1 is bold."""
    overrides, entries, rels = [], [], []
    for i, (name, rows, widths) in enumerate(sheets, 1):
        overrides.append('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType='
                         '"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % i)
        entries.append('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (escape(name), i, i))
        rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                    'relationships/worksheet" Target="worksheets/sheet%d.xml"/>' % (i, i))
    rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                'relationships/styles" Target="styles.xml"/>' % (len(sheets) + 1))
    workbook = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                "<sheets>%s</sheets><calcPr fullCalcOnLoad=\"1\"/></workbook>" % "".join(entries))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        put(z, "[Content_Types].xml", CT_XLSX % "\n".join(overrides))
        put(z, "_rels/.rels", RELS % "xl/workbook.xml")
        put(z, "xl/workbook.xml", workbook)
        put(z, "xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   + "".join(rels) + "</Relationships>")
        put(z, "xl/styles.xml", STYLES)
        for i, (_, rows, widths) in enumerate(sheets, 1):
            put(z, "xl/worksheets/sheet%d.xml" % i, sheet_xml(rows, widths))


# ----------------------------------------------------------------- docx

CT_DOCX = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

# The styles of a new Word document (Calibri 11, single lines, 6 pt after a
# paragraph), so that every Word version shows the same text, and Title,
# Heading 1 and Heading 2 are in the Styles gallery and the Navigation Pane.
DOCX_STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Arial"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="10"/><w:qFormat/><w:pPr><w:spacing w:after="160"/><w:contextualSpacing/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri Light" w:hAnsi="Calibri Light"/><w:spacing w:val="-10"/><w:kern w:val="28"/><w:sz w:val="56"/><w:szCs w:val="56"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="240" w:after="60"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri Light" w:hAnsi="Calibri Light"/><w:color w:val="2F5496"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="160" w:after="40"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri Light" w:hAnsi="Calibri Light"/><w:color w:val="2F5496"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:uiPriority w:val="34"/><w:qFormat/><w:pPr><w:ind w:left="720"/><w:contextualSpacing/></w:pPr></w:style>
<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
</w:styles>"""

DOCX_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""


def write_docx(path, paragraphs):
    """paragraphs: strings; "**text**" makes the whole paragraph bold."""
    out = []
    for p in paragraphs:
        bold = p.startswith("**") and p.endswith("**")
        text = p[2:-2] if bold else p
        rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
        out.append('<w:p><w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (rpr, escape(text)))
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
           + "".join(out) + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
           '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
           "</w:sectPr></w:body></w:document>")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        put(z, "[Content_Types].xml", CT_DOCX)
        put(z, "_rels/.rels", RELS % "word/document.xml")
        put(z, "word/document.xml", doc)
        put(z, "word/_rels/document.xml.rels", DOCX_RELS)
        put(z, "word/styles.xml", DOCX_STYLES)


# ----------------------------------------------------------------- pptx

def write_pptx(path, markdown):
    """A talk from Markdown (`title:` and `subtitle:` make the Title Slide).
    SOURCE_DATE_EPOCH fixes the dates: the same text gives the same file."""
    cmd = ["quarto", "pandoc"] if shutil.which("quarto") else ["pandoc"]
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "talk.md")
        with open(src, "w", encoding="utf-8") as f:
            f.write(markdown)
        env = dict(os.environ, SOURCE_DATE_EPOCH="1767225600")  # 2026-01-01
        subprocess.run(cmd + [src, "-o", path], check=True, env=env)


# ----------------------------------------------------------------- the files

DS = "courses/digital-skills"

FILES = {
    # Lecture 1, productivity apps: eight prices to add by hand and with AutoSum (Experiment 1).
    DS + "/week-01/files/prices-start.xlsx": ("xlsx", [
        ("Prices", [["Price (JD)"], [10], [25], [15], [30], [20], [5], [35], [10]], [14]),
    ]),
    # Lecture 3, Office concepts: a staff notice to find the parts, use the ribbon and save (59 words).
    DS + "/week-03/files/notice-start.docx": ("docx", [
        "**Sunrise Company: Staff Notice**",
        "Dear colleagues,",
        "Our office moves to the second floor next Sunday. The new rooms have more light and a small kitchen.",
        "Please put your files in boxes on Thursday afternoon. Write your name on every box.",
        "We meet in Room 21 at 9:00 on Sunday morning.",
        "Thank you for your help.",
        "Yousef Haddad, Office Manager",
    ]),
    # Lecture 4, Word (1): a notice with no formatting, to format, give styles,
    # make a list and a table, and add a picture (files/books.png, drawn in
    # images/books.svg). Not the Family Day notice: that is the Game challenge.
    DS + "/week-04/files/book-fair-start.docx": ("docx", [
        "Book Fair at the College Library",
        "The college library holds a book fair for all students and staff. You can buy new books, "
        "swap your old books and meet two writers from Jordan. Come with your friends and your family.",
        "When and where",
        "The fair is in the library hall from Sunday to Tuesday, from 10:00 to 15:00.",
        "What you can bring",
        "Old books in good condition",
        "Your student card",
        "A bag for your new books",
        "How to swap a book",
        "Take one old book to the swap desk.",
        "Get a swap ticket.",
        "Choose a new book from the swap table.",
        "Prices",
        "Entry to the fair is free for everyone.",
    ]),
    # Lecture 5, AI with Word: a short report to sum up (Experiment 2) and to
    # translate (Experiment 4). Not Huda's Thursday memo: that is the Game challenge.
    DS + "/week-05/files/report-start.docx": ("docx", [
        "**Report: The New Sunrise Shop in Zarqa**",
        "Sunrise Company opens its second shop next Saturday at 9:00. The new shop is in Zarqa, "
        "on King Abdullah Street, next to the post office.",
        "The shop has 6 staff, and Rana Saleh is the manager. It sells notebooks, pens, bags and school books.",
        "The shop is open from Saturday to Thursday, from 9:00 to 20:00. It is closed on Friday.",
        "On the first day, the first 50 customers get a free bag. Children under 12 get a free pen.",
        "Customers can pay in cash or by card. They can also order online and collect their order at the shop.",
    ]),
    # Lecture 7, Excel (2): the sales of the next week (200 JD), to sort, filter
    # and colour (Experiments 1-3), and two small tables for the charts
    # (Experiment 4). Not the week of the page: that is the Game challenge.
    DS + "/week-07/files/sales-start.xlsx": ("xlsx", [
        ("Sales", [["Day", "Item", "Type", "Qty", "Total (JD)"],
                   ["Sun", "Pen", "Paper", 30, 15],
                   ["Sun", "Water", "Drinks", 18, 9],
                   ["Mon", "Bag", "Bags", 2, 24],
                   ["Mon", "Notebook", "Paper", 15, 30],
                   ["Tue", "Juice", "Drinks", 28, 14],
                   ["Tue", "Pen", "Paper", 24, 12],
                   ["Wed", "Water", "Drinks", 34, 17],
                   ["Wed", "Bag", "Bags", 4, 48],
                   ["Thu", "Notebook", "Paper", 10, 20],
                   ["Thu", "Juice", "Drinks", 22, 11]], [8, 12, 10, 8, 12]),
        ("Types", [["Type", "Sales (JD)"], ["Paper", 77], ["Drinks", 51], ["Bags", 72]], [12, 12]),
        ("Days", [["Day", "Sales (JD)"], ["Sun", 24], ["Mon", 54], ["Tue", 26], ["Wed", 65], ["Thu", 31]], [10, 12]),
    ]),
    # Lecture 8, PowerPoint: a short talk in the default theme, with one slide
    # of six long points (Experiment 3) and one of three short points
    # (the animation of Experiment 4). Not Slide Doctor: that is the Game challenge.
    DS + "/week-09/files/talk-start.pptx": ("pptx", """---
title: "Saving Water at Home"
subtitle: "A short talk for the Sunrise staff"
---

## Small changes at home

- When you brush your teeth, the tap does not need to run all the time, so close it.
- A dripping tap in the kitchen wastes water all day and all night, so fix it soon.
- A short shower uses much less water than a full bath, and it is just as clean.
- Wash the car with a bucket of water, not with a hose that runs for a long time.
- Water the plants early in the morning or in the evening, when the sun is not strong.
- Use the washing machine only when it is full, and choose a short programme.

## What we do at the office

- Report a dripping tap at once.
- Turn off the tap after you wash.
- Boil only the water that you need.
"""),
    # Lecture 6, Excel (1): the shop list (Experiments 1-3) and a week of sales (Experiment 4).
    DS + "/week-06/files/shop-start.xlsx": ("xlsx", [
        ("Shop", [["Item", "Price (JD)", "Quantity"],
                  ["Notebook", 2, 10],
                  ["Pen", 0.5, 40],
                  ["Bag", 12, 3]], [14, 12, 11, 13, 14, 16]),
        ("Week", [["Day", "Sales (JD)"],
                  ["Sunday", 12],
                  ["Monday", 18],
                  ["Tuesday", 25],
                  ["Wednesday", 15],
                  ["Thursday", 30]], [14, 12]),
    ]),
}


def main():
    for rel, (kind, data) in FILES.items():
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if kind == "xlsx":
            write_xlsx(path, data)
        elif kind == "pptx":
            write_pptx(path, data)
        else:
            write_docx(path, data)
        print("wrote", rel)


if __name__ == "__main__":
    main()
