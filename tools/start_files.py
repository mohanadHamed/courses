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
for .docx (plain paragraphs, some bold; no styles, so the students give the
styles themselves).
"""

import os
import zipfile
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        z.writestr("[Content_Types].xml", CT_XLSX % "\n".join(overrides))
        z.writestr("_rels/.rels", RELS % "xl/workbook.xml")
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   + "".join(rels) + "</Relationships>")
        z.writestr("xl/styles.xml", STYLES)
        for i, (_, rows, widths) in enumerate(sheets, 1):
            z.writestr("xl/worksheets/sheet%d.xml" % i, sheet_xml(rows, widths))


# ----------------------------------------------------------------- docx

CT_DOCX = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""


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
        z.writestr("[Content_Types].xml", CT_DOCX)
        z.writestr("_rels/.rels", RELS % "word/document.xml")
        z.writestr("word/document.xml", doc)


# ----------------------------------------------------------------- the files

DS = "courses/digital-skills"

FILES = {
    # Lecture 1, productivity apps: eight prices to add by hand and with AutoSum (Experiment 1).
    DS + "/week-01/files/prices-start.xlsx": ("xlsx", [
        ("Prices", [["Price (JD)"], [10], [25], [15], [30], [20], [5], [35], [10]], [14]),
    ]),
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
        else:
            write_docx(path, data)
        print("wrote", rel)


if __name__ == "__main__":
    main()
