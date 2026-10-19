// Pocket Pets support desk: answer four messages (one mistake).
const part = (t) => /core|GHz|move in jumps|50 of them/.test(t) ? "cpu" : /blurry|title screen|4 GB|8 GB|stutters/.test(t) ? "ram" : "storage";
await wait(500); click("#start");
for (let i = 0; i < 4; i++) {
  await wait(1600);
  const t = document.querySelector("#card .text").textContent;
  let p = part(t);
  if (i === 1) p = p === "cpu" ? "storage" : "cpu";            // a mistake on purpose
  click(`[data-p="${p}"]`);
  await wait(i === 1 ? 2700 : 1600);
}
