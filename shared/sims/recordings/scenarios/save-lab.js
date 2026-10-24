// Save Lab: lose unsaved text, then save, then AutoSave in OneDrive keeps everything.
const d = document.getElementById("doc");
const type = async (t) => { for (const ch of t) { d.value += ch; d.dispatchEvent(new Event("input")); await wait(35); } };
await wait(600); await type(" We read books."); await wait(400); click("#cut"); await wait(1500);
click("#cloud"); await wait(700); click("#auto"); await wait(700);
await type(" We read books."); await wait(2600); click("#cut"); await wait(2200);
