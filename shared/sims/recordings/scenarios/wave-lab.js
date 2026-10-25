// Wave Lab: louder and higher, then a better sample rate and bit depth.
await wait(1000); WL.set({ f: 880 }); await wait(1300); WL.set({ a: 0.4 }); await wait(1300);
WL.set({ wave: "square" }); await wait(1200); WL.set({ wave: "sine", rate: 22050 }); await wait(1300);
WL.set({ bits: 8 }); await wait(1200); WL.set({ rate: 48000, bits: 16, ch: 2 }); await wait(1800);
