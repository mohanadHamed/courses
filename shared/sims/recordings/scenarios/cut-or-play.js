// Cut or Play?: round 1, first "gameplay" (wrong), then "cutscene"; round 2 "gameplay".
const b = () => document.querySelectorAll("#choices button");
await wait(900); b()[1].click(); await wait(1500); b()[0].click(); await wait(1900);
click("#next"); await wait(900); b()[1].click(); await wait(1600);
