// Audit Board: set some statuses, one wrong, check; then correct the audit.
await wait(900); AB.set(0, "cleared"); await wait(400); AB.set(1, "cleared"); await wait(400); AB.set(4, "replace"); await wait(400); AB.set(5, "replace"); await wait(600); AB.check(); await wait(1600);
AB.solve(); await wait(600); AB.check(); await wait(2000);
