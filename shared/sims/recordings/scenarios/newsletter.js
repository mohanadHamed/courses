// Newsletter Check: check the six sentences, fix the three mistakes, publish.
const S = () => [...document.querySelectorAll("#draft .s")];
const ok = (i) => S()[i].querySelector(".b button:first-child").click();
const fix = async (i, part) => {
  S()[i].querySelector(".b button:last-child").click(); await wait(700);
  [...S()[i].querySelectorAll(".fixes button")].find((b) => b.textContent.includes(part)).click(); await wait(800);
};
await wait(800);
ok(0); await wait(500);
await fix(1, "700");
ok(2); await wait(500);
await fix(3, "Delete");
ok(4); await wait(500);
await fix(5, "Saturday");
click("#publish");
await wait(2500);
