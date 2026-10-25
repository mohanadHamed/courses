// Shape Lab: one die, three dice, then coins in the round room.
await wait(700); SH.go(); await wait(1300); SH.set({ dice: 3 }); SH.go(); await wait(1500);
SH.set({ mode: "circle", sqrt: false }); SH.go(); await wait(1500); SH.set({ sqrt: true }); SH.go(); await wait(1700);
