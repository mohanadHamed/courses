// AI Chat: choose the right answer for three prompts.
const pick = (p) => (/ID number|card/.test(p) ? 2 : /When did|15%/.test(p) ? 1 : 0);
for (let n = 0; n < 3; n++) {
  await wait(1100);
  const prompt = document.querySelector("#chat .you").textContent;
  document.querySelectorAll("#opts button")[pick(prompt)].click();
  await wait(2000); click("#next");
}
