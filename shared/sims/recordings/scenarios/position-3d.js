// The 3D viewer: move the player with the sliders.
const set = async (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event("input", { bubbles: true })); await wait(700); };
await wait(600);
await set("x", 1); await set("y", 0); await set("z", 1);
await set("x", 2); await set("y", 2); await set("z", 4);
await set("y", 4); await set("x", 5);
