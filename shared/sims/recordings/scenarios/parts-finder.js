// Parts Finder: round 1 by name, with one wrong tap, then two cards of round 2.
const tapPart = (p) => document.querySelector(`.part[data-part="${p}"]`).dispatchEvent(new MouseEvent("click", { bubbles: true }));
await wait(700); tapPart("cpu"); await wait(1300); tapPart("ram"); await wait(1300); click("#next");
await wait(700); tapPart("cpu"); await wait(1200); click("#next");
await wait(700); tapPart("ssd"); await wait(1200); click("#next");
await wait(700); tapPart("psu"); await wait(1300); tapPart("gpu"); await wait(1400);
