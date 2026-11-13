#!/usr/bin/env python3
"""Export figures and posters (SVG) to PNG on a computer without Helvetica or Arial.

    python3 plans/helpers/export_png.py courses/.../images/x.svg [more.svg ...]

The PNG is made like the posters (shared/sims/README.md): quarto typst
compile at 200 ppi. The SVG itself is not changed: a temporary copy uses
Liberation Sans (the same widths as Arial), found with --font-path.
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_DIR = "/usr/share/fonts/truetype/liberation"


def export(svg):
    svg = os.path.abspath(svg)
    text = open(svg, encoding="utf-8").read()
    text = text.replace("Helvetica, Arial, sans-serif", "Liberation Sans")
    tmp_dir = tempfile.mkdtemp(dir=os.path.join(ROOT, "plans", "helpers"))
    try:
        tmp = os.path.join(tmp_dir, "fig.svg")
        open(tmp, "w", encoding="utf-8").write(text)
        rel = "/" + os.path.relpath(tmp, ROOT)
        png = svg[:-4] + ".png"
        subprocess.run(["quarto", "typst", "compile", "--root", ROOT, "--font-path", FONT_DIR,
                        "--input", "svg=" + rel, os.path.join(ROOT, "shared/sims/export-poster.typ"),
                        png, "--ppi", "200"], check=True, cwd=ROOT)
        print("wrote", os.path.relpath(png, ROOT))
    finally:
        for f in os.listdir(tmp_dir):
            os.remove(os.path.join(tmp_dir, f))
        os.rmdir(tmp_dir)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        export(path)
