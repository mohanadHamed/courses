// Guard Brain: the guard sees the player near, then the rules are put in the right order.
await wait(1000); GB.facts({ s: true }); await wait(1200); GB.facts({ n: true }); await wait(1500);
GB.order(["Attack", "Chase", "Flee"]); await wait(1400); GB.facts({ w: true }); await wait(1300);
GB.order(["Flee", "Attack", "Chase"]); await wait(2000);
