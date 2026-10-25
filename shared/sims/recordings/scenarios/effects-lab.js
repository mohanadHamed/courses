// Effects Lab: 60 fps for smooth slow motion, match the colours, move the title.
await wait(1200); EF.set({ src: 60 }); await wait(1500); EF.set({ exp: -20, temp: -10 }); await wait(800); EF.set({ exp: 0, temp: 0 }); await wait(1400);
EF.set({ ty: 80 }); await wait(1800);
