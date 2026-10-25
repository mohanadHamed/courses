// Cloud Stack: IaaS first with one wrong layer, then right.
await wait(900); CS.set(["you", "you", "you", "prov", "prov", "prov", "prov"]); await wait(700); CS.check(); await wait(1500);
CS.set(["you", "you", "you", "you", "prov", "prov", "prov"]); await wait(600); CS.check(); await wait(1400);
CS.model("PaaS"); await wait(600); CS.set(["you", "you", "prov", "prov", "prov", "prov", "prov"]); await wait(600); CS.check(); await wait(1600);
