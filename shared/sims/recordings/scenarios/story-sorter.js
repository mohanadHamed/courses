// Story Sorter: three cards of round 1 (one wrong answer), the kite rises.
const pick = (c) => click(`#choices [data-c="${c}"]`);
await wait(800); pick("character"); await wait(1300); click("#next");
await wait(800); pick("character"); await wait(1200); pick("setting"); await wait(1300); click("#next");
await wait(800); pick("conflict and stakes"); await wait(1300); click("#next");
await wait(800); pick("character"); await wait(1200);
