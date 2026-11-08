// Check Lab: the spelling (two words and a name), then Find and Replace 9:00 -> 10:00.
await wait(800); click("#spell"); await wait(900); click([...document.querySelectorAll("#menu button")].find((b) => b.textContent === "second")); await wait(1000);
click("#spell"); await wait(800); click([...document.querySelectorAll("#menu button")].find((b) => b.textContent === "customers")); await wait(1000);
click("#spell"); await wait(800); click([...document.querySelectorAll("#menu button")].find((b) => b.textContent === "Ignore")); await wait(1300);
click("#replace"); await wait(500); await type("#find", "9:00", 110); await type("#with", "10:00", 110); await wait(400); click("#all"); await wait(2200);
