// Yaw Lab: turn the tank to 90°, then to −45°, then to 180°.
await wait(900);
for (const t of [15, 30, 45, 60, 75, 90]) { YL.set(t); await wait(260); }
await wait(1300);
for (const t of [60, 30, 0, -15, -30, -45]) { YL.set(t); await wait(260); }
await wait(1300); YL.set(180); await wait(1800);
