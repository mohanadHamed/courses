// Share Settings, task 1: Anyone + Can edit is wrong; Specific people (Rana) + Can view is right.
const who = (v) => { const r = document.querySelector(`input[value="${v}"]`); r.checked = true; r.dispatchEvent(new Event("change")); };
const perm = (p) => click(`.seg [data-p="${p}"]`);
await wait(800); who("anyone"); await wait(500); perm("edit"); await wait(500); click("#link"); await wait(1800);
who("specific"); await wait(400);
const n = document.getElementById("names"); for (const ch of "Rana") { n.value += ch; await wait(90); }
await wait(300); perm("view"); await wait(500); click("#link"); await wait(2200);
