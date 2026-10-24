// Contents Builder: heading styles, insert the contents, change a heading, update.
const b = (t) => [...document.querySelectorAll(".ribbon button")].find((x) => x.textContent === t).click();
await wait(600);
for (const s of ["Heading 1", "Normal", "Heading 1", "Heading 2", "Heading 2", "Heading 1"]) { b(s); await wait(380); }
b("Insert contents"); await wait(1500); b("Change a heading"); await wait(1700); b("Update Table"); await wait(2000);
