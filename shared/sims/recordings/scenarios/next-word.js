// Next Word: build the sentence by hand (the likely 8), then let the AI choose once more.
const tapWord = (w) => { const b = [...document.querySelectorAll("#cands .cand")].find((x) => x.firstChild.textContent === w); if (b) b.click(); };
await wait(700);
for (const w of ["at", "8", "a.m.", "every", "morning."]) { tapWord(w); await wait(650); }
await wait(2200);
click("#again");
await wait(4500);
