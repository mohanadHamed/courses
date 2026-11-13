// Phish Finder, message 1: Safe (wrong), then Phishing with its signs; message 2: Safe.
const btn = (a) => document.querySelector(`#btns [data-a="${a}"]`);
await wait(900); click(btn("safe")); await wait(1500); click(btn("phish")); await wait(2200);
click("#next"); await wait(900); click(btn("safe")); await wait(2000);
