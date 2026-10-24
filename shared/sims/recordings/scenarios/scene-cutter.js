// Scene Cutter, scene 1: cut a key line by mistake, bring it back, then cut the weak lines.
const t = (i) => click(`.ln[data-i="${i}"]`);
await wait(700); t(2); await wait(500); t(4); await wait(500); click("#check"); await wait(1800);
t(4); await wait(500);
for (const i of [3, 5, 6, 7]) { t(i); await wait(500); }
click("#check"); await wait(2500);
