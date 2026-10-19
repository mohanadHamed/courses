// Vector Dash: choose the velocity = displacement ÷ frames, then launch.
const num = (s) => Number(s.replace("−", "-"));
for (let lv = 0; lv < 2; lv++) {
  await wait(700);
  const g = document.getElementById("goal").textContent.match(/From \((−?\d+), (−?\d+)\) to \((−?\d+), (−?\d+)\) in (\d+)/);
  if (!g) break;
  const [sx, sy, tx, ty, n] = g.slice(1).map(num);
  const vx = (tx - sx) / n, vy = (ty - sy) / n;
  for (let i = 0; i < Math.abs(vx); i++) { click(`[data-c="x"][data-d="${vx > 0 ? 1 : -1}"]`); await wait(180); }
  for (let i = 0; i < Math.abs(vy); i++) { click(`[data-c="y"][data-d="${vy > 0 ? 1 : -1}"]`); await wait(180); }
  await wait(500); click("#go");
  await wait(n * 450 + 1600); click("#go");             // "Next level"
}
