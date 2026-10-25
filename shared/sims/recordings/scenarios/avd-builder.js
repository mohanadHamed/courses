// AVD Builder: the P5 twin, the oldest phone, a tablet, then software graphics.
await wait(1000); AV.set({ prof: "small phone 720×1600, 4 GB", img: "Android 11 (API 30)" }); await wait(1000); AV.create(); await wait(1200);
AV.set({ img: "Android 8 (API 26)" }); await wait(700); AV.create(); await wait(1200);
AV.set({ prof: "tablet 1600×2560, 6 GB", img: "Android 13 (API 33)" }); await wait(1000); AV.create(); await wait(1200);
AV.set({ gfx: "software" }); await wait(1800);
