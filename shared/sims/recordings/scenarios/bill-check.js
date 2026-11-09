// Bill Check: the totals with a formula, copy down, SUM, then the verdict.
await wait(700); BC.select("D2"); await type(".ms-in", "=B2*C2", 90); await wait(400); click(".ms-ok"); await wait(1300);
BC.select("D2"); await wait(300); click("#down"); await wait(1300);
BC.select("D4"); await type(".ms-in", "=SUM(D2:D3)", 80); await wait(300); click(".ms-ok"); await wait(1500);
click("#sheetRight"); await wait(2000);
