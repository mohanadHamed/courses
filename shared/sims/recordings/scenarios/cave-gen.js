// Cave Generator: seeds 43 and back to 42, random tiles, then tests of 100 seeds.
await wait(900); CG.seed(43); await wait(1000); CG.seed(42); await wait(1000); CG.mode("random tiles"); await wait(1000); CG.seed(44); await wait(1000); CG.test(); await wait(1600); CG.mode("random walk"); CG.test(); await wait(1600);
