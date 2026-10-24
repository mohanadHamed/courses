// List and Table Lab: numbering for the steps, bullets for the things, then a 5 × 2 table with a header row.
await wait(700); click('[data-l="0"][data-k="num"]'); await wait(1100);
click('[data-l="1"][data-k="bul"]'); await wait(1100);
click('#grid span[data-r="4"][data-c="3"]'); await wait(1300);
click('#grid span[data-r="5"][data-c="2"]'); await wait(1300);
const h = document.getElementById("header"); h.checked = true; h.dispatchEvent(new Event("change")); await wait(2000);
