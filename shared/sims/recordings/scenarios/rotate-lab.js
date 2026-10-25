// Rotate Lab: turn around the origin, then around a pivot at (1, 0).
for (const t of [45, 60, 90]) { RL.set(t, [0, 0]); await wait(900); }
for (const t of [90, 120, 150, 180]) { RL.set(t, [1, 0]); await wait(900); }
RL.set(-90, [2, 1]); await wait(1500);
