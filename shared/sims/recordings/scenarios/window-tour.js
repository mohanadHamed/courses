// Window Tour: Word tasks (one wrong tap), then the first Excel tasks.
const z = (k) => click(`[data-z="${k}"]`);
await wait(800); z("ribbon"); await wait(900);
for (const k of ["title", "ribbon", "tab"]) { z(k); await wait(800); }
click('[data-app="excel"]'); await wait(900);
for (const k of ["cell", "col", "sheet"]) { z(k); await wait(800); }
await wait(600);
