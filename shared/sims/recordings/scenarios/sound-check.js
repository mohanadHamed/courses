// Sound Check: round 1 first louder (wrong), then ducking; round 2 right.
await wait(800); click('#choices button:nth-child(2)'); await wait(1500);
click('#choices button:nth-child(1)'); await wait(1700); click("#next"); await wait(700);
click('#choices button:nth-child(1)'); await wait(1800);
