// Vector Lab: move v to (3, 1), scale it by 2, 0.5 and −1, then show the unit vector of (6, 8).
const k = document.getElementById("k");
const setK = (v) => { k.value = v; k.dispatchEvent(new Event("input")); };
await wait(500); click('[data-c="0"][data-d="1"]'); await wait(500);
for (const v of [2, 0.5, -1]) { setK(v); await wait(1100); }
setK(1); await wait(500);
for (let i = 0; i < 3; i++) { click('[data-c="0"][data-d="1"]'); await wait(160); }
for (let i = 0; i < 7; i++) { click('[data-c="1"][data-d="1"]'); await wait(160); }
await wait(500); const u = document.getElementById("unit"); u.checked = true; u.dispatchEvent(new Event("change"));
await wait(2000);
