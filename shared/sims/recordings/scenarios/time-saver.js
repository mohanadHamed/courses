// Time Saver: add the prices by hand (type the total), then AutoSum, then change a price.
await wait(700); click("#start");
await wait(1800);
document.querySelector("#answer").value = "155"; await wait(500); click("#check");
await wait(1800); click("#sum");
await wait(2200); document.querySelectorAll("#grid td.edit")[2].click();
await wait(2500);
