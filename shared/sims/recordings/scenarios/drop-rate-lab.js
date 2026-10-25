// Drop Rate Lab: 5 %, simulate; then 11 %; then 5 % with a pity timer.
await wait(900); DR.sim(); await wait(1500); DR.set({ p: 11 }); await wait(1300); DR.set({ p: 5, pity: true }); await wait(700); DR.sim(); await wait(1800);
