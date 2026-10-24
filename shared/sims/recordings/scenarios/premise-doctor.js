// Premise Doctor, draft 1: four parts are missing (goal, obstacle, stakes, player action).
await wait(900);
for (const k of ["goal", "obstacle", "stakes", "play"]) { click(`#parts [data-k="${k}"]`); await wait(450); }
await wait(400); click("#check"); await wait(2600);
