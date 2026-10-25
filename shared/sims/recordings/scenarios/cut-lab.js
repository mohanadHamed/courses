// Cut Lab: a slow wipe first, then a cut on the action; then the dissolve for time passing.
await wait(600); CU.play(); await wait(3200); CU.set({ tr: "cut" }); await wait(500); CU.play(); await wait(2600);
CU.set({ pl: "evening → next morning", tr: "cross dissolve", dur: 1 }); await wait(500); CU.play(); await wait(3000);
