// Help Desk, message 1: a wrong answer, then the PDF; message 2: Bold.
const opt = (t) => [...document.querySelectorAll("#opts button")].find((b) => b.textContent.startsWith(t));
await wait(900); click(opt("the Excel file")); await wait(1500);
click(opt("a PDF file")); await wait(1800);
click("#next"); await wait(900); click(opt("Home")); await wait(2200);
