// Lighthouse: round 1, first −90° (wrong), then 90°; round 2 starts.
await wait(900); click('[data-k="-90"]'); await wait(2300);
click('[data-k="90"]'); await wait(2500); click("#next"); await wait(900);
click('[data-k="180"]'); await wait(2200);
