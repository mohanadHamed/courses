// Path Finder: open the folders and tap the file of the task (three rounds).
const rowFor = (name) => [...document.querySelectorAll("#tree .node")].find((r) => r.textContent.trim().split(" ").slice(1).join(" ") === name);
for (let round = 0; round < 3; round++) {
  await wait(900);
  const path = document.querySelector("#task code").textContent.replace(/^C:\\Users\\Sara\\/, "");
  for (const p of path.split("\\")) {
    const r = rowFor(p);
    if (!r) continue;
    if (r.textContent.trim().startsWith("📂")) continue;      // this folder is already open
    r.click(); await wait(600);
  }
  await wait(1100); click("#next");
}
