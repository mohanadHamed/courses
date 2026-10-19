// Tap Runner in slow motion: step frame by frame; the parts of the computer light up.
const c = document.getElementById("c");
tap(c); await wait(600);
click("#slow"); await wait(500);
for (let i = 0; i < 40; i++) {
  if (i === 2 || i === 22) tap(c);                       // a tap: the input of the next frame
  click("#step"); await wait(200);
}
