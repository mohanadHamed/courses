// Loop Builder: the example loop plays; calm state mutes the drums; then chase again.
await wait(1200); LB.play(); await wait(3000);
LB.set({ state: "calm" }); await wait(2500); LB.set({ state: "chase", bpm: 130 }); await wait(2500);
