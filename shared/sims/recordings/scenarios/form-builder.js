// Form Builder: the four types, then a test order.
const t = (q, x) => click(`[data-q="${q}"][data-t="${x}"]`);
await wait(800); t(0, "Text"); await wait(500); t(1, "Text"); await wait(1100); t(1, "Choice"); await wait(600); t(2, "Number"); await wait(500); t(3, "Date"); await wait(700); click("#test"); await wait(2400);
