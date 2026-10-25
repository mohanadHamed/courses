// Cloud Cost Planner: near region, CDN, fewer hours, then more players.
await wait(1000); CC.set({ region: "Bahrain (near)" }); await wait(1300); CC.set({ cdn: "through a CDN" }); await wait(1300);
CC.set({ hours: 8 }); await wait(1400); CC.set({ players: 120000 }); await wait(1800);
