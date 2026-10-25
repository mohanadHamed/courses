// Reference Lab: =B2*F1 copied down (zeros), then =B2*$F$1 copied down.
await wait(600); RLab.select("C2"); await type(".ms-in", "=B2*F1", 90); click(".ms-ok"); await wait(500);
RLab.select("C2"); click("#down"); await wait(2000);
await type(".ms-in", "=B2*$F$1", 90); click(".ms-ok"); await wait(400); RLab.select("C2"); click("#down"); await wait(2200);
