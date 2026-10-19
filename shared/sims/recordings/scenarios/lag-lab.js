// Lag Lab: jump locally, then with the lag of cloud gaming.
const c = document.getElementById("c");
tap(c);
let j = setInterval(() => tap(c), 800);
await wait(3600); clearInterval(j);
click('#modes button[data-lag="220"]'); await wait(300); tap(c);
j = setInterval(() => tap(c), 800);
await wait(4000); clearInterval(j);
