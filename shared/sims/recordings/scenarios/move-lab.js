// Move Lab: diagonal without and with normalizing, then acceleration and facing, then let go.
await wait(600); ML.input(1, 1); await wait(1500); ML.rule("normalize input", true); await wait(1500);
ML.rule("accelerate", true); ML.rule("face the velocity", true); ML.input(-1, 0); await wait(1600); ML.input(0, 1); await wait(1300); ML.input(0, 0); await wait(1800);
