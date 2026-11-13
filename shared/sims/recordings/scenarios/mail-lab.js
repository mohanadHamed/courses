// Mail Lab, task 1: Omar and Lina in To, Mr Yousef in Cc; a vague subject first, then the clear one.
const seg = (p, w) => click(`.seg[data-p="${p}"] [data-w="${w}"]`);
const pick = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event("change")); };
await wait(800); seg("Omar", "to"); await wait(450); seg("Lina", "to"); await wait(450); seg("Mr Yousef", "cc"); await wait(500);
pick("subj", "Hello"); await wait(450); pick("file", "agenda.docx"); await wait(450); click("#send"); await wait(1900);
pick("subj", "Agenda: staff meeting on Sunday"); await wait(600); click("#send"); await wait(2300);
