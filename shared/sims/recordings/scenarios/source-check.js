// Source Check: source 1 used, source 2 skipped.
await wait(1000); SC.tick([0, 1, 2]); await wait(800); SC.use(); await wait(2000);
SC.go(1); await wait(1200); SC.skip(); await wait(2200);
