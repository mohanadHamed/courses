// Transition Lab: a quiet Fade on all slides, then the points come one by one (Fade).
await wait(600);
TL.set({ tr: "Fade", dur: 0.7, all: true });
await wait(1200);
TL.set({ an: "Fade" });
await wait(900);
TL.next();
await wait(1500);
TL.next(); await wait(900);
TL.next(); await wait(900);
TL.next(); await wait(1300);
TL.next(); await wait(1500);
TL.next(); await wait(900);
