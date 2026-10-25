// Clean Take: round 1 right, round 2 first wrong (Normalize), then right.
await wait(800); click('#choices button:nth-child(1)'); await wait(1800); click("#next"); await wait(700);
click('#choices button:nth-child(2)'); await wait(1600); click('#choices button:nth-child(1)'); await wait(2000);
