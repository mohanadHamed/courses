// Record a simulator or mini-game as a sequence of PNG frames (headless Chrome).
// The frames are joined into an animated GIF by make-gif.swift.
//
//   deno run -A shared/sims/recordings/record.ts <url> <out-dir> <scenario.js> [seconds] [width]
//
// <scenario.js> is plain JavaScript that runs inside the page and plays the
// game (clicks, taps); it may use the helpers wait(ms), tap(el, x, y), click(sel).
// Deno comes with Quarto (quarto/bin/tools/<arch>/deno); Chrome must be installed.

const [url, outDir, scenarioPath, secondsArg, widthArg] = Deno.args;
const seconds = Number(secondsArg || 8), width = Number(widthArg || 600);
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333;
const profile = await Deno.makeTempDir();

const chrome = new Deno.Command(CHROME, {
  // HEADLESS=0: a normal window off-screen (WebGL scenes redraw only there).
  args: [Deno.env.get("HEADLESS") === "0" ? "--window-position=-3000,0" : "--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--no-first-run",
    "--hide-scrollbars", "--mute-audio", `--window-size=${width},1200`,
    "--use-angle=swiftshader", "--enable-unsafe-swiftshader"],             // WebGL (3D viewer) in headless mode
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
  return r.result?.value;
}

await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width, height: 1200, deviceScaleFactor: 1, mobile: false });
const loaded = new Promise((r) => events.push((m) => { if (m.method === "Page.loadEventFired") r(true); }));
await send("Page.navigate", { url });
await loaded;
await new Promise((r) => setTimeout(r, 900));

// Helpers for the scenario, then start it without waiting for it.
const scenario = await Deno.readTextFile(scenarioPath);
await evaluate(`
  window.wait = (ms) => new Promise((r) => setTimeout(r, ms));
  window.click = (sel) => { const el = typeof sel === "string" ? document.querySelector(sel) : sel; if (el) el.click(); return el; };
  window.tap = (el, x, y) => { const r = el.getBoundingClientRect();
    const o = { clientX: r.left + (x ?? r.width / 2), clientY: r.top + (y ?? r.height / 2), bubbles: true, pointerId: 1, isPrimary: true };
    el.dispatchEvent(new PointerEvent("pointerdown", o)); el.dispatchEvent(new PointerEvent("pointerup", o)); };
  window.key = (code) => { window.dispatchEvent(new KeyboardEvent("keydown", { code, key: code === "Space" ? " " : code, bubbles: true }));
    window.dispatchEvent(new KeyboardEvent("keyup", { code, key: code === "Space" ? " " : code, bubbles: true })); };
  (async () => { try { ${scenario} } catch (e) { console.error(e); } })();
  true;`);

// The area to record: the simulator's <main class="sim">.
const box = await evaluate(`(() => { const r = document.querySelector("main.sim").getBoundingClientRect();
  return { x: Math.floor(r.left), y: Math.floor(r.top + scrollY), w: Math.ceil(r.width), h: Math.ceil(r.height) }; })()`);
await Deno.mkdir(outDir, { recursive: true });
const delays: number[] = [];
const t0 = performance.now();
let n = 0, last = t0;
while (performance.now() - t0 < seconds * 1000) {
  const shot = await send("Page.captureScreenshot", { format: "png", clip: { x: box.x, y: box.y, width: box.w, height: box.h, scale: 1 } });
  await Deno.writeFile(`${outDir}/frame_${String(n).padStart(4, "0")}.png`, Uint8Array.from(atob(shot.data), (c) => c.charCodeAt(0)));
  const now = performance.now();
  if (n > 0) delays.push((now - last) / 1000);
  last = now; n++;
  const rest = 110 - (performance.now() - now);           // about 9 frames per second
  if (rest > 0) await new Promise((r) => setTimeout(r, rest));
}
delays.push(1.2);                                         // hold the last frame a little longer
await Deno.writeTextFile(`${outDir}/delays.txt`, delays.map((d) => d.toFixed(3)).join("\n"));
console.log(`${n} frames, ${box.w}x${box.h}`);
ws.close(); chrome.kill(); await chrome.status;
await Deno.remove(profile, { recursive: true }).catch(() => {});
