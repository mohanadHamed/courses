// Door Logic: round 1 first OR (wrong), then AND; round 2 OR, the door opens.
await wait(800); click('#choices button:nth-child(2)'); await wait(1700);
click('#choices button:nth-child(1)'); await wait(1800); click("#next"); await wait(700);
click('#choices button:nth-child(1)'); await wait(2200);
