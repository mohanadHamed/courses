// Meeting Planner, Sunday: 8:00 and 10:00 are busy, 11:00 is free for all three; then Online.
const slot = (h) => click(`.slot[data-h="${h}"]`);
await wait(800); slot(8); await wait(1300); slot(10); await wait(1300); slot(11); await wait(1400);
click('#place [data-w="room"]'); await wait(1500); click('#place [data-w="online"]'); await wait(2200);
