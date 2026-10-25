// Formula Lab: type =B2*C2 in D2, copy down, then SUM in D5.
await wait(700); FL.select("D2"); await type(".ms-in", "=B2*C2", 90); await wait(400); click(".ms-ok"); await wait(1500);
click("#down"); await wait(1600);
FL.select("D5"); await type(".ms-in", "=SUM(D2:D4)", 80); await wait(300); click(".ms-ok"); await wait(1800);
