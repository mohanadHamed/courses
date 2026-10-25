// Outline Lab: fix two levels, correct the number, delete the made-up source.
await wait(1000); OL.level(1, 1); await wait(900); OL.level(OL.find(/^E-forms/), 1); await wait(1100);
OL.text(OL.find(/9,000/), "We print 6,500 pages a month"); await wait(1100); OL.del(OL.find(/Source/)); await wait(1100);
OL.text(OL.find(/^Half the paper/), "Half the paper in three months"); await wait(1800);
