// Market Desk, message 1: everybody (wrong), then parents and students.
const opt = (t) => [...document.querySelectorAll("#opts button")].find((b) => b.textContent.startsWith(t));
await wait(900); click(opt("everybody")); await wait(1500); click(opt("parents")); await wait(2200);
