// Sound Stage: walk the fox towards the fire and back.
const hold = async (id, ms) => { const b = document.getElementById(id); const r = b.getBoundingClientRect();
  const o = { clientX: r.left + 5, clientY: r.top + 5, bubbles: true, pointerId: 1 };
  b.dispatchEvent(new PointerEvent("pointerdown", o)); await wait(ms); b.dispatchEvent(new PointerEvent("pointerup", o)); };
await wait(400); click("#start"); await wait(500);
await hold("right", 3200); await wait(400); await hold("left", 2600);
