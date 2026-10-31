// Move Lab: diagonal without and with normalizing, then facing the velocity up and to the left.
await wait(600); ML.input(1, 1); await wait(1500); ML.rule("normalize input", true); await wait(1500);
ML.rule("face the velocity", true); ML.input(0, 1); await wait(1600); ML.input(-1, 0); await wait(1600); ML.input(1, -1); await wait(1500);
