// Rule Detective: round 1 first OR (wrong), then AND; round 2 right.
await wait(900); click('#choices button:nth-child(2)'); await wait(1700);
click('#choices button:nth-child(1)'); await wait(1700); click("#next"); await wait(700);
click('#choices button:nth-child(1)'); await wait(1800);
