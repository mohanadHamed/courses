// Projection Lab: v = (5, 0) along (1, 0), then along (0.6, 0.8); then the wall slide.
const c = document.getElementById("c");
await wait(900); click('[data-u="0.6,0.8"]'); await wait(1600);
click('[data-u="0.8,0.6"]'); await wait(1400);
click('[data-m="wall"]'); await wait(1600);
const r = c.getBoundingClientRect(), u = Math.min((c.clientWidth - 30) / 12, 34);
// drag the start of v to (−4, 2): v becomes (4, −2)
tap(c, r.width / 2 - 4 * u, 15 + 5 * u - 2 * u); await wait(2200);
