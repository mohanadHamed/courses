// DigComp self-check: choose levels; the profile grows.
const sels = [...document.querySelectorAll("select")];
const levels = [3, 2, 4, 1, 3, 2, 5, 2, 3, 1, 4, 2];
for (let i = 0; i < Math.min(sels.length, levels.length); i++) {
  sels[i].value = String(levels[i]); sels[i].dispatchEvent(new Event("change")); await wait(500);
}
