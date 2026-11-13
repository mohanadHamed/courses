// Password Check: a weak example, then a passphrase typed letter by letter.
const ex = (t) => [...document.querySelectorAll("#ex button")].find((b) => b.textContent === t);
await wait(800); click(ex("sami2005")); await wait(1800);
const p = document.getElementById("pw"); p.value = "";
for (const ch of "Blue-Camel-Rain-47") { p.value += ch; p.dispatchEvent(new Event("input")); await wait(110); }
await wait(2400);
