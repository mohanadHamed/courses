// Service Desk, message 1: a booking (wrong), then an online store.
const opt = (t) => [...document.querySelectorAll("#opts button")].find((b) => b.textContent.startsWith(t));
await wait(900); click(opt("a booking")); await wait(1500); click(opt("an online store")); await wait(2200);
