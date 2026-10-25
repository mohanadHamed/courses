// Deck Checker: mark slide 3 first as OK (wrong), then the right problems of slides 3 and 4.
await wait(900); DC.mark(0, "ok"); await wait(500); DC.mark(1, "pic"); await wait(500); DC.mark(2, "ok"); await wait(1200); DC.mark(2, "num"); await wait(800); DC.mark(3, "claim"); await wait(1800);
