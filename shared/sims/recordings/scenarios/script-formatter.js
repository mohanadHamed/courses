// Script Formatter: tag the eight lines of the opening scene, then format the page.
const order = ["heading", "action", "action", "character", "paren", "dialogue", "action", "transition"];
await wait(600);
for (const k of order) { click(`[data-k="${k}"]`); await wait(650); }
click("#format"); await wait(3000);
