// Tilt Lab: drag the pad to tilt right, hold still (the gyroscope goes to 0), then tilt towards the bottom.
const c = document.getElementById("c"), r = c.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
const ev = (t, x, y) => c.dispatchEvent(new PointerEvent(t, { clientX: x, clientY: y, pointerId: 1, bubbles: true, isPrimary: true }));
await wait(600); ev("pointerdown", cx, cy);
for (let k = 1; k <= 12; k++) { ev("pointermove", cx + k * 8, cy); await wait(50); }
await wait(2200);
for (let k = 1; k <= 12; k++) { ev("pointermove", cx + 96 - k * 8, cy + k * 8); await wait(50); }
await wait(2600); ev("pointerup", cx, cy + 96); await wait(600);
