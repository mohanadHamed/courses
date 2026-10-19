// Data Trip: fetch from the cache, the RAM and the flash storage; then change the cache hits.
await wait(600); click('#levels button[data-i="0"]');
await wait(1100); click('#levels button[data-i="1"]');
await wait(1700); click('#levels button[data-i="2"]');
await wait(3000);
const r = document.getElementById("hits");
for (const v of [99, 90, 70, 50]) { r.value = v; r.dispatchEvent(new Event("input")); await wait(700); }
