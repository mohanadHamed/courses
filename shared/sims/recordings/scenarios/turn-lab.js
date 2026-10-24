// Turn Lab: facing 350°, the target at (6, 1); the turret turns 20° left. Then a target behind.
const c = document.getElementById("c"), W = c.clientWidth, H = c.clientHeight, u = Math.min((W - 30) / 12, 28);
await wait(600); click('[data-f="350"]'); await wait(900);
tap(c, W / 2 + 6 * u, H / 2 - 1 * u); await wait(1400);
click("#go"); await wait(1600);
tap(c, W / 2 - 3 * u, H / 2 - 3 * u); await wait(1300);
click("#go"); await wait(2400);
