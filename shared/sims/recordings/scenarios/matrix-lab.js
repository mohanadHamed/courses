// Matrix Lab: A + B, explain one entry, then k × A, then the size mismatch.
await wait(700); tap(document.querySelectorAll(".mat.res span")[1]); await wait(1500);
click('[data-k="k"]'); await wait(600); setVal('#kbox input', 2); await wait(600);
tap(document.querySelectorAll(".mat.res span")[3]); await wait(1500);
click('[data-k="add"]'); await wait(500); click("#shape"); await wait(1800);
