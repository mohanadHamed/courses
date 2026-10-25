// Packet Journey: TCP with no loss, TCP with 20 % loss, then UDP with 20 % loss.
await wait(800); PJ.send(); await wait(4200);
PJ.set({ loss: 20 }); await wait(500); PJ.send(); await wait(5200);
PJ.set({ proto: "UDP" }); await wait(700); PJ.send(); await wait(4200);
