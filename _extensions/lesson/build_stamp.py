#!/usr/bin/env python3
"""Stamp the site with its build number and keep phones on the newest build
(project post-render, runs last).

- Build number: GitHub Actions run number in CI (`GITHUB_RUN_NUMBER`), else
  "local". With the short commit and the date, it is shown in small text at the
  bottom of every page, so the teacher can see which build a phone shows.
- `version.json` at the site root holds the build number.
- Every local link and file in a page (CSS, JavaScript, PDF, slides, other
  pages, simulators) gets `?v=<build>`, so a new build never mixes with files
  the browser keeps from an older one.
- A small script on every page asks for `version.json` (never from the cache)
  when the page opens and when the student comes back to the tab. If the site
  has a newer build, the page reloads itself once with the new build in its
  address, so the browser fetches it again.

Only the Python standard library is used.
"""

import datetime
import glob
import json
import os
import re
import subprocess
import sys

STAMP_MARK = "data-build-stamp"


def build_info(project_dir):
    sha = os.environ.get("GITHUB_SHA", "")[:7]
    if not sha:
        try:
            sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=project_dir,
                                 capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            sha = ""
    now = datetime.datetime.now(datetime.timezone.utc)
    run = os.environ.get("GITHUB_RUN_NUMBER")
    # A local build gets a new number on every render, so the reload check works there too.
    build = run if run else "local-" + now.strftime("%Y%m%d%H%M%S")
    label = ("Build %s" % run) if run else "Local build"
    return {"build": build, "label": label, "sha": sha, "date": now.strftime("%Y-%m-%d %H:%M UTC")}


LINK_RE = re.compile(r'(\s(?:href|src)=")([^"#?]+?\.(?:css|js|pdf|pptx|html|json|png|svg|jpg|woff2))((?:\?[^"#]*)?)(#[^"]*)?"')


def bust(match, build):
    pre, path, query, frag = match.group(1), match.group(2), match.group(3) or "", match.group(4) or ""
    if re.match(r"^(?:[a-z]+:|//)", path):          # http:, https:, mailto:, data:, //cdn
        return match.group(0)
    if "v=" in query:
        return match.group(0)
    query = (query + "&" if query else "?") + "v=" + build
    return '%s%s%s%s"' % (pre, path, query, frag)


def page_script(build, root, info):
    stamp = "%s · %s%s" % (info["label"], info["date"], (" · " + info["sha"]) if info["sha"] else "")
    return """
<div class="build-stamp" %s>%s</div>
<style>.build-stamp{text-align:center;font-size:11px;color:#9aa0a6;padding:6px 0 10px;letter-spacing:.2px}@media print{.build-stamp{display:none}}</style>
<script>
(() => {
  // Newest build check (build_stamp.py). Reload once if the site has a newer build.
  const BUILD = %s, URL_V = %s;
  const check = () => {
    fetch(URL_V + "?t=" + Date.now(), { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then((v) => {
        if (!v || !v.build || v.build === BUILD) return;
        const key = "reloaded-for:" + v.build;
        try { if (sessionStorage.getItem(key)) return; sessionStorage.setItem(key, "1"); } catch (_) {}
        const u = new URL(location.href);
        u.searchParams.set("v", v.build);
        location.replace(u.toString());
      })
      .catch(() => {});
  };
  check();
  document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") check(); });
  window.addEventListener("pageshow", (e) => { if (e.persisted) check(); });
})();
</script>
""" % (STAMP_MARK, stamp, json.dumps(build), json.dumps(root + "version.json"))


def main():
    project_dir = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    site = os.path.join(project_dir, "_site")
    if not os.path.isdir(site):
        return 0
    info = build_info(project_dir)
    build = info["build"]
    with open(os.path.join(site, "version.json"), "w", encoding="utf-8") as f:
        json.dump(info, f)

    count = 0
    for path in glob.glob(os.path.join(site, "**", "*.html"), recursive=True):
        rel = os.path.relpath(path, site)
        if rel.startswith("site_libs" + os.sep):
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        if "</body>" not in html:
            continue
        # A page rendered again in this run has no old stamp; an old one is replaced.
        html = re.sub(r'\n<div class="build-stamp" %s>.*?</script>\n' % STAMP_MARK, "\n", html, flags=re.S)
        html = re.sub(r'(\s(?:href|src)="[^"#]*?)[?&]v=[^"&#]*', r"\1", html)
        html = LINK_RE.sub(lambda m: bust(m, build), html)
        depth = rel.count(os.sep)
        root = "../" * depth
        is_sim = os.sep + "sims" + os.sep in os.sep + rel or rel.startswith("shared" + os.sep)
        if not is_sim:
            html = html.replace("</body>", page_script(build, root, info) + "</body>", 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
    print("Build stamp: %s (%d pages)" % (info["label"] if build.startswith("local") else build, count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
