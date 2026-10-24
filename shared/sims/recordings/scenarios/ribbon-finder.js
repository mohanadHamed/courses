// Ribbon Finder: Bold on Home; then Pictures (first a wrong tab, then Insert).
const tabBtn = (t) => [...document.querySelectorAll("#tabs button")].find((b) => b.textContent === t);
const cmd = (c) => document.querySelector(`#body [data-c="${c}"]`);
await wait(800); click(cmd("Bold")); await wait(1400);
click("#next"); await wait(700);
click(tabBtn("Layout")); await wait(700); click(cmd("Margins")); await wait(1100);
click(tabBtn("Insert")); await wait(700); click(cmd("Pictures")); await wait(2200);
