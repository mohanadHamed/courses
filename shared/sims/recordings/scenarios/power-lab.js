// Power Lab: Do not disturb on, then more apps, then the battery drops and power saving starts.
await wait(1500); PL.set({ dnd: true }); await wait(1500);
PL.set({ apps: 7 }); await wait(1600); PL.set({ apps: 0 }); await wait(800);
for (const b of [60, 40, 20]) { PL.set({ bat: b }); await wait(600); }
await wait(900); PL.set({ saver: true }); await wait(2200);
