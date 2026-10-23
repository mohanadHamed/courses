// App Launcher: read the job and tap the right app (one wrong try first).
const RIGHT = { letter: "Word", prices: "Excel", slides: "PowerPoint", meeting: "Outlook", phone: "OneDrive", video: "Teams", summary: "Copilot", visitors: "Excel" };
const appFor = (job) => RIGHT[Object.keys(RIGHT).find((k) => job.includes(k))];
for (let n = 0; n < 4; n++) {
  await wait(900);
  const app = appFor(document.querySelector("#job").textContent);
  const btns = [...document.querySelectorAll("#apps .app")];
  if (n === 0) { btns.find((b) => b.dataset.app !== app).click(); await wait(1000); }
  btns.find((b) => b.dataset.app === app).click();
  await wait(1300); click("#next");
}
