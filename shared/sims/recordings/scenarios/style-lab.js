// Style Lab: style the lines one after the other (the Navigation Pane grows), then change Heading 1 once.
const st = (s) => click(`[data-s="${s}"]`);
await wait(600); document.querySelectorAll("#page p")[0].click(); await wait(300);
for (const s of ["Title", "Heading 1", "Normal", "Heading 2", "Normal", "Heading 2", "Normal", "Heading 1", "Normal"]) { st(s); await wait(420); }
click("#check"); await wait(1200); click("#look"); await wait(1400); click("#look"); await wait(1200);
