// Spec Check: old laptop on low, handheld on high, office PC on high, gaming PC on ultra.
await wait(1000); SPC.pick("old laptop", "medium"); await wait(1300); SPC.pick(null, "low"); await wait(1400); SPC.pick("handheld PC", "high"); await wait(1500);
SPC.pick("office PC", "high"); await wait(1500); SPC.pick("gaming PC", "ultra"); await wait(1600);
