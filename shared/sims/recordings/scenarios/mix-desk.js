// Mix Desk: ducking on, the voice up, the interface down: every warning turns green.
await wait(1800); MD.set({ duck: true }); await wait(1500); MD.set({ f: { voice: 2 } }); await wait(1500); MD.set({ f: { UI: -4 } }); await wait(2500);
