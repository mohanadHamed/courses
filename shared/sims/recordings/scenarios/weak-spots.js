// Weak Spots: classify three AI answers.
const KIND = { "book": 0, "newest version": 1, "pens": 2, "nurse": 3, "homework": 4, "tips": 5, "award": 0 };
for (let n = 0; n < 3; n++) {
  await wait(1200);
  const q = document.querySelector("#q").textContent;
  const k = Object.keys(KIND).find((x) => q.includes(x));
  document.querySelectorAll("#opts button")[KIND[k]].click();
  await wait(1700); click("#next");
}
