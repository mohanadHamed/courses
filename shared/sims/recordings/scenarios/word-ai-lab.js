// Word AI Lab: Sum up, tap a right part, then the wrong one, then insert.
await wait(600); click('#tabs [data-k="Sum up"]'); await wait(1200);
tap(document.querySelector('#out span[data-i="0"]')); await wait(1300);
tap(document.querySelector('#out span[data-i="2"]')); await wait(2600);
click("#ins"); await wait(1600);
