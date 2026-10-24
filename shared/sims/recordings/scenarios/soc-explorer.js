// SoC Explorer: tap the GPU and the modem, then answer the first quiz question.
await wait(600); click('[data-k="gpu"]'); await wait(1700);
click('[data-k="modem"]'); await wait(1700);
click("#quiz"); await wait(1500);
click('[data-k="cpu"]'); await wait(1300);
click('[data-k="gpu"]'); await wait(1800);
