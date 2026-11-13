// Query Lab, task 1: Type = Drinks, Run.
const set = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event("change")); };
await wait(900); set("cf", "Type"); await wait(600); set("cv", "Drinks"); await wait(600); click("#run"); await wait(2600);
