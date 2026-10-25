// Cat Catch: catch the first cat in the ring, tap the second one too early.
const until = async (f, ms = 6000) => { const t = performance.now(); while (!f() && performance.now() - t < ms) await wait(15); };
await until(() => CC.y() > (CC.ZT + CC.ZB) / 2); CC.tap(); await wait(400);
await until(() => CC.y() > 0.3); CC.tap(); await wait(2600);
