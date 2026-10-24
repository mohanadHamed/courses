// Marble Peak, level 1: roll down, right along the bottom, then up.
const hold = async (code, ms) => { window.dispatchEvent(new KeyboardEvent("keydown", { code })); await wait(ms); window.dispatchEvent(new KeyboardEvent("keyup", { code })); };
await wait(500); await hold("ArrowDown", 1300); await hold("ArrowRight", 1500); await hold("ArrowUp", 1200); await hold("ArrowRight", 1400); await hold("ArrowDown", 1400);
