// Emulator or Real?: round 1 first a real phone (wrong), then the emulator.
await wait(1000); click('#choices button:nth-child(2)'); await wait(1800); click('#choices button:nth-child(1)'); await wait(1900);
click("#next"); await wait(900); click('#choices button:nth-child(2)'); await wait(1800);
