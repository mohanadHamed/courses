// Input Lab: three fingers on the pad, the stick pushed half way, then button A.
const pad = document.getElementById("pad"), r = pad.getBoundingClientRect();
const ev = (el, t, id, x, y, type = "touch") => el.dispatchEvent(new PointerEvent(t, { clientX: x, clientY: y, pointerId: id, bubbles: true, pointerType: type, isPrimary: id === 1 }));
await wait(700);
for (let k = 0; k < 3; k++) { ev(pad, "pointerdown", 11 + k, r.left + 60 + k * 70, r.top + 80); await wait(500); }
await wait(900);
for (let k = 0; k < 3; k++) ev(pad, "pointerup", 11 + k, r.left + 60 + k * 70, r.top + 80);
const st = document.getElementById("stick"), s = st.getBoundingClientRect(), cx = s.left + s.width / 2, cy = s.top + s.height / 2;
ev(st, "pointerdown", 21, cx, cy, "mouse");
for (let k = 1; k <= 10; k++) { ev(st, "pointermove", 21, cx + k * 2, cy, "mouse"); await wait(60); }
await wait(1200);
ev(st, "pointerup", 21, cx + 20, cy, "mouse");
const a = document.getElementById("ba"); a.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true })); await wait(900);
a.dispatchEvent(new PointerEvent("pointerup", { bubbles: true })); await wait(800);
