// Talk Planner (five-slide talk): put the slides in order, add notes, set the times.
await wait(800); TP.order(["Title", "The problem", "The idea", "An example", "Thank you and questions"]); await wait(900);
TP.note("Title", "Good morning, I am Sami from class B."); await wait(400);
TP.note("The problem", "Many students work until four and cannot come."); await wait(400);
TP.note("The idea", "Open until seven on three days."); await wait(400);
TP.note("An example", "Twenty students in my class would come."); await wait(400);
TP.note("Thank you and questions", "Thank you, now your questions please."); await wait(500);
TP.time("The idea", 45); await wait(400); TP.time("An example", 45); await wait(1800);
