// The frames of a course video (AUTHORING.md, "Blended courses"): headless
// Chrome draws the video page at every 1/fps second, and each picture is saved
// as a PNG (00000.png, 00001.png …) for make-video.swift.
//
//   deno run -A shared/sims/recordings/record-video.ts <page.html> <timing.json> <frames-dir> [fps] [poster.png] [poster-seconds]
//
// The page (videos/<name>.html with video-kit.js) has window.drawAt(t): it
// draws the picture at time t (from the times of the voice in timing.json)
// and returns a key. While the key stays the same, the picture is the same,
// so the frame is linked to the last one instead of taken again.
// Deno comes with Quarto (quarto/bin/tools/<arch>/deno); Chrome must be installed.

const [page, timingPath, outDir, fpsArg, posterPath, posterArg] = Deno.args;
const fps = Number(fpsArg || 30), W = 1280, H = 720;
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9334;
const profile = await Deno.makeTempDir();
const chrome = new Deno.Command(CHROME, {
  args: ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--no-first-run",
    "--hide-scrollbars", "--mute-audio", "--allow-file-access-from-files", `--window-size=${W},${H}`],
  stdout: "null", stderr: "null",
}).spawn();

async function json(path: string, method = "GET") {
  for (let i = 0; i < 50; i++) {
    try { return await (await fetch(`http://127.0.0.1:${PORT}${path}`, { method })).json(); }
    catch { await new Promise((r) => setTimeout(r, 200)); }
  }
  throw new Error("Chrome did not start");
}
const target = await json(`/json/new?about:blank`, "PUT");
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0;
const waiting = new Map<number, (v: any) => void>();
const events: ((m: any) => void)[] = [];
ws.onmessage = (e) => {
  const m = JSON.parse(e.data);
  if (m.id && waiting.has(m.id)) { waiting.get(m.id)!(m); waiting.delete(m.id); }
  else events.forEach((f) => f(m));
};
function send(method: string, params: Record<string, unknown> = {}): Promise<any> {
  const n = ++id;
  ws.send(JSON.stringify({ id: n, method, params }));
  return new Promise((r) => waiting.set(n, (m) => r(m.result ?? m)));
}
async function evaluate(expression: string) {
  const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails));
  return r.result?.value;
}
async function shot(path: string) {
  const s = await send("Page.captureScreenshot", { format: "png", clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
  await Deno.writeFile(path, Uint8Array.from(atob(s.data), (c) => c.charCodeAt(0)));
}

await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: false });
const loaded = new Promise((r) => events.push((m) => { if (m.method === "Page.loadEventFired") r(true); }));
await send("Page.navigate", { url: new URL(page, `file://${Deno.cwd()}/`).href });
await loaded;
const timing = await Deno.readTextFile(timingPath);
await evaluate(`(async () => { await document.fonts.ready; window.TIMING = ${timing}; return true; })()`);

await Deno.mkdir(outDir, { recursive: true });
const total = Math.ceil(JSON.parse(timing).total * fps);
let last = "", taken = 0;
for (let i = 0; i < total; i++) {
  const key = await evaluate(`drawAt(${i / fps})`);
  const file = `${outDir}/${String(i).padStart(5, "0")}.png`;
  if (key !== last || i === 0) { await shot(file); taken++; }
  else await Deno.link(`${outDir}/${String(i - 1).padStart(5, "0")}.png`, file);
  last = key;
}
if (posterPath) {
  // The poster: the end of the first scene (all its parts), without a caption.
  const scenes = JSON.parse(timing).scenes;
  const at = posterArg ? Number(posterArg) : scenes.length > 1 ? scenes[1].start - 0.05 : JSON.parse(timing).total / 2;
  await evaluate(`drawAt(${at}, true)`);
  await shot(posterPath);
}
console.log(`record-video: ${total} frames (${taken} pictures) at ${fps} fps, ${W}x${H}`);
ws.close(); chrome.kill(); await chrome.status;
await Deno.remove(profile, { recursive: true }).catch(() => {});
