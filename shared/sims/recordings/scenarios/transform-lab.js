// Transform Lab: scale 2 about the origin, then about the centre, then mirror.
await wait(800); setVal('#sl label:nth-child(3) input', 2); setVal('#sl label:nth-child(4) input', 2); await wait(1600);
click('#opt [data-k="centre"]'); await wait(1600);
setVal('#sl label:nth-child(3) input', -1); setVal('#sl label:nth-child(4) input', 1); await wait(1400);
click('#opt [data-k="feet"]'); await wait(1400); click('#opt [data-k="order"]'); await wait(1200);
