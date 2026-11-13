// Team Desk, message 1: Reply all (wrong), then Reply; message 2: Cc.
const opt = (t) => [...document.querySelectorAll("#opts button")].find((b) => b.textContent.startsWith(t));
await wait(900); click(opt("Reply all")); await wait(1500);
click(opt("Reply")); await wait(1800);
click("#next"); await wait(900); click(opt("in Cc")); await wait(2200);
