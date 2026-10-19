// Juice It: jump with no media, then switch all the media layers on.
const c = document.getElementById("c");
const jump = setInterval(() => tap(c), 900);
await wait(3000); click("#all");
await wait(4500); clearInterval(jump);
