// Launch Planner: Android only, then iOS without a Mac, then with a Mac, then both.
await wait(1500); LP.set({ plat: "ios" }); await wait(1800); LP.set({ mac: true }); await wait(1600); LP.set({ plat: "both" }); await wait(2200);
