// Truth Table Lab: two examples, then quiz mode with one wrong cell.
await wait(1300); TT.set("p -> q"); await wait(1600); TT.set("p && (q || r)"); await wait(1200);
TT.quiz(true); await wait(900); TT.guess([true, true, false, false, false, false, false, false]); await wait(900); TT.check(); await wait(2000);
