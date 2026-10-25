// Matrix Chain: scale 2, then turn to 90°, then move to (5, 1).
await wait(900); MC.set({ k: 2 }); await wait(1300);
for (const t of [30, 60, 90]) { MC.set({ th: t }); await wait(500); }
await wait(700); MC.set({ tx: 5, ty: 1 }); await wait(2200);
