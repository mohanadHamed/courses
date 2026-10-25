// Roll Lab: a few single rolls, then 10, 100 and 1000.
await wait(800); RL.roll(1); await wait(600); RL.roll(1); await wait(600); RL.roll(10); await wait(1000);
RL.roll(100); await wait(1000); RL.roll(1000); await wait(1200); RL.ev("at least one 6 (two dice)"); await wait(500); RL.roll(1000); await wait(1800);
