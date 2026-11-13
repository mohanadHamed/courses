// Web Desk, message 1: twenty pages (wrong), then Home, Service and Contact.
const opt = (t) => [...document.querySelectorAll("#opts button")].find((b) => b.textContent.startsWith(t));
await wait(900); click(opt("twenty")); await wait(1500); click(opt("Home")); await wait(2200);
