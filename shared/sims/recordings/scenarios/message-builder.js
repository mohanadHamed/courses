// A wrong option first, then the right one, twice.
const wrong = () => { const r = window.QK; const b = [...document.querySelectorAll("#opts button")]; return b; };
await wait(900); QK.pick(1); await wait(1400); QK.right(); await wait(1700); QK.right(); await wait(2200);
