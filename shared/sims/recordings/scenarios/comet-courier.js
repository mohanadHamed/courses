// Comet Courier: 4 × (2, 1) crashes into the comet; 1 × (8, 4) delivers.
const $ = (s) => document.querySelector(s);
const set = (id, v) => { for (let i = 0; i < Math.abs(v); i++) { click(`[data-d="${id}${v > 0 ? "+" : "-"}"]`); } };
await wait(500);
click('#frames button[data-n="4"]'); await wait(400); set("vx", 2); await wait(300); set("vy", 1); await wait(700);
click("#go"); await wait(3600);
click('#frames button[data-n="1"]'); await wait(400); set("vx", 6); await wait(300); set("vy", 3); await wait(700);
click("#go"); await wait(2500);
