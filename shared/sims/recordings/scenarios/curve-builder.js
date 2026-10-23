// Curve Builder: the first draft, then move the peak from stage 3 to stage 7 and add a hook.
const step = (i, d, n) => { for (let k = 0; k < n; k++) click(`[data-i="${i}"][data-d="${d}"]`); };
await wait(900);
for (let k = 0; k < 5; k++) { step(2, -1, 1); await wait(170); }
for (let k = 0; k < 3; k++) { step(6, 1, 1); await wait(200); }
for (let k = 0; k < 2; k++) { step(5, 1, 1); await wait(200); }
for (let k = 0; k < 3; k++) { step(0, 1, 1); await wait(200); }
step(3, -1, 3); await wait(300);
await wait(1800); click('[data-p="final"]'); await wait(1500);
