// Rooftop Rescue: row down the street; the lines play on their triggers; at the roof, Nour answers.
await wait(900);
for (let k = 0; k < 40; k++) { click("#row"); await wait(190); if (document.querySelector('[data-c="a"]')) break; }
await wait(900); click('[data-c="a"]'); await wait(2000);
