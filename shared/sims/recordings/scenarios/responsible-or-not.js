// Responsible or Not?: round 1 first "OK: it is faster" (wrong), then the right answer.
await wait(1000); click('#choices button:nth-child(2)'); await wait(1800); click('#choices button:nth-child(1)'); await wait(1900);
click("#next"); await wait(900); click('#choices button:nth-child(1)'); await wait(1800);
