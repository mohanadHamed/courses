// Table Lab: sort by Total largest first, filter Drinks, then all, then highlight > 20.
await wait(1200); TL.sort(4, -1); await wait(2000); TL.filter("Drinks"); await wait(2000);
TL.filter("All"); await wait(900); TL.hl(20); await wait(2200);
