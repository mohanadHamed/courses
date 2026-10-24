// Silent Station: find the clues in the room, then choose a path through the story.
const c = document.getElementById("c"), sx = c.clientWidth / 600;
const tapAt = (x, y) => tap(c, x * sx, y * sx);
await wait(700);
for (const [x, y] of [[314, 178], [420, 165], [545, 95], [360, 183], [400, 272]]) { tapAt(x, y); await wait(650); }
await wait(1300);
click("#choices button"); await wait(1400);
click("#choices button"); await wait(2000);
