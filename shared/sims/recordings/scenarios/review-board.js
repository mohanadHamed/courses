// Review Board: round 1 approve; round 2 first approve (wrong), then reject.
await wait(800); click('#choices button:nth-child(1)'); await wait(1500); click("#next"); await wait(700);
click('#choices button:nth-child(2)'); await wait(1600); click('#choices button:nth-child(1)'); await wait(1800);
