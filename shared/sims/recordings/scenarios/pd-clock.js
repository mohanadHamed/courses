// Public Domain Clock: 1950 under life + 70, then 1960 under both rules.
await wait(1000); PD.set({ died: 1950 }); await wait(1700); PD.set({ died: 1960, rule: 50 }); await wait(1600); PD.set({ rule: 70 }); await wait(1800);
