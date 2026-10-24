// Battery Lab: from the story settings (60 fps, bright, 5 h) to 120 fps and high graphics (hot), then 30 fps and low brightness.
await wait(1000); click('[data-k="fps"][data-v="120"]'); await wait(1500);
click('[data-k="gfx"][data-v="1"]'); await wait(1800);
click('[data-k="fps"][data-v="30"]'); await wait(1300);
click('[data-k="gfx"][data-v="0"]'); await wait(900);
click('[data-k="bright"][data-v="0"]'); await wait(1800);
