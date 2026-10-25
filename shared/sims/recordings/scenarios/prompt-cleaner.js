// Prompt Cleaner: clean Huda's reminder (the amount stays), then start Sami's e-mail.
await wait(1000); PC.clean(1); await wait(900); PC.clean(3); await wait(900); PC.clean(5); await wait(1100); PC.clean(9); await wait(1500);
PC.pick("Sami's e-mail"); await wait(900); PC.clean(5); await wait(1000); PC.clean(9); await wait(1400);
