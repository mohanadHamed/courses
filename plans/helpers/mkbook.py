#!/usr/bin/env python3
"""Make a seminar worksheet (seminar-NN-book.qmd) from its page (seminar-NN.qmd).

    mkbook.py PAGE SPEC

SPEC is a text file:

    lead text (one paragraph, may span lines)
    ===
    1. exercise | its answer
    2. exercise | its answer

The worksheet gets the page's title, ILOs and number, the lead, the page from
"## Recall" up to "## At home" or "## Wrap-up" (whichever comes first), without
the "Why:" reasons, then "## Exercises" and "## Answers to the exercises".
"""
import re
import sys


def main(page, spec):
    text = open(page, encoding="utf-8").read()
    fm_end = text.find("\n---", 3)
    fm, body = text[3:fm_end], text[fm_end + 4:]
    desc = re.search(r'^description: "(.*)"$', fm, re.M).group(1)
    desc = re.sub(r"^(Seminar|Practice) · ", "", desc)
    kind = "Practice" if re.search(r"^practice:", fm, re.M) else "Seminar"
    fm = re.sub(r'^description: ".*"$', 'description: "%s worksheet · %s"' % (kind, desc), fm, flags=re.M)
    fm = fm.replace("format: lesson-html", "format: lesson-typst")

    start = body.index("## Recall")
    stops = [m.start() for m in re.finditer(r"^## (At home|Wrap-up)", body, re.M)]
    main_part = body[start:min(stops)].rstrip() + "\n"
    # Drop the Why: reasons (and the blank line before each).
    main_part = re.sub(r"\n\n    Why: [^\n]*(\n    [^\n]+)*", "", main_part)
    # Simulators: the PDF shows a poster and a QR code; no height needed.
    main_part = re.sub(r'(\{\{< *sim [^>]*?) height="\d+"', r"\1", main_part)

    raw = open(spec, encoding="utf-8").read()
    lead, rest = raw.split("\n===\n")
    ex, ans = [], []
    for line in rest.strip().splitlines():
        if not line.strip():
            continue
        m = re.match(r"\s*\d+\.\s*(.*?)\s*\|\s*(.*)$", line)
        ex.append(m.group(1))
        ans.append(m.group(2))

    out = ["---" + fm + "\n---\n", "::: {.lead}", lead.strip(), ":::\n", main_part]
    out.append("## Exercises\n")
    out += ["%d. %s" % (i + 1, e) for i, e in enumerate(ex)]
    out.append("\n## Answers to the exercises\n\n::: {.answers}")
    out += ["%d. %s" % (i + 1, a) for i, a in enumerate(ans)]
    out.append(":::\n")
    book = page[:-4] + "-book.qmd"
    open(book, "w", encoding="utf-8").write("\n".join(out))
    print("wrote", book)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
