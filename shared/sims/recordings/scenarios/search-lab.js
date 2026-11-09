// Search Lab: an ad first (wrong), then the official result; three searches.
await wait(900); click(document.querySelectorAll(".res")[0]); await wait(1500);
click(document.querySelectorAll(".res")[1]); await wait(1700); click("#next"); await wait(900);
click(document.querySelectorAll(".res")[0]); await wait(1700); click("#next"); await wait(900);
click(document.querySelectorAll(".res")[2]); await wait(2200);
