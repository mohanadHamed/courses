// Drawbridge: round 1, first −90° (wrong), then 90°.
await wait(800); click('[data-k="-90°"]'); await wait(2100);
click('[data-k="90°"]'); await wait(2300); click("#next"); await wait(800);
click('[data-k="30°"]'); await wait(1800);
