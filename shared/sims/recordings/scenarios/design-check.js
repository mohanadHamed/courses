// Design Check: fix the contrast and the menu, then the phone preview.
const f = (k) => click(`#fixes [data-k="${k}"]`);
await wait(900); f("contrast"); await wait(1200); f("nav"); await wait(1200); f("pic"); await wait(1200); click("#view"); await wait(2400);
