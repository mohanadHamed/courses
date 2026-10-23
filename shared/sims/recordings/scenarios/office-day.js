// Monday at Sunrise Company: the best choices for the six jobs (finish at 10:25).
const BEST = [["Outlook", 0], ["Excel", 1], ["PowerPoint", 0], ["Word", 0], ["Excel", 1], ["OneDrive", 1]];
await wait(600);
for (const [app, ai] of BEST) {
  [...document.querySelectorAll("#apps button")].find((b) => b.textContent === app).click(); await wait(350);
  document.querySelectorAll("#ai button")[ai].click(); await wait(350);
  click("#go"); await wait(800);
}
await wait(2000);
