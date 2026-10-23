// Dot Lab: turn the orange arrow from in front, to the side, to behind (drag with pointer events).
const c = document.getElementById("c");
const drag = async (pts) => {
  const r = c.getBoundingClientRect(), u = Math.min(r.width, r.height) / 13;
  const at = (x, y) => ({ clientX: r.left + r.width / 2 + x * u, clientY: r.top + r.height / 2 - y * u, bubbles: true, pointerId: 1, isPrimary: true });
  c.dispatchEvent(new PointerEvent("pointerdown", at(...pts[0])));
  for (const p of pts.slice(1)) { await wait(260); c.dispatchEvent(new PointerEvent("pointermove", at(...p))); }
  c.dispatchEvent(new PointerEvent("pointerup", at(...pts[pts.length - 1])));
};
await wait(600);
await drag([[2, 2], [2, 3], [1, 3], [0, 3]]); await wait(1300);
await drag([[0, 3], [-1, 3], [-2, 2], [-3, 1]]); await wait(1300);
await drag([[-3, 1], [-2, 2], [0, 3], [2, 3], [3, 1]]); await wait(1000);
