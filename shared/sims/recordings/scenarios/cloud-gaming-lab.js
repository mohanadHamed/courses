// Cloud Gaming Lab: raise the bandwidth, 1080p, lower the ping, then 4K.
await wait(1200); CG.set({ bw: 12 }); await wait(1500); CG.set({ res: "1080p" }); await wait(1300); CG.set({ bw: 22 }); await wait(1400);
CG.set({ ping: 30 }); await wait(1600); CG.set({ res: "4K", bw: 25 }); await wait(1800);
