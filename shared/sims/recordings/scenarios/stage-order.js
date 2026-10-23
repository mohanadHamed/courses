// Stage Order: place the cards (the guardian too early), check, then fix the order.
const pl = (k) => click(`#deck [data-k="${k}"]`);
await wait(600);
for (const k of ["alarm", "map", "guardian", "caves", "eel", "garden", "dark", "lights"]) { pl(k); await wait(260); }
click("#check"); await wait(1800);
click("#reset"); await wait(400);
for (const k of ["alarm", "map", "caves", "garden", "eel", "dark", "guardian", "lights"]) { pl(k); await wait(200); }
click("#check"); await wait(1800);
