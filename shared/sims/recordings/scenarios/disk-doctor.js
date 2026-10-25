// Disk Doctor: round 1, first "the stick is full" (wrong), then FAT32.
const b = () => document.querySelectorAll("#choices button");
await wait(900); b()[1].click(); await wait(1600); b()[0].click(); await wait(2200);
click("#next"); await wait(900); b()[1].click(); await wait(1500);
