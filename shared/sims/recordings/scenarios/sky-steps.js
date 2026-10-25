// Sky Steps: round 1, first "move (5, 4)" (wrong), then "move (4, 3)".
await wait(800); click('[data-k="move (5, 4)"]'); await wait(1900);
click('[data-k="move (4, 3)"]'); await wait(2000); click("#next"); await wait(800);
click('[data-k="scale 2 about the origin"]'); await wait(1800);
