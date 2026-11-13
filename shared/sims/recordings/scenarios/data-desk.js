// Data Desk, message 1: Name (wrong), then the primary key; message 2: Currency.
const opt = (t) => [...document.querySelectorAll("#opts button")].find((b) => b.textContent.startsWith(t));
await wait(900); click(opt("Name")); await wait(1500); click(opt("CustomerID")); await wait(1800);
click("#next"); await wait(900); click(opt("Currency")); await wait(2200);
