// Ember Trail media hunt: answer the first orders by tapping the elements.
const c = document.getElementById("c");
const W = c.clientWidth, H = c.clientHeight;
const at = (fx, fy) => tap(c, fx * W, fy * H);
const answers = { audio: [0.62, 0.74], interface: [0.13, 0.08], cinematic: [0.62, 0.10], feedback: [0.80, 0.50], guidance: [0.90, 0.68], story: [0.36, 0.42] };
await wait(500); click("#start");
for (let i = 0; i < 5; i++) {
  await wait(1300);
  const o = document.getElementById("order").textContent;
  const k = Object.keys(answers).find((a) => o.includes(a));
  if (i === 1) at(0.30, 0.72);                    // the fox is not interface: a mistake on purpose
  else if (k) at(...answers[k]);
  await wait(i === 1 ? 1500 : 700);
}
