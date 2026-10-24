// Normal Lab: raise corner C (the normal tilts), swap B and C (the normal points down),
// then look from below (the camera sees the back side).
const h = document.getElementById("h");
const set = (x) => { h.value = x; h.dispatchEvent(new Event("input")); };
await wait(900); set(1); await wait(900); set(2); await wait(1300);
click("#swap"); await wait(1600);
click("#swap"); await wait(600);
click("#below"); await wait(2400);
click("#above"); await wait(800);
