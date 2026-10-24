// PDF Export: the desktop path File › Save As › PDF › Save, then the web path.
const c = (t) => click([...document.querySelectorAll("#win button")].find((b) => b.dataset.c === t));
await wait(800); c("File"); await wait(700); c("Save As"); await wait(700); c("PDF (*.pdf)"); await wait(700); c("Save"); await wait(1500);
click('[data-m="web"]'); await wait(700); c("File"); await wait(700); c("Export"); await wait(700); c("Download as PDF"); await wait(700); c("Download"); await wait(1800);
