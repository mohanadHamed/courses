// Edit Doctor: round 1 first a longer wipe (wrong), then the cut on action.
await wait(1000); click('#choices button:nth-child(2)'); await wait(1800); click('#choices button:nth-child(1)'); await wait(1900);
click("#next"); await wait(900); click('#choices button:nth-child(1)'); await wait(1800);
