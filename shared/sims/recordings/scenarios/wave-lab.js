// Wave Lab: play the lift (Bob), then the orbit, then the sweep.
await wait(500); click("#play"); await wait(3200);
click('[data-m="orbit"]'); await wait(2600);
click('[data-m="sweep"]'); await wait(2600);
