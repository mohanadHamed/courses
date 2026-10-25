// Board Builder: choose four shots (one wrong), check, fix panel 4, check again.
const s = document.querySelectorAll(".pn select");
const set = (i, v) => { s[i].value = v; s[i].dispatchEvent(new Event("change")); };
await wait(600); set(0, "wideStreet"); await wait(600); set(1, "medNour"); await wait(600); set(2, "closeNour"); await wait(600); set(3, "wideRoof"); await wait(800);
click("#check"); await wait(2200); set(3, "closeSalma"); await wait(800); click("#check"); await wait(1800);
