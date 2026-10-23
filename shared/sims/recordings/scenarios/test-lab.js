// Test Lab: the first requests, one wrong device, then the right ones.
const dev = (id) => click(`.dev[data-id="${id}"]`);
await wait(800); dev("P1"); await wait(1400); dev("L1"); await wait(1600); click("#next");
await wait(900); dev("P1"); await wait(1600); click("#next");
await wait(900); dev("P2"); await wait(1600);
