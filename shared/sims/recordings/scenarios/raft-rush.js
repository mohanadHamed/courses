// Raft Rush, round 1: paddle (0, 4) drifts past the dock; paddle (−3, 4) lands on it.
const set = (i, n) => { for (let k = 0; k < Math.abs(n); k++) click(`[data-c="${i}"][data-d="${n > 0 ? 1 : -1}"]`); };
await wait(500);
for (let k = 0; k < 4; k++) { set(1, 1); await wait(180); }
await wait(500); click("#go"); await wait(1800); click("#go"); await wait(400);
for (let k = 0; k < 3; k++) { set(0, -1); await wait(220); }
await wait(700); click("#go"); await wait(2400);
