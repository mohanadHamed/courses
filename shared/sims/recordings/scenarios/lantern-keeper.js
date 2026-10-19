// Lantern Keeper: float and collect fireflies; switch aesthetics and story off and on.
const c = document.getElementById("c");
let t = 0;
const flap = setInterval(() => tap(c), 520);
await wait(2600); click('[data-k="aesthetics"]');
await wait(1800); click('[data-k="aesthetics"]');
await wait(1200); click('[data-k="story"]');
await wait(1500); click('[data-k="story"]');
await wait(1500); clearInterval(flap);
