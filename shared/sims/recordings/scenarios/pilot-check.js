// Pilot Check: round 1 first 0.083 (wrong), then 0.167.
await wait(1000); click('#choices button:nth-child(3)'); await wait(1800); click('#choices button:nth-child(1)'); await wait(1900);
click("#next"); await wait(900); click('#choices button:nth-child(1)'); await wait(1800);
