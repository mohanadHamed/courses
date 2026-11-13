// Key Lab, task 1: Name (wrong), then CustomerID.
const o = (x) => click(`#opts [data-o="${x}"]`);
await wait(900); o("Name"); await wait(1600); o("CustomerID"); await wait(2500);
