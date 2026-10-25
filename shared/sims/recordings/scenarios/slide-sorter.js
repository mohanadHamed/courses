// Slide Sorter: move the question to the top, check, then sort and check again.
await wait(900); SS.move(2, -1); await wait(500); SS.move(1, -1); await wait(600); SS.check(); await wait(1500); SS.solve(); await wait(700); SS.check(); await wait(1800);
