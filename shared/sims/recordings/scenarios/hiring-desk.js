// Hiring Desk: sort the three tasks of the story into DigComp areas, then hire.
await wait(900); click("#next");
const AREA = { "e-mails of customers": 1, "short videos": 2, "code on the phone": 3 };
for (let n = 0; n < 3; n++) {
  await wait(1000);
  const text = document.querySelector("#card .text").textContent;
  const key = Object.keys(AREA).find((k) => text.includes(k));
  document.querySelectorAll("#opts button")[AREA[key]].click();
  await wait(1300); click("#next");
}
await wait(600);
// Jump to the hiring stage and hire Lina.
for (let n = 3; n < 12; n++) { document.querySelector("#opts button").click(); click("#next"); }
await wait(1500);
document.querySelectorAll("#opts .person")[1].click();
await wait(2500);
