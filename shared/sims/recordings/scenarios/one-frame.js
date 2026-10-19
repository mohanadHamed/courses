// Tap Runner: jump over the blocks.
const c = document.getElementById("c");
tap(c);
const j = setInterval(() => tap(c), 750);
await wait(7500); clearInterval(j);
