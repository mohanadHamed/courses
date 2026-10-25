// Sample Space Lab: even on one die, then A or B, then not A on two dice.
await wait(900); SS.set({ a: "even" }); await wait(1300); SS.set({ op: "A or B" }); await wait(1600);
SS.set({ ex: "Two dice", a: "at least one 6", b: "sum 7", op: "A" }); await wait(1400); SS.set({ op: "not A" }); await wait(2000);
