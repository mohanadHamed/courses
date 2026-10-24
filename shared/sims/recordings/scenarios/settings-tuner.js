// Settings Tuner, Laptop L1: High textures do not fit, 1080p with shadows is too slow, then it works.
const pick = (k, v) => click(`.seg[data-k="${k}"] button[data-v="${v}"]`);
await wait(700); click("#test"); await wait(1500);
pick("tex", 2); await wait(600); click("#test"); await wait(1500);
pick("sh", 0); await wait(700); click("#test"); await wait(2200);
