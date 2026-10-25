// Rights Check: Pasha passes all five questions, the theme music stops at question 2.
await wait(900); for (let i = 0; i < 5; i++) { RC.next(); await wait(650); } await wait(900);
RC.check("theme music"); await wait(700); RC.next(); await wait(700); RC.next(); await wait(1600);
