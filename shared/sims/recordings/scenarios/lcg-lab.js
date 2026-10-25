// LCG Lab: the full period of 16, then c = 4 (period 1), then m = 256, then a new seed.
await wait(600); LG2.set({ seed: 7 });
await wait(1200); LG2.set({ c: 4 }); await wait(1600); LG2.set({ c: 3, m: 256 }); await wait(1600); LG2.set({ seed: 99 }); await wait(1800);
