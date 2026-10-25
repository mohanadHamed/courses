// Seed Lab: seed 42 twice, 43, then the bug.
await wait(900); SD.build(42); await wait(1100); SD.build(42); await wait(1100); SD.build(43); await wait(1500); SD.build(43, true); await wait(2000);
