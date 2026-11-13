// Report Lab: group by Type, sort by Price, show the totals.
const tick = (id) => { const e = document.getElementById(id); e.checked = true; e.dispatchEvent(new Event("change")); };
await wait(900); tick("g"); await wait(1500); tick("s"); await wait(1500); tick("t"); await wait(2600);
