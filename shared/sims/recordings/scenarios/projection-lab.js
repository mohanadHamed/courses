// Projection Lab: v = (5, 0) along (1, 0), then along (0.6, 0.8) and (0.8, 0.6); then v = (2, 4).
const c = document.getElementById("c");
await wait(900); click('[data-u="0.6,0.8"]'); await wait(1600);
click('[data-u="0.8,0.6"]'); await wait(1800);
const r = c.getBoundingClientRect(), u = Math.min((c.clientWidth - 30) / 12, 34);
// drag the tip of v to (2, 4): along 4, side 2 (to the left)
tap(c, r.width / 2 + 2 * u, 15 + 6 * u - 4 * u); await wait(2600);
