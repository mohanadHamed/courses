// Right Tool: choose the tool for four jobs (one wrong try first).
const RT = { "library": 1, "40 prices": 2, "thank-you": 0, "dollar": 1, "trip": 0, "average": 2, "article": 0, "scholarship": 1 };
for (let n = 0; n < 4; n++) {
  await wait(900);
  const job = document.querySelector("#job").textContent;
  const right = RT[Object.keys(RT).find((x) => job.includes(x))];
  const tools = document.querySelectorAll("#tools .tool");
  if (n === 0) { tools[(right + 1) % 3].click(); await wait(900); }
  tools[right].click();
  await wait(1200); click("#next");
}
