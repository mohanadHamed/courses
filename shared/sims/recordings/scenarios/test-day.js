// Test Day: round 1, first "start the test anyway" (wrong), then the right step.
const b = () => document.querySelectorAll("#choices button");
await wait(900); b()[2].click(); await wait(1500); b()[0].click(); await wait(2000);
click("#next"); await wait(900); b()[0].click(); await wait(1600);
