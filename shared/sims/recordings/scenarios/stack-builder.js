// Stack Builder: Android, one wrong layer first, then the right order; then iOS.
await wait(900); SB.pick("App framework"); await wait(1600);
for (const n of ["Linux kernel", "Libraries", "App framework", "Apps"]) { SB.pick(n); await wait(750); }
await wait(1200);
SB.os("ios"); await wait(700);
for (const n of ["Apple's kernel", "Libraries", "App framework", "Apps"]) { SB.pick(n); await wait(600); }
await wait(1500);
