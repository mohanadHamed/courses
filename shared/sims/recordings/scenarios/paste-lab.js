// Paste Lab: copy in Excel, paste in Word, then try the Paste Options.
await wait(800); click("#copy"); await wait(900); click("#paste"); await wait(1200);
click('#opts [data-o="pic"]'); await wait(1300);
click('#opts [data-o="dest"]'); await wait(1600);
click('#opts [data-o="keep"]'); await wait(1600);
