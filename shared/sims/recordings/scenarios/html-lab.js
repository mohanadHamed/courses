// HTML Lab: the heading green and bigger, then the first question.
const set = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event("change")); };
await wait(900); set("col", "green"); await wait(1100); set("size", "36px"); await wait(1100);
[...document.querySelectorAll("#q button")][0].click(); await wait(2400);
