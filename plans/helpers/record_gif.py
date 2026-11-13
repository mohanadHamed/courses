#!/usr/bin/env python3
"""Record a simulator or mini-game as a GIF on Linux (no Swift needed).

    python3 plans/helpers/record_gif.py <name> [<name> ...]

Reads the line of <name> in shared/sims/recordings/record-all.sh (page,
seconds, GIF) and its scenario (shared/sims/recordings/scenarios/<name>.js),
plays it in headless Chromium with Node Playwright (the same helpers as
record.ts: wait, click, tap, key), takes about 9 frames a second of
<main class="sim"> (with 120 px more below it, for the feedback lines that
appear later) and joins them into a looping GIF with Pillow. Frames
that do not change are merged, so the GIF stays small. Needs Node with the
playwright package (NODE_PATH) and Python with Pillow.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REC = os.path.join(ROOT, "shared", "sims", "recordings")

NODE = r"""
const { chromium } = require('playwright');
const fs = require('fs');
const [url, outDir, scenarioPath, secondsArg] = process.argv.slice(2);
const seconds = Number(secondsArg || 8);
const HELPERS = `
window.wait = (ms) => new Promise((r) => setTimeout(r, ms));
window.click = (sel) => { const el = typeof sel === "string" ? document.querySelector(sel) : sel; if (el) el.click(); return el; };
window.tap = (el, x, y) => { const r = el.getBoundingClientRect();
  const o = { clientX: r.left + (x ?? r.width / 2), clientY: r.top + (y ?? r.height / 2), bubbles: true, pointerId: 1, isPrimary: true };
  el.dispatchEvent(new PointerEvent("pointerdown", o)); el.dispatchEvent(new PointerEvent("pointerup", o)); };
window.key = (code) => { window.dispatchEvent(new KeyboardEvent("keydown", { code, key: code === "Space" ? " " : code, bubbles: true }));
  window.dispatchEvent(new KeyboardEvent("keyup", { code, key: code === "Space" ? " " : code, bubbles: true })); };
`;
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 600, height: 1200 }, deviceScaleFactor: 1 });
  const errors = [];
  pg.on('pageerror', (e) => errors.push(String(e)));
  await pg.goto(url); await pg.waitForTimeout(900);
  const scenario = fs.readFileSync(scenarioPath, 'utf8');
  await pg.evaluate(HELPERS + "(async () => { try { " + scenario + " } catch (e) { console.error(e); } })(); true;");
  const box = await pg.evaluate(() => { const r = document.querySelector("main.sim").getBoundingClientRect();
    return { x: Math.floor(r.left), y: Math.floor(r.top + scrollY), width: Math.ceil(r.width), height: Math.ceil(r.height) + 120 }; });
  const delays = []; const t0 = Date.now(); let n = 0, last = t0;
  while (Date.now() - t0 < seconds * 1000) {
    await pg.screenshot({ path: `${outDir}/f${String(n).padStart(4, '0')}.png`, clip: box });
    const now = Date.now(); if (n > 0) delays.push((now - last) / 1000); last = now; n++;
    const rest = 110 - (Date.now() - now); if (rest > 0) await pg.waitForTimeout(rest);
  }
  delays.push(1.2);
  fs.writeFileSync(`${outDir}/info.json`, JSON.stringify({ delays, box, errors }));
  await b.close();
})();
"""


def entry(name):
    for line in open(os.path.join(REC, "record-all.sh"), encoding="utf-8"):
        parts = line.strip().split("|")
        if parts and parts[0] == name and len(parts) >= 4:
            return parts[1], float(parts[2]), parts[3]
    sys.exit("no line for %s in record-all.sh" % name)


def record(name):
    page_rel, seconds, gif_rel = entry(name)
    tmp = tempfile.mkdtemp()
    try:
        script = os.path.join(tmp, "rec.js")
        open(script, "w").write(NODE)
        env = dict(os.environ)
        env.setdefault("NODE_PATH", "/opt/node22/lib/node_modules")
        url = "file://" + os.path.join(ROOT, page_rel) + "?fixed-order"
        subprocess.run(["node", script, url, tmp, os.path.join(REC, "scenarios", name + ".js"), str(seconds)],
                       check=True, env=env)
        info = json.load(open(os.path.join(tmp, "info.json")))
        if info["errors"]:
            print("page errors:", info["errors"])
        files = sorted(f for f in os.listdir(tmp) if f.endswith(".png"))
        out, durs = [], []
        for f, d in zip(files, info["delays"]):
            im = Image.open(os.path.join(tmp, f)).convert("RGB")
            if out and im.tobytes() == out[-1].tobytes():
                durs[-1] += d
            else:
                out.append(im)
                durs.append(d)
        pal = [im.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for im in out]
        gif = os.path.join(ROOT, gif_rel)
        pal[0].save(gif, save_all=True, append_images=pal[1:], duration=[max(20, int(d * 1000)) for d in durs],
                    loop=0, optimize=True, disposal=1)
        print("wrote %s: %d frames, %dx%d, %d KB" % (gif_rel, len(pal), info["box"]["width"], info["box"]["height"],
                                                     os.path.getsize(gif) // 1024))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    for n in sys.argv[1:]:
        record(n)
