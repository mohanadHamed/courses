// Header and Footer Lab: type the header once, add page numbers, then Different First Page.
const h = document.getElementById("head"), text = "Digital Skills · Class report";
await wait(700);
for (let i = 1; i <= text.length; i += 3) { h.value = text.slice(0, i); h.dispatchEvent(new Event("input")); await wait(80); }
h.value = text; h.dispatchEvent(new Event("input")); await wait(900);
const n = document.getElementById("num"); n.value = "bottom"; n.dispatchEvent(new Event("change")); await wait(1500);
const f = document.getElementById("first"); f.checked = true; f.dispatchEvent(new Event("change")); await wait(2200);
